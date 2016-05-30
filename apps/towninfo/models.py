from __future__ import unicode_literals
from datetime import datetime
from django.db import models

# Create your models here.
class Player(models.Model):
    playerid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length = 50)
    player_alliance = models.CharField(max_length = 50)

class Town(models.Model):
    townid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length = 50)
    mapX = models.IntegerField()
    mapY = models.IntegerField()
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

class Town_history(models.Model):
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    founded_on = models.DateTimeField()
    change_type = models.CharField(max_length = 50)
    change_date = models.DateTimeField()
    previous_status = models.CharField(max_length = 50)
    current_status = models.CharField(max_length = 50)
    
class Player_history(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    changed_alliance_at = models.DateTimeField()
    changed_name_at = models.DateTimeField()
    abandoned_at = models.DateTimeField()
    prev_status = models.CharField(max_length = 50)
    curr_status = models.CharField(max_length = 50)

    