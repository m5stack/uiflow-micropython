# Glass2 Unit

<!-- .. include:: ../refs/unit.glass2.ref -->

Glass2 Unit is a 1.51-inch transparent OLED display unit that adopts the SSD1309 driver solution.

Support the following products:

    |Glass2Unit|

## UiFlow2 Example

#### Draw Text

Open the |cores3_glass2_example.m5f2| project in UiFlow2.

This example displays the text "GLASS2" on the screen.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Draw Text

This example displays the text "GLASS2" on the screen.

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
from unit import Glass2Unit

label0 = None
label1 = None
i2c0 = None
glass2_0 = None

def setup():
    global label0, label1, i2c0, glass2_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("CoreS3", 127, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    glass2_0 = Glass2Unit(i2c0, 0x3C)
    label1 = Widgets.Label(
        "GLASS2", 26, 21, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18, glass2_0
    )

def loop():
    global label0, label1, i2c0, glass2_0
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

## class Glass2Unit

## Glass2Unit
Initialize the Glass2 Unit.

:param i2c: The I2C bus the Glass2 Unit is connected to.
:type i2c: I2C | PAHUBUnit
:param int address: The I2C address of the Glass2 Unit, default is 0x3C.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from unit import Glass2Unit
        glass2_0 = Glass2Unit(i2c0, 0x3c)

    Glass2Unit class inherits Display class, See :ref:`hardware.Display <hardware.Display>` for more details.
