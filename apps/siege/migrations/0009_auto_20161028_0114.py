# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-10-28 01:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siege', '0008_auto_20161010_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siege',
            name='landing_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 28, 1, 14, 13, 174158)),
        ),
        migrations.AlterField(
            model_name='siege_army',
            name='time_offset',
            field=models.IntegerField(default=0),
        ),
    ]
