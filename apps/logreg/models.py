from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from timezones.zones import PRETTY_TIMEZONE_CHOICES
# Create your models here.

class Player(models.Model):
    TIMEZONES = (

        )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alliance_name = models.CharField(max_length=20, blank=True)
    time_zone = models.CharField(max_length=255, choices=PRETTY_TIMEZONE_CHOICES, blank=True, null=True,)
    illyId = models.IntegerField()

    def __unicode__(self):
        return unicode(self.user.username)

