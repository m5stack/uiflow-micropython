<!-- .. currentmodule:: Widgets -->

# class Circle -- display circle

Circle is the basic object type used to display text.

<!-- .. include:: ../refs/widgets.circle.ref -->

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import time

circle0 = None
title0 = None

import random

def setup():
    global circle0, title0

    M5.begin()
    Widgets.fillScreen(0x222222)
    circle0 = Widgets.Circle(63, 111, 15, 0xFFFFFF, 0xFFFFFF)
    title0 = Widgets.Title("Circle Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)

    circle0.setVisible(True)

def loop():
    global circle0, title0
    M5.update()
    circle0.setRadius(r=(random.randint(1, 30)))
    circle0.setColor(
        color=0x000000,
        fill_c=(random.randint(0, 255) << 16)
        | (random.randint(0, 255) << 8)
        | random.randint(0, 255),
    )
    circle0.setCursor(x=(random.randint(1, 320)), y=(random.randint(1, 240)))
    time.sleep(0.5)

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

    |circle_core2_example.m5f2|

## Constructors

<!-- .. class:: Widgets.Circle(x: int, y: int, r: int, fg_color: int=0xffffff, bg_color: int=0xffffff) -->

    Create a Circle object. It accepts the following parameters:

        - ``x`` is the starting X-axis coordinate displayed.
        - ``y`` is the starting Y-axis coordinate displayed.
        - ``r`` is the radius of the circle.
        - ``fg_color`` is the foreground color of the displayed circle.
        - ``bg_color`` is the background color of the displayed circle.

## Methods

<!-- .. method:: Widgets.setColor(fg_color: int=0xffffff, bg_color: int=0x000000) -->

    Set the color of the Circle object. Accept the following parameters:

        - ``fg_color`` is the foreground color of the displayed circle.
        - ``bg_color`` is the background color of the displayed circle.

    UIFLOW2:

<!-- .. method:: Widgets.setCursor(x: int, y: int) -->

    Set the position of the Circle object. Accept the following parameters:

        - ``x`` is the starting X-axis coordinate displayed.
        - ``y`` is the starting Y-axis coordinate displayed.

    UIFLOW2:

<!-- .. method:: Widgets.setRadius(radius: int) -->

    Set the radius of the Circle object. Accept the following parameters:

        - ``r`` is the radius of the circle.

    UIFLOW2:

<!-- .. method:: Widgets.setVisible(visible: bool) -->

    Set the visibility of the Circle object. Accept the following parameters:

        - ``visible`` is the visibility of the displayed circle.

    UIFLOW2:
