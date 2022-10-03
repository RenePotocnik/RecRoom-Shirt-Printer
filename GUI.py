import os
import time
from pathlib import Path
from tkinter import *
from tkinter import messagebox, filedialog, Button, IntVar, Tk
from typing import List, Tuple

from PIL import ImageTk

import Encoding
import Importing
import List_Create_Importing

IMAGE = None
DITHERED_IMAGE = None
IMAGE_PATH = None
IMG_DATA = []
IMG_DATA_UNCUT: List[Tuple[int, str]]
PATH = None
DATA_PATH = None
warned = False

image_button = None
d_image_button = None


def update_image_button():
    global image_button
    height = (300 / IMAGE.width) * IMAGE.height
    tk_image = ImageTk.PhotoImage(IMAGE.resize((300, int(height))))
    image_button["image"] = tk_image
    image_button.image = tk_image
    image_info["text"] = f"Width: {IMAGE.width}\nHeight: {IMAGE.height}"


def scale():
    # Create a new window and buttons
    win2 = Toplevel(win)
    win2.title("Scale Image")
    win2.resizable(False, False)
    win2.attributes('-topmost')
    x, y = (win.winfo_x(), win.winfo_y())
    win2.geometry(f"+{x}+{y}")

    scaled: bool = False

    def scale_to_w_h_():
        global IMAGE
        try:
            w: int = int(scale_to_w_in.get())
            h: int = int(scale_to_h_in.get())
        except ValueError:
            return
        IMAGE = IMAGE.resize((w, h))
        update_image_button()
        win2.destroy()

    def fit_to_width_():
        global IMAGE
        try:
            w: int = int(fit_to_width_in.get())
            h: int = int(w / IMAGE.width * IMAGE.height)
        except ValueError:
            return
        IMAGE = IMAGE.resize((w, h))
        update_image_button()
        win2.destroy()

    def fit_to_height_():
        global IMAGE
        try:
            h: int = int(fit_to_height_in.get())
            w: int = int(h / IMAGE.height * IMAGE.width)
        except ValueError:
            return
        IMAGE = IMAGE.resize((w, h))
        update_image_button()
        win2.destroy()

    # Scale to WIDTH and HEIGHT
    scale_to_w_h = Button(win2, text="Scale To Width & Height", width=25, command=scale_to_w_h_)
    scale_to_w_l = Label(win2, text="Width:")
    scale_to_w_in = Entry(win2, width=5)
    scale_to_h_l = Label(win2, text="Height:")
    scale_to_h_in = Entry(win2, width=5)

    scale_to_w_h_row: int = 0
    scale_to_w_h.grid(row=scale_to_w_h_row, column=0, padx=10, pady=10)
    scale_to_w_l.grid(row=scale_to_w_h_row, column=1)
    scale_to_w_in.grid(row=scale_to_w_h_row, column=2, padx=10)
    scale_to_h_l.grid(row=scale_to_w_h_row, column=3)
    scale_to_h_in.grid(row=scale_to_w_h_row, column=4, padx=10)

    # Fit to WIDTH
    fit_to_width = Button(win2, text="Fit To Width", width=25, command=fit_to_width_)
    fit_to_width_l = Label(win2, text="Width:")
    fit_to_width_in = Entry(win2, width=5)

    fit_to_width_row: int = 1
    fit_to_width.grid(row=fit_to_width_row, column=0, pady=10)
    fit_to_width_l.grid(row=fit_to_width_row, column=1)
    fit_to_width_in.grid(row=fit_to_width_row, column=2, padx=10)

    # Fit to HEIGHT
    fit_to_height = Button(win2, text="Fit To Height", width=25, command=fit_to_height_)
    fit_to_height_l = Label(win2, text="Height:")
    fit_to_height_in = Entry(win2, width=5)

    fit_to_height_row: int = 2
    fit_to_height.grid(row=fit_to_height_row, column=0, pady=10)
    fit_to_height_l.grid(row=fit_to_height_row, column=1)
    fit_to_height_in.grid(row=fit_to_height_row, column=2, padx=10)


def importing():
    global importing_, warned

    if importing_.get() == 0:
        messagebox.showerror("No Selection", "You must select one of the two ways of importing.")
        return

    elif importing_.get() == 1:
        print("Variable importing")
        try:
            with open("coordinates.json", "r"):
                pass
        except FileNotFoundError:
            if not warned:
                messagebox.showwarning("Coordinates Not Calibrated",
                                       "It seems that you haven't calibrated your coordinates yet.\n"
                                       "If you proceed, the default coordinates will be used - only for 16:9 monitors.")
                warned = True
                return
        IMG_DATA.insert(0, "BEGIN")
        IMG_DATA.append("END")
        time.sleep(1)
        Importing.copy_into_rr_variable(IMG_DATA, ask_for_coords_calibration=False, ask_to_continue=False)

    elif importing_.get() == 2:
        print("List Create importing")
        if List_Create_Importing.monitor_check() == -1:
            messagebox.showerror("Monitor Size Not Compatible", "A monitor with a 16:9 aspect ratio is needed for"
                                                                "List Create Importing.\n"
                                                                "Use Variable Importing instead.")
            return
        List_Create_Importing.copy_to_recroom(IMG_DATA, ask_to_continue=False)


