from datetime import datetime
from django import db, template
from ..views import calc_dist, calc_time, calculate_target_coord, calc_launch_time
from django.forms.models import model_to_dict
from ..models import (Siege_army)

register = template.Library()
date_format = "%m-%d-%Y %H:%M:%S"

@register.inclusion_tag('siege/siege_armies_partial.html', takes_context=True)
def siege_armies_partial(context):
    siege = context['siege']['id']
    print "#################Siege: {0}".format(siege)
    armies = Siege_army.objects.filter(siege_id=siege).select_related('siege_id', 'army_id')
    result = [(lambda x: model_to_dict(x))(x) for x in armies]
    print "Result: {0}".format(result)
    mydict = {}
    mydict['siegeId'] = siege
    for idx, army in enumerate(armies):
        the_army = army.army_id
        the_siege = army.siege_id
        result[idx]['player'] = the_army.player.__str__()
        result[idx]['city']= the_army.city.name
        origin_x = the_army.city.x_coord
        origin_y = the_army.city.y_coord
        target = calculate_target_coord(army.siege_square, the_siege.x_coord, the_siege.y_coord)
        dist = calc_dist(origin_x, origin_y, target[0], target[1])
        speed = the_army.speed
        result[idx]['armyId'] = army.army_id.id
        result[idx]['siegearmyId'] = army.id
        result[idx]['speed'] = speed
        result[idx]['troop_type'] = the_army.troop_type
        result[idx]['dist'] = "%.3f" % (dist)
        result[idx]['troop_count'] = the_army.troop_count
        travel_time = calc_time(speed, dist)
        result[idx]['travel_time'] = "%.3f" % (travel_time)
        launch_time = calc_launch_time(the_siege.landing_time, travel_time, result[idx]['time_offset'])
        result[idx]['launch_time'] = datetime.strftime(launch_time, date_format)
        result[idx]['time_offset'] = get_timestring(result[idx]['time_offset'])
    mydict['result'] = result
    return {"mydict" : mydict}

def get_timestring(seconds):
    timestring = ""
    if seconds < 0:
        timestring += "-"
    seconds = abs(seconds)
    hours = abs(int(round(seconds/3600)))
    minutes = abs(int(round(seconds - hours*3600)/60))
    sec = seconds - hours*3600 - minutes * 60

    timestring += "%02d"%(hours) + ":" + "%02d"%(minutes) + ":" + "%02d"%(sec)
    return timestring
