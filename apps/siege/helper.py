import re
from datetime import datetime, timedelta
from math import sqrt

date_format = "%m-%d-%Y %H:%M:%S"
date_format2 = "%"
offset_regex = re.compile(r'(-?)(\d{2,}):([0-5][0-9]):([0-5][0-9])')


def calc_dist(x1, y1, x2, y2):
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)


def calc_time(speed, distance):
    hours = float(distance) / float(speed)
    return hours


# Parse time offset string
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
