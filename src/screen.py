import ctypes
from typing import Optional
import numpy
import mnk
import time
from PIL import Image
import cv2
from mss import mss

SIEGE_WINDOW_NAMES = ["Rainbow Six"]

win32 = ctypes.windll.user32
win32.SetProcessDPIAware()

SCREEN_WIDTH = win32.GetSystemMetrics(0)
SCREEN_HEIGHT = win32.GetSystemMetrics(1)

SCALE_WIDTH = SCREEN_WIDTH/1920 # screen width/1920
SCALE_HEIGHT = SCREEN_HEIGHT/1080 # screen height/1080

def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(
            f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap

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

def getResScaleX(x):
    return int(SCALE_WIDTH * x)

def getResScaleY(y):
    return int(SCALE_HEIGHT * y)

def convertRegion(left, top, width, height):
    return (getResScaleX(left), getResScaleY(top), getResScaleX(width), getResScaleY(height))

def gameInFocus():
    window = getForegroundWindowTitle()
    return window in SIEGE_WINDOW_NAMES

def getForegroundWindowTitle() -> Optional[str]:
    hWnd = win32.GetForegroundWindow()
    length = win32.GetWindowTextLengthW(hWnd)
    buf = ctypes.create_unicode_buffer(length + 1)
    win32.GetWindowTextW(hWnd, buf, length + 1)
    
    return buf.value if buf.value else None

def capture_screenshot():
    # Capture entire screen
    with mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        # Convert to PIL/Pillow Image
        return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

def searchImage(image, region, screen):
    img_cv = cv2.cvtColor(numpy.array(screen), cv2.COLOR_RGB2BGR)
    res = cv2.matchTemplate(img_cv[region[1]:region[1]+region[3], region[0]:region[0]+region[2]], image, cv2.TM_CCOEFF_NORMED)
    return (res >= 0.8).any()

def scrape(active):
    screen = capture_screenshot()

    if searchImage(play_again, convertRegion(350, 150, 300, 50), screen):
        print('pressing play_again.')
        mnk.click(active,x=500,y=225)
        time.sleep(5)
        return

    if searchImage(play_again_highlighted, convertRegion(340, 135, 340, 60), screen):
        print('pressing play_again_highlighted.')
        mnk.click(active,x=500,y=225)
        time.sleep(5)
        return

    if searchImage(reconnect, convertRegion(350, 150, 300, 50), screen):
        print('pressing reconnect.')
        mnk.click(active,x=500,y=225)
        time.sleep(5)
        return

    if searchImage(reconnect_highlighted, convertRegion(340, 135, 340, 60), screen):
        print('pressing reconnect_highlighted.')
        mnk.click(active,x=500,y=225)
        time.sleep(5)
        return

    if searchImage(popup_message_highlighted, convertRegion(640, 900, 650, 100), screen):
        print('pressing popup_message_highlighted.')
        mnk.click(active,x=950,y=950)
        time.sleep(1)
        return

    if searchImage(commend, convertRegion(1140, 880, 360, 100), screen):
        print('pressing commend.')
        mnk.click(active,x=1325,y=930)
        time.sleep(1)
        mnk.click(active,x=950,y=930)
        time.sleep(1)
        return

    if searchImage(find_another_match, convertRegion(1170, 930, 320, 140), screen):
        print('pressing find_another_match.')
        mnk.click(active,x=1330,y=1000)
        time.sleep(1)
        return

    if searchImage(find_another_match_highlighted, convertRegion(1170, 930, 320, 140), screen):
        print('pressing find_another_match_highlighted.')
        mnk.click(active,x=1330,y=1000)
        time.sleep(1)
        return