# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-10 22:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_auto_20190410_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='mylecture',
            name='topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='topic_seen', to='courses.Topic'),
        ),
    ]