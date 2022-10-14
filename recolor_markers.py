import ctypes
import subprocess
import sys
import time
import tkinter
from tkinter import filedialog
import common

# Enable color support in a CMD window
# subprocess.call(r"reg add HKEY_CURRENT_USER\Console /v VirtualTerminalLevel /t REG_DWORD /d 0x00000001 /f")

try:
    import pyautogui
    import pyperclip
    from PIL import Image, ImageGrab
    from PIL.Image import Transform, Resampling
except ModuleNotFoundError:
    print(f"""
    \033[91mMandatory modules are missing/not yet installed!\033[0m
    Please execute the following line in `CMD` and run the script again:
        '{sys.executable} -m pip install -U PyAutoGUI pyperclip Pillow'
        """)
    # Ask the user to install all the necessary packages automatically
    if input("Proceed to run the command automatically? [yes/no] ").find("yes") != -1:
        subprocess.call(f"{sys.executable} -m pip install -U PyAutoGUI pyperclip Pillow")
    exit()


# Get the monitor dimensions
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
SCREEN_DIMENSIONS: tuple[int, int] = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
SCREEN_CENTER: tuple[int, int] = int(SCREEN_DIMENSIONS[0] / 2), int(SCREEN_DIMENSIONS[1] / 2)

TOP_COLOR: tuple[int, int, int] = (242, 133, 76)
TOP_COLOR_COORDS: list[tuple[int, int]] = [
    (int(SCREEN_DIMENSIONS[0] * 0.1445), int(SCREEN_DIMENSIONS[1] * 0.0625)),
    (int(SCREEN_DIMENSIONS[0] * 0.1562), int(SCREEN_DIMENSIONS[1] * 0.0625) + 2)
]
MIDDLE_COLOR: tuple[int, int, int] = (241, 232, 217)
MIDDLE_COLOR_COORDS: list[tuple[int, int]] = [
    (int(SCREEN_DIMENSIONS[0] * 0.5546), int(SCREEN_DIMENSIONS[1] * 0.2916)),
    (int(SCREEN_DIMENSIONS[0] * 0.5859), int(SCREEN_DIMENSIONS[1] * 0.2916) + 2)
]

COLOR_BUTTON: tuple[int, int] = (
    int(SCREEN_DIMENSIONS[0] * (380 / 2560)),
    int(SCREEN_DIMENSIONS[1] * (480 / 1440))
)
CUSTOM_BUTTON: tuple[int, int] = (
    int(SCREEN_DIMENSIONS[0] * (1820 / 2560)),
    int(SCREEN_DIMENSIONS[1] * (1170 / 1440))
)
COLOR_INPUT: tuple[int, int] = (
    int(SCREEN_DIMENSIONS[0] * (1830 / 2560)),
    int(SCREEN_DIMENSIONS[1] * (910 / 1440))
)
DONE_BUTTON: tuple[int, int] = (
    int(SCREEN_DIMENSIONS[0] * (1830 / 2560)),
    int(SCREEN_DIMENSIONS[1] * (1050 / 1440)),
)


def get_file() -> str:
    print("Select the marker color data file...", end="")
    root = tkinter.Tk()
    root.attributes("-topmost", 1)
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Marker Colors", "*.txt")])
    root.destroy()
    print(" " * 38)
    return file_path


def recolor(color: str, delay: float = 0.5) -> None:
    """
    Starting from the marker's configure menu;
        > Click "Color" button
        > Click "Custom" button
        > Click on the hex color input box
        > Click "Done"
        > Press "F"

    :param color: String including the HEX color
    :param delay: The delay between actions
    """
    pyperclip.copy(color)
    pyautogui.click(COLOR_BUTTON[0], COLOR_BUTTON[1])
    time.sleep(delay)
    pyautogui.click(CUSTOM_BUTTON[0], CUSTOM_BUTTON[1])
    time.sleep(delay)
    pyautogui.click(COLOR_INPUT[0], COLOR_INPUT[1])
    time.sleep(delay)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(delay)
    pyautogui.click(DONE_BUTTON[0], DONE_BUTTON[1])
    time.sleep(delay)
    pyautogui.press("f")


