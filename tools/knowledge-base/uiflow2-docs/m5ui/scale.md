<!-- .. currentmodule:: m5ui -->

# M5Scale

<!-- .. include:: ../refs/m5ui.scale.ref -->

M5Scale is a widget that can be used to create scales in the user interface. Scale Widgets show linear or circular scales with configurable ranges, tick counts, placement, labeling, and subsections (Sections) with custom styling.

## UiFlow2 Example

#### scale example

Open the |scale_core2_example.m5f2| project in UiFlow2.

This example demonstrates how to create a scale widget with a range of values and custom styling.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### scroll example

This example demonstrates how to create a scale widget with a range of values and custom styling.

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
scale0 = None

def setup():
    global page0, scale0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    scale0 = m5ui.M5Scale(
        x=7,
        y=92,
        w=300,
        h=0,
        start_pos=0,
        end_pos=100,
        tick_count=11,
        tick_every=2,
        show_mode=lv.scale.MODE.HORIZONTAL_TOP,
        parent=page0,
    )

    page0.screen_load()
    scale0.set_style_line_width(2, lv.PART.MAIN)
    scale0.set_line_color(0x6600CC, 255, lv.PART.MAIN)
    scale0.set_style_line_width(4, lv.PART.INDICATOR)
    scale0.set_line_color(0xFF9900, 255, lv.PART.INDICATOR)
    scale0.set_style_line_width(6, lv.PART.ITEMS)
    scale0.set_line_color(0x66FF99, 255, lv.PART.ITEMS)

def loop():
    global page0, scale0
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

#### M5Scale

## M5Scale
Create a scale object.

:param int x: The x position of the scale.
:param int y: The y position of the scale.
:param int w: The width of the scale. If not specified, it will be set based on the mode.
:param int h: The height of the scale. If not specified, it will be set based on the mode.
:param int start_pos: The starting position of the scale.
:param int end_pos: The ending position of the scale.
:param int tick_count: The total number of ticks on the scale.
:param int tick_every: The interval between major ticks on the scale.
:param int mode: The mode of the scale. It can be one of the following:

    Options:

        - `lv.scale.MODE.HORIZONTAL_TOP`: Horizontal top scale.
        - `lv.scale.MODE.HORIZONTAL_BOTTOM`: Horizontal bottom scale.
        - `lv.scale.MODE.VERTICAL_LEFT`: Vertical left scale.
        - `lv.scale.MODE.VERTICAL_RIGHT`: Vertical right scale.
        - `lv.scale.MODE.ROUND_INNER`: Round inner scale.
        - `lv.scale.MODE.ROUND_OUTER`: Round outer scale.

:param lv.obj parent: The parent object to attach the scale to. If not specified, the scale will be attached to the default screen.

MicroPython Code Block:

    .. code-block:: python

        from m5ui import M5Scale
        import lvgl as lv

        m5ui.init()
        scale_0 = M5Scale(x=10, y=10, w=200, h=20, start_pos=0, end_pos=100, tick_count=11, tick_every=2, mode=lv.scale.MODE.HORIZONTAL_TOP, parent=page0)

### `set_mode`

### `set_size`

### `set_pos`

### `set_x`

### `set_y`

### `align_to`

<!-- .. py:method:: set_flag(flag, value) -->

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                scale_0.set_flag(lv.obj.FLAG.HIDDEN, True)

<!-- .. py:method:: set_range(start_pos, end_pos) -->

        Set the range of the scale.

        :param int start_pos: The start position of the scale.
        :param int end_pos: The end position of the scale.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                scale_0.set_range(0, 100)

<!-- .. py:method:: set_major_tick_every(tick_every) -->

        Set the interval for major ticks on the scale.

        :param int tick_every: The interval for major ticks.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                scale_0.set_major_tick_every(10)

