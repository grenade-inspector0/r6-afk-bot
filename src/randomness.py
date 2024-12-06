import os
import sys
import time
import random

coord_range = {"maximum_x": 1000, "maximum_y": 1000}

def get_coord(coord_type=None):
    return random.randint(0, coord_range["maximum_x"]) if coord_type == "x" else random.randint(0, coord_range["maximum_y"])

def get_direction(exclude=None):
    keys = ["w", "a", "s", "d"]
    keys.remove(exclude) if exclude != None else ""
    key = random.choice(keys)
    return key

def get_positive_messages(num=3, allow_duplicates=False):
    if getattr(sys, 'frozen', False):
        file_path = os.path.join(sys._MEIPASS, 'assets', 'messages.txt')
    else:
        file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'messages.txt')
    with open(file_path, 'r') as file:
        messages = [line.strip() for line in file.readlines()]
    positive_messages = []
    while len(positive_messages) < num:
        new_message = random.choice(messages)
        if allow_duplicates:
            positive_messages.append(new_message)
        elif new_message not in positive_messages:
            positive_messages.append(new_message)
    return positive_messages