def await_config_menu(interval: float = 0.2) -> bool:
    """
    Return True when the configure menu opens

    :param interval: How often to check for menu
    :return: True if the menu has been found
    """
    # Move mouse to center of screen
    pyautogui.scroll(20, x=SCREEN_CENTER[0], y=SCREEN_CENTER[1])

    while True:
        common.is_window_active()
        scr: Image = ImageGrab.grab()
        if (
                common.color_in_coords(image=scr, color=TOP_COLOR, coordinates=TOP_COLOR_COORDS, tolerance=20)
                and
                common.color_in_coords(image=scr, color=MIDDLE_COLOR, coordinates=MIDDLE_COLOR_COORDS, tolerance=20)
        ):
            time.sleep(interval)
            return True
        time.sleep(interval)


def hex_to_rgb(hex):
    rgb = []
    [rgb.append(int(hex[i:i + 2], 16)) for i in (0, 2, 4)]
    return tuple(rgb)


def create_color_template(colors: list[str]) -> Image:
    template_dimensions: tuple[int, int] = (4, 15)  # [0] markers down, [1] markers right
    img: Image = Image.new(mode="RGBA",
                           size=(template_dimensions[0], template_dimensions[1]),
                           color=(0, 0, 0, 0))
    img_data = img.load()
    y: int = 0
    for n, color in enumerate(colors):
        if n and n % template_dimensions[0] == 0:
            y += 1
        rgb_color = hex_to_rgb(color)
        img_data[n % template_dimensions[0], y] = rgb_color

    return img.resize((template_dimensions[0] * 100, template_dimensions[1] * 100),
                      resample=Transform.AFFINE).rotate(90, Resampling.NEAREST, expand=True)


def main(print_with_colors: bool = True):
    marker_colors: list[str] = []
    try:
        with open(get_file(), "r") as file:
            for line in file.readlines():
                marker_colors.append(line.strip())
    except FileNotFoundError:
        print("File not found. Try again.")
        exit(main())
    print(f"Found {len(marker_colors)} colors in file.")

    print(f"""
        Requirements:
    Must have a 16:9 aspect ration monitor (e.g.: 1920x1080, 2160x1440...)
    You can check by going to;
    | Settings -> System -> Display -> Display Resolution |
    *here you can also temporarily change the resolution to the right amount 
    
        Instructions:
    When told to, `ALT-TAB` into RecRoom.
    CONFIGURE the markers one by one, in order from "Salmon" to "Black".
    After configuring the marker, the script will recolor the marker and exit the config menu;
    During this time, try NOT to move your mouse or press any buttons on your keyboard.
    Now move to the next marker, and repeat the process.
    
    The image that opened shows all marker colors in the same order as in RecRoom 
    (starting from the BOTTOM LEFT corner, moving UP and resetting back down, one the RIGHT)
    
    """)
    create_color_template(colors=marker_colors).show()
    input("Press ENTER, Open RecRoom and configure the first marker.")
    for n, color in enumerate(marker_colors):
        common.is_window_active()  # Do not continue if Rec Room is not the window in focus
        rgb_c = hex_to_rgb(color)
        if print_with_colors:
            print(f"\033[38;2;{rgb_c[0]};{rgb_c[1]};{rgb_c[2]}m")
        print(f"Waiting for marker {n + 1} configure menu...", end=" ")
        await_config_menu()  # Don't continue if the configure menu is not open
        print("DONE")
        common.is_window_active()  # Do not continue if Rec Room is not the window in focus
        print(f"Recoloring marker {n + 1} to '#{color}'...", end=" ")
        recolor(color)
        print("DONE")
    if print_with_colors:
        print("\033[0m")
    input("\nDONE\nPress enter to close\n> ")


if __name__ == '__main__':
    main(print_with_colors="y" in input("Print Colored Text (Experimental) - does not affect performance? [y/n]\n> "))
