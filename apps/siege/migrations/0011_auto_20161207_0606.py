# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-12-07 06:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siege', '0010_auto_20161201_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siege',
            name='landing_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 7, 6, 6, 15, 280007)),
        ),
    ]
