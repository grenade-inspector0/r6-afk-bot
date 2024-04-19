"""AFK bot for R6"""

import time
import threading
import ctypes
import keyboard
from active import ActiveManager
from mnk import MouseAndKeyboard
import screen
from config import Config

VERSION = 0.04
APP_NAME = f"VeryBannable AFK bot for Rainbow Six v{str(VERSION)}"

USER32 = ctypes.windll.user32
USER32.SetProcessDPIAware() # neccesary if the user has scaling enabled in Windows

__CONFIG = Config()
__MNK = MouseAndKeyboard()
__ACTIVE = ActiveManager()

global link_time
link_time = time.time()

def run_inputs():
    """Run the inputs."""
    while True:
        active = __ACTIVE
        __MNK.keypress(active, key = '5')

        __MNK.move_mouse(active, x=960, y=540)

        time.sleep(0.5)

        global link_time

        if __CONFIG.spam_link and time.time() > (link_time + __CONFIG.link_delay):
            __MNK.send_text(active, text = __CONFIG.link)
            link_time = time.time()

        if not __ACTIVE.user_active():
            break

def run_scraping():
    while True:
        active = __ACTIVE
        active.scrape(__MNK)

        if not __ACTIVE.user_active():
            break

class Threads:
    """Tracks the threads that should run when the bot is on
    and joins them when they should close."""
    def __init__(self) -> None:
        self.runner_thread = threading.Thread(target=run_inputs)
        self.scraper_thread = threading.Thread(target=run_scraping)

    def start(self):
        """Start bot"""
        self.runner_thread.start()
        self.scraper_thread.start()

    def stop(self):
        """Stop bot"""
        self.runner_thread.join()
        self.scraper_thread.join()
        if not self.runner_thread.is_alive():
            self.runner_thread = threading.Thread(target=run_inputs)
        if not self.scraper_thread.is_alive():
            self.scraper_thread = threading.Thread(target=run_scraping)

__THREADS = Threads()

def __on_press():
    """Activate/deactivate the bot when the hot key is pressed."""
    __ACTIVE.switch_active()

    if __ACTIVE.user_active():
        __THREADS.start()
        print("Activated.")
    else:
        __THREADS.stop()
        print("Deactivated.")

if __name__ == "__main__":
    ctypes.windll.kernel32.SetConsoleTitleW(APP_NAME)
    print(f'v{VERSION}')
    print(f'Resolution: {screen.SCREEN_WIDTH}x{screen.SCREEN_HEIGHT}')

    keyboard.add_hotkey(hotkey='f2', callback=__on_press, suppress=True)

    print("Ready.")

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            exit(1)