"""Screen stuff"""

import os
import cv2
import time
import numpy
import ctypes
import pytesseract
from PIL import Image, ImageGrab

# default path - C:\Users\YOUR_USER\AppData\Local\Programs\Tesseract-OCR
pytesseract.pytesseract.tesseract_cmd = fr"{os.getenv('LOCALAPPDATA')}\Programs\Tesseract-OCR\tesseract.exe"

win32 = ctypes.windll.user32
win32.SetProcessDPIAware()

SCREEN_WIDTH = win32.GetSystemMetrics(0)
SCREEN_HEIGHT = win32.GetSystemMetrics(1)

SCALE_WIDTH = SCREEN_WIDTH/1920 # screen width/1920
SCALE_HEIGHT = SCREEN_HEIGHT/1080 # screen height/1080

coords = {"play_again": (375, 505, 174, 250), "operators": (208, 318, 52, 90), "locker": (374, 450, 52, 90), "section_1": (309, 440, 760, 815), "new_gamemode": (84, 441, 100, 257), "queueing": (808, 1026, 38, 68), "match_found": (862, 987, 36, 64), "end_of_game": (1261, 1465, 1002, 1033), "new_match_with_squad": (1541, 1755, 980, 1030), "ready_up": (1587, 1784, 996, 1044), "ok_popup": (692, 727, 920, 950), "other_popups": (699, 965, 927, 951), "reconnect": (837, 1080, 38, 68), "reconnect_queue": (385, 530, 185, 251), "banned": (655, 1045, 38, 68)}
keywords = {"in_lobby": ["play again", "operators", "locker", "new playlist", "new event", "tactical"], "queueing": ["crossplay", "match found"], "end_of_game": ["find another", "new match with", "ready to play"], "popups": ["ok", "cancel", "reconnect"], "reconnect": "reconnect", "banned": ["suspended", "banned"]}

def get_res_scale_x(x):
    return int(SCALE_WIDTH * x)

def get_res_scale_y(y):
    return int(SCALE_HEIGHT * y)

def take_screenshot(coords=None):
    im = ImageGrab.grab(bbox=coords) # lowest x, lowest y, highest x, highest y
    im.save(f'{os.environ.get('TEMP')}\\temp.png')

def read_screenshot(coords_type=None, keyword=None):
    if coords != None and keyword != None:
        take_screenshot((get_res_scale_x(coords[coords_type][0]), get_res_scale_y(coords[coords_type][2]), get_res_scale_x(coords[coords_type][1]), get_res_scale_y(coords[coords_type][3])))
        result = pytesseract.image_to_string(Image.open(f'{os.environ.get('TEMP')}\\temp.png'))
        if keyword in result.lower():
            return True
        else:
            return False

def detect_state(active, mnk, CRAPTOP):
    state = {"in_lobby": False, "queueing": False, "in_game": True, "reconnect": False, "popup": False, "end_of_game": False, "squad_leader": False, "ready_up": False, "banned": False}
    state["in_lobby"] = read_screenshot("play_again", keywords["in_lobby"][0])
    
    if not state["in_lobby"]:
        if read_screenshot("banned", keywords["banned"][0]) or read_screenshot("banned", keywords["banned"][1]):
            state["banned"] = True
            return state
        elif read_screenshot("operators", keywords["in_lobby"][1]) or read_screenshot("locker", keywords["in_lobby"][2]):
            mnk.select_button(active, x_coord=132, y_coord=71)
            time.sleep(4) if CRAPTOP else time.sleep(3)
            if read_screenshot("new_gamemode", keywords["in_lobby"][3]) or read_screenshot("new_gamemode", keywords["in_lobby"][4]):
                mnk.select_button(active, x_coord=110, y_coord=220)
                time.sleep(4) if CRAPTOP else time.sleep(3)
                if read_screenshot("section_1", keywords["in_lobby"][5]):
                    mnk.select_button(active, x_coord=343, y_coord=780)
                    time.sleep(4) if CRAPTOP else time.sleep(3)
                    mnk.select_button(active, x_coord=1030, y_coord=791)
                else:
                    mnk.select_button(active, x_coord=836, y_coord=783)
                    time.sleep(4) if CRAPTOP else time.sleep(3)
                    mnk.select_button(active, x_coord=1030, y_coord=791)
                time.sleep(2) if CRAPTOP else time.sleep(1)
            else:
                state["in_lobby"] = True # if the button doesn't need to be fixed, then toggle the in_lobby variable on.
        else:
            pass # do nothing  

    state["queueing"] = read_screenshot("queueing", keywords["queueing"][0])
    if not state["queueing"]:
        state["queueing"] = read_screenshot("match_found", keywords["queueing"][1])
    
    state["end_of_game"] = read_screenshot("end_of_game", keywords["end_of_game"][0])
    if not state["end_of_game"]:
        if read_screenshot("new_match_with_squad", keywords["end_of_game"][1]):
            state["end_of_game"] = True
            state["squad_leader"] = True
        elif read_screenshot("ready_up", keywords["end_of_game"][2]):
            state["end_of_game"] = True
            state["ready_up"] = True
        else:
            pass # do nothing because it means we're not in a game or in a party

    state["popup"] = read_screenshot("ok_popup", keywords["popups"][0])
    if not state["popup"]:
        for x in range(1, len(keywords["popups"])):
            state["popup"] = read_screenshot("other_popups", keywords["popups"][x])
            if state["popup"]:
                state["in_lobby"] = False
                state["queueing"] = False
                state["in_game"] = False
                state["reconnect"] = False
                state["end_of_game"] = False
                return state
    
    state["reconnect"] = read_screenshot("reconnect", keywords["reconnect"])
    if state["reconnect"]:
        if not read_screenshot("reconnect_queue", keywords["reconnect"]):
            state["reconnect"] = False
    
    for key, value in state.items():
        if value == True:
            if key != "in_game":
                state["in_game"] = False
                break
    return state
