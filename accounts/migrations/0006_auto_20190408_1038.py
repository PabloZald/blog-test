# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-08 16:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20190403_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birthday',
            field=models.DateField(blank=True, help_text='Agrega tu fecha de nacimiento para tener una mejor experiencia de usuario y para comprobar que eres mayor de 13 años, de lo contrario tu cuenta puede ser bloqueada.', null=True, verbose_name='Fecha de nacimiento'),
        ),
    ]
