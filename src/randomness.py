import time
import random

messages = ["Good luck, have fun!", "What a save!", "Close one", "Nice clutch", "You've got this!", "You're unstoppable!", "I wish everyone here a nice day :)"]
coord_range = {"maximum_x": 1000, "maximum_y": 1000}

def get_coord(coord_type=None):
    return random.randint(0, coord_range["maximum_x"]) if coord_type == "x" else random.randint(0, coord_range["maximum_y"])

def get_direction(exclude=None):
    keys = ["w", "a", "s", "d"]
    keys.remove(exclude) if exclude != None else ""
    key = random.choice(keys)
    return key

def get_positive_messages(num=3, allow_duplicates=False):
    positive_messages = []
    while True:
        if len(messages) >= 3:
            break
        else:
            new_message = random.choice(messages)
            if allow_duplicates:
                positive_messages.append(new_message)
            else:
                if new_message in positive_messages:
                    continue
                else:
                    positive_messages.append(new_message)
    return positive_messages