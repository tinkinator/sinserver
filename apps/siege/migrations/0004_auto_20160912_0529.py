# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-12 05:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siege', '0003_auto_20160910_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='siege',
            name='landing_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 12, 5, 29, 58, 441144)),
        ),
        migrations.AlterField(
            model_name='siege',
            name='E',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='siege',
            name='N',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='siege',
            name='NE',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='siege',
            name='NW',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='siege',
            name='S',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='siege',
            name='SE',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='siege',
            name='SW',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='siege',
            name='W',
            field=models.BooleanField(default=False),
        ),
    ]