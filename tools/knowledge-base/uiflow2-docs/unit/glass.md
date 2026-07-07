# Glass Unit

<!-- .. include:: ../refs/unit.glass.ref -->

Unit Glass is a 1.51-inch transparent OLED expansion screen unit. It adopts STM32+SSD1309 driver scheme,resolution is 128*64, monochrome display, transparent area is 128*56.

Support the following products:

    |GlassUnit|

## UiFlow2 Example

#### Draw Text

Open the |cores3_glass_example.m5f2| project in UiFlow2.

This example displays the text "GLASS" on the screen.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Draw Text

This example displays the text "GLASS" on the screen.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from unit import GlassUnit

label0 = None
label1 = None
i2c0 = None
glass_0 = None

def setup():
    global label0, label1, i2c0, glass_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("CoreS3", 138, 111, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    glass_0 = GlassUnit(i2c0, 0x3D)
    label1 = Widgets.Label(
        "GLASS", 32, 21, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18, glass_0
    )

def loop():
    global label0, label1, i2c0, glass_0
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

#### class GlassUnit

## GlassUnit
Initialize the Glass Unit.

:param i2c: The I2C bus the Glass Unit is connected to.
:type i2c: I2C | PAHUBUnit
:param int address: The I2C address of the Glass Unit, default is 0x3D.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from unit import GlassUnit
        glass_0 = GlassUnit(i2c0, 0x3d)

    GlassUnit class inherits Display class, See :ref:`hardware.Display <hardware.Display>` for more details.