def encoding():
    global IMG_DATA, save_data, empty2, variable_import, list_create_import, import_data, data_info, tab_to_recroom, \
        IMG_DATA_UNCUT, time_for_print

    IMG_DATA = Encoding.encode(img=DITHERED_IMAGE, dither_=False)

    data_info["text"] = f"Generated {len(IMG_DATA)} strings ({len(IMG_DATA) // 64 + 1} List Creates)"
    data_info.grid(row=7, column=1, columnspan=2, sticky=W)
    save_data.grid(row=8, column=0, sticky=W)

    main_delay: float = 0.025
    min_for_print: float = (len(''.join(IMG_DATA)) * (main_delay * 2 + main_delay / 2)) / 60
    time_for_print["text"] = f"EST. time needed to print (delay: {main_delay}):\n" \
                             f"{int(min_for_print // 60)} hours,\n" \
                             f"{round(min_for_print % 60, 1)} minutes."
    time_for_print.grid(row=7, column=3, columnspan=2, rowspan=3, sticky=N)

    empty2.grid(row=9, columnspan=4)
    variable_import.grid(row=9, column=0, sticky=W, pady=(20, 0))
    list_create_import.grid(row=10, column=0, columnspan=3, sticky=W)
    import_data.grid(row=11, column=0, sticky=W)

    tab_to_recroom.grid(row=11, column=1, columnspan=4)

    variable_import["text"] = f"Variable Importing\n" \
                              f"Space Needed: {len(IMG_DATA)} Strings\n" \
                              f"Available Space: 2500 Strings"

    list_create_import["text"] = f"List Create Importing\n" \
                                 f"Space Needed: {len(IMG_DATA) // 64 + 1} Lists\n" \
                                 f"Available Space: 40 Lists"


def save_image_data():
    global IMG_DATA, save_data, open_encoded_data, DATA_PATH
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", 1)
    root.title("Select folder to save image data")
    DATA_PATH = filedialog.askdirectory() + "/encoded_" + str(IMAGE_PATH.stem) + ".txt"
    root.destroy()

    img_data_new = [f"#{n} - " + s for n, s in enumerate(IMG_DATA)]

    with open(DATA_PATH, "w") as strings_file:
        strings_file.writelines("\n".join(img_data_new))

    save_data["text"] = "Saved"

    open_encoded_data.grid(row=8, column=0, columnspan=2, sticky=E)


def save_new_image():
    global save_image, PATH
    root = Tk()
    root.attributes("-topmost", 1)
    root.withdraw()
    PATH = filedialog.askdirectory() + "/converted_" + str(IMAGE_PATH.stem.split("/")[-1]) + ".png"
    print(PATH)
    root.destroy()

    DITHERED_IMAGE.save(PATH)

    save_image["text"] = "Saved"


def dither_image():
    global IMAGE, keep_detail, DITHERED_IMAGE, save_image, d_image_button, save_data, encode, empty

    DITHERED_IMAGE = Encoding.quantize(IMAGE, ask_for_dither=False, dither=keep_detail.get(), open_image=False)

    if d_image_button:
        # If the dithered image button/image already exists, delete it
        d_image_button.destroy()

    # Image button
    height = (300 / DITHERED_IMAGE.width) * DITHERED_IMAGE.height
    tk_image = ImageTk.PhotoImage(DITHERED_IMAGE.resize((300, int(height))))
    d_image_button = Button(win, image=tk_image, command=DITHERED_IMAGE.show)
    d_image_button.image = tk_image
    d_image_button.grid(row=1, column=4, rowspan=5, sticky=N)

    save_image.grid(row=0, column=4, sticky=E)
    empty.grid(row=6, columnspan=4, sticky=W)
    encode.grid(row=7, column=0, sticky=W)

    if save_data:
        save_data["text"] = "Save Encoded Data"


def image():
    global IMAGE, keep_detail, keep_detail, dither_button, image_button, load_image, image_info, load_from_txt_file, \
        scale_image, IMAGE_PATH

    IMAGE = Encoding.get_image(check_palette=False)
    IMAGE_PATH = Path(IMAGE.filename)
    load_image.grid(row=0, column=0, sticky=W, padx=0, pady=0)
    load_from_txt_file.destroy()

    if not IMAGE:
        messagebox.showinfo("No Image Selected", "Select an image in order to proceed.")
        return
    if IMAGE.palette:
        messagebox.showerror("Invalid Image", "Open the image in MS Paint, save it, and select it again.")
        print("Image has `Palette` attribute. Open it in Paint and save.")
        os.system(f'mspaint.exe')
        return

    if image_button:
        # If the selected image button/image already exists, delete it
        image_button.destroy()

    # Image button
    height = (300 / IMAGE.width) * IMAGE.height
    tk_image = ImageTk.PhotoImage(IMAGE.resize((300, int(height))))
    image_button = Button(win, image=tk_image, command=IMAGE.show)
    image_button.image = tk_image
    image_button.grid(row=1, column=0, columnspan=2, sticky=N, rowspan=5)

    dither_button.grid(row=3, column=2, sticky=S)
    keep_detail_button.grid(row=4, column=2, sticky=N)

    image_info["text"] = f"Width: {IMAGE.width}\nHeight: {IMAGE.height}"
    image_info.grid(row=1, column=2, sticky=S)

    scale_image.grid(row=2, column=2, sticky=N)