<!-- .. py:method:: set_total_tick_count(tick_count) -->

        Set the total tick count of the scale.

        :param int tick_count: The total tick count.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                scale_0.set_total_tick_count(11)

<!-- .. py:method:: set_label_show(label_show) -->

        Set the visibility of the scale labels.

        :param bool label_show: If True, the labels are shown; if False, they are hidden.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                scale_0.set_label_show(True)

<!-- .. py:method:: set_mode(show_mode) -->

        Set the display mode of the scale.

        :param int show_mode: The display mode.

            Optional:

                - `lv.scale.MODE.HORIZONTAL_TOP`: Horizontal top scale.
                - `lv.scale.MODE.HORIZONTAL_BOTTOM`: Horizontal bottom scale.
                - `lv.scale.MODE.VERTICAL_LEFT`: Vertical left scale.
                - `lv.scale.MODE.VERTICAL_RIGHT`: Vertical right scale.
                - `lv.scale.MODE.ROUND_INNER`: Round inner scale.
                - `lv.scale.MODE.ROUND_OUTER`: Round outer scale.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                scale_0.set_mode(lv.SCALE.MODE.HORIZONTAL_TOP)

<!-- .. py:method:: set_text_src(text_src) -->

        Set the source of the scale label text.

        :param list text_src: The source of the scale label text.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                scale_0.set_text_src(["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100", None])

<!-- .. py:method:: set_line_color(color, opa, part) -->

        Set the color of the line.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                scale_0.set_line_color(0xFF0000, 255, lv.PART.MAIN)
                scale_0.set_line_color(0x00FF00, 255, lv.PART.ITEMS)
                scale_0.set_line_color(0x0000FF, 255, lv.PART.INDICATOR)

<!-- .. py:method:: set_style_line_width(width, part) -->

        Set the line width of the scale.

        :param int width: The line width to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                scale_0.set_style_line_width(2, lv.PART.MAIN)
                scale_0.set_style_line_width(2, lv.PART.ITEMS)
                scale_0.set_style_line_width(2, lv.PART.INDICATOR)

<!-- .. py:method:: set_text_color(color, opa, part) -->

        Set the color of the text.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to lv.PART.INDICATOR.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                scale_0.set_text_color(0xFF0000, 255, lv.PART.INDICATOR)

<!-- .. py:method:: set_style_text_font(font, part) -->

        Set the font of the scale label text.

        :param lv.lv_font_t font: The font to set.
        :param int part: The part of the object to apply the style to lv.PART.INDICATOR.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                scale_0.set_style_text_font(lv.font_montserrat_14, lv.PART.INDICATOR)

<!-- .. py:method:: set_pos(x, y) -->

        Set the position of the scale.

        :param int x: The x-coordinate of the scale.
        :param int y: The y-coordinate of the scale.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                scale_0.set_pos(100, 100)

<!-- .. py:method:: set_x(x) -->

        Set the x-coordinate of the scale.

        :param int x: The x-coordinate of the scale.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                scale_0.set_x(100)

<!-- .. py:method:: set_y(y) -->

        Set the y-coordinate of the scale.

        :param int y: The y-coordinate of the scale.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                scale_0.set_y(100)

<!-- .. py:method:: set_size(width, height) -->

        Set the size of the scale.

        :param int width: The width of the scale.
        :param int height: The height of the scale.

        MicroPython Code Block:

<!-- .. code-block:: python -->

                scale_0.set_size(100, 50)

<!-- .. py:method:: set_width(width) -->

        Set the width of the scale.

        :param int width: The width of the scale.

        MicroPython Code Block:

<!-- .. code-block:: python -->

                scale_0.set_width(100)

<!-- .. py:method:: set_height(height) -->

        Set the height of the scale.

        :param int height: The height of the scale.

        MicroPython Code Block:

<!-- .. code-block:: python -->

                scale_0.set_height(50)

<!-- .. py:method:: align_to(obj, align, x, y) -->

        Align the scale to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                scale_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
