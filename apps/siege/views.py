from __future__ import division
import json
import re
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, render_to_response
from django.utils import timezone
from django import db, template
from django.http import JsonResponse, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms.models import model_to_dict
from math import sqrt
from .models import (Siege, Siege_army, City, Army, SiegeForm, Player, ArmyForm, CityForm)
from .templatetags import siege_tags
from .helper import *

date_format = "%m-%d-%Y %H:%M:%S"
date_format2 = "%"
offset_regex = re.compile(r'(-?)(\d{2,}):([0-5][0-9]):([0-5][0-9])')

# Landing page
@login_required(login_url='/', redirect_field_name=None)
def manage(request):
    sieges = {
        'sieges': Siege.objects.all(),
        'form': SiegeForm(label_suffix="")
        }
    return render(request, 'siege/manage.html', sieges)


# Create new siege
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


# Render siege editing page
@login_required(login_url='/', redirect_field_name=None)
def edit_siege(request, siege):
    # Take the user to the edit siege page
    if request.method == 'GET':
        context = {}
        inner_queryset = set(Siege_army.objects.all())
        army_query = Army.objects.filter(siege_army__isnull=True)
        the_siege = model_to_dict(Siege.objects.get(id=siege))
        context['armies'] = [(lambda x: model_to_dict(x))(x) for x in army_query]

        for idx, army in enumerate(context['armies']):
            print "%%%%%%%%%%%%, %s" % army
            city = City.objects.get(id=army['city'])
            army['city'] = city.name
            army['player'] = Player.objects.get(id=army['player']).__str__()
            distance = calc_dist(city.x_coord, city.y_coord, the_siege['x_coord'], the_siege['y_coord'])
            army['dist'] = "%.3f" % (distance)
            travel_time = calc_time(army['speed'], distance)
            army['time'] = "%.3f" % (travel_time)
            launch_time = calc_launch_time(the_siege['landing_time'], travel_time)
            army['launch_time'] = datetime.strftime(launch_time, date_format)
            army['troop_type'] = army_query[idx].get_troop_type_display()
            army['engines'] = "%s/%s" % (army_query[idx].siege_engines, army_query[idx].wall_engines)
        squares = [k for (k,v) in the_siege.items() if (v == True and k != "id")]
        the_siege['landing_time'] = datetime.strftime(the_siege['landing_time'], date_format)
        context['siege'] = the_siege
        context['siege_armies'] = inner_queryset
        context['squares'] = squares
        context['orders'] = [x[0] for x in Siege_army.ORDERS]

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
            siegeObj = form.save(commit=False)
            siegeObj.save()
            return redirect('/siege/'+siege)
        else:
            print form.errors
        return render(request, 'siege/manage.html', {'form': form})


# Add army to siege
@login_required(login_url='/', redirect_field_name=None)
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
        newSiegeArmy = Siege_army(siege_id=the_siege, army_id=the_army, player_id=the_army.player, siege_square=square, time_offset=offset, orders=request.POST["Orders"])
        newSiegeArmy.save()
        partial_context = {}
        partial_context['siege'] = {}
        partial_context['siege']['id'] = siege
        context = siege_tags.siege_armies_partial(partial_context)
        return render_to_response('siege/siege_armies_partial.html', context)


# Update siege army
@login_required(login_url='/', redirect_field_name=None)
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


# Get armies and render armies page
@login_required(login_url='/', redirect_field_name=None)
def show_armies(request):
    context = {}
    player = request.user.username
    context['player_id'] = request.user.player.id
    context['player'] = player
    cities = [(lambda x: model_to_dict(x))(x) for x in City.objects.filter(player=request.user.player)]
    print "Cities: {0}".format(cities)
    cities_list = [{'name':x['name'], 'id':x['id']} for x in cities]
    context['cities'] = cities_list
    armies = Army.objects.select_related('city').filter(player=request.user.player)
    context['armies'] = [(lambda x: model_to_dict(x))(x) for x in armies]
    for idx, army in enumerate(context['armies']):
        context['armies'][idx]['city'] = armies[idx].city.name
        context['armies'][idx]['troop_type'] = armies[idx].get_troop_type_display()
        context['armies'][idx]['troop_type_info'] = armies[idx].troop_type
    context['form'] = ArmyForm(label_suffix = "")
    print context
    return render(request, 'siege/armies.html', context)


# Create new army
@login_required(login_url='/', redirect_field_name=None)
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


# Update army
@login_required(login_url='/', redirect_field_name=None)
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


