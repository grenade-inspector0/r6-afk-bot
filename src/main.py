import os
import sys
import time
import ctypes
import random
import screen
import keyboard
import threading
from screen import detect_state
from active import ActiveManager
from mnk import MouseAndKeyboard
from randomness import get_coord, get_direction, get_positive_messages

CRAPTOP = False

VERSION = 1.10
APP_NAME = f"AFK Bot for Rainbow Six Siege v{str(VERSION)}"

USER32 = ctypes.windll.user32
USER32.SetProcessDPIAware()

__MNK = MouseAndKeyboard()
__ACTIVE = ActiveManager()

last_key = None
last_message = None

IS_BANNED = False

def run_inputs():
    """Run the inputs."""
    global IS_BANNED
    global last_key
    global last_message
    while not IS_BANNED:
        active = __ACTIVE
        state = detect_state(active, __MNK, CRAPTOP=CRAPTOP)
        if state["banned"]:
            if os.path.exists(f"{os.environ.get('TEMP')}\\temp.png"):
                os.remove(f"{os.environ.get('TEMP')}\\temp.png")
            IS_BANNED = True
            os.system("cls")
            print("Ban Detected.\nAFK Bot Deactivated.")
            sys.exit()
        elif state["popup"]:
            # accept the popup
            __MNK.select_button(active, x_coord=744, y_coord=946)
        elif state["reconnect"]:
            # reconnect to the game then sleep until in the game
            __MNK.select_button(active, x_coord=482, y_coord=215)
            time.sleep(15) if CRAPTOP else time.sleep(10)
        elif state["in_lobby"]:
            # move mouse to the main menu
            __MNK.select_button(active, x_coord=132, y_coord=71)
            time.sleep(4) if CRAPTOP else time.sleep(1.5)
            # press play again
            __MNK.select_button(active, x_coord=440, y_coord=213)
            time.sleep(7.5) if CRAPTOP else time.sleep(2)
        elif state["queueing"]:
            # move mouse randomly until in a game
            for x in range(random.randint(2, 5)):
                __MNK.move_mouse(active, x=get_coord(coord_type="x"), y=get_coord(coord_type="y"))
        elif state["in_game"]:
            for x in range(random.randint(2, 5)):
                key = get_direction(last_key if last_key != None else None)
                __MNK.keypress(active, key=key)
                last_key = key

                __MNK.move_mouse(active, x=get_coord(coord_type="x"), y=get_coord(coord_type="y"))
            time.sleep(1)    
            if time.time() > (last_message + 300):
                messages = get_positive_messages()
                for message in messages:
                    __MNK.send_text(active, text=message)
                    time.sleep(random.uniform(1.5, 2.5))
                last_message = time.time()
        elif state["end_of_game"]:
            if state["squad_leader"]:
                # press new match with squad if found to be in a squad as the squad leader
                __MNK.select_button(active, x_coord=1652, y_coord=1023)
                time.sleep(3.5) if CRAPTOP else time.sleep(2)
                __MNK.select_button(active, x_coord=736, y_coord=985)
            elif state["ready_up"]:
                # press ready up if found to be in a squad, but not the squad leader
                __MNK.select_button(active, x_coord=1677, y_coord=1027)
                # move mouse randomly until in a game
                for x in range(random.randint(5, 10)):
                    __MNK.move_mouse(active, x=get_coord(coord_type="x"), y=get_coord(coord_type="y"))
            else:
                # press find another match if found to not be in a squad
                __MNK.select_button(active, x_coord=1370, y_coord=1026)

        if not __ACTIVE.user_active():
            break
        else:
            time.sleep(2.5) # this sleep timer is mainly for older computers with worse graphics, but it's also useful for the state detection

class Threads:
    """Tracks the threads that should run when the bot is on
    and joins them when they should close."""
    def __init__(self) -> None:
        self.runner_thread = threading.Thread(target=run_inputs)

    def start(self):
        """Start bot"""
        self.runner_thread.start()

    def stop(self):
        """Stop bot"""
        self.runner_thread.join()
        if not self.runner_thread.is_alive():
            self.runner_thread = threading.Thread(target=run_inputs)

__THREADS = Threads()

def __on_press():
    """Activate/deactivate the bot when the hot key is pressed."""
    global last_message
    __ACTIVE.switch_active()

    if __ACTIVE.user_active():
        __THREADS.start()
        if last_message == None:
            last_message = time.time()
        print("Activated.")
    else:
        __THREADS.stop()
        if os.path.exists(f"{os.environ.get('TEMP')}\\temp.png"):
            os.remove(f"{os.environ.get('TEMP')}\\temp.png")
        last_message = None
        print("Deactivated.")

if __name__ == "__main__":
    os.system("cls")
    if os.path.exists(f"{os.getenv('LOCALAPPDATA')}/Programs/Tesseract-OCR/tesseract.exe"):
        ctypes.windll.kernel32.SetConsoleTitleW(APP_NAME)
        print(f'v{VERSION}')
        print(f'Resolution: {screen.SCREEN_WIDTH}x{screen.SCREEN_HEIGHT}')

        keyboard.add_hotkey(hotkey='f2', callback=__on_press, suppress=True)

        print("Ready.")

        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                sys.exit()
    else:
        print("[ERROR] Tesseract.exe not found...\nTry to install it again and see if it fixes it.")
        sys.exit()