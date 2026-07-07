
# OLED Unit

<!-- .. sku: u119 -->

<!-- .. include:: ../refs/unit.oled.ref -->

Unit OLED is a 1.3-inch OLED expansion screen unit. Driveing by SH1107, and the resolution is 128*64, monochrome display.

Support the following products:

    |OLEDUnit|

## UiFlow2 Example

#### Draw Text

Open the |cores3_oled_example.m5f2| project in UiFlow2.

This example displays the text "OLED" on the screen.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Draw Text

This example displays the text "OLED" on the screen.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from unit import OLEDUnit

label0 = None
label1 = None
i2c0 = None
oled_0 = None

def setup():
    global label0, label1, i2c0, oled_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("CoreS3", 127, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    oled_0 = OLEDUnit(i2c0, 0x3C)
    label1 = Widgets.Label("OLED", 5, 53, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18, oled_0)

def loop():
    global label0, label1, i2c0, oled_0
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

#### class OLEDUnit

## OLEDUnit
Initialize the OLED Unit.

:param i2c: The I2C bus the OLED Unit is connected to.
:type i2c: I2C | PAHUBUnit
:param int address: The I2C address of the OLED Unit, default is 0x3C.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from unit import OLEDUnit
        oled_0 = OLEDUnit(i2c0, 0x3c)

    OLEDUnit class inherits Display class, See :ref:`hardware.Display <hardware.Display>` for more details.
