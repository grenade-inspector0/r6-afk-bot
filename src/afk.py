print("v 0.01")

import time
import keyboard
import ctypes
import threading
import mnk
import screen

print(f'Resolution: {screen.SCREEN_WIDTH}x{screen.SCREEN_HEIGHT}')

global active
active = False

def run():
    while active:
        screen.scrape(active)

        mnk.keypress(active, key = '5')

        mnk.moveMouse(active, x=960, y=540)

        time.sleep(0.5)

global runner_thread
runner_thread = threading.Thread(target=run)

def on_press():
    global active
    active = not active

    global runner_thread

    if active:
        print("Activated.")
    else:
        print("Deactivated.")

    if not runner_thread.is_alive():
        runner_thread = threading.Thread(target=run)

    if active:
        runner_thread.start()
    else:
        runner_thread.join()

if __name__ == "__main__":
    ctypes.windll.kernel32.SetConsoleTitleW("ez")
    keyboard.add_hotkey(hotkey='f2', callback=on_press, suppress=True)

    print("Ready.")

    while True:
        time.sleep(1)