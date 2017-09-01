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


def calculate_target_coord(square, x, y, orders):
    if orders == "blockade" or orders == "siege":
        return (x, y)
    if square == "N":
        if y != 0:
            y_coord = int((abs(y) - 1) * y / abs(y))
        else:
            y_coord = -1
        return (x, y_coord)
    elif square == "NE":
        if y != 0:
            y_coord = int((abs(y) - 1) * y / abs(y))
        else:
            y_coord = -1
        if x != 0:
            x_coord = int((abs(x) + 1) * x / abs(x))
        else:
            x_coord = 1
        return (x_coord, y_coord)
    elif square == "E":
        if x != 0:
            x_coord = int((abs(x) + 1) * x / abs(x))
        else:
            x_coord = 1
        return (x_coord, y)
    elif square == "SE":
        if x != 0:
            x_coord = int((abs(x) + 1) * x / abs(x))
        else:
            x_coord = 1
        if y != 0:
            y_coord = int((abs(y) + 1) * y / abs(y))
        else:
            y_coord = 1
        return (x_coord, y_coord)
    elif square == "S":
        if y != 0:
            y_coord = int((abs(y) + 1) * y / abs(y))
        else:
            y_coord = 1
        return (x, y_coord)
    elif square == "SW":
        if x != 0:
            x_coord = int((abs(x) - 1) * x / abs(x))
        else:
            x_coord = -1
        if y != 0:
            y_coord = int((abs(y) + 1) * y / abs(y))
        else:
            y_coord = 1
        return (x_coord, y_coord)
    elif square == "W":
        if x != 0:
            x_coord = int((abs(x) - 1) * x / abs(x))
        else:
            x_coord = -1
        return (x_coord, y)
    elif square == "NW":
        if x != 0:
            x_coord = int((abs(x) - 1) * x / abs(x))
        else:
            x_coord = -1
        if y != 0:
            y_coord = int((abs(y) - 1) * y / abs(y))
        else:
            y = -1
        return (x_coord, y_coord)
    else:
        return (x, y)
