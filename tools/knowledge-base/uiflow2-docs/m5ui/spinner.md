<!-- .. currentmodule:: m5ui -->

# M5Spinner

<!-- .. include:: ../refs/m5ui.spinner.ref -->

M5Spinner is a spinning arc over a ring, typically used to show some type of activity is in progress.

## UiFlow2 Example

#### spinner

Open the |core2_spinner_example.m5f2| project in UiFlow2.

This example shows a spinning arc over a ring.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### spinner

This example shows a spinning arc over a ring.

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
spinner0 = None

def setup():
    global page0, spinner0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    spinner0 = m5ui.M5Spinner(
        x=71,
        y=81,
        w=100,
        h=100,
        anim_t=10000,
        angle=180,
        bg_c=0xE7E3E7,
        bg_c_indicator=0x2193F3,
        parent=page0,
    )

    page0.screen_load()

def loop():
    global page0, spinner0
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

#### M5Spinner

## M5Spinner
Create a spinner object.

:param int x: The x position of the spinner.
:param int y: The y position of the spinner.
:param int w: The width of the spinner.
:param int h: The height of the spinner.
:param int anim_t: The animation time in milliseconds.
:param int angle: The angle of the spinner in degrees.
:param int bg_c: The background color of the spinner in hexadecimal format.
:param int bg_c_indicator: The indicator color of the spinner in hexadecimal format.
:param lv.obj parent: The parent object to attach the spinner to. If not specified, the spinner will be attached to the default screen.

UiFlow2 Code Block:

    None

MicroPython Code Block:

    .. code-block:: python

        from m5ui import M5Spinner
        import lvgl as lv

        m5ui.init()
        spinner_0 = M5Spinner(x=120, y=80, w=60, h=30, anim_t=1000, angle=180, bg_c=0xE7E3E7, bg_c_indicator=0x0288FB, parent=page0)

### `set_spinner_color`
Set the color of the spinner.

:param int color: The color of the spinner in hexadecimal format.
:param int opa: The opacity of the color (0-255).
:param int part: The part of the spinner to set the color for.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        spinner_0.set_spinner_color(0x2196F3, 255, lv.PART.MAIN | lv.STATE.DEFAULT)

<!-- .. py:method:: set_flag(flag, value) -->

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                spinner_0.set_flag(lv.obj.FLAG.HIDDEN, True)

<!-- .. py:method:: set_pos(x, y) -->

        Set the position of the spinner.

        :param int x: The x-coordinate of the spinner.
        :param int y: The y-coordinate of the spinner.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                spinner_0.set_pos(100, 100)

<!-- .. py:method:: set_x(x) -->

        Set the x-coordinate of the spinner.

        :param int x: The x-coordinate of the spinner.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                spinner_0.set_x(100)

<!-- .. py:method:: set_y(y) -->

        Set the y-coordinate of the spinner.

        :param int y: The y-coordinate of the spinner.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                spinner_0.set_y(100)

<!-- .. py:method:: set_size(width, height) -->

        Set the size of the spinner.

        :param int width: The width of the spinner.
        :param int height: The height of the spinner.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                spinner_0.set_size(100, 50)

<!-- .. py:method:: align_to(obj, align, x, y) -->

        Align the spinner to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                spinner_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)

<!-- .. py:method:: set_anim_params(anim_t, angle) -->

        Set the animation parameters of the spinner.

        :param int anim_t: The animation time in milliseconds.
        :param int angle: The angle of the spinner in degrees.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                spinner_0.set_anim_params(1000, 180)
