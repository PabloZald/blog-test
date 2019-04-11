import datetime

from django.template.defaultfilters import date as _date
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
# from django.contrib.sites.models import Site

from django.core.validators import RegexValidator
from django.core.mail import send_mail
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
# from sorl.thumbnail import ImageField
from courses.utils import unique_slug_generator

import uuid # Requerido para crear instancias únicas.

User = settings.AUTH_USER_MODEL
    

    # NINGUNO = 'Ninguno'
    # DOCTOR = 'Dr.'
    # TEC = 'Téc.'
    # ING = 'Ing.'
    # ARQ = 'Arq.'
    # LIC = 'Lic.'
    # MTR = 'Mtr.'
    # MBA = 'MBA'
    # MSC = 'M.Sc.'
    # MA = 'M.A.'
    # MJUR = 'M.Jur'
    # LLM = 'LL.M'
    # BCL = 'BCL'
    # OTHER = 'Otro'

    # ACADEMIC_OPTIONS = (
    #     (NINGUNO = 'Ninguno'),
    #     (DOCTOR = 'Dr.'),
    #     (TEC = 'Téc.'),
    #     (ING = 'Ing.'),
    #     (ARQ = 'Arq.'),
    #     (LIC = 'Lic.'),
    #     (MTR = 'Mtr.'),
    #     (MBA = 'MBA'),
    #     (MED = 'M.Ed'),
    #     (MSC = 'M.Sc'),
    #     (MA = 'M.A.'),
    #     (MJUR = 'M.Jur'),
    #     (LLM = 'LL.M.'),
    #     (BCL = 'BCL'),
    #     (OTHER = 'Otro'), 
    # )

GENDER_CHOICES = (
    ('hombre','hombre'),
    ('mujer', 'mujer'),
    ('otro', 'otro'),
)


def profile_picture_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/site_site-name/<filename>
    site_folder = unique_slug_generator(instance, instance.user_full_name())
    return 'accounts/{0}/{1}'.format(site_folder, filename)


class UserProfile(models.Model):
    user                            =   models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    degree                          =   models.CharField(_("Profesión o título académico"), max_length=100, blank=True, help_text='Escribe tu último título académico ej. "Doctorado en medicina", "Licenciatura en enfermería".')
    abbreviation                    =   models.CharField(_('Abreviatura de tu nivel académico'), max_length=20, blank=True, help_text='Ej. Dr. Lic. Ing. Mtr. Mba')
    academic_abbreviation_visible   =   models.BooleanField(_("Abreviatura de tu nivel académico visible"), default=False, help_text='La abreviatura de tu nivel académico será visible junto con tu nombre.')
    speciality                      =   models.CharField(_("Especialidad en tu profesión"), max_length=100, blank=True, help_text='Escribe la especialidad que desempeñas, si la posees.')
    gender                          =   models.CharField(_("Sexo"), max_length=6, blank=True, choices=GENDER_CHOICES)
    country                         =   models.CharField(_("País"), max_length=100, blank=True,)
    city                            =   models.CharField(_("Ciudad"), max_length=100, blank=True,)
    description                     =   models.TextField(_("Descripción"), max_length=2000, blank=True, null=True, help_text='Pequeña introducción de ti, máximo 2000 caracteres.')
    website                         =   models.URLField(_("Sitio web"), blank=True)
    birthday                        =   models.DateField(_("Fecha de nacimiento"), help_text='Agrega tu fecha de nacimiento para tener una mejor experiencia de usuario y para comprobar que eres mayor de 13 años, de lo contrario tu cuenta puede ser bloqueada.', null=True, blank=True)
    phone                           =   PhoneNumberField('Teléfono ej. +503 2502 6108', blank=True)
    whatsapp                        =   PhoneNumberField('WhatsApp ej. +503 7390 5006', blank=True)
    # image                           =   models.ImageField(upload_to=site_user_image_directory_path, blank=True)
    # profile_picture                 =   models.ImageField(upload_to=site_user_image_directory_path, blank=True)
    profile_picture                 =   models.ImageField(upload_to=profile_picture_directory_path, blank=True)
    # banner              =   models.ImageField(upload_to='banner_image', blank=True)
    last_updated                    =   models.DateTimeField(auto_now_add=True)
    views                           =   models.PositiveIntegerField(default=0, blank=True)
    is_instructor                   =   models.BooleanField(default=False)
    slug                            =   models.SlugField(_("URL del perfil"), max_length=255, null=True, blank=True, help_text='URL personalizada para el perfil.')

    def __str__(self):
        return self.user_full_name()

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = "Perfiles"

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'slug': self.slug}) 

    def user_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        if self.abbreviation:
            full_name = '%s %s %s' % (self.abbreviation, self.user.first_name, self.user.last_name)
        else:
            full_name = '%s %s' % (self.user.first_name, self.user.last_name)
        return full_name.strip()

    def full_profile(self):
        score = 0
        if self.user.first_name:
            score += 10
        if self.user.last_name:
            score += 10
        if self.user.email:
            score += 10
        if self.birthday:
            score += 10
        if self.gender:    
            score += 10
        if self.country:
            score += 10
        if self.city:
            score += 10
        if self.profile_picture:
            score += 10
        if self.phone:
            score += 10
        if self.description:
            score += 10
        return score

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self, self.user_full_name())
        super().save()


class CityOption(models.Model):
    city_name           =   models.CharField(_('Nombre de la ciudad'), max_length=100, blank=True)
    postal_code         =   models.CharField(_('Código postal'), max_length=20, blank=True)
    state               =   models.CharField(_('Estado, provincia o departamento'), max_length=100, blank=True)
    country             =   models.CharField(_('País'), max_length=100, blank=True)
    address_region      =   models.CharField(_('Región usando el formato ISO 3166-1 Ej. SV, AR, MX.'), max_length=20, blank=True)

    def __str__(self):
        return self.city_name

    class Meta:
        ordering = ['city_name']
        verbose_name = 'Ciudad'
        verbose_name_plural = "Ciudades"


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_= kwargs['instance']
        # slug_ = unique_slug_generator(user_.slug)
        user_profile = UserProfile.objects.create(user=user_)
        
post_save.connect(create_profile, sender=User)