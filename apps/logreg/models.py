from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from timezones.zones import PRETTY_TIMEZONE_CHOICES
# Create your models here.

class Player(models.Model):
    TIMEZONES = (

        )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alliance_name = models.CharField(max_length=20, blank=True)
    time_zone = models.CharField(max_length=255, choices=PRETTY_TIMEZONE_CHOICES, blank=True, null=True,)
    illyId = models.IntegerField(null=True)

    def __unicode__(self):
        return unicode(self.user.username)

@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()
