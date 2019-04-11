# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-30 17:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': 'Curso', 'verbose_name_plural': 'Cursos'},
        ),
        migrations.AlterModelOptions(
            name='lecture',
            options={'ordering': ['order', 'title'], 'verbose_name': 'Lección', 'verbose_name_plural': 'Lecciones'},
        ),
        migrations.AlterModelOptions(
            name='mycourses',
            options={'verbose_name': 'Mis cursos', 'verbose_name_plural': 'Mis cursos'},
        ),
    ]