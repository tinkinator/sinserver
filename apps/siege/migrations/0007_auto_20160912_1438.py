# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-12 14:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siege', '0006_auto_20160912_1438'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='army',
            name='army_id',
        ),
        migrations.AlterField(
            model_name='siege',
            name='landing_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 12, 14, 38, 55, 507845)),
        ),
    ]
