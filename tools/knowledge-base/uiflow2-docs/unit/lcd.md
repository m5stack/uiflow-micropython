# LCD Unit

<!-- .. sku: U120 -->

<!-- .. include:: ../refs/unit.lcd.ref -->

Unit LCD is a 1.14 inch color LCD expansion screen unit. It adopts ST7789V2
drive scheme, the resolution is 135*240, and it supports
RGB666 display (262,144 colors). The internal integration of ESP32-PICO control
core (built-in firmware, display development is more convenient), support
through I2C (addr: 0x3E) communication interface for control and firmware
upgrades. The back of the screen is integrated with a magnetic design,
which can easily adsorb the metal surface for fixing. The LCD screen extension
is suitable for embedding in various instruments or control devices that need
to display simple content as a display panel.

Support the following products:

    |LCDUnit|

## UiFlow2 Example

#### Draw Text

Open the |cores3_lcd_example.m5f2| project in UiFlow2.

This example displays the text "LCD" on the screen.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Draw Text

This example displays the text "LCD" on the screen.

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
from unit import LCDUnit

label0 = None
label1 = None
i2c0 = None
lcd_0 = None

def setup():
    global label0, label1, i2c0, lcd_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("CoreS3", 127, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    lcd_0 = LCDUnit(i2c0, 0x3E)
    label1 = Widgets.Label("LCD", 48, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18, lcd_0)

def loop():
    global label0, label1, i2c0, lcd_0
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

#### class LCDUnit

## LCDUnit
Initialize the LCD Unit.

:param i2c: The I2C bus the LCD Unit is connected to.
:type i2c: I2C
:param int address: The I2C address of the LCD Unit, default is 0x3E.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from unit import LCDUnit
        lcd_0 = LCDUnit(i2c0, 0x3e)

    LCDUnit class inherits Display class, See :ref:`hardware.Display <hardware.Display>` for more details.
