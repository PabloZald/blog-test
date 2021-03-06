# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-02 20:42
from __future__ import unicode_literals

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CityOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(blank=True, max_length=100, verbose_name='Nombre de la ciudad')),
                ('postal_code', models.CharField(blank=True, max_length=20, verbose_name='Código postal')),
                ('state', models.CharField(blank=True, max_length=100, verbose_name='Estado, provincia o departamento')),
                ('country', models.CharField(blank=True, max_length=100, verbose_name='País')),
                ('address_region', models.CharField(blank=True, max_length=20, verbose_name='Región usando el formato ISO 3166-1 Ej. SV, AR, MX.')),
            ],
            options={
                'verbose_name': 'Ciudad',
                'verbose_name_plural': 'Ciudades',
                'ordering': ['city_name'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(blank=True, help_text='Escribe tu último título académico ej. "Doctorado en medicina".', max_length=100, verbose_name='Profesión o título académico')),
                ('abbreviation', models.CharField(blank=True, max_length=20, verbose_name='Abreviatura de tu nivel académico')),
                ('academic_abbreviation_visible', models.BooleanField(default=False, help_text='La abreviatura de tu nivel académico será visible junto con tu nombre.', verbose_name='Abreviatura de tu nivel académico visible')),
                ('speciality', models.CharField(blank=True, help_text='Escribe la especialidad que desempeñas, si la posees.', max_length=100, verbose_name='Especialidad en tu profesión')),
                ('gender', models.CharField(blank=True, choices=[('hombre', 'hombre'), ('mujer', 'mujer'), ('otro', 'otro')], max_length=6, verbose_name='Sexo')),
                ('country', models.CharField(blank=True, max_length=100, verbose_name='País')),
                ('city', models.CharField(blank=True, max_length=100, verbose_name='Ciudad')),
                ('description', models.TextField(blank=True, help_text='Pequeña introducción de ti, máximo 2000 caracteres.', max_length=2000, null=True, verbose_name='Descripción')),
                ('website', models.URLField(blank=True, verbose_name='Sitio web')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='+503 2502 6108')),
                ('whatsapp', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='WhatsApp ej. +503 7390 5006')),
                ('image', models.ImageField(blank=True, upload_to=accounts.models.profile_picture_directory_path)),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
                ('views', models.PositiveIntegerField(blank=True, default=0)),
                ('is_instructor', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, help_text='URL personalizada para el perfil.', max_length=255, null=True, verbose_name='URL del perfil')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
