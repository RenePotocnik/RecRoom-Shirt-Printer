# About this release
The repository you're currently viewing is an experimental version.\
If you decide to download it and try it, join [this discord server](https://discord.gg/GuzwRMsyW8) and give feedback and report and problems you may experience.

If you want the stable release, tested by hundreds or people, go to [this release](https://github.com/RenePotocnik/RecRoom-Shirt-Printer/tree/v1.0)

# Shirt Printer

This repository is for converting, encoding and importing a PNG image into a RecRoom invention (`Shirt Printer - Dorm`)
.\
Said invention only works in your **Dorm Room** because of the **Shirt Customizer**.\
It works best if you're the only person in the room.

There are limitations to the printer as it is an invention and not a dedicated, published room.

If you're experiencing any problems, try fixing them yourself first, by following these steps:

* Are you alone in the room? - The print can behave differently if there's more than one person in the room
* Re-import the image and restart the print (if the print stops midway)
* Restart your game - sometimes RecRoom just needs a little break
* Delete the invention (using `Delete Everything` in your maker-pen) and spawn the invention again - maybe you
  un-wired/deleted something

If none of the steps above work, you can message me on:

* Discord: [**McRen#2940**](https://discordapp.com/users/236809680947511297/)
* Discord Server: [**Rec Room Printing**](https://discord.gg/GuzwRMsyW8)
* RecRoom: [**@McReny**](https://rec.net/user/McReny)

**Respect the [Code of Conduct](https://recroom.com/code-of-conduct)**\
I am not responsible for any bans that may occur as a result of using my invention.


----

## Getting the right coordinates for importing

If you have a monitor with a **16:9 aspect ratio** you can skip the calibration, by just entering "n" when prompted to calibrate.

If your monitor is not a _16:9_ ratio, or if you are not sure about it, calibrate/set your own coordinates by running 
`Coordinate_Calibration.py` and [following the steps bellow](#prepare-for-successful-calibration).

### Prepare for successful calibration

To calibrate successfully, follow all of these steps **exactly**:
1. Spawn a `String Variable` using your makerpen.
2. **Configure** the `String Variable` with your makerpen.
3. Expand `Chip Settings`, scroll all the way down until you see a `Value` input box.
4. Run `Coordinate_Calibration.py`
5. When prompted: *"Press ENTER to open RecRoom and press on the "Value" box (TOP-LEFT corner)."*
   1. Press ENTER
   2. The RecRoom window will be brought back into focus
   3. **Click in the TOP-LEFT corner of the white square UNDER _"Value"_ text**. ![Where to click in the Value input box](Tutorials/ClickHere.png)
6. When prompted: *"Press ENTER to open RecRoom and press the two arrows facing away from each-other."*
   1. Press ENTER
   2. The RecRoom window will be brought back into focus
   3. **Click on the two arrows aiming away from each other ↕ (second from the right at the top)** ![Where to click on the done button](Tutorials/ClickHere_DoneButton.png)


https://user-images.githubusercontent.com/76653181/182597821-a03e5a8b-de1b-4bb6-baab-a938ecc22ab9.mp4


----

# The Invention

The invention is called `"Shirt Printer - Dorm"`\
It takes a lot of ink, thus you will need to delete everything in your dorm room. Don't worry, you can always load the
previous saves of the room in your watch;\
`This Room` -> press the "_round arrow_" button left of the `Save Room` button.

[Video: How to delete everything in a room using the makerpen](https://user-images.githubusercontent.com/76653181/179421434-a57c714e-b90f-4bf7-a618-e6614ed1c789.mp4)

## Spawning the invention

When spawning the invention you must **spawn it from your watch** and **not** your maker-pen.
![InventionStore](https://user-images.githubusercontent.com/76653181/179567901-62f7d174-b256-40df-ad33-be1a6f080abe.png)
![SpawnInvention](https://user-images.githubusercontent.com/76653181/179421897-ecddd84d-d33b-4b5d-aa27-9e1b5735ebed.png)

## Running the script

Download the ZIP file containing all scripts.\
Run `Shirt-Printer.py`.

In the newly opened window, open a PNG image you want to print.\
I suggest the image is already converted into a RecRoom color palette
(Photoshop ACO swatch files are included), and scaled to the appropriate size.\
If the image is not converted it will automatically get converted and dithered.\
Templates for the shirt are in the included `Shirt_Templates` map.

## Importing using `String Variable`

After the data has been encoded, you will be prompted to import it to RecRoom.\
For this you'll have to **Configure** the `String Variable`. You will have to **replace** the existing one with a new
one (see video below)\
When you see the white `Value` input field, enter `y` in the script.\
Tab back into RecRoom and _wait_...\
I strongly recommend doing this step last, because all data gets erased if you save the room or `Reset Components`

If you want a more robust way of importing, go to [this part](#importing-using-list-create)

If you get any messages/errors saying to calibrate your coordinates [follow this tutorial](#prepare-for-successful-calibration)


[Video: replacing the variable and preparing for importing](https://user-images.githubusercontent.com/76653181/179419753-4981f9bb-0b66-47bb-8796-cbedddf5ef56.mp4)


## Importing using `List Create`
Unlike the _**Variable**_ import method, using the _**List Create**_ import method you can save the imported image data as an invention, spawn it and connect it to the printer for easy repeated and remote printing.

Unlike the printer itself, this invention _**does not work in your dorm**_.\
Create a room (or use an existing one) and follow these steps:
* Spawn the invention called `List Create Importing`
* Grab the `Trigger Handle` with your _**RIGHT HAND**_ (and do not let go of it)
* Grab your maker-pen with your _**LEFT HAND**_ 
* In the maker-pen menu (F), select `Edit`
* Edit the circuit board named `List Create Data`
* Take a seat
* In the maker-pen menu (F), select `Wire`
* Look at the **center of the first string input** (see image and [video](Tutorials/ListCreateImportingSetup.mp4) below for example) ![First string input](Tutorials/ListCreateImportStringInput.png)


[Video: How to prepare for List Create Importing](https://user-images.githubusercontent.com/76653181/182598067-d859d649-65d3-4742-92c4-75e64d01c3f4.mp4)


* `Alt - Tab` back into the script window, and do as instructed
* When the importing is done, save the `List Create Data` circuit board *(you can ignore the others)* as an invention
* Go back to your dorm room and spawn the newly created invention
* Wire `List Create Data` to the `Image Data Input`
* Wire `Run` from the delay at the bottom to `Load Data`
* Wire `Data Loaded` to `Load` in the `Shirt Printer` circuit board
* On the `Shirt Printer` circuit board, change `Variable Import` from `True` to `False` 


[Video: How to connect the List Create Imported data](https://user-images.githubusercontent.com/76653181/182651483-7bc7728c-663a-405d-aa40-be7bb896ce89.mp4)


## Spawning the shirt customizer

When the importing process is finished, you will have to spawn in your **Shirt Customizer**.\
The placement is very important! If the canvas is not flush with the wall the print might not work at all.\
Spawn the shirt customizer, grab it and push it into the corner _as shown in the video_.

[Video: placing the shirt customizer in the corner of your dorm](https://user-images.githubusercontent.com/76653181/179420703-911f9aff-a5a3-432a-934f-2ab1b35848b0.mp4)

It should look like the picture below.

![ShrtCutomizerInTheCorner](https://user-images.githubusercontent.com/76653181/179421185-9eff3a75-6e41-43d8-a1ca-a811894f8304.png)

### Alternative method of placing the shirt customizer
Spawn the invention `Board Placement Seat` (**from your watch, not your makerpen**)\
This will place a seat in the exact position for optimal board placement.\
**Spawning the invention has a chance of spawning it at the incorrect angle (it is supposed to be rotated)**

When entering the seat **do not move your mouse**. Best way to do this is to look at the seat, lift your mouse of the table, click on the seat and press **TAB** (open your watch menu).\
Then navigate to your backpack and spawn the Shirt Customizer. You can then leave and delete the seat. 

![Invention image](https://user-images.githubusercontent.com/76653181/180603926-e4006af3-8395-43eb-b3aa-844328399fdd.png)


## Adjusting printer settings

Next step is on the circuit board named `Shirt Printer`.\
You will have to change those inputs to suit your imported image\
There's comments to help you understand better;

* `Front And Back` - Set this to `True` if you're printing both-sided, set it to `False` if you're printing only one
  side.
* `Variable Import` - If you're importing the image using the included _**Variable Import**_ keep this to `True`. Set it to `False` if you're importing using the _**List Create**_ method
* `Main Delay` - Controls the speed of the system; if the number is too low you may experience "ghost pixels" (white
  dots), If so, increase the delay.
* `Image Width` - The most important one of them all; enter the same number as the width of the image you imported. if
  it's off even by one it **will mess up**
* `Image Height` - not as important as width; it only affects the progress display

![ShirtPrinterCircuitboardInputs](https://user-images.githubusercontent.com/76653181/179420840-0fd58e89-7a05-41b3-a81f-efd2e614c3dc.png)

##
Now press the `Start` button and wait. Preferably alone.

----

If you have any problems with the scripts, the invention or anything else, you can contact me on:

- [Discord: **McRen#2940**](https://discordapp.com/users/236809680947511297/)
- [RecRoom: **@McReny**](https://rec.net/user/McReny)
