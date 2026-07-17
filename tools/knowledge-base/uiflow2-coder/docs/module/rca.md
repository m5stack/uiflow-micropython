# RCA Module

Module RCA is a female jack terminal block for transmitting composite video (audio or video), one of the most common A/V connectors, which transmits  video or audio signals from a component device to an output  device (i.e., a display or speaker).

Support the following products:

    RCAModule

## MicroPython Example

#### Draw Text

This example displays the text "RCA" on the screen.

```python
import os, sys, io
import M5
from M5 import *
from module import RCAModule

label0 = None
label1 = None
module_rca = None

def setup():
    global label0, label1, module_rca

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Core2", 133, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    module_rca = RCAModule(
        26,
        width=216,
        height=144,
        output_width=0,
        output_height=0,
        signal_type=RCAModule.NTSC,
        use_psram=0,
        output_level=0,
    )
    label1 = Widgets.Label(
        "RCA", 88, 61, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18, module_rca
    )

def loop():
    global label0, label1, module_rca
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

#### Class RCAModule

## `RCAModule`
Initialize the RCA Module.

- Parameter `pin` (`int`): The dac pin to which the RCA Module is connected.
- Parameter `width` (`int`): The width of the RCA display.
- Parameter `height` (`int`): The height of the RCA display.
- Parameter `output_width` (`int`): The width of the output of the RCA display.
- Parameter `output_height` (`int`): The height of the output of the RCA display.
- Parameter `signal_type` (`int`): The signal type of the RCA display. NTSC=0, NTSC_J=1, PAL=2, PAL_M=3, PAL_N=4.
- Parameter `use_psram` (`int`): The use of psram of the RCA display.
- Parameter `output_level` (`int`): The output level of the RCA display.

```python
from module import RCAModule
module_rca = RCAModule(26, width=216, height=144, output_width=0, output_height=0, signal_type=RCAModule.NTSC, use_psram=0, output_level=0)
```

    RCAModule class inherits Display class, See `hardware.Display <hardware.Display>` for more details.
