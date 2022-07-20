# Shirt Printer

This repository is for converting, encoding and importing a PNG image into a RecRoom invention (`Shirt Printer - Dorm`)
.\
Said invention only works in your **Dorm Room** because of the **Shirt Customizer**.\
It works best if you're the only person in the room.

There are limitations to the printer as it is an invention and not a dedicated, published room.\
One of these _limitations_ is pixel bleed - because the "Magic Markers" are still in beta, they can't be used in the
invention.

If you're experiencing any problems, try fixing them yourself first, by following these steps:

* Are you alone in the room? - The print can behave differently if there's more than one person in the room
* Re-import the image and restart the print (if the print stops midway)
* Restart your game - sometimes RecRoom just needs a little break
* Delete the invention (using `Delete Everything` in your maker-pen) and spawn the invention again - maybe you
  un-wired/deleted something

If none of the steps above work, you can message me on:

* Discord: [**McRen#2940**](https://discordapp.com/users/236809680947511297/)
* RecRoom: [**@McReny**](https://rec.net/user/McReny)

**Respect the [Code of Conduct](https://recroom.com/code-of-conduct)**\
I am not responsible for any bans that may occur as a result of using my invention.


----

## Supported Devices

**ONLY 16:9 screen ratio supported**\
*If you're not sure about your screen ratio, run the script - It'll warn you if your monitor isn't supported*\
If you really want to import, yet you don't have the acceptable screen ratio, got to `Setting -> System -> Display`
and change your `Display resolution` to `1920 x 1080`

----

## The Invention

The invention is called `"Shirt Printer - Dorm"`\
It takes a lot of ink, thus you will need to delete everything in your dorm room. Don't worry, you can always load the
previous saves of the room in your watch;\
`This Room` -> press the "_round arrow_" button left of the `Save Room` button.

https://user-images.githubusercontent.com/76653181/179421434-a57c714e-b90f-4bf7-a618-e6614ed1c789.mp4

##

When spawning the invention you must **spawn it from your watch** and **not** your maker-pen.
![InventionStore](https://user-images.githubusercontent.com/76653181/179567901-62f7d174-b256-40df-ad33-be1a6f080abe.png)
![SpawnInvention](https://user-images.githubusercontent.com/76653181/179421897-ecddd84d-d33b-4b5d-aa27-9e1b5735ebed.png)

##

Run `Shirt-Printer.py`.

In the newly opened window, open a PNG image you want to print.\
I suggest the image is already converted into a RecRoom color palette
(Photoshop ACO swatch files are included), and scaled to the appropriate size.\
If the image is not converted it will automatically get converted and dithered.\
Templates for the shirt are in the `Shirt_Templates` map.

##   

After the data has been encoded, you will be prompted to import it to RecRoom.\
For this you'll have to **Configure** the `String Variable`. You will have to **replace** the existing one with a new
one (see video below)\
When you see the white `Value` input field, enter `y` in the script.\
Tab back into RecRoom and _wait_...\
I strongly recommend doing this step last, because all data gets erased if you save the room or `Reset Gadgets` 

https://user-images.githubusercontent.com/76653181/179419753-4981f9bb-0b66-47bb-8796-cbedddf5ef56.mp4

##   

When the importing process is finished, you will have to spawn in your **Shirt Customizer**.\
The placement is very important! If the canvas is not flush with the wall the print might not work at all.
Spawn the shirt customizer, grab it and push it into the corner _as shown in the video_.

https://user-images.githubusercontent.com/76653181/179420703-911f9aff-a5a3-432a-934f-2ab1b35848b0.mp4

It should look like the picture below. _Note one side of the clamp sticking through the board. Don't move the clamp._

![ShrtCutomizerInTheCorner](https://user-images.githubusercontent.com/76653181/179421185-9eff3a75-6e41-43d8-a1ca-a811894f8304.png)

##   

Next step is on the circuit board named `Shirt Printer`.\
You will have to change those inputs to suit your imported image\
There's comments to help you understand better;

* `Front And Back` - Set this to `True` if you're printing both-sided, set it to `False` if you're printing only one
  side.
* `Variable Import` - If you're importing the image always keep this to `True`. You only set it to `False` if you
  request me to import an image and let you print it (comes with a fee)
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
