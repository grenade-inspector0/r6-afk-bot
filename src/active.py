import ctypes
import screen

USER32 = ctypes.windll.user32

SIEGE_WINDOW_NAMES = ["Rainbow Six"]

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

    def scrape(self, mnk):
        screen.scrape(self, mnk)