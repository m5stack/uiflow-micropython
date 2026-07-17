# addon DisplayOut

`DisplayOut` enables HDMI display output on Unit PoE-P4 by registering the
PoE-P4 HDMI interface as an M5 display. Use it when an external HDMI monitor is
connected to the Unit PoE-P4 display output.

Support the following products:

    UNIT_POEP4

## MicroPython Example

#### HDMI output

This example initializes the HDMI output and draws basic widgets on the external display.

```python
import os, sys, io
import M5
from M5 import *
from addon import DisplayOut

title = None
circle0 = None
rect0 = None
label0 = None
line0 = None
triangle0 = None
addon_display_out_0 = None

def setup():
    global title, circle0, rect0, label0, line0, triangle0, addon_display_out_0

    M5.begin()
    addon_display_out_0 = DisplayOut(1280, 720, 60)
    Widgets.fillScreen(0x000000, addon_display_out_0)
    title = Widgets.Title(
        "addon Display Out For PoE-P4 Example",
        3,
        0xFFFFFF,
        0x0000FF,
        Widgets.FONTS.Montserrat18,
        addon_display_out_0,
    )
    circle0 = Widgets.Circle(118, 182, 68, 0xFFFFFF, 0xFFFFFF, addon_display_out_0)
    rect0 = Widgets.Rectangle(885, 338, 217, 217, 0xFFFFFF, 0xFFFFFF, addon_display_out_0)
    label0 = Widgets.Label(
        "label0",
        556,
        149,
        1.0,
        0xFFFFFF,
        0x222222,
        Widgets.FONTS.Montserrat18,
        addon_display_out_0,
    )
    line0 = Widgets.Line(398, 446, 448, 446, 0xFFFFFF, addon_display_out_0)
    triangle0 = Widgets.Triangle(
        765, 346, 735, 376, 794, 376, 0xFFFFFF, 0xFFFFFF, addon_display_out_0
    )

def loop():
    global title, circle0, rect0, label0, line0, triangle0, addon_display_out_0
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

#### DisplayOut

## `DisplayOut`
Create an HDMI display output for Unit PoE-P4.

`DisplayOut` registers the Unit PoE-P4 HDMI output as an M5 display and
returns the display object created by `M5.addDisplay`. The display can
then be used by the standard M5 display APIs.

- Parameter `width` (`int`): The logical width of the HDMI output. Default is `1280`.
- Parameter `height` (`int`): The logical height of the HDMI output. Default is `720`.
- Parameter `refresh_rate` (`int`): The refresh rate of the HDMI output in Hz. Default is `60`.
- Returns: The display object registered by `M5.addDisplay`.
- Return type: object

> Note: Unit PoE-P4 HDMI output supports `1280x720@60Hz` and
> `1920x1080@30Hz` timings.

```python
from addon import DisplayOut

display = DisplayOut(1280, 720, 60)
```
