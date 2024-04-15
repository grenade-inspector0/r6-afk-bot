"""Screen stuff"""

import ctypes
import time
from PIL import Image
import cv2
from mss import mss
import numpy
import mnk

win32 = ctypes.windll.user32
win32.SetProcessDPIAware()

SCREEN_WIDTH = win32.GetSystemMetrics(0)
SCREEN_HEIGHT = win32.GetSystemMetrics(1)

SCALE_WIDTH = SCREEN_WIDTH/1920 # screen width/1920
SCALE_HEIGHT = SCREEN_HEIGHT/1080 # screen height/1080

def __image(path):
    img = cv2.imread(path)
    i = cv2.resize(img, (0, 0), fx=SCALE_WIDTH, fy=SCALE_HEIGHT, interpolation= cv2.INTER_CUBIC)
    return i
 
play_again = __image('assets/images/play_again.jpg')
play_again_highlighted = __image('assets/images/play_again_highlighted.jpg')
reconnect_highlighted =  __image('assets/images/reconnect_highlighted.jpg')
reconnect =  __image('assets/images/reconnect.jpg')

popup_message_highlighted =  __image('assets/images/popup_message_highlighted.jpg')     

find_another_match_highlighted =  __image('assets/images/find_another_match_highlighted.jpg')
find_another_match =  __image('assets/images/find_another_match.jpg')

commend =  __image('assets/images/commend.jpg')

def get_res_scale_x(x):
    return int(SCALE_WIDTH * x)

def get_res_scale_y(y):
    return int(SCALE_HEIGHT * y)

def convert_region(left, top, right, bottom):
    return (get_res_scale_x(left), get_res_scale_y(top), get_res_scale_x(right), get_res_scale_y(bottom))

def __capture_screenshot():
    # Capture entire screen
    with mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        # Convert to PIL/Pillow Image
        return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

def __search_image(image, region, screen):
    img_cv = cv2.cvtColor(numpy.array(screen), cv2.COLOR_RGB2BGR)
    res = cv2.matchTemplate(img_cv[region[1]:region[3], region[0]:region[2]], image, cv2.TM_CCOEFF_NORMED)
    return (res >= 0.8).any()

def scrape(active):
    if not active.is_active():
        time.sleep(1)
        return

    screen = __capture_screenshot()

    if __search_image(play_again, convert_region(350, 150, 650, 200), screen):
        print('pressing play_again.')
        mnk.click(active, x=500,y=225)
        time.sleep(5)
        return

    if __search_image(play_again_highlighted, convert_region(340, 135, 680, 185), screen):
        print('pressing play_again_highlighted.')
        mnk.click(active, x=500,y=225)
        time.sleep(5)
        return

    if __search_image(reconnect, convert_region(350, 150, 650, 200), screen):
        print('pressing reconnect.')
        mnk.click(active, x=500,y=225)
        time.sleep(5)
        return

    if __search_image(reconnect_highlighted, convert_region(340, 135, 680, 185), screen):
        print('pressing reconnect_highlighted.')
        mnk.click(active, x=500,y=225)
        time.sleep(5)
        return

    if __search_image(popup_message_highlighted, convert_region(640, 900, 1290, 1000), screen):
        print('pressing popup_message_highlighted.')
        mnk.click(active, x=950,y=950)
        time.sleep(1)
        return

    if __search_image(commend, convert_region(1140, 880, 1500, 980), screen):
        print('pressing commend.')
        mnk.click(active, x=1330,y=930)
        time.sleep(0.5)
        mnk.click(active, x=950,y=930)
        time.sleep(0.5)
        mnk.click(active, x=570,y=930)
        time.sleep(0.5)
        mnk.click(active, x=250,y=930)
        time.sleep(0.5)
        return

    if __search_image(find_another_match, convert_region(1170, 930, 1490, 1070), screen):
        print('pressing find_another_match.')
        mnk.click(active, x=1330,y=1000)
        time.sleep(1)
        return

    if __search_image(find_another_match_highlighted, convert_region(1170, 930, 1490, 1070), screen):
        print('pressing find_another_match_highlighted.')
        mnk.click(active, x=1330,y=1000)
        time.sleep(1)
        return
