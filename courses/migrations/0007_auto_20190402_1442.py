# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-02 20:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20190401_1616'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['-pk'], 'verbose_name': 'Curso', 'verbose_name_plural': 'Cursos'},
        ),
    ]
