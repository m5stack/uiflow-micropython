# DigiClock Unit

<!-- .. include:: ../refs/unit.digi_clock.ref -->

UNIT-Digi-Clock is a 2.1 inch 4-digit 7-segment display module. There are
decimal points on each digit and an extra wire for colon-dots in the center,
which can display Decimals and Clock. This module adopts TM1637 as the driver
IC, and STM32F030 as I2C communication. I2C address can be modified per 4-bit
dip switch. The red LED supports 8 brightness. And we have reserved 4 fixing
holes there.

Support the following products:

    |DigiClockUnit|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import DigiClockUnit
import time

label0 = None
i2c0 = None
digiclock_0 = None

now = None

def setup():
    global label0, i2c0, digiclock_0, now

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 99, 97, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu40)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    digiclock_0 = DigiClockUnit(i2c0, 0x30)
    now = str((str(((time.localtime())[3])) + str(":"))) + str(((time.localtime())[4]))
    digiclock_0.set_string(now)
    label0.setText(str(now))

def loop():
    global label0, i2c0, digiclock_0, now
    M5.update()
    if now != (str((str(((time.localtime())[3])) + str(":"))) + str(((time.localtime())[4]))):
        now = str((str(((time.localtime())[3])) + str(":"))) + str(((time.localtime())[4]))
        label0.setText(str(now))
        digiclock_0.set_string(now)
    digiclock_0.set_raw(1, 2)
    time.sleep(1)
    digiclock_0.set_raw(0, 2)
    time.sleep(1)

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

UIFLOW2 Example:

<!-- .. only:: builder_html -->

    |cores3_digi_clock_example.m5f2|

## class DigiClockUnit

## Constructors

<!-- .. class:: DigiClockUnit(i2c: I2C, address: int | list | tuple = 0x30) -->

    Initialize the DigiClockUnit.

    :param I2C i2c: I2C port to use.
    :param int | list | tuple address: I2C address of the DigiClockUnit.

    UIFLOW2:

## Methods

<!-- .. method:: DigiClockUnit.clear() -> None -->

    Clear the display.

    UIFLOW2:

<!-- .. method:: DigiClockUnit.set_brightness(brightness: int) -> None -->

    Set the brightness of the display.

    :param int brightness: The brightness of the display, range from 0 to 8.

    UIFLOW2:

<!-- .. method:: DigiClockUnit.set_raw(data: int, index: int) -> None -->

    Write raw data to the display.

    :param int data: The data to write.
    :param int index: The index of the data, range from 0 to 4.

    UIFLOW2:

<!-- .. method:: DigiClockUnit.set_char(char: str, index: int) -> None -->

    Write a character to the display.

    :param str char: The character to write.
    :param int index: The index of the character, range from 0 to 4.

    UIFLOW2:

<!-- .. method:: DigiClockUnit.set_string(string: str) -> None -->

    Write a string to the display.

    :param str string: The string to write.

    UIFLOW2:

<!-- .. method:: DigiClockUnit.get_fw_version() -> int -->

    Get the firmware version of the DigiClockUnit.

    :return: The firmware version.

    UIFLOW2:
