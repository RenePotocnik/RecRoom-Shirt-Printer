import os
import subprocess
import sys
import time
import tkinter
from math import sqrt
from pathlib import Path
from tkinter import filedialog
from typing import Tuple, List, Dict

from PIL.Image import Quantize

try:
    import pyautogui
    import pyperclip
    from PIL import Image, ImageGrab
except ModuleNotFoundError:
    print(f'Please execute the following line and run the script again:\n'
          f'{sys.executable} -m pip install -U PyAutoGUI pyperclip Pillow')
    # Ask the user to install all the necessary packages automatically
    if input("Proceed to run the command automatically? [yes/no] ").find("yes") != -1:
        subprocess.call(f"{sys.executable} -m pip install -U PyAutoGUI pyperclip Pillow")
    exit()

MaxStringLength: int = 280  # Maximum length string
ColorCount: int = 128  # Amount of possible colors - magic markers

# Typing alias for color
PixelColor = Tuple[int, int, int]

marker_colors: List[PixelColor] = []
color_char_dict: Dict[PixelColor, str] = {}


def get_image(check_palette: bool = True) -> Image:
    """
    Open file explorer, wait for user to open a PNG image
    :return: The image
    """
    print("Open image", end="\r")
    root = tkinter.Tk()
    root.attributes("-topmost", 1)
    root.withdraw()
    img_path = filedialog.askopenfilename(filetypes=[("Image", "*.png")])
    root.destroy()

    img = None
    if img_path:
        img = Image.open(img_path)

    if check_palette:
        # If the image has attributed `palette` its metadata is a bit different.
        # To solve this just open the image in paint and save it
        if img.palette:
            print("Image has `Palette` attribute. Open it in Paint and save.")
            os.system(f'mspaint.exe "{Path(img_path)}"')
            return None

    return img


def progress_update(y: int, img: Image, prefix='Progress', suffix='', length=50) -> None:
    """
    Display a progress bar in the console
    :param y: The `y` value of the image
    :param img: The image
    :param prefix: Optional: Text in-front of the progress bar
    :param suffix: Optional: Text behind the progress bar
    :param length: Optional: The length of the progress bar
    """
    completed = int(length * y // img.height)
    empty = length - completed
    bar = "#" * completed + " " * empty
    percent = f"{100 * (y / float(img.height)):.2f}"
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end="\r")

    # Print New Line on Complete
    if y == img.height:
        print(" " * (length + 30), end="\r")


def color_to_chars(img: Image) -> None:
    """
    Function assigns a char to each RGB value, and creates a list of all the marker colors

    :param img: The image, converted into `len(chars)` colors (128)
    :return: Returns to global variables: `marker_colors` and `color_char_dict`
    """
    global marker_colors, color_char_dict

    chars: str = "!#$%&'()*+,-./:;<=>?@[]^_`{|}~¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸" \
                 "¹º»¼½¾¿ÀÁÂÃÄÅÇÈÉÊÆËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿIiMm"
    colors: List[int, PixelColor] = img.getcolors()
    for n, (amount, color) in enumerate(colors):
        color_char_dict[color] = chars[n]
        marker_colors.append(color)


def encode(img: Image, vertical_print: bool = False) -> list[str] or None:
    pixel_color: List[str] = []

    # `vertical_print` just changes the orientation of the encoding process.
    for y in range(img.height):
        for x in range(img.width):
            p = img.getpixel((y, x) if vertical_print else (x, y))  # Gets the color of the pixel at `x, y`
            if len(p) == 4:  # If the value is RGBA, the last `int` is removed
                p = p[:3]
            pixel_color.append(color_char_dict[p])
        # Print the progress
        progress_update(y + 1, img, "Encoding")

    colors: List[Tuple[int, str]] = []
    count: int = 0
    current_color: str = pixel_color[0]
    # `count` is the amount of `current_color` in a row

    for c in pixel_color:
        if c != current_color:
            colors.append((count, current_color))
            count = 0
            current_color = c
        count += 1
    colors.append((count, current_color))

    print(f"Compressed {len(pixel_color)} chars into {len(colors)} chars")

    s: str = ""
    img_data: List[str] = []
    for amount, color in colors:
        if amount > 1:
            ns = f"{amount}{color}"
        else:
            ns = color

        if len(s + ns) > MaxStringLength:  # 512
            img_data.append(s)
            s = ""
        s += ns

    img_data.append(s)
    return img_data


def recolor_markers(delay: float = 0.3) -> None:
    """
    Function recolors the magic markers to their needed color.

    Sequence of events:

    > Press "F" - open the makerpen menu

    > Click on "Color" in the `Recolor Tool Settings`

    > Click on "Custom" in the `Color` menu

    > Click on the HEX color value input field

    > Paste the HEX color

    > Click "Done"

    > Press "F" - close the makerpen menu

    > Left Click - recolor

    > Right Click - moveto the next marker
    """
    global marker_colors
    pyautogui.press("f")


def main(list_size: int, output_strings: bool = False, wait_for_input: bool = False):
    """
    Function to tie together all others.
    Prompt for image, encode and output

    :param list_size: The max list size; 50 for `Variable` importing, 64 for `List Create` importing
    :param output_strings: Print the encoded image strings into the console
    :param wait_for_input: Wait for the user to continue. Useful when running this file directly so that it stays open
    """

    img: Image = get_image()
    if not img:
        exit()
    img = img.convert("RGB").quantize(colors=ColorCount,
                                      method=Quantize.MEDIANCUT,
                                      kmeans=1,
                                      palette=None,
                                      dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")
    color_to_chars(img=img)
    img_data: list[str] = encode(img)

    with open("image_data.txt", "w") as strings_file:
        strings_file.writelines("\n".join(img_data))

    if output_strings:
        print("Copying strings\n_______________\n")
        time.sleep(2)
        # Print all image data strings
        print("\n\n".join(img_data))

    # Print amount of {`MaxStringLength`} char long strings, image dimensions and total `List Create`s needed.
    print(f"\nGenerated {len(img_data) + 2} strings for image WxH {img.width}x{img.height}")
    print(f"Space needed: {len(img_data) // list_size} Lists (+ {len(img_data) % list_size})")

    if wait_for_input:
        input("Press enter to continue")

    return img, img_data


if __name__ == '__main__':
    try:
        main(output_strings=True,
             wait_for_input=True,
             list_size=50 if "1" in input("1. Variable Import\n2. List Create Import\n> ") else 64)
    except KeyboardInterrupt:
        pass
