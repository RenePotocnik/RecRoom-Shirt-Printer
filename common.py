import datetime
import logging
import sys
import time
from typing import NamedTuple

import pyautogui
from PIL import ImageGrab


def setup_logger(level=logging.DEBUG, disable_imported: bool = False) -> logging.Logger:
    import logging.config

    if disable_imported:
        logging.config.dictConfig({'version': 1, 'disable_existing_loggers': True})

    logger_ = logging.getLogger(__file__)

    stream_handler = logging.StreamHandler(sys.stdout)
    # noinspection SpellCheckingInspection
    stream_handler.setFormatter(logging.Formatter("[{asctime}] [{levelname:7}] {message}", style='{'))
    logger_.addHandler(stream_handler)

    filehandler = logging.FileHandler(f"{__file__}_{datetime.datetime.now():%Y%m%d}.log")
    # noinspection SpellCheckingInspection
    filehandler.setFormatter(logging.Formatter("[{asctime}] [{name}.{funcName}:{lineno}] [{levelname}] {message}",
                                               style='{'))
    logger_.addHandler(filehandler)

    logger_.setLevel(level)
    return logger_


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


class Colors(NamedTuple):
    text = (55, 57, 61)  # The color of text in the Variable Input field (black)
    white = (229, 225, 216)  # The white background of the Variable Input field
    green = (187, 205, 182)  # The Variable Input field sometimes turns green - this is that color.


class ImageCoords(NamedTuple):
    min_y: int
    min_x: int

    max_y: int
    max_x: int


def found_colors(main_color: tuple[int, int, int], coordinates: ImageCoords) -> bool:
    """
    Returns True if `main_color` is found in the given coordinates

    :param main_color: The color to compare the detected color to
    :param coordinates: Coordinates of the window of pixels to be checked and compared
    :return: If the color in any of the pixels match the `main_color`
    """

    def is_color(compare_color: tuple[int, int, int], main_color_: tuple[int, int, int], tolerance: int = 30) -> bool:
        """
        Compare `compare_color` to `main_color` with a given tolerance

        :param compare_color: The color that is being compared
        :param main_color_: The color that is being compared
        :param tolerance: How close the colors can be (1 - 255)
        :return: Is `compare_color` same/similar as `main_color`
        """
        return ((abs(compare_color[0] - main_color_[0]) < tolerance)
                and (abs(compare_color[1] - main_color_[1]) < tolerance)
                and (abs(compare_color[2] - main_color_[2]) < tolerance))

    image = ImageGrab.grab()

    for coords_x in range(coordinates.min_x, coordinates.max_x):
        if is_color(image.getpixel((coords_x, coordinates.min_y)), main_color):
            return True

    return False
