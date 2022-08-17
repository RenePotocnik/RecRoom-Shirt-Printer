import ctypes
import json
import time
from typing import NamedTuple, Tuple, Dict, List

import pyautogui
import pyperclip
from PIL import ImageGrab

import Encoding
from common import is_window_active, color_in_coords

# Check if the users monitor is 1440p or 1080p
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
SCREEN_DIMENSIONS: Tuple[int, int] = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


class Colors(NamedTuple):
    text = (55, 57, 61)  # The color of text in the Variable Input field (black)
    white = (229, 225, 216)  # The white background of the Variable Input field
    green = (187, 205, 182)  # The Variable Input field sometimes turns green - this is that color.


def copy_into_rr_variable(img_data: list[str], delay: float = 0.3, pause_at_50: bool = False,
                          stop_at_500: bool = False, ask_for_coords_calibration: bool = True,
                          ask_to_continue: bool = True):
    """
    Function copies strings of data into the RecRoom Variable.

    :param img_data: A list of strings to be imported into RecRoom
    :param delay: The delay between main actions (click > copy > confirm)
    :param pause_at_50: Should the script pause for a given amount of time every 50 imported strings
    (could prevent disconnection)
    :param stop_at_500: Should the script full stop every 500 imported strings, and wait for the user to press enter
    (could prevent disconnection)
    :param ask_for_coords_calibration: If there's no `coordinates.json`, remind user
    :param ask_to_continue: Should the user be asked when they want to continue
    """

    # These are the old, pre-made button coordinates only meant for 16:9 display aspect ratios
    input_field: Tuple[int, int] = (int(SCREEN_DIMENSIONS[0] * 0.5),
                                    int(SCREEN_DIMENSIONS[1] * 0.5625))
    confirm_expand_button: Tuple[int, int] = (int(SCREEN_DIMENSIONS[0] * 0.841015),
                                              int(SCREEN_DIMENSIONS[1] * 0.083333))

    color_check: List[Tuple[int, int]] = [(int(SCREEN_DIMENSIONS[0] * 0.1121), int(SCREEN_DIMENSIONS[1] * 0.4611)),
                                          (int(SCREEN_DIMENSIONS[0] * 0.1953), int(SCREEN_DIMENSIONS[1] * 0.5208))]

    # Check if there's a `coordinates.json` file; if there is -> use the coords written in there
    try:
        # Read the file for coordinates
        with open("coordinates.json", "r") as coords_file:
            coords: Dict[str, Tuple[int, int]] = json.load(coords_file)
            input_field = coords["InputField"]
            confirm_expand_button = coords["DoneButton"]
            color_check: List[Tuple[int, int]] = [(coords["InputField"][0] - 10, coords["InputField"][1] - 10),
                                                  (coords["InputField"][0] + 300, coords["InputField"][1] + 200)]
            print("Reading coordinates from `coordinates.json`...")

    except FileNotFoundError:
        if ask_for_coords_calibration:
            # If there's no file, the user hasn't calibrated coordinates yet. Ask to continue using preset or exit.
            if input("`coordinates.json` file not found.\n"
                     "You didn't calibrate the button coordinates yet.\n"
                     "Run `Coordinate_Calibration` if you wish to calibrate.\n"
                     'Enter "y" to exit this script,\n'
                     'or enter "n" to continue with preset coordinates (only for monitors with a 16:9 aspect ratio)\n'
                     '[default: y] > ').lower().find("n") == -1:
                exit()

    num_strings: int = len(img_data)
    sec_to_import: float = delay * 3 * num_strings
    print(f"Minimum time needed for importing: {int(sec_to_import // 60)} minutes, {int(sec_to_import % 60)} seconds")

    if ask_to_continue:
        if input(f"\nProceed to copy all {num_strings} strings to RecRoom? [y/n] ").lower() == "n":
            return

    time_at_start = time.time()

    "########################CONTINUE###########################"
    # If you want to continue from an existing string, set `continue_from` to `False`
    # and enter the string into the bottom `if` statement
    start_from_beginning: bool = True
    continue_from_string: str = "|Enter the string here|"
    "###########################################################"

    for num, string in enumerate(img_data):
        is_window_active("Rec Room")

        if start_from_beginning or continue_from_string in string:
            start_from_beginning = True
        else:
            continue

        # Copy current string into clipboard
        pyperclip.copy(string)
        print(f"Copying string #{num}/{num_strings - 1}")

        # In RR, click on the input field
        pyautogui.click(input_field)
        time.sleep(delay)

        # Max 10 tries to successfully copy the string
        for _ in range(10):
            # Paste the string into input
            pyautogui.hotkey("ctrl", "v")
            time.sleep(delay)
            if color_in_coords(image=ImageGrab.grab(),
                               color=Colors.text,
                               coordinates=color_check):
                break
            print("Failed copy")
            pyautogui.click(input_field)
            pyautogui.hotkey("ctrl", "a")
            time.sleep(delay * 2)

        # Max 10 tries to successfully confirm the string
        for _ in range(10):
            # Click on the "confirm" area
            pyautogui.click(confirm_expand_button)
            time.sleep(delay / 2)
            pyautogui.scroll(-50, x=confirm_expand_button[0], y=int(SCREEN_DIMENSIONS[1] / 2))
            time.sleep(delay)
            if color_in_coords(image=ImageGrab.grab(),
                               color=Colors.text,
                               coordinates=color_check):
                break
            print("Failed confirm")
            time.sleep(delay * 2)

        # Optional:

        if stop_at_500 and num and num % 500 == 0:
            # Every 500 entries stop and let the player continue when they see fit
            input("Stopped. Press enter to continue")
            continue
        if pause_at_50 and num and num % 50 == 0:
            # Every 50 entries give RR some time to process and catch up. Could prevent crashing :shrug:
            time.sleep(30)

    time_to_copy = time.time() - time_at_start
    minutes = time_to_copy // 60
    seconds = time_to_copy % 60
    print(f"Copying complete. Copied {num_strings - 1} strings in {minutes} min and {seconds:.1f} sec")


def main(from_file: bool = False):
    img_data: list[str]
    # Call function for encoding an image
    if not from_file:
        image, img_data = Encoding.main(list_size=50)
    else:
        try:
            with open("image_data.txt", "r") as f:
                temp: list[str] = f.readlines()
                img_data = [line.strip() for line in temp]
        except FileNotFoundError:
            print("The file `image_data.txt` was not found. ")
            image, img_data = Encoding.main(list_size=50)

    # Insert beginning and end.
    img_data.insert(0, "BEGIN")
    img_data.append("END")

    copy_into_rr_variable(img_data, delay=0.4, pause_at_50=False, stop_at_500=False)


if __name__ == "__main__":
    print("You're running `Importing.py` directly.\n"
          "This will take the encoded data in `image_data.txt` and import it.\n")
    main(from_file=True)
