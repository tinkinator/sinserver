# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-12-13 00:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siege', '0013_auto_20161209_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siege',
            name='landing_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 13, 0, 43, 22, 908187)),
        ),
    ]
