import os
from django.conf import settings
from django.db import models
from django.db.models import Prefetch, Q
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
# Create your models here.
from categories.models import Category
from videos.models import Video
from django.utils.text import slugify

from .fields import PositionField
from .utils import unique_slug_generator, make_display_price

# Create your models here.

class Certificate(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL)
    course          = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True)
    pdf             = models.FileField(upload_to='pdfs/', null=True, blank=True)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    slug            = models.SlugField(blank=True, max_length = 255,) # unique = False

    def __str__(self):
        return str(self.course)
    
    @property
    def pdfname(self):
        return os.path.basename(self.pdf.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.get_full_name())
        super().save()

    class Meta:
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'


class MyCourses(models.Model):
    user            = models.OneToOneField(settings.AUTH_USER_MODEL)
    courses         = models.ManyToManyField('Course', related_name='owned', blank=True)
    # lectures        = models.ManyToManyField('Lecture', related_name='lecture_seen', blank=True)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.courses.all().count())

    class Meta:
        verbose_name = 'Mis cursos'
        verbose_name_plural = 'Mis cursos'


def post_save_user_create(sender, instance, created, *args, **kwargs):
    if created:
        MyCourses.objects.get_or_create(user=instance)

post_save.connect(post_save_user_create, sender=settings.AUTH_USER_MODEL)


class CourseQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def lectures(self):
        return self.prefetch_related('lecture_set')

    def topics(self):
        qs = Topic.objects.prefetch_related('lecture_set')
        return self.prefetch_related(Prefetch('topics', queryset=qs, to_attr='topic_courses'))

    def featured(self):
        return self.filter(Q(category__slug__iexact='featured')) #| Q(secondary__slug__iexact='featured'))

    def reviews(self):
        return self.prefetch_related('review_set')

    def owned(self, user):
        if user.is_authenticated(): 
            qs = MyCourses.objects.filter(user=user)
        else:
            qs = MyCourses.objects.none()
        return self.prefetch_related(
                Prefetch('owned',
                        queryset=qs,
                        to_attr='is_owner'
                )
            )


class CourseManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all().active()
        #return super(CourseManager, self).all()


def course_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    folder = unique_slug_generator(instance)
    return 'courses-images/{0}/{1}'.format(folder, filename)

class Course(models.Model):
    user                    = models.ForeignKey(settings.AUTH_USER_MODEL)
    title                   = models.CharField(max_length=150)
    slug                    = models.SlugField(blank=True, max_length = 255,) # unique = False
    image                   = models.ImageField(blank=True, null=True, upload_to=course_directory_path,)
    category                = models.ForeignKey(Category, related_name='primary_category', null=True, blank=True)
    secondary               = models.ManyToManyField(Category, related_name='secondary_category', blank=True)
    order                   = PositionField(collection='category')
    description             = models.TextField()
    price                   = models.DecimalField(_("Precio Neto"), max_digits=6, decimal_places=2, blank=True, null=True, help_text='Si existe un descuento especial agrega una cantidad al precio neto, de lo contrario deja este campo vacío y utiliza solo el precio de lista.')
    list_price              = models.DecimalField(_("Precio de lista o precio regular"), max_digits=6, decimal_places=2, blank=True, null=True)
    active                  = models.BooleanField(default=True)
    updated                 = models.DateTimeField(auto_now=True)
    certificate_sample      = models.ImageField(blank=True, null=True, upload_to=course_directory_path,)
    timestamp               = models.DateTimeField(auto_now_add=True)

    objects = CourseManager() # Course.objects.all()

    # newsomething = CourseManager() # Course.newsomething.all()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Curso'
        verbose_name_plural = "Cursos"

    def get_absolute_url(self):
        return reverse("courses:detail", kwargs={"slug": self.slug})

    def get_purchase_url(self):
        return reverse("courses:purchase", kwargs={"slug": self.slug})

    def display_price(self):
        return make_display_price(self.list_price)

    def user_full_name(self):
        if self.user.userprofile.abbreviation:
            full_name = '%s %s %s' % (self.user.userprofile.abbreviation, self.user.first_name, self.user.last_name)
        else:
            full_name = '%s %s' % (self.user.first_name, self.user.last_name)
        return full_name.strip()

    @property
    def get_price(self):
        if self.price and self.list_price:
            return self.price
        return self.list_price


def post_save_course_receiver(sender, instance, created, *args, **kwargs):
    if not instance.category in instance.secondary.all():
        instance.secondary.add(instance.category)

post_save.connect(post_save_course_receiver, sender=Course)


class TopicQuerySet(models.query.QuerySet):
    def unused(self):
        return self.filter(lecture__isnull=True)

    def topic_lectures(self):
        return self.prefetch_related('lecture_set')

class TopicManager(models.Manager):
    def get_queryset(self):
        return TopicQuerySet(self.model, using=self._db)

    def topic_lectures(self):
        return self.get_queryset().prefetch_related('lecture_set')

class Topic(models.Model):
    course          = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name='topics')
    title           = models.CharField(max_length=255,)
    order           = PositionField(collection='course')
    
    objects = TopicManager() # Course.objects.all()

    def __str__(self):
        return self.title




class LectureQuerySet(models.query.QuerySet):
    def lecture_seen(self, user, topic ):
        if user.is_authenticated(): 
            qs = MyLecture.objects.filter(user=user, topic=topic)
        else:
            qs = MyLecture.objects.none()
        return self.prefetch_related(
                Prefetch('lecture_seen',
                        queryset=qs,
                        to_attr='was_seen'
                )
            )


class LectureManager(models.Manager):
    def get_queryset(self):
        return LectureQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()
        #return super(CourseManager, self).all()


class Lecture(models.Model):
    course          = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    video           = models.ForeignKey(Video, on_delete=models.SET_NULL, blank=True, null=True)
    topic           = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    title           = models.CharField(max_length=255,)
    order           = PositionField(collection='course')
    slug            = models.SlugField(blank=True) # unique = False
    free            = models.BooleanField(default=False)
    description     = models.TextField(blank=True)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    objects = LectureManager()

    def __str__(self):
        return self.title

    class Meta:
        unique_together = (('slug', 'course'),)
        ordering = ['order', 'title'] # 0 - 100 , a-z
        verbose_name = 'Lección'
        verbose_name_plural = "Lecciones"

    def get_absolute_url(self):
        return reverse("courses:lecture-detail", 
                kwargs={
                    "cslug": self.course.slug,
                    "lslug": self.slug,
                    }
            )


class MyLecture(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL)
    # course          = models.OneToOneField('Course',)
    topic           = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, related_name='topic_seen')
    # lectures        = models.ManyToManyField('Lecture', related_name='lecture_seen', blank=True)
    lecture         = models.ForeignKey(Lecture, on_delete=models.SET_NULL, null=True, related_name='lecture_seen')
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.lecture)

    class Meta:
        verbose_name = 'Mis lecciones'
        verbose_name_plural = 'Mis lecciones'


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    course      = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    comment     = models.TextField(_("Comentario"), max_length=500, blank=True)
    rating      = models.IntegerField(_("Calificación"),choices=RATING_CHOICES)
    pub_date    = models.DateTimeField(auto_now_add=True)




def pre_save_course_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_course_receiver, sender=Course)






