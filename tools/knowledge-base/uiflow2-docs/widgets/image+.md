<!-- .. currentmodule:: Widgets -->

# class ImagePlus -- display remote image

The `ImagePlus` class extends the `Widgets.Image` class to provide additional functionalities for handling images with dynamic updates.

<!-- .. include:: ../refs/widgets.image+.ref -->

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from image_plus import ImagePlus

title0 = None
image_plus0 = None

def setup():
    global title0, image_plus0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("Image+ CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    image_plus0 = ImagePlus(
        "https://static-cdn.m5stack.com/resource/public/assets/aboutus/m5logo2022.png",
        43,
        51,
        True,
        3000,
        default_img="res/img/default.png",
    )

    image_plus0.setVisible(True)
    image_plus0.set_update_period(5000)
    image_plus0.set_update_enable(True)

def loop():
    global title0, image_plus0
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

    |imageplus_cores3_example.m5f2|

## Constructors

<!-- .. class:: ImagePlus(url, x, y, enable, period, default_img="res/img/default.jpg", parent=None) -->

    Create an `ImagePlus` object. It accepts the following parameters:

        - ``url`` is the URL of the image to be fetched and displayed.
        - ``x`` is the starting X-axis coordinate where the image will be displayed.
        - ``y`` is the starting Y-axis coordinate where the image will be displayed.
        - ``enable`` is a boolean indicating whether periodic updates of the image are enabled.
        - ``period`` is the update period in milliseconds when `enable` is `True`.
        - ``default_img`` is the path to the default image file to be displayed if the URL fetch fails. Supported formats are BMP, JPG, and PNG. Default is `"res/img/default.jpg"`.
        - ``parent`` is the graphical object on which the image will be drawn. If not provided, the default display will be used.

## Methods

<!-- .. method:: ImagePlus.set_update_enable(enable: bool) -->

    Enable or disable periodic updates of the image. Accept the following parameters:

        - ``enable`` is a boolean indicating whether updates should be enabled.

    UIFLOW2:

<!-- .. method:: ImagePlus.set_update_period(period: int) -->

    Set the update period for fetching and displaying the image. Accept the following parameters:

        - ``period`` is the update period in milliseconds.

    UIFLOW2:

<!-- .. method:: ImagePlus.setCursor(x: int, y: int) -->

    Set the position of the ImagePlus object. Accept the following parameters:

        - ``x`` is the starting X-axis coordinate displayed.
        - ``y`` is the starting Y-axis coordinate displayed.

    UIFLOW2:

<!-- .. method:: ImagePlus.setVisible(visible: bool) -->

    Set the visibility of the ImagePlus object. Accept the following parameters:

        - ``visible`` is the visibility of the displayed iamge.

    UIFLOW2:

<!-- .. method:: ImagePlus.is_valid_image() -> bool -->

    Check if the fetched image is valid. Returns `True` if the image is valid, otherwise `False`.

    UIFLOW2:
