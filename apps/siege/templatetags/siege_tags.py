from datetime import datetime
from django import db, template
from ..views import calc_dist, calc_time, calculate_target_coord, calc_launch_time
from django.forms.models import model_to_dict
from ..models import (Siege_army)

register = template.Library()
date_format = "%d %b %H:%M:%S"

@register.inclusion_tag('siege/siege_armies_partial.html')
def siege_armies_partial():
    armies = Siege_army.objects.all().select_related('siege_id', 'army_id')
    result = [(lambda x: model_to_dict(x))(x) for x in armies]
    print "Result: {0}".format(result)
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
        result[idx]['speed'] = speed
        result[idx]['troop_type'] = the_army.troop_type
        result[idx]['dist'] = "%.3f" % (dist)
        travel_time = calc_time(speed, dist)
        result[idx]['travel_time'] = "%.3f" % (travel_time)
        launch_time = calc_launch_time(the_siege.landing_time, travel_time, result[idx]['time_offset'])
        result[idx]['launch_time'] = datetime.strftime(launch_time, date_format)
    print "Number of queries made: {0}".format(len(db.connection.queries))
    return {"result" : result}
