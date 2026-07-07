
# MiniOLED Unit

<!-- .. include:: ../refs/unit.minioled.ref -->

MiniOLED UNIT is a 0.42-inch I2C interface OLED screen unit, it's a 72*40, monochrome white display.

Support the following products:

    |MiniOLEDUnit|

## UiFlow2 Example

#### Draw Text

Open the |cores3_minioled_example.m5f2| project in UiFlow2.

This example displays the text "Mini" on the screen.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Draw Text

This example displays the text "Mini" on the screen.

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
from unit import MiniOLEDUnit

label0 = None
label1 = None
i2c0 = None
minioled_0 = None

def setup():
    global label0, label1, i2c0, minioled_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("CoreS3", 127, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    minioled_0 = MiniOLEDUnit(i2c0, 0x3C)
    label1 = Widgets.Label(
        "Mini", 15, 9, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18, minioled_0
    )

def loop():
    global label0, label1, i2c0, minioled_0
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

#### class MiniOLEDUnit

## MiniOLEDUnit
Initialize the Mini OLED Unit.

:param i2c: The I2C bus the Mini OLED Unit is connected to.
:type i2c: I2C | PAHUBUnit
:param int address: The I2C address of the Mini OLED Unit, default is 0x3C.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from unit import MiniOLEDUnit
        minioled_0 = MiniOLEDUnit(i2c0, 0x3c)

    MiniOLEDUnit class inherits Display class, See :ref:`hardware.Display <hardware.Display>` for more details.
