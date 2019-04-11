from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save

# Create your models here.
from courses.utils import unique_slug_generator

class VideoQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def unused(self):
        return self.filter(lecture__isnull=True)


class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()



class Video(models.Model):
    title           = models.CharField(max_length=120)
    slug            = models.SlugField(blank=True)
    embed_code      = models.TextField()
    free            = models.BooleanField(default=True)
    member_required = models.BooleanField(default=False)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    objects = VideoManager()

    def __str__(self): 
        return self.title

    def get_absolute_url(self):
        #return "/videos/{slug_arg}/".format(slug_arg=self.slug)
        return reverse("videos:detail", kwargs={"slug": self.slug})

def pre_save_video_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_video_receiver, sender=Video)