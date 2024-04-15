"""AFK bot for R6"""

import time
import threading
import ctypes
import keyboard
import mnk
import screen

VERSION = 0.02
APP_NAME = f"VeryBannable AFK bot for Rainbow Six v{str(VERSION)}"

SIEGE_WINDOW_NAMES = ["Rainbow Six"]

USER32 = ctypes.windll.user32
USER32.SetProcessDPIAware() # neccesary if the user has scaling enabled in Windows

class ActiveManager:
    """Tracks whether or not the bot is active and if the window is in focus."""
    def __init__(self) -> None:
        self.__user_active = False

    @staticmethod
    def __window_in_focus() -> bool:
        hwnd = USER32.GetForegroundWindow()
        length = USER32.GetWindowTextLengthW(hwnd)
        buf = ctypes.create_unicode_buffer(length + 1)
        USER32.GetWindowTextW(hwnd, buf, length + 1)

        window = buf.value if buf.value else None
        in_focus = window in SIEGE_WINDOW_NAMES
        return in_focus

    def user_active(self) -> bool:
        """Returns true if the user inputs indicate the bot bot should be running"""
        return self.__user_active

    def is_active(self) -> bool:
        """Returns true if bot actions should be performed."""
        if not self.__user_active:
            return False

        return ActiveManager.__window_in_focus()

    def switch_active(self) -> None:
        """Switch whether the bot is active."""
        self.__user_active = not self.__user_active

    def scrape(self):
        screen.scrape(self)

__ACTIVE = ActiveManager()

def run_inputs():
    """Run the inputs."""
    while True:
        active = __ACTIVE
        mnk.keypress(active, key = '5')

        mnk.move_mouse(active, x=960, y=540)

        time.sleep(0.5)

        if not __ACTIVE.user_active():
            break

def run_scraping():
    while True:
        active = __ACTIVE
        active.scrape()

class ThreadManager:
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

__THREADS = ThreadManager()

def __on_press():
    """Activate/deactivate the bot when the hot key is pressed."""
    __ACTIVE.switch_active()

    if __ACTIVE.user_active():
        print("Activated.")
        __THREADS.start()
    else:
        print("Deactivated.")
        __THREADS.stop()

if __name__ == "__main__":
    ctypes.windll.kernel32.SetConsoleTitleW(APP_NAME)
    print(f'v{VERSION}')
    print(f'Resolution: {screen.SCREEN_WIDTH}x{screen.SCREEN_HEIGHT}')

    keyboard.add_hotkey(hotkey='f2', callback=__on_press, suppress=True)

    print("Ready.")

    while True:
        time.sleep(1)