def load_from_file():
    global IMG_DATA, load_image, txt_data_info, empty2, variable_import, list_create_import, import_data
    print("Select TXT file.", end="\r")
    root = Tk()
    root.withdraw()
    txt_file_path = filedialog.askopenfilename(filetypes=[("Image Data", "*.txt")])
    root.destroy()

    try:
        with open(txt_file_path, "r") as strings:
            temp: list[str] = strings.readlines()
            IMG_DATA = [line.strip().split(" ")[-1] for line in temp]
    except FileNotFoundError:
        messagebox.showerror("FIle Not Found", "The file does not exist. Please select a different file.")
        return

    load_image.destroy()
    load_from_txt_file["text"] = "Loaded"
    load_from_txt_file.grid(row=0, padx=0, pady=0)

    txt_data_info["text"] = f"Found {len(IMG_DATA)} strings ({len(IMG_DATA) // 64 + 1} Lists)"
    txt_data_info.grid(row=0, column=1)

    empty2.grid(row=6, columnspan=4)
    variable_import.grid(row=7, column=0, sticky=W, pady=(20, 0))
    list_create_import.grid(row=8, column=0, columnspan=3, sticky=W)
    import_data.grid(row=9, column=0, sticky=W)
    tab_to_recroom.grid(row=9, column=1, columnspan=4)

    variable_import["text"] = f"Variable Importing\n" \
                              f"Space Needed:{len(IMG_DATA)} Strings\n" \
                              f"Available Space: 2500 Strings"

    list_create_import["text"] = f"List Create Importing\n" \
                                 f"Space Needed: {len(IMG_DATA) // 64 + 1} Lists\n" \
                                 f"Available Space: 40 Lists"


# Create the main window, add title, make it un-resizable, put it on top, place in center of screen
win: Tk = Tk()
win.title("RecRoom Printer")
win.resizable(False, False)
win.attributes('-topmost')
win.eval('tk::PlaceWindow . center')
# win.attributes("-alpha", 0.9)

# Create a button to load the image
load_image: Button = Button(text="Load Image", width=25, command=image)
load_image.grid(row=0, column=0, sticky=W, padx=20, pady=20)

# Create button to load image data from txt file
load_from_txt_file = Button(win, text="Load From TXT File", width=25, command=load_from_file)
load_from_txt_file.grid(row=1, column=0, padx=20, pady=20)

# Display info about the txt file including the data
txt_data_info = Label(win)

# Create button to save the encoded image data to a .txt file
save_data: Button = Button(win, text="Save Encoded Data", width=25, command=save_image_data)

# Option to keep detail or not - dither or no
keep_detail: IntVar = IntVar()
keep_detail_button: Checkbutton = Checkbutton(win, text="Keep Detail", variable=keep_detail)

# Create a button to convert the image into RecRoom colors
dither_button: Button = Button(win, text="Dither Image", width=25, command=dither_image)

# Create an empty line (don't know how else to do it)
empty = Label(win, text="")
# Create a button to encode the selected image
encode: Button = Button(text="Encode Image", width=25, command=encoding)

# Create a button to save the converted image to the selected file
save_image = Button(win, text="Save New Image", command=save_new_image)

# Create button to open the saved encoded data in notepad
open_encoded_data = Button(win, text="Open", width=10, font="Helvetica 8 italic",
                           command=lambda: os.system(f'notepad.exe "{DATA_PATH}"'))

# Create an empty line (don't know how else to do it)
empty2 = Label(win, text="")

# Choose way of importing - Variable import, List Create import
importing_ = IntVar()
variable_import = Radiobutton(win, text="Variable Importing", variable=importing_, value=1)
list_create_import = Radiobutton(win, text="List Create Importing", variable=importing_, value=2)

# Create button to confirm selection of importing
import_data = Button(win, text="Begin Import", width=25, command=importing)

# Tell user to alt-tab back into RecRoom fto start importing
tab_to_recroom = Label(win, text="Importing Will Start Once You Press 'Begin Import'\n"
                                 " and ALT-TAB Back Into RecRoom", fg="#f00",
                       font="Helvetica 10 bold")

# Label to show info about the encoded image
data_info = Label(win)
time_for_print = Label(win)

# Display image info: width and height
image_info = Label(win)

# Create button to scale the image
scale_image = Button(win, text="Scale Image", command=scale)

win.mainloop()
