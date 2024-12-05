import time
import random

coord_range = {"maximum_x": 1000, "maximum_y": 1000}

def get_direction(exclude=None):
    keys = ["w", "a", "s", "d"]
    keys.remove(exclude) if exclude != None else ""
    key = random.choice(keys)
    return key

def get_coord(coord_type=None):
    return random.randint(0, coord_range["maximum_x"]) if coord_type == "x" else random.randint(0, coord_range["maximum_y"])