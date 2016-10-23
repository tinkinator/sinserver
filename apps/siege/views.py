from __future__ import division
import json
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.utils import timezone
from django import db, template
from django.http import JsonResponse, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms.models import model_to_dict
from math import sqrt
from .models import (Siege, Siege_army, City, Army, SiegeForm, Player, ArmyForm)

date_format = "%d %b %H:%M:%S"

@login_required(login_url='/', redirect_field_name=None)
def manage(request):
    sieges = {
        'sieges': Siege.objects.all(),
        'form': SiegeForm(label_suffix="")
        }
    return render(request, 'siege/manage.html', sieges)

@login_required(login_url='/', redirect_field_name=None)
def create_siege(request):
    if request.method == "POST":
        print request.POST
        form = SiegeForm(request.POST)
        if form.is_valid():
            siege = form.save(commit=False)
            siege.save()
            return redirect('manage')
        else:
            print form.errors
    else:
        form = SiegeForm()
    return render(request, 'siege/manage.html', {'form': form})

@login_required(login_url='/', redirect_field_name=None)
def armies(request):
    armies = {
    }
    return render(request, 'siege/armies.html')

@login_required(login_url='/', redirect_field_name=None)
def edit_siege(request, siege):
    # Takes the user to the edit siege page
    inner_queryset = set(Siege_army.objects.all())
    armies = Army.objects.filter(siege_army__isnull=True).values()
    the_siege = model_to_dict(Siege.objects.get(id=siege))
    for army in armies:
        city = City.objects.get(id__in=Army.objects.filter(id=army['id']))
        army['city'] = city.name
        army['player'] = Player.objects.get(id=army['player_id']).__str__()
        distance = calc_dist(city.x_coord, city.y_coord, the_siege['x_coord'], the_siege['y_coord'])
        army['dist'] = "%.3f" % (distance)
        travel_time = calc_time(army['speed'], distance)
        army['time'] = "%.3f" % (travel_time)
        launch_time = calc_launch_time(the_siege['landing_time'], travel_time)
        army['launch_time'] = datetime.strftime(launch_time, date_format)
        print "Launch time: {0}".format(launch_time)
    squares = [k for (k,v) in the_siege.items() if (v == True and v != "id")]
    context = {
        'armies': armies,
        'siege': the_siege, 
        'siege_armies': inner_queryset,
        'squares': squares,
        'orders': [x[0] for x in Siege_army.ORDERS]
    }
    print "Number of queries made: {0}".format(len(db.connection.queries))
    return render(request, 'siege/edit_siege.html', context)

def add_army(request, siege):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        offset = request.POST["Offset"]
        time = datetime.strptime(offset,"%H:%M:%S")
        time_offset = timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
        if request.POST["Square"] == "id":
            square = "DIR"
        else:
            square = request.POST["Square"]
        the_siege = Siege.objects.get(id=int(siege))
        the_army = Army.objects.get(id=int(request.POST["armyId"]))
        newSiegeArmy = Siege_army(siege_id=the_siege, army_id=the_army, siege_square=square, time_offset=time_offset, orders=request.POST["Orders"])
        newSiegeArmy.save();
        return HttpResponse("Mkay!")

def show_armies(request):
    context = {}
    player = request.user.username
    context['player_id'] = request.user.id
    context['player'] = player
    cities = [(lambda x: model_to_dict(x))(x) for x in City.objects.filter(player=request.user.player)]
    print "Cities: {0}".format(cities)
    cities_list = [{'name':x['name'], 'id':x['id']} for x in cities]
    context['cities'] = cities_list
    armies = Army.objects.select_related('city').filter(player=request.user.player)
    context['armies'] = [(lambda x: model_to_dict(x))(x) for x in armies]
    for idx, army in enumerate(context['armies']):
        context['armies'][idx]['city'] = armies[idx].city.name
    context['form'] = ArmyForm(label_suffix = "")
    print context
    return render(request, 'siege/armies.html', context)

def create_army(request):
    player = request.user.username
    if request.method == "POST":
        form = ArmyForm(request.POST)
        if form.is_valid():
            army = form.save(commit=False)
            print "Army: {0}".format(army)
            army.save()
            return redirect('armies')
        else:
            print "Errors: {0}".format(form.errors)
    else:
        form = ArmyForm()
    return render(request, 'siege/armies.html', {'form': form, 'player': player})


def calc_dist(x1, y1, x2, y2):
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calc_time(speed, distance):
    hours = float(distance) / float(speed)
    return hours
    

def calc_launch_time(landing_time, offset1, offset2=None):
    delta = timedelta(hours = offset1)
    if offset2 is not None:
        delta += offset2
    return landing_time - delta

def calculate_target_coord(square, x, y):
    if square == "N":
        return (x, y-1)
    elif square == "NE":
        return (x+1, y-1)
    elif square == "E":
        return (x+1, y)
    elif square == "SE":
        return (x+1, y+1)
    elif square == "S":
        return (x, y+1)
    elif square == "SW":
        return (x-1, y+1)
    elif square == "W":
        return (x-1, y)
    elif square == "NW":
        return (x-1, y-1)
    else:
        return (x, y)




