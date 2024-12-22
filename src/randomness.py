import os
import sys
import time
import random

coord_range = {"maximum_x": 1000, "maximum_y": 1000}

def get_coord(coord_type=None):
    return random.randint(0, coord_range["maximum_x"]) if coord_type == "x" else random.randint(0, coord_range["maximum_y"])

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

def get_direction(exclude=None):
    keys = ["w", "a", "s", "d"]
    keys.remove(exclude) if exclude != None else ""
    key = random.choice(keys)
    return key

def get_actions():
    actions = []
    for x in range(random.randint(random.randint(3, 5), random.randint(6, 8))):
        match random.randint(1, 5):
            case 1:
                actions.append("dk") # directional key
            case 2:
                actions.append("dk_shift") # directional key + shift
            case 3:
                actions.append("mm") # mousement movement
            case 4:
                actions.append("mm_dk") # mousement movement + directional key
            case 5:
                for x in range(random.randint(1, 3)):
                    actions.append(random.choice(["dk", "dk_shift", "mm", "mm_dk"]))
    return actions