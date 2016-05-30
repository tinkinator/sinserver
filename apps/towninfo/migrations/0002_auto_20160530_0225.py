# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-30 02:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('towninfo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('changed_alliance_at', models.DateTimeField()),
                ('changed_name_at', models.DateTimeField()),
                ('abandoned_at', models.DateTimeField()),
                ('prev_status', models.CharField(max_length=50)),
                ('curr_status', models.CharField(max_length=50)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='towninfo.Player')),
            ],
        ),
        migrations.RemoveField(
            model_name='town_history',
            name='abandoned_at',
        ),
        migrations.RemoveField(
            model_name='town_history',
            name='changed_alliance_at',
        ),
        migrations.RemoveField(
            model_name='town_history',
            name='destroyed_at',
        ),
        migrations.RemoveField(
            model_name='town_history',
            name='registered_at',
        ),
        migrations.RemoveField(
            model_name='town_history',
            name='relocated_at',
        ),
        migrations.RemoveField(
            model_name='town_history',
            name='renamed_at',
        ),
        migrations.AddField(
            model_name='town_history',
            name='change_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 30, 2, 25, 34, 800066, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='town_history',
            name='change_type',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
