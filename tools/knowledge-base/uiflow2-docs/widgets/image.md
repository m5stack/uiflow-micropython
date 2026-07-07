<!-- .. currentmodule:: Widgets -->

# class Image -- display image

Image is the basic object type used to display images.

<!-- .. include:: ../refs/widgets.image.ref -->

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *

image0 = None
title0 = None

def setup():
    global image0, title0

    M5.begin()
    Widgets.fillScreen(0x222222)
    image0 = Widgets.Image("res/img/SCR-20240902-itcy.png", 71, 64)
    title0 = Widgets.Title("Image CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)

    image0.setImage("res/img/default.png")
    image0.setImage("res/img/SCR-20240902-itcy.png")
    image0.setCursor(x=0, y=0)
    image0.setVisible(True)

def loop():
    global image0, title0
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

UIFLOW2 Example:

<!-- .. only:: builder_html -->

    |image_cores3_example.m5f2|

## Constructors

<!-- .. class:: Widgets.Image(str: file, x: int, y: int, parent) -->

    Create an Image object. It accepts the following parameters:

        - ``file`` is the path to the image file to be displayed. Supported formats are BMP, JPG, and PNG.
        - ``x`` is the starting X-axis coordinate where the image will be displayed.
        - ``y`` is the starting Y-axis coordinate where the image will be displayed.
        - ``parent`` is the graphical object on which the image will be drawn. If not provided, the default display will be used.

## Methods

<!-- .. method:: Image.setCursor(x: int, y: int) -->

    Set the position of the Imgae object. Accept the following parameters:

        - ``x`` is the starting X-axis coordinate displayed.
        - ``y`` is the starting Y-axis coordinate displayed.

    UIFLOW2:

<!-- .. method:: Image.setImage(str: file) -->

    Set the image to be displayed.

        - ``file`` is the path to the new image file to be displayed.

    UIFLOW2:

<!-- .. method:: Image.setVisible(visible: bool) -->

    Set the visibility of the Imgae object. Accept the following parameters:

        - ``visible`` is the visibility of the displayed image.

    UIFLOW2:
