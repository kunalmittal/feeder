# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-04 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0002_auto_20161104_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='courses',
            field=models.ManyToManyField(to='myadmin.Course'),
        ),
    ]
