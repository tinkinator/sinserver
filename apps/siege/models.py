from __future__ import unicode_literals
from ..logreg.models import Player
from django.db import models
from django import forms
from django.forms import ModelForm, DateTimeInput
from datetime import datetime

# Create your models here.
class Siege(models.Model):
    target_player = models.CharField(max_length = 100)
    target_city = models.CharField(max_length = 100)
    x_coord = models.SmallIntegerField()
    y_coord = models.SmallIntegerField()
    landing_time = models.DateTimeField(default=datetime.now())
    N = models.BooleanField(default=False)
    NE = models.BooleanField(default=False)
    E = models.BooleanField(default=False)
    SE = models.BooleanField(default=False)
    S = models.BooleanField(default=False)
    SW = models.BooleanField(default=False)
    W = models.BooleanField(default=False)
    NW = models.BooleanField(default=False)
    DIR = models.BooleanField(default=True)
    def __str__(self):
        return str(self.target_player) + "-- " + str(self.target_city)
    class Meta:
        db_table = 'sieges'

class SiegeForm(ModelForm):
    landing_time = forms.DateTimeField(input_formats=['%m/%d/%Y %I:%M %p', '%m-%d-%Y %H:%M:%S'])
    class Meta:
        model = Siege
        fields = (
            'target_player',
            'target_city',
            'x_coord',
            'y_coord',
            'landing_time',
            'N',
            'NE',
            'E',
            'SE',
            'S',
            'SW',
            'W',
            'NW',
            )


class City(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    x_coord = models.SmallIntegerField()
    y_coord = models.SmallIntegerField()
    region = models.CharField(max_length = 100)
    def __unicode__(self):
        return str(self.player) + "-" + str(self.name)
    class Meta:
        db_table = 'cities'

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = (
            'name',
            'player',
            'x_coord',
            'y_coord',
            'region'
        )


class Army(models.Model):
    TROOPTYPE_CHOICES = (
        ('SP_T1', 'T1 Spears'),
        ('SP_T2', 'T2 Spears'),
        ('BOW_T1', 'T1 Bows'),
        ('BOW_T2', 'T2 Bows'),
        ('INF_T1', 'T1 Infantry'),
        ('INF_T2', 'T2 Infantry'),
        ('CAV_T1', 'T1 Cavalry'),
        ('CAV_T2', 'T2 Cavalry'),
        ('MIX_SP', 'Mixed spears'),
        ('MIX_BOW', 'Mixed bows'),
        ('MIX_INF', 'Mixed infantry'),
        ('MIX_CAV', 'Mixed cav'),
        ('MIX', 'Kitchen sink')
    )

    ELITE_CHOICES = (
        ('CAV', 'Anti-Cavalry'),
        ('INF', 'Anti-Infantry'),
        ('BOW', 'Anti-Bow')
    )

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    troop_type = models.CharField(choices=TROOPTYPE_CHOICES, max_length = 100)
    troop_count = models.IntegerField(default=0)
    siege_engines = models.SmallIntegerField(default=0)
    wall_engines = models.SmallIntegerField(default=0)
    speed = models.DecimalField(max_digits=5, decimal_places=3,default=0)
    elite_divs_number = models.SmallIntegerField()
    elite_type = models.CharField(choices=ELITE_CHOICES, max_length = 100, blank=True)
    away = models.BooleanField(default=False)
    def __str__(self):
        return str(self.player) + "-" + str(self.city) + "-" + str(self.troop_type) + "-" + str(self.troop_count)
    class Meta:
        db_table = 'armies'

class ArmyForm(ModelForm):
    class Meta:
        model = Army
        fields = (
            'player',
            'city',
            'troop_type',
            'troop_count',
            'speed',
            'siege_engines',
            'wall_engines',
            'elite_type',
            'elite_divs_number',
            )


class Siege_army(models.Model):
    SQUARES = (
        ('N', 'North'),
        ('NE', 'Northeast'),
        ('E', 'East'),
        ('SE', 'Southeast'),
        ('S', 'South'),
        ('SW', 'Southwest'),
        ('W', 'West'),
        ('NW', 'Northwest'),
        ('DIR', 'Direct')
        )
    
    ORDERS = (
        ('occupy', 'occupy'),
        ('attack', 'attack'),
        ('blockade', 'blockade'),
        ('siege', 'siege')
        )

    siege_id = models.ForeignKey(Siege, on_delete=models.CASCADE)
    army_id = models.ForeignKey(Army, on_delete=models.CASCADE)
    siege_square = models.CharField(max_length = 3, choices=SQUARES)
    time_offset = models.IntegerField(default=0)
    time_sent = models.DateTimeField(null=True)
    orders = models.CharField(choices=ORDERS, max_length = 30, default='occupy')
    class Meta:
        db_table = 'siege_armies'
    
    
