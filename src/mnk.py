"""Mouse and keyboard functions"""

import time
import ctypes
import random
import screen
import keyboard
import pydirectinput
from active import ActiveManager

win32 = ctypes.windll.user32

# delay between press and release
KEYDELAY = 0.1

class MouseAndKeyboard:
    """Control Mouse And Keyboard"""
    def __init__(self) -> None:
        self.__actions = []
        self.__running = False

    def __run(self, active: ActiveManager):
        while len(self.__actions) > 0:
            action = self.__actions.pop(0)
            if active.is_active():
                fn = action[0]
                kwargs = action[1]
                fn(active=active, **kwargs)
        self.__running = False

    def __action(self, active: ActiveManager, function, **kwargs):
        self.__actions.insert(0, (function, kwargs))

        if not self.__running:
            self.__running = True
            self.__run(active)

    def select_button(self, active, x_coord, y_coord):
        for x in range(5):
            x = x_coord + random.choice([1, -1])
            y = y_coord + random.choice([1, -1])
            self.__action(active, self.move_mouse, x=x, y=y)
        self.__action(active, self.click, x=x_coord, y=y_coord)

    def click(self, active, **kwargs):
        """ Clicks mouse at current postion or at provided x and y.
        Usage - click(active, x = "x", y = "y")
        """
        self.__action(active, self.__click, **kwargs)
        
    def __click(self, **kwargs):
        x = kwargs.get('x')
        y = kwargs.get('y')

        if x is not None and y is not None:
            pydirectinput.moveTo(screen.get_res_scale_x(x), screen.get_res_scale_y(y))

        win32.mouse_event(0x0002, 0, 0, 0, 0) # Left click press
        time.sleep(KEYDELAY)
        win32.mouse_event(0x0004, 0, 0, 0, 0) # Left click release

    def keypress(self, active, **kwargs):
        """ Presses given key.
        Usage - keypress(active, key = "key")
        """
        self.__action(active, self.__keypress, **kwargs)

    def __keypress(self, **kwargs):
        key = kwargs.get('key')

        if key is not None:
            keyboard.press(key)
            time.sleep(random.uniform(0.5, 1.5))
            keyboard.release(key)

    def send_text(self, active, **kwargs):
        """Sends text"""
        self.__action(active, self.__send_text, **kwargs)

    def __send_text(self, **kwargs):
        text = kwargs.get('text')

        if text is not None:
            keyboard.press("t")
            time.sleep(KEYDELAY)
            keyboard.release("t")

            keyboard.press("backspace")
            time.sleep(KEYDELAY)
            keyboard.release("backspace")

            keyboard.write(text, KEYDELAY)

            keyboard.press("enter")
            time.sleep(KEYDELAY)
            keyboard.release("enter")

            keyboard.press("enter")
            time.sleep(KEYDELAY)
            keyboard.release("enter")

    def move_mouse(self, active, **kwargs):
        """Move mouse"""
        self.__action(active, self.__move_mouse, **kwargs)

    def __move_mouse(self, **kwargs):
        x = kwargs.get('x')
        y = kwargs.get('y')

        time.sleep(KEYDELAY)

        if x is not None and y is not None:
            pydirectinput.moveTo(screen.get_res_scale_x(x), screen.get_res_scale_y(y))
