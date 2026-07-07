<!-- .. currentmodule:: m5ui -->

# M5Line

<!-- .. include:: ../refs/m5ui.line.ref -->

M5Line is a widget that can be used to create lines in the user interface. It can be used to draw shapes and connect points.

## UiFlow2 Example

#### points connect

Open the |cores3_line_example.m5f2| project in UiFlow2.

This example creates a line that connects multiple points.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### points connect

This example creates a line that connects multiple points.

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
line0 = None

def setup():
    global page0, line0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    line0 = m5ui.M5Line(
        points=[5, 5, 70, 70, 120, 10, 180, 60, 190, 70, 200, 80, 210, 90, 220, 100],
        width=7,
        color=0x2196F3,
        rounded=True,
        parent=page0,
    )

    page0.screen_load()

def loop():
    global page0, line0
    M5.update()
    if M5.Touch.getCount():
        line0.add_point(M5.Touch.getX(), M5.Touch.getY())

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

#### M5Line

## M5Line
Create a line object.

:param list points: A list of points where each point is a pair of x and y coordinates.
:param int width: The width of the line.
:param int color: The color of the line in hexadecimal format.
:param bool rounded: If True, the line will have rounded ends; otherwise, it will have square ends.
:param lv.obj parent: The parent object to attach the line to. If not specified, the line will be attached to the default screen.

MicroPython Code Block:

    .. code-block:: python

        from m5ui import M5Line
        import lvgl as lv

        m5ui.init()
        line_0 = M5Line(
            points=[5, 5, 70, 70, 120, 10, 180, 60, 240, 20],
            width=2,
            color=0x2196F3,
            rounded=True,
            parent=page0,
        )

### `set_points`
Set the points of the line.

:param list points: A list of points where each point is a pair of x and y coordinates.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        line_0.set_points([0, 0, 100, 100, 200, 50])

### `add_point`
Add a point to the line end.

:param int x: The x position of the point.
:param int y: The y position of the point.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        line_0.add_point(100, 100)

### `set_style_radius`

<!-- .. py:method:: set_line_color(color, opa, part) -->

        Set the color of the line.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                line_0.set_line_color(0xFF0000, 255, lv.PART.MAIN)

<!-- .. py:method:: set_style_line_width(width,  part) -->

        Set the width of the line.

        :param int width: The width to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                line_0.set_style_line_width(2, lv.PART.MAIN)

<!-- .. py:method:: set_flag(flag, value) -->

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.set_flag(lv.obj.FLAG.HIDDEN, True)

<!-- .. py:method:: set_pos(x, y) -->

        Set the position of the line.

        :param int x: The x-coordinate of the line.
        :param int y: The y-coordinate of the line.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                line_0.set_pos(100, 100)

<!-- .. py:method:: set_x(x) -->

        Set the x-coordinate of the line.

        :param int x: The x-coordinate of the line.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                line_0.set_x(100)

<!-- .. py:method:: set_y(y) -->

        Set the y-coordinate of the line.

        :param int y: The y-coordinate of the line.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                line_0.set_y(100)

<!-- .. py:method:: align_to(obj, align, x, y) -->

        Align the line to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                line_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
