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
    q = list(Army.objects.filter(player__alliance_name='300').values('troop_type').annotate(Sum('troop_count')))
    q2 = Army.objects.filter(player__alliance_name='300').values('siege_engines').aggregate(Sum('siege_engines'))
    q3 = Army.objects.filter(player__alliance_name='300').values('wall_engines').aggregate(Sum('wall_engines'))
    result = {}
    result['siege'] = q2['siege_engines__sum']
    result['wall'] = q3['wall_engines__sum']
    for d in q:
        result[d['troop_type']] = d['troop_count__sum']
    result[u'Spear'] = 0
    result[u'Bow'] = 0
    result[u'Infs'] = 0
    result[u'Cav'] = 0

    if 'INF_T1' in result:
        result['Infs'] += result['INF_T1']
    else:
        result[u'INF_T1'] = 0
    if 'INF_T2' in result:
        result['Infs'] += result['INF_T2']
    else:
        result[u'INF_T2'] = 0
    if 'BOW_T1' in result:
        result['Bow'] += result['BOW_T1']
    else:
        result[u'BOW_T1'] = 0
    if 'BOW_T2' in result:
        result['Bow'] += result['BOW_T2']
    else:
        result[u'BOW_T2'] = 0
    if 'SP_T1' in result:
        result['Spear'] += result['SP_T1']
    else:
        result[u'SP_T1'] = 0
    if 'SP_T2' in result:
        result['Spear'] += result['SP_T2']
    else:
        result[u'SP_T2'] = 0
    if 'CAV_T1' in result:
        result['Cav'] += result['CAV_T1']
    else:
        result[u'CAV_T1'] = 0
    if 'CAV_T2' in result:
        result['Cav'] += result['CAV_T2']
    else:
        result[u'CAV_T2'] = 0
    print result
    return render(request, 'combats/stats.html', result)