"""Mouse and keyboard functions"""

import time
import ctypes
import pydirectinput
import keyboard
from afk import ActiveManager
import screen

win32 = ctypes.windll.user32

# delay between press and release
KEYDELAY = 0.1

def __action(active: ActiveManager, function, **kwargs):
    if active.is_active():
        function(**kwargs)

def click(active, **kwargs):
    """ Clicks mouse at current postion or at provided x and y.
    Usage - click(active, x = "x", y = "y")
    """
    __action(active, __click, **kwargs)
    
def __click(**kwargs):
    x = kwargs.get('x')
    y = kwargs.get('y')

    if x is not None and y is not None:
        pydirectinput.moveTo(screen.get_res_scale_x(x), screen.get_res_scale_y(y))

    win32.mouse_event(0x0002, 0, 0, 0, 0) # Left click press
    time.sleep(KEYDELAY)
    win32.mouse_event(0x0004, 0, 0, 0, 0) # Left click release

def keypress(active, **kwargs):
    """ Presses given key.
    Usage - keypress(active, key = "key")
    """
    __action(active, __keypress, **kwargs)

def __keypress(**kwargs):
    key = kwargs.get('key')

    if key is not None:
        keyboard.press(key)
        time.sleep(KEYDELAY)
        keyboard.release(key)

def send_text(active, **kwargs):
    """Sends text"""
    __action(active, __send_text, **kwargs)

def __send_text(**kwargs):
    text = kwargs.get('text')

    if text is not None:
        keyboard.press("t")
        time.sleep(KEYDELAY)
        keyboard.release("t")

        keyboard.press("backspace")
        time.sleep(KEYDELAY)
        keyboard.release("backspace")

        keyboard.write(text, 0.01)

        keyboard.press("enter")
        time.sleep(KEYDELAY)
        keyboard.release("enter")

def move_mouse(active, **kwargs):
    """Move mouse"""
    __action(active, __move_mouse, **kwargs)

def __move_mouse(**kwargs):
    x = kwargs.get('x')
    y = kwargs.get('y')

    time.sleep(KEYDELAY)

    if x is not None and y is not None:
        pydirectinput.moveTo(screen.get_res_scale_x(x), screen.get_res_scale_y(y))
