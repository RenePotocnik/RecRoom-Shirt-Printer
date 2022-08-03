import ctypes
from typing import NamedTuple, Tuple, List

import pyautogui
import pyperclip
from PIL import ImageGrab

import Encoding
import time


class ImageCoords(NamedTuple):
    min_y: int
    min_x: int

    max_y: int
    max_x: int


# Check if the users monitor is 1440p or 1080p
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
SCREEN_DIMENSIONS: Tuple[int, int] = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
if round(SCREEN_DIMENSIONS[0] / SCREEN_DIMENSIONS[1], 2) != 1.78:
    exit(input("\nScreen aspect ratio not optimal for importing.\n"
               "Press enter to exit\n"
               "> "))

DonePosition = Tuple[int, int]


class Colors(NamedTuple):
    text = (55, 57, 61)  # The color of text in the Variable Input field (black)
    white = (229, 225, 216)  # The white background of the Variable Input field
    green = (187, 205, 182)  # The Variable Input field sometimes turns green - this is that color.


def is_window_active(window_title: str = "Rec Room") -> bool:
    """
    Does not return before `window_title` becomes the active window
    Returns true when `window_title` becomes the active window

    :param window_title: The title of the window
    :return: When the window becomes active
    """
    if window_title not in (pyautogui.getActiveWindowTitle() or ""):  # getActiveWindowTitle is sometimes `None`
        print(f"Waiting for {window_title} to be the active window... ", end="\r", flush=True)
        # While RecRoom window is not active, sleep
        while window_title not in (pyautogui.getActiveWindowTitle() or ""):
            time.sleep(0.1)
        print(" " * 70, end="\r")  # Empty the last line in the console
        time.sleep(0.5)
    return True


def is_color(compare_color: tuple[int, int, int], main_color: tuple[int, int, int], tolerance: int = 30) -> bool:
    """
    Compare `compare_color` to `main_color` with a given tolerance

    :param compare_color: The color that is being compared
    :param main_color: The color that is being compared
    :param tolerance: How close the colors can be (1 - 255)
    :return: Is `compare_color` same/similar as `main_color`
    """
    return ((abs(compare_color[0] - main_color[0]) < tolerance)
            and (abs(compare_color[1] - main_color[1]) < tolerance)
            and (abs(compare_color[2] - main_color[2]) < tolerance))


def found_colors(main_color: tuple[int, int, int], coordinates: ImageCoords) -> bool:
    """
    Returns True if `main_color` is found in the given coordinates

    :param main_color: The color to compare the detected color to
    :param coordinates: Coordinates of the window of pixels to be checked and compared
    :return: If the color in any of the pixels match the `main_color`
    """
    image = ImageGrab.grab()

    for coords_x in range(coordinates.min_x, coordinates.max_x):
        if is_color(image.getpixel((coords_x, coordinates.min_y)), main_color):
            return True

    return False


def copy_to_recroom(img_data: list[str], delay: float = 0.3, last_successful_string: str or None = None) -> None:
    """
    Function copies 512 char string into RecRoom List Creates.
    :param last_successful_string: The last successfully copied string.
           Useful if importing fails somewhere in the middle
    :param delay: The main delay between actions
    :param img_data: A list of strings of color data for each pixel
    """
    window_title = "Rec Room"
    num_strings = len(img_data)

    # Coordinates for all the buttons
    input_field: DonePosition = (int(SCREEN_DIMENSIONS[0] * 0.5), int(SCREEN_DIMENSIONS[1] * 0.34))
    done_button: DonePosition = (int(SCREEN_DIMENSIONS[0] * 0.11), int(SCREEN_DIMENSIONS[1] * 0.52))

    if input(f"\nProceed to copy all {num_strings} strings to {window_title}? [y/n] ").lower().find("y") != -1:
        time_at_start = time.time()

        for num, string in enumerate(img_data):
            # Every loop check if RecRoom is the window in focus.
            is_window_active(window_title)

            if last_successful_string:
                # `last_successful_string` is not None
                if last_successful_string in string:
                    # `last_successful_string` is in the current string -> set the var. to None
                    last_successful_string = None
                else:
                    # `last_successful_string` is not in the current string -> move to the next string
                    continue
            else:
                # `last_successful_string` is None -> user did not enter any string to continue from
                pass

            # Copy current string into clipboard
            pyperclip.copy(string)
            print(f"Copying string #{num + 1}/{num_strings}")
            time.sleep(delay)

            # Click `List Create` string entry
            pyautogui.click()
            time.sleep(delay)

            # Click on the input field
            pyautogui.click(input_field)
            time.sleep(delay)

            # Paste the string into input field
            pyautogui.hotkey("ctrl", "v")
            time.sleep(delay)

            # Click "Done"
            pyautogui.click(done_button)
            time.sleep(delay)

            # Exit out of the input field menu
            pyautogui.press("esc")
            time.sleep(delay * 2)

            # Move down using trigger handle in right hand
            pyautogui.click(button='right')
            time.sleep(delay / 2)

        # Print out the time used for importing
        time_to_copy = time.time() - time_at_start
        minutes = time_to_copy // 60
        seconds = time_to_copy % 60
        print(f"Copying complete. Copied {num_strings} strings in {minutes} min and {seconds:.1f} sec")


def main():
    img_data: List[str] = []
    # Call function for encoding an image
    image, img_data = Encoding.main(list_size=64)

    "########### GLOBAL IMPORTING DELAY ############"
    # This is the delay that controls the speed of the importing process
    # If you're experiencing miss-input/failed string input, increase this number
    # Increasing the delay means longer importing times
    delay: float = 0.3
    "########### GLOBAL IMPORTING DELAY ############"

    "###### LAST SUCCESSFULLY IMPORTED STRING ######"
    # If the importing failed/the string did not import successfully, enter THE LAST IMPORTED STRING into `last_string`
    # variable (instead of `None`)
    # This will re-import all the data from that string onward (including the last string/the one you entered as last)
    last_string = None
    "###### LAST SUCCESSFULLY IMPORTED STRING ######"

    copy_to_recroom(img_data=img_data, delay=delay, last_successful_string=last_string)


if __name__ == "__main__":
    main()
