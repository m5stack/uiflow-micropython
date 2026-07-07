
# Display Module

<!-- .. sku: M126 -->

<!-- .. include:: ../refs/module.display.ref -->

Display Module 13.2 is an expansion module for HD audio and video, using GAOYUN GW1NR series FPGA chip to output display signals, and employing the LT8618S chip for signal output conditioning.

Support the following products:

    |DisplayModule|

## UiFlow2 Example

#### Draw Text

Open the |cores3_display_example.m5f2| project in UiFlow2.

This example displays the text "Display" on the screen.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

This example displays the text "Display" on the screen.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import DisplayModule

label0 = None
label1 = None
module_display = None

def setup():
    global label0, label1, module_display

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("CoreS3", 127, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    module_display = DisplayModule(
        width=1280,
        height=720,
        output_width=1280,
        output_height=720,
        refresh_rate=60,
        pixel_clock=74250000,
        scale_w=1,
        scale_h=1,
    )
    label1 = Widgets.Label(
        "Display", 506, 318, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu72, module_display
    )

def loop():
    global label0, label1, module_display
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

Example output:

    None

## **API**

#### Class DisplayModule

## DisplayModule
Initialize the Display Module.

:param int width: The logical width of the Display Module. Default is 1280px.
:param int height: The logical height of the Display Module. Default is 720px.
:param int refresh_rate: The refresh rate of the Display Module. Default is 60Hz.
:param int output_width: The width of the output of the Display Module. Default is 1280px.
:param int output_height: The height of the output of the Display Module. Default is 720px.
:param int scale_w: The scale width of the Display Module. Default is 1.
:param int scale_h: The scale height of the Display Module. Default is 1.
:param int pixel_clock: The pixel clock of the Display Module. Default is 74250000.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from module import DisplayModule
        module_display = DisplayModule(1280, 720, 60, 1280, 720, 1, 1, 74250000)

    DisplayModule class inherits Display class, See :ref:`hardware.Display <hardware.Display>` for more details.
