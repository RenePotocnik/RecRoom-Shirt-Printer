import ctypes
import json
import logging
import subprocess
import sys
import time
from tkinter import *

from common import setup_logger, is_window_active

try:
    import pyautogui
    from PIL import Image, ImageGrab
except ModuleNotFoundError:
    print(f'Please execute the following line and run the script again:\n'
          f'{sys.executable} -m pip install -U PyAutoGUI')
    # Ask the user to install all the necessary packages automatically
    if input("Proceed to run the command automatically? [yes/no] ").find("yes") != -1:
        subprocess.call(f"{sys.executable} -m pip install -U PyAutoGUI")
    exit()


InputField = None
DoneButton = None

ctypes.windll.shcore.SetProcessDpiAwareness(2)


def coordinate_selection():
    global InputField, DoneButton

    def init_window() -> Tk:
        # Initialize the Tk window;  Alpha: 0.1, Fullscreen: True
        win_ = Tk()
        win_.attributes('-alpha', 0.05)
        win_.attributes('-fullscreen', True)
        win_.attributes("-topmost", True)
        return win_

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
        time.sleep(0.1)
        win.mainloop()
        time.sleep(0.1)

    print(f"Input button: {InputField}\nDone Button (arrows ↕): {DoneButton}")
    with open("coordinates.json", "w") as coords_file:
        json.dump({
            "InputField": InputField,
            "DoneButton": DoneButton
        }, coords_file, indent=4)


log: logging.Logger = setup_logger()


if __name__ == '__main__':
    try:
        coordinate_selection()
        exit(input("\n"
                   "Coordinate calibration done!\n"
                   "Press ENTER to exit\n"
                   "> "))
    except (Exception, KeyboardInterrupt):
        log.exception("ERROR", exc_info=True)
