import datetime
import subprocess
import sys
import time
import tkinter
from tkinter import filedialog
from typing import Tuple, List, Dict

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

# Typing alias for color
PixelColor = Tuple[int, int, int]

COLOR_CHAR_DICT: Dict[PixelColor, str] = {}


def get_image() -> Image:
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

    :param img: The image, converted into `len(chars)` colors
    :return: Returns to global variables: `marker_colors` and `color_char_dict`
    """
    global COLOR_CHAR_DICT

    chars: str = r"!#$%&()*+,./:;<=>?@[Ñ]^_{|}~¢£¤¥¦§¨©ª«¬Ö®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÈ"
    try:
        colors: List[int, PixelColor] = img.getcolors(61)
        for n, (amount, color) in enumerate(colors):
            COLOR_CHAR_DICT[color] = chars[n]
    except TypeError:
        exit(input("Your image contains too many colors! Choose a different image.\n"
                   "Press enter to exit."))


def encode(img: Image, vertical_print: bool = False) -> list[str] or None:
    pixel_color: List[str] = []

    # `vertical_print` just changes the orientation of the encoding process.
    for y in range(img.height):
        for x in range(img.width):
            p = img.getpixel((y, x) if vertical_print else (x, y))  # Gets the color of the pixel at `x, y`
            if len(p) == 4:  # If the value is RGBA, the last `int` is removed
                p = p[:3]
            pixel_color.append(COLOR_CHAR_DICT[p])
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


def print_marker_colors():
    global COLOR_CHAR_DICT

    for color in COLOR_CHAR_DICT:
        print(f"{'%02x%02x%02x' % color} - {COLOR_CHAR_DICT[color]}")


def save_file(data: list[str], prefix: str, include_datetime: bool = True, suffix: str = "txt") -> None:
    """
    Prompt user to select a directory where to save `data`

    :param data: The list of strings to put into a file, joined by a new line
    :param prefix: The file name
    :param include_datetime: Include the date and time after `prefix`
    :param suffix: The file ending. Default: `.str`
    """
    root = tkinter.Tk()
    root.attributes("-topmost", 1)
    root.withdraw()
    # Include datetime if `include_datetime` set to true
    dt: str = f"{datetime.datetime.now():%d-%H-%M-%S}" if include_datetime else ""
    # Prompt user to select a file, add the prefix, datetime and suffix (add . if not already present)
    data_path = filedialog.askdirectory() + f"/{prefix}_{dt}{'' if suffix[0] == '.' else '.'}{suffix}"
    root.destroy()
    with open(data_path, "w") as strings_file:
        strings_file.writelines("\n".join(data))
    print(f"Saved strings to '{data_path}'")


def main(list_size: int, output_strings: bool = False, wait_for_input: bool = False):
    """
    Function to tie together all others.
    Prompt for image, encode and output

    :param list_size: The max list size; 50 for `Variable` importing, 64 for `List Create` importing
    :param output_strings: Print the encoded image strings into the console
    :param wait_for_input: Wait for the user to continue. Useful when running this file directly so that it stays open
    """

    img = None
    while not img:
        img: Image = get_image()
    img = img.convert("RGB")

    img.show()
    color_to_chars(img=img)
    img_data: list[str] = encode(img)

    if output_strings:
        print("Copying strings\n_______________\n")
        time.sleep(2)
        # Print all image data strings
        print("\n\n".join(img_data))

    # Print amount of {`MaxStringLength`} char long strings, image dimensions and total `List Create`s needed.
    print(f"\nGenerated {len(img_data) + 2} strings for image WxH {img.width}x{img.height}")
    print(f"Space needed: {len(img_data) // list_size} Lists (+ {len(img_data) % list_size})")
    print_marker_colors()

    if "y" in input("Save marker color data? [y/n]\n> ").lower():
        save_file(data=[f"{'%02x%02x%02x' % color}" for color in COLOR_CHAR_DICT], prefix="marker_colors")

    if "y" in input("Save image data? [y/n]\n> ").lower():
        save_file(data=img_data, prefix="encoded_image")
    if wait_for_input:
        input("Press enter to continue.")

    return img, img_data


if __name__ == '__main__':
    try:
        main(output_strings=True,
             wait_for_input=True,
             list_size=50 if "1" in input("1. Variable Import\n2. List Create Import\n> ") else 64)
    except KeyboardInterrupt:
        pass