# Get cities and render cities page
@login_required(login_url='/', redirect_field_name=None)
def show_cities(request):
    context = {}
    context['player'] = request.user.username
    context['player_id'] = request.user.player.id
    context['cities'] = City.objects.filter(player=request.user.player)
    return render(request, 'siege/towns.html', context)


# Create new city
@login_required(login_url='/', redirect_field_name=None)
def create_city(request):
    print "Creating a city, player: %s" % request.user.player.id
    player = request.user.username
    print request.POST
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.save(commit=False)
            print city
            city.save()
            return redirect('cities')
        else:
            print "Errors: {0}".format(form.errors)
    else:
        form = CityForm()
    return render(request, 'siege/towns.html', {'form': form, 'player': player})


# Update city
@login_required(login_url='/', redirect_field_name=None)
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
        return render(request, 'siege/towns.html', {'form': form, 'player': player})


# Render siege schedule page
@login_required(login_url='/', redirect_field_name=None)
def schedule(request, siege):
    the_siege = Siege.objects.get(id=int(siege))
    q = Siege_army.objects.filter(siege_id=siege).select_related('siege_id', 'army_id')
    armies = [(lambda x: model_to_dict(x))(x) for x in q]
    context = {}
    context['target_player'] = the_siege.target_player
    context['target_city'] = the_siege.target_city
    context['target_x'] = the_siege.x_coord
    context['target_y'] = the_siege.y_coord
    context['landing_time'] = datetime.strftime(the_siege.landing_time, date_format)
    for idx, army in enumerate(q):
        the_army = army.army_id
        armies[idx]['player'] = the_army.player.__str__()
        armies[idx]['city'] = the_army.city.name
        speed = the_army.speed
        armies[idx]['speed'] = speed
        armies[idx]['troop_type'] = the_army.get_troop_type_display()
        armies[idx]['troop_count'] = the_army.troop_count
        orders = army.orders
        target = calculate_target_coord(army.siege_square, the_siege.x_coord, the_siege.y_coord, orders)
        dist = calc_dist(the_army.city.x_coord, the_army.city.y_coord, target[0], target[1])
        travel_time = calc_time(speed, dist)
        launch_time = calc_launch_time(the_siege.landing_time, travel_time, armies[idx]['time_offset'])
        armies[idx]['launch_time'] = datetime.strftime(launch_time, date_format)
        armies[idx]['engines'] = "%s/%s" % (the_army.siege_engines, the_army.wall_engines)
    context['armies'] = armies
    return render(request, 'siege/schedule.html', context)

# Render player's siege schedule page
@login_required(login_url='/', redirect_field_name=None)
def player_schedule(request):
    q = Siege_army.objects.filter(player_id=request.user.player.id).select_related('player_id', 'army_id')
    sieges = Siege.objects.all().values()
    armies = [(lambda x: model_to_dict(x))(x) for x in q]
    siegedict = {}
    for siege in sieges:
        siegedict[siege['id']] = siege
        siegedict[siege['id']]['armies'] = []
        siegedict[siege['id']]['name'] = siege['target_player'] + ", " + siege['target_city'] + ", X:" + str(siege['x_coord']) + ", Y:" + str(siege['y_coord'])
    context = {}
    print(siegedict)
    for idx, army in enumerate(q):
        the_army = army.army_id
        new_army = {}
        siege_idx = armies[idx]['siege_id']
        new_army['player'] = the_army.player.__str__()
        new_army['city'] = the_army.city.name
        speed = the_army.speed
        siege = siegedict[siege_idx]
        new_army['speed'] = speed
        new_army['troop_type'] = the_army.get_troop_type_display()
        new_army['troop_count'] = the_army.troop_count
        siege_x = siege['x_coord']
        siege_y = siege['y_coord']
        landing_time = siege['landing_time']
        new_army['orders'] = army.orders
        new_army['siege_square'] = army.get_siege_square_display()
        target = calculate_target_coord(army.siege_square, siege_x, siege_y, army.orders)
        dist = calc_dist(the_army.city.x_coord, the_army.city.y_coord, target[0], target[1])
        travel_time = calc_time(speed, dist)
        launch_time = calc_launch_time(landing_time, travel_time, armies[idx]['time_offset'])
        new_army['launch_time'] = datetime.strftime(launch_time, date_format)
        new_army['engines'] = "%s/%s" % (the_army.siege_engines, the_army.wall_engines)
        siegedict[siege_idx]['armies'].append(new_army)
    print siegedict
    context['sieges'] = siegedict
    return render(request, 'siege/myschedule.html', context)






