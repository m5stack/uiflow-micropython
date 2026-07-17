# Atomic Display Base

The is the class of the Atomic Display Base, which is used to display images and text on the screen.

Support the following products:

    Atomic Display Base  Atom Display         Atom Display-Lite

Below is the detailed support for Atomic Display Base on the host:

    Controller        Status  |
     Atom Echo        O     |
     Atom Lite        S     |
     Atom Matrix      S     |
     AtomS3           S     |
     AtomS3 Lite      S     |
     AtomS3R          S     |
     AtomS3R-CAM      S     |
     AtomS3R-Ext      S     |

- S: Supported.

- O: Optional, It conflicts with some internal resource of the host.

## MicroPython Example

#### Draw Text

This example displays the text "M5Stack" on the screen.

```python
import os, sys, io
import M5
from M5 import *
from base import AtomicDisplayBase

label0 = None
label1 = None
base_display = None

def setup():
    global label0, label1, base_display

    M5.begin()
    label1 = Widgets.Label("M5Stack", 23, 53, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    base_display = AtomicDisplayBase(
        width=1280,
        height=720,
        refresh_rate=60,
        output_width=1280,
        output_height=720,
        scale_w=1,
        scale_h=1,
        pixel_clock=74250000,
    )
    label0 = Widgets.Label(
        "M5STACK", 466, 318, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu72, base_display
    )

def loop():
    global label0, label1, base_display
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

#### Draw Image

This example displays the image on the screen.

```python
import os, sys, io
import M5
from M5 import *
from base import AtomicDisplayBase

image0 = None
image1 = None
base_display = None

def setup():
    global image0, image1, base_display

    M5.begin()
    image0 = Widgets.Image("res/img/default.jpg", 51, 51, scale_x=1, scale_y=1)

    base_display = AtomicDisplayBase(
        width=1280,
        height=720,
        refresh_rate=60,
        output_width=1280,
        output_height=720,
        scale_w=1,
        scale_h=1,
        pixel_clock=74250000,
    )
    image1 = Widgets.Image(
        "res/img/default.jpg", 443, 213, scale_x=10, scale_y=10, parent=base_display
    )
    image0.setImage("res/img/default.jpg")
    image1.setImage("res/img/default.jpg")

def loop():
    global image0, image1, base_display
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

## **API**

#### AtomicDisplayBase

## `AtomicDisplayBase`
Initialize the Atomic Display Base.

- Parameter `width` (`int`): The logical width of the Atomic Display Base. Default is 1280px.
- Parameter `height` (`int`): The logical height of the Atomic Display Base. Default is 720px.
- Parameter `refresh_rate` (`int`): The refresh rate of the Atomic Display Base. Default is 60Hz.
- Parameter `output_width` (`int`): The width of the output of the Atomic Display Base. Default is 1280px.
- Parameter `output_height` (`int`): The height of the output of the Atomic Display Base. Default is 720px.
- Parameter `scale_w` (`int`): The scale width of the Atomic Display Base. Default is 1.
- Parameter `scale_h` (`int`): The scale height of the Atomic Display Base. Default is 1.
- Parameter `pixel_clock` (`int`): The pixel clock of the Atomic Display Base. Default is 74250000.

```python
from base import AtomicDisplayBase
atom_display = AtomicDisplayBase(1280, 720, 60, 1280, 720, 1, 1, 74250000)
```
