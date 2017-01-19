from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json, os, requests
from django.db.models import Sum
from ..siege.models import (Siege, Siege_army, City, Army, SiegeForm, Player, ArmyForm, CityForm)
from urlparse import urljoin


# Create your views here.
COMBATS_PORT = os.getenv('COMBATS_SERVICE_SERVICE_PORT', '5000')
COMBATS_HOST = os.getenv('COMBATS_SERVICE_SERVICE_HOST', 'localhost')
COMBATS_PATH = "http://" + COMBATS_HOST + ":" + COMBATS_PORT


def health(request):
    r = requests.get(COMBATS_PATH)
    data = r.json()
    response = json.dumps(data)
    return HttpResponse(response, content_type='application/json')


@login_required(login_url='/', redirect_field_name=None)
def stats(request):

    #get alliance total troop counts
    q = list(Army.objects.filter(player__alliance_name='300').values('troop_type').annotate(Sum('troop_count')))
    q2 = Army.objects.filter(player__alliance_name='300').values('siege_engines').aggregate(Sum('siege_engines'))
    q3 = Army.objects.filter(player__alliance_name='300').values('wall_engines').aggregate(Sum('wall_engines'))
    troop_counts = format_troop_counts(q)
    troop_counts['siege'] = q2['siege_engines__sum']
    troop_counts['wall'] = q3['wall_engines__sum']

    #get last week's total kills
    req1 = requests.get(COMBATS_PATH+'/combats/totals/300')
    res1 = req1.json()
    print "#########RESPONSE: %s ##########" % res1
    totals = format_weekly_totals(res1)

    #get last month's top 10 combats
    req2 = requests.get(COMBATS_PATH+'/combats/topten/300')
    res2 = req2.json()['list']
    print "#########RESPONSE: %s ##########" % res2

    context = {'troop_counts': troop_counts, 'totals': totals, 'topten': res2}
    return render(request, 'combats/stats.html', context)


@login_required(login_url='/', redirect_field_name=None)
def update(request):
    if request.user.is_staff:
        r = requests.get(COMBATS_PATH+"/dbupd/")
        data = r.json()
        response = json.dumps(data)
        return HttpResponse(response, content_type='application/json')
    else:
        return HttpResponse("You do not have permissions to view this page")


# View to administer players in the combats API
@login_required(login_url='/', redirect_field_name=None)
def admin(request):
    if request.user.is_staff:
        if request.method == "GET":
            r = requests.get(COMBATS_PATH + "/players")
            data = r.json()
            return render(request, 'combats/admin.html', data)
        elif request.method == "POST":
            payload = json.dumps(request.POST)
            print payload
            r = requests.post(COMBATS_PATH+"/players/", payload)
            print r.status_code
            if r.status_code == 200:
                return redirect('comadmin')
            else:
                r = requests.get(COMBATS_PATH + "/players")
                data = r.json()
                data['error'] = r.reason
                return render(request, 'combats/admin.html', data)
    else:
        return HttpResponse("You do not have sufficient permissions to view this page")


# Formats the query results for alliance's troop counts.
def format_troop_counts(q):
    troop_counts={}
    for d in q:
        troop_counts[d['troop_type']] = d['troop_count__sum']
    troop_counts[u'Spear'] = 0
    troop_counts[u'Bow'] = 0
    troop_counts[u'Infs'] = 0
    troop_counts[u'Cav'] = 0

    if 'INF_T1' in troop_counts:
        troop_counts['Infs'] += troop_counts['INF_T1']
    else:
        troop_counts[u'INF_T1'] = 0
    if 'INF_T2' in troop_counts:
        troop_counts['Infs'] += troop_counts['INF_T2']
    else:
        troop_counts[u'INF_T2'] = 0
    if 'BOW_T1' in troop_counts:
        troop_counts['Bow'] += troop_counts['BOW_T1']
    else:
        troop_counts[u'BOW_T1'] = 0
    if 'BOW_T2' in troop_counts:
        troop_counts['Bow'] += troop_counts['BOW_T2']
    else:
        troop_counts[u'BOW_T2'] = 0
    if 'SP_T1' in troop_counts:
        troop_counts['Spear'] += troop_counts['SP_T1']
    else:
        troop_counts[u'SP_T1'] = 0
    if 'SP_T2' in troop_counts:
        troop_counts['Spear'] += troop_counts['SP_T2']
    else:
        troop_counts[u'SP_T2'] = 0
    if 'CAV_T1' in troop_counts:
        troop_counts['Cav'] += troop_counts['CAV_T1']
    else:
        troop_counts[u'CAV_T1'] = 0
    if 'CAV_T2' in troop_counts:
        troop_counts['Cav'] += troop_counts['CAV_T2']
    else:
        troop_counts[u'CAV_T2'] = 0
    return troop_counts


# Formats the query results for weekly alliance totals.
def format_weekly_totals(res):
    totals = {}
    for k, v in res.items():
        n_players = len(v['Allies'])
        for i in v['Allies']:
            player = i
            for key in v.keys():
                if key != 'Allies':
                    enemy = key
                    for tally in v[enemy]:
                        unit_type = tally['Unit type']
                        casualties = int(tally['Casualties'])/n_players
                        print "Player: %s, unit_type: %s, casualties: %s" %(player, unit_type, casualties)
                        if player not in totals:
                            totals[player] = {enemy: {unit_type: casualties}}
                        else:
                            if enemy not in totals[player]:
                                totals[player][enemy] = {unit_type: casualties}
                            else:
                                if unit_type not in totals[player][enemy]:
                                    totals[player][enemy][unit_type] = casualties
                                else:
                                    totals[player][enemy][unit_type] += casualties
    for k, v in totals.items():
        for enemy, tally in totals[k].items():
            totals[k][enemy]['Total'] = reduce(lambda x, value: x + value, tally.values(), 0)
    return totals





