<!-- .. currentmodule:: m5ui -->

# M5Image

<!-- .. include:: ../refs/m5ui.image.ref -->

M5Image is a widget that can be used to create image in the user interface.

## UiFlow2 Example

#### show image

Open the |cores3_show_image_example.m5f2| project in UiFlow2.

This example shows how to display an image on the screen.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### show image

This example shows how to display an image on the screen.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv

page0 = None
image0 = None
image1 = None

def setup():
    global page0, image0, image1

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    image0 = m5ui.M5Image("/flash/res/img/uiflow.jpg", x=129, y=54, parent=page0)
    image1 = m5ui.M5Image("/flash/res/img/uiflow.png", x=129, y=118, parent=page0)

    page0.screen_load()
    image0.set_image("/flash/res/img/uiflow.jpg")
    image1.set_image("/flash/res/img/uiflow.png")

def loop():
    global page0, image0, image1
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

```

Example output:

    None

## **API**

#### M5Image

## M5Image
Create a image object.

:param str path: The path of the image file.
:param int x: The x position of the image.
:param int y: The y position of the image.
:param lv.obj parent: The parent object to attach the image to. If not specified, the image will be attached to the default screen.

MicroPython Code Block:

    .. code-block:: python

        from m5ui import M5Image
        import lvgl as lv

        m5ui.init()
        image_0 = M5Image("/flash/res/img/defalut.jpg", x=10, y=10, parent=page0)
        image_1 = M5Image("/flash/res/img/uiflow.jpg", x=50, y=50, parent=page0)

### `set_image`
Set the image to be displayed.

:param str path: The path of the image file.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        image_0.set_image("/flash/res/img/uiflow.jpg")
        image_1.set_image("/sd/uiflow.png")

### `set_rotation`
Set the rotation of the image.

:param int rotation: The rotation angle in degrees (0, 90, 180, 270).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        image_0.set_rotation(90)

### `set_scale`
Set the scale of the image.

:param float scale_x: The horizontal scale factor.
:param float scale_y: The vertical scale factor.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        image_0.set_scale(2.0, 2.0)

### `set_style_radius`

<!-- .. py:method:: set_flag(flag, value) -->

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                image_0.set_flag(lv.obj.FLAG.HIDDEN, True)

<!-- .. py:method:: set_pos(x, y) -->

        Set the position of the image.

        :param int x: The x-coordinate of the image.
        :param int y: The y-coordinate of the image.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                image_0.set_pos(100, 100)

<!-- .. py:method:: set_x(x) -->

        Set the x-coordinate of the image.

        :param int x: The x-coordinate of the image.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                image_0.set_x(100)

<!-- .. py:method:: set_y(y) -->

        Set the y-coordinate of the image.

        :param int y: The y-coordinate of the image.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                image_0.set_y(100)

<!-- .. py::method:: get_width() -->

        Get the width of the image.

        :return: The width of the image.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                image_0.get_width()

<!-- .. py::method:: get_height() -->

        Get the height of the image.

        :return: The height of the image.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                image_0.get_height()

<!-- .. py:method:: align_to(obj, align, x, y) -->

        Align the image to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                image_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
