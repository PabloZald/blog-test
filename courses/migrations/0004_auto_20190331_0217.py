# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-31 02:17
from __future__ import unicode_literals

import courses.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20190330_2137'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('order', courses.fields.PositionField(default=-1)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='topics', to='courses.Course')),
            ],
        ),
        migrations.AddField(
            model_name='lecture',
            name='topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.Topic'),
        ),
    ]
