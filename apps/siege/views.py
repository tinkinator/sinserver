from __future__ import division
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms.models import model_to_dict
from math import sqrt
from .models import (Siege, Siege_army, City, Army, SiegeForm, Player)

@login_required(login_url='/', redirect_field_name=None)
def manage(request):
    sieges = {
        'sieges': Siege.objects.all(),
        'form': SiegeForm(label_suffix="")
        }
    print sieges['form']
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
    inner_queryset = set(Siege_army.objects.all())
    armies = Army.objects.filter(siege_army__isnull=True).values()
    the_siege = model_to_dict(Siege.objects.get(id=siege))
    for army in armies:
        print army
        city = City.objects.get(id__in=Army.objects.filter(id=army['id']))
        army['city'] = city.name
        army['player'] = Player.objects.get(id=army['player_id']).__str__()
        distance = calc_dist(city.x_coord, city.y_coord, the_siege['x_coord'], the_siege['y_coord'])
        army['dist'] = distance
        army['time'] = calc_time(army['speed'], distance)
    squares = [k for (k,v) in the_siege.items() if (v == True and v != "id")]
    context = {
        'armies': armies,
        'siege': the_siege, 
        'siege_armies': inner_queryset,
        'squares': squares,
        'orders': [x[0] for x in Siege_army.ORDERS]
    }
    return render(request, 'siege/edit_siege.html', context)

def add_army(request):
        pass

def reload_siege_partial():
    pass

def calc_dist(x1, y1, x2, y2):
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calc_time(speed, distance):
    hours = float(distance) / float(speed)
    return  "%.3f" % (hours)

