# JoyC Hat

<!-- .. include:: ../refs/hat.joyc.ref -->

The following products are supported:

    |JoyCHat|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from hat import JoyCHat

circle0 = None
circle1 = None
label0 = None
label1 = None
label2 = None
label3 = None
i2c0 = None
hat_joyc_0 = None

value = None
in_min = None
in_max = None
out_min = None
out_range = None
x = None
y = None
last_x = None
last_y = None

# Describe this function...
def map_to_range(value, in_min, in_max, out_min, out_range):
    global x, y, last_x, last_y, circle0, circle1, label0, label1, label2, label3, i2c0, hat_joyc_0
    return int((value - in_min) * out_range / (in_max - in_min) + out_min)

def setup():
    global \
        circle0, \
        circle1, \
        label0, \
        label1, \
        label2, \
        label3, \
        i2c0, \
        hat_joyc_0, \
        x, \
        out_range, \
        out_min, \
        y, \
        value, \
        in_min, \
        in_max, \
        last_x, \
        last_y

    M5.begin()
    circle0 = Widgets.Circle(67, 120, 50, 0xFFFFFF, 0x000000)
    circle1 = Widgets.Circle(67, 120, 4, 0xFFFFFF, 0xFFFFFF)
    label0 = Widgets.Label("X:", 6, 185, 1.0, 0x74F707, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Y:", 6, 212, 1.0, 0x74F707, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("0", 25, 185, 1.0, 0x74F707, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("0", 21, 212, 1.0, 0x74F707, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(26), sda=Pin(0), freq=100000)
    hat_joyc_0 = JoyCHat(i2c0, 0x38)
    hat_joyc_0.swap_x(True)
    hat_joyc_0.swap_y(True)
    last_x = 67
    last_y = 120

def loop():
    global \
        circle0, \
        circle1, \
        label0, \
        label1, \
        label2, \
        label3, \
        i2c0, \
        hat_joyc_0, \
        x, \
        out_range, \
        out_min, \
        y, \
        value, \
        in_min, \
        in_max, \
        last_x, \
        last_y
    M5.update()
    x = last_x + map_to_range(hat_joyc_0.get_x(0), -128, 127, -43, 86)
    y = last_y + map_to_range(hat_joyc_0.get_y(0), -128, 127, -43, 86)
    circle1.setCursor(x=x, y=y)
    if hat_joyc_0.get_button_status(0):
        circle1.setColor(color=0xFF0000, fill_c=0xFF0000)
    else:
        circle1.setColor(color=0xFFFFFF, fill_c=0x6600CC)
    label2.setText(str(hat_joyc_0.get_x(0)))
    label3.setText(str(hat_joyc_0.get_y(0)))

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

    |stickc_plus2_joyc_example.m5f2|

## class JoyCHat

## Constructors

<!-- .. class:: JoyCHat(i2c, address: int | list | tuple = 0x38) -->

    Create a new instance of the JoyCHat class.

    :param i2c: I2C bus
    :param address: I2C address

    UIFLOW2:

## Methods

<!-- .. method:: JoyCHat.get_x_raw(channel: int = 0) -> int -->

    Get the raw x-axis value.

    :param channel: 0 or 1

    :return: x-axis value

    UIFLOW2:

<!-- .. method:: JoyCHat.get_y_raw(channel: int = 0) -> int -->

    Get the raw y-axis value.

    :param channel: 0 or 1

    :return: y-axis value

    UIFLOW2:

<!-- .. method:: JoyCHat.get_x(channel: int = 0) -> int -->

    Get the x-axis value.

    :param channel: 0 or 1

    :return: x-axis value

    UIFLOW2:

<!-- .. method:: JoyCHat.get_y(channel: int = 0) -> int -->

    Get the y-axis value.

    :param channel: 0 or 1

    :return: y-axis value

    UIFLOW2:

<!-- .. method:: JoyCHat.swap_x(swap: bool = True) -> None -->

    Swap x-axis direction

    :param swap: True or False

    UIFLOW2:

<!-- .. method:: JoyCHat.swap_y(swap: bool = True) -> None -->

    Swap y-axis direction

    :param swap: True or False

    UIFLOW2:

<!-- .. method:: JoyCHat.get_button_status(channel: int = 0) -> bool -->

    Get the button status.

    :param channel: 0 or 1
    :return: True or False

    UIFLOW2:

<!-- .. method:: JoyCHat.fill_color() -> None -->

    Fill the screen with a color.

    UIFLOW2:
