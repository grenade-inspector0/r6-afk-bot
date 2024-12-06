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

coords = {"play_again": (375, 505, 174, 250), "operators": (208, 318, 52, 90), "locker": (374, 450, 52, 90), "queueing": (808, 1026, 38, 68), "find_another_match": (1261, 1465, 1002, 1033), "ok_popup": (692, 727, 920, 950), "other_popup_messages": (699, 965, 927, 951), "reconnect": (837, 1080, 38, 68), "reconnect_queue": (385, 530, 185, 251)}
keywords = {"play_again": ["play again"], "operators": ["operators"], "locker": ["locker"], "queueing": ["crossplay"], "find_another_match": ["find another"], "ok_popup": ["ok"], "other_popup_messages": ["cancel", "reconnect"], "reconnect": ["reconnect"], "reconnect_queue": ["reconnect"]}

def get_res_scale_x(x):
    return int(SCALE_WIDTH * x)

def get_res_scale_y(y):
    return int(SCALE_HEIGHT * y)

def take_screenshot(coords=None):
    im = ImageGrab.grab(bbox=coords)
    im.save('temp.png')

def read_screenshot(coords_type=None, keyword=None):
    if coords != None and keyword != None:
        take_screenshot((get_res_scale_x(coords[coords_type][0]), get_res_scale_y(coords[coords_type][2]), get_res_scale_x(coords[coords_type][1]), get_res_scale_y(coords[coords_type][3])))
        result = pytesseract.image_to_string(Image.open('temp.png'))
        if keyword in result.lower():
            return True
        else:
            return False

def scrape(mnk):
    state = {"in_lobby": False, "queueing": False, "in_game": True, "reconnect": False, "ok_popup": False, "other_popups": False, "end_of_game": False}

    state["in_lobby"] = read_screenshot("play_again", keywords["play_again"][0])
    if not state["in_lobby"]:
        if read_screenshot("operators", keywords["operators"][0]) or read_screenshot("locker", keywords["locker"][0]):
            state["in_lobby"] = True

    state["queueing"] = read_screenshot("queueing", keywords["queueing"][0])
    state["end_of_game"] = read_screenshot("find_another_match", keywords["find_another_match"][0])
    state["ok_popup"] = read_screenshot("ok_popup", keywords["ok_popup"][0])

    for x in range(len(keywords["other_popup_messages"])):
        state["other_popups"] = read_screenshot("other_popup_messages", keywords["other_popup_messages"][x])
        if state["other_popups"]:
            state["in_lobby"] = False
            state["queueing"] = False
            state["in_game"] = False
            state["reconnect"] = False
            state["end_of_game"] = False
            return state
    
    state["reconnect"] = read_screenshot("reconnect", keywords["reconnect"][0])
    if state["reconnect"]:
        if not read_screenshot("reconnect_queue", keywords["reconnect_queue"][0]):
            print("okay")
            state["reconnect"] = False
    
    for key, value in state.items():
        if value == True:
            if key != "in_game":
                state["in_game"] = False
                break
    return state
