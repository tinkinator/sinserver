from __future__ import division
import json
import re
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
from .models import (Siege, Siege_army, City, Army, SiegeForm, Player, ArmyForm, CityForm)

date_format = "%m-%d-%Y %H:%M:%S"
date_format2 = "%"
offset_regex = re.compile(r'(-?)(\d{2,}):([0-5][0-9]):([0-5][0-9])')


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
        form = SiegeForm(request.POST)
        print form
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
    # Take the user to the edit siege page
    if request.method == 'GET':
        inner_queryset = set(Siege_army.objects.all())
        armies = Army.objects.filter(siege_army__isnull=True).values()
        the_siege = model_to_dict(Siege.objects.get(id=siege))

        for army in armies:
            print "%%%%%%%%%%%%, %s" % army
            city = City.objects.get(id=army['city_id'])
            army['city'] = city.name
            army['player'] = Player.objects.get(id=army['player_id']).__str__()
            distance = calc_dist(city.x_coord, city.y_coord, the_siege['x_coord'], the_siege['y_coord'])
            army['dist'] = "%.3f" % (distance)
            travel_time = calc_time(army['speed'], distance)
            army['time'] = "%.3f" % (travel_time)
            launch_time = calc_launch_time(the_siege['landing_time'], travel_time)
            army['launch_time'] = datetime.strftime(launch_time, date_format)
        squares = [k for (k,v) in the_siege.items() if (v == True and k != "id")]
        the_siege['landing_time'] = datetime.strftime(the_siege['landing_time'], date_format)
        context = {
            'armies': armies,
            'siege': the_siege,
            'siege_armies': inner_queryset,
            'squares': squares,
            'orders': [x[0] for x in Siege_army.ORDERS]
        }
        print "Number of queries made: {0}".format(len(db.connection.queries))
        return render(request, 'siege/edit_siege.html', context)
    # Delete a siege and re-render manage.html
    elif request.method == 'DELETE':
        the_siege = Siege.objects.get(id=int(siege))
        the_siege.delete()
        return HttpResponse("success")
    elif request.method == "POST":
        print request.POST
        thesiege = Siege.objects.get(id=int(siege))
        form = SiegeForm(request.POST, instance=thesiege)
        print form
        if form.is_valid():
            siege = form.save(commit=False)
            siege.save()
            return redirect('manage')
        else:
            print form.errors
        return render(request, 'siege/manage.html', {'form': form})


def add_army_tosiege(request, siege):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        offset = offset_fromstring(request.POST["Offset"])
        if request.POST["Square"] == "id":
            square = "DIR"
        else:
            square = request.POST["Square"]
        the_siege = Siege.objects.get(id=int(siege))
        the_army = Army.objects.get(id=int(request.POST["armyId"]))
        newSiegeArmy = Siege_army(siege_id=the_siege, army_id=the_army, siege_square=square, time_offset=offset, orders=request.POST["Orders"])
        newSiegeArmy.save()
        return HttpResponse("Mkay!")

    
def update_siegearmy(request, siege, army):
    if request.method == 'PUT':
        print "%%%%%%%%%%%%%%%%%%%%"
        body = json.loads(request.body.decode('utf-8'))
        siege_army = Siege_army.objects.get(id=int(army))
        offset = offset_fromstring(body['offset'])
        print "Siege army changes: %s, offset: %s" % (body, offset)
        siege_army.time_offset = offset
        siege_army.siege_square = body['siege_square']
        siege_army.orders = body['orders']
        siege_army.save()
        return HttpResponse("Mkay!")
    elif request.method == 'DELETE':
        siege_army = Siege_army.objects.get(id=int(army))
        siege_army.delete()
        return HttpResponse("1 siege deleted")


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


def save_army(request, army):
    thearmy = Army.objects.get(id=int(army))
    print ("$$$$$$$$$$$$$$$$$$$$$$ POST data: %s" % request.POST)
    if request.method == "POST":
        if "ajax" in request.POST:
            speed = float(request.POST["speed"])
            thearmy.speed = speed
            if "troop_count" in request.POST:
                thearmy.troop_count = int(request.POST["troop_count"])
            thearmy.save()
            return HttpResponse("success")
        form = ArmyForm(request.POST, instance=thearmy)
        if form.is_valid():
            form.save()
            return redirect("armies")
        return HttpResponse("Form was invalid, saving failed")
    elif request.method == "DELETE":
        thearmy = Army.objects.get(id=int(army))
        thearmy.delete()
        return HttpResponse("1 army deleted")


@login_required(login_url='/', redirect_field_name=None)
def show_cities(request):
    context = {}
    context['player'] = request.user.username
    context['player_id'] = request.user.id
    context['cities'] = City.objects.filter(player=request.user.player)
    return render(request, 'siege/towns.html', context)


def create_city(request):
    print "something else happened??????"
    player = request.user.username
    if request.method == "POST":
        form = CityForm(request.POST)
        print "Form: {0}".format(form)
        if form.is_valid():
            city = form.save(commit=False)
            city.save()
            return redirect('cities')
        else:
            print "Errors: {0}".format(form.errors)
    else:
        form = CityForm()
    return render(request, 'siege/armies.html', {'form': form, 'player': player})

def save_city(request, city):
    if request.method == "DELETE":
        thecity = City.objects.get(id=int(city))
        thecity.delete()
        return HttpResponse("1 city deleted")
    elif request.method == "POST":
        print ("%%%%%%%%%%%%%%%%%%%%% POST data: {0}".format(request.POST))
        player = request.user.username
        the_city = City.objects.get(id=int(city))
        form = CityForm(request.POST, instance=the_city)
        if form.is_valid():
            form.save()
            return redirect('cities')
        return render(request, 'siege/cities.html', {'form': form, 'player': player})


def calc_dist(x1, y1, x2, y2):
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)


def calc_time(speed, distance):
    hours = float(distance) / float(speed)
    return hours

def offset_fromstring(offset_string):
    offset = re.match(offset_regex, offset_string)
    offset_seconds = int(
        offset.group(2)) * 3600 \
                     + int(offset.group(3)) * 60 \
                     + int(offset.group(4))
    if offset.group(1):
        offset_seconds = -offset_seconds
    return offset_seconds

def calc_launch_time(landing_time, offset1, offset2=None):
    delta = timedelta(hours = offset1)
    if offset2 is not None:
        delta2 = timedelta(seconds = offset2)
        if offset2 < 0:
            delta -= delta2
        else:
            return landing_time - delta + delta2
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




