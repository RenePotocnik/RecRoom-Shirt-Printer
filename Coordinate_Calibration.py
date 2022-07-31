import ctypes
import json
import time
from tkinter import *
from typing import List, Any

import pyautogui

InputField = None
DoneButton = None

ctypes.windll.shcore.SetProcessDpiAwareness(2)


def is_window_active(window_title: str = "Rec Room") -> bool:
    """
    Does not return before `window_title` becomes the active window
    Returns true when `window_title` becomes the active window

    :param window_title: The title of the window
    :return: When the window becomes active
    """
    if window_title not in (pyautogui.getActiveWindowTitle() or ""):  # getActiveWindowTitle is sometimes `None`
        print(f"Waiting for {window_title} to become the active window... ", end="\r", flush=True)
        # While RecRoom window is not active, sleep
        while window_title not in (pyautogui.getActiveWindowTitle() or ""):
            time.sleep(0.1)
        print(" " * 70, end="\r")  # Empty the last line in the console
        time.sleep(0.5)
    return True


def coordinate_selection():
    global InputField, DoneButton

    def init_window() -> Tk:
        # Initialize the Tk window;  Alpha: 0.1, Fullscreen: True
        win = Tk()
        win.attributes('-alpha', 0.05)
        win.attributes('-fullscreen', True)
        return win

    def set_coords(e):
        # Triggers when `Left Mouse Button` is pressed on the window
        global InputField, DoneButton

        if not InputField:
            print(f"Clicked Input field on {e.x}x{e.y}")
            InputField = (e.x, e.y)
        elif not DoneButton:
            print(f"Clicked Done Button on {e.x}x{e.y}")
            DoneButton = (e.x, e.y)
        win.destroy()

    input('\n'
          '    COORDINATE COORDINATION\n'
          'Not everyone has the same monitor size. You will be prompted to first click on the "Value" box, '
          'and then the two arrows facing away from each-other ↕.\n'
          'If you dont do this correctly, the importing script will not work\n'
          'You can look on the GitHub page for a video tutorial.\n'
          'Press enter to continue.\n'
          '> ')

    for num in range(2):
        if num == 0:
            input('Press ENTER, open RecRoom and press on the "Value" box (TOP-LEFT corner).\n'
                  '(look at the GitHub tutorial for reference).\n'
                  '> ')
        else:
            input('Press ENTER, open RecRoom and press the two arrows facing away from each-other ↕.\n'
                  '(look at the GitHub tutorial for reference).\n'
                  '> ')
        win = init_window()
        win.bind('<Button-1>', set_coords)
        is_window_active()
        time.sleep(1)
        win.mainloop()
        time.sleep(1)

    print(f"Input button: {InputField}\nDone Button (arrows ↕): {DoneButton}")
    with open("coordinates.json", "w") as coords_file:
        json.dump({
            "InputField": InputField,
            "DoneButton": DoneButton
        }, coords_file, indent=4)


if __name__ == '__main__':
    coordinate_selection()
