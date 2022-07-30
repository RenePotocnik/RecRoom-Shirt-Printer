import ctypes
import json
import time
from tkinter import *

InputField = None
DoneButton = None

ctypes.windll.shcore.SetProcessDpiAwareness(2)


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
            input('Press ENTER to open RecRoom and press on the "Value" box (TOP-LEFT corner).\n> ')
        else:
            input('Press ENTER to open RecRoom and press the two arrows facing away from each-other ↕'
                  '(look at the GitHub tutorial for reference.\n> ')
        win = init_window()
        win.bind('<Button-1>', set_coords)
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
