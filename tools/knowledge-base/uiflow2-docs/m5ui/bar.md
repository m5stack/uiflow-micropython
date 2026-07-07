<!-- .. currentmodule:: m5ui -->

# M5Bar

<!-- .. include:: ../refs/m5ui.bar.ref -->

M5Bar is a widget that can be used to create progress bars in the user interface. It displays values within a specified range using a visual bar indicator. The bar can be customized with different colors, gradients, and can optionally display the current value as text.

## UiFlow2 Example

#### Temperature meter

Open the |cores3_temperature_meter_example.m5f2| project in UiFlow2.

This example demonstrates how to create a temperature meter that shows the current temperature.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Temperature meter

This example demonstrates how to create a temperature meter that shows the current temperature.

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
from hardware import I2C
from hardware import Pin
from unit import ENVPROUnit
import time

page0 = None
bar0 = None
label0 = None
i2c0 = None
envpro_0 = None

def setup():
    global page0, bar0, label0, i2c0, envpro_0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    bar0 = m5ui.M5Bar(
        x=148,
        y=21,
        w=20,
        h=200,
        min_value=0,
        max_value=50,
        value=25,
        bg_c=0x2193F3,
        color=0x2193F3,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "label0",
        x=181,
        y=112,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    envpro_0 = ENVPROUnit(i2c0)
    page0.screen_load()
    bar0.set_bg_grad_color(
        0xFF0000, 255, 0x0000FF, 255, lv.GRAD_DIR.VER, lv.PART.INDICATOR | lv.STATE.DEFAULT
    )

def loop():
    global page0, bar0, label0, i2c0, envpro_0
    M5.update()
    bar0.set_value(int(envpro_0.get_temperature()), True)
    label0.set_text(str(envpro_0.get_temperature()))
    time.sleep(1)

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

#### M5Bar

## M5Bar
Initialize a new M5Bar widget.

:param int x: The x-coordinate of the bar.
:param int y: The y-coordinate of the bar.
:param int w: The width of the bar.
:param int h: The height of the bar.
:param int min_value: The minimum value of the bar range.
:param int max_value: The maximum value of the bar range.
:param int value: The initial value of the bar.
:param bool is_show_value: Whether to display the current value as text.
:param int bg_c: The background color of the bar.
:param int color: The indicator color of the bar.
:param lv.obj parent: The parent object. If None, uses the active screen.
:return: None

UiFlow2 Code Block:

    None

MicroPython Code Block:

    .. code-block:: python

        bar = M5Bar(x=50, y=50, w=200, h=30, min_value=0, max_value=100, value=50)

### `set_value`
Set the current value of the bar.

:param int value: The value to set.
:param bool anim_enable: Whether to enable animation when changing the value.
:return: None

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        bar.set_value(75, True)

### `set_range`
Set the value range of the bar.

:param int min_value: The minimum value.
:param int max_value: The maximum value.
:return: None

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        bar.set_range(0, 200)

### `set_style_radius`

<!-- .. py:method:: get_value() -->

        Get the current value of the bar.

        :return: The current value of the bar.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                current_value = bar.get_value()

<!-- .. py:method:: get_min_value() -->

        Get the minimum value of the bar range.

        :return: The minimum value.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                min_val = bar.get_min_value()

<!-- .. py:method:: get_max_value() -->

        Get the maximum value of the bar range.

        :return: The maximum value.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                max_val = bar.get_max_value()

<!-- .. py:method:: set_flag(flag, value) -->

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                bar.set_flag(lv.obj.FLAG.HIDDEN, True)

<!-- .. py:method:: toggle_flag(flag) -->

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                bar.toggle_flag(lv.obj.FLAG.HIDDEN)

<!-- .. py:method:: set_state(state, value) -->

        Set the state of the bar. If ``value`` is True, the state is set; if False, the state is unset.

        :param int state: The state to set.
        :param bool value: If True, the state is set; if False, the state is unset.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                bar.set_state(lv.STATE.PRESSED, True)

<!-- .. py:method:: toggle_state(state) -->

        Toggle the state of the bar. If the state is set, it is unset; if not set, it is set.

        :param int state: The state to toggle.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                bar.toggle_state(lv.STATE.PRESSED)

<!-- .. py:method:: set_bg_color(color, opa, part) -->

        Set the background color of the bar.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                bar.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

                bar.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.INDICATOR | lv.STATE.DEFAULT)

<!-- .. py:method:: set_bg_grad_color(color, opa, grad_color, grad_opd, grad_dir, part) -->

        Set the background gradient color of the bar.

        :param int color: The start color of the gradient, can be an integer (RGB).
        :param int opa: The opacity of the start color (0-255).
        :param int grad_color: The end color of the gradient, can be an integer (RGB).
        :param int grad_opd: The opacity of the end color (0-255).
        :param int grad_dir: The direction of the gradient (e.g., lv.GRAD_DIR.VER).
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                bar.set_bg_grad_color(0x00FF00, 255, 0xFF0000, 255, lv.GRAD_DIR.HOR, lv.PART.MAIN | lv.STATE.DEFAULT)
                bar.set_bg_grad_color(0x00FF00, 255, 0xFF0000, 255, lv.GRAD_DIR.HOR, lv.PART.INDICATOR | lv.STATE.DEFAULT)

<!-- .. py:method:: set_pos(x, y) -->

        Set the position of the bar.

        :param int x: The x-coordinate of the bar.
        :param int y: The y-coordinate of the bar.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                bar.set_pos(100, 100)

<!-- .. py:method:: set_x(x) -->

        Set the x-coordinate of the bar.

        :param int x: The x-coordinate of the bar.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                bar.set_x(100)

<!-- .. py:method:: set_y(y) -->

        Set the y-coordinate of the bar.

        :param int y: The y-coordinate of the bar.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                bar.set_y(100)

<!-- .. py:method:: set_size(width, height) -->

        Set the size of the bar.

        :param int width: The width of the bar.
        :param int height: The height of the bar.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                bar.set_size(200, 30)

<!-- .. py:method:: set_width(width) -->

        Set the width of the bar.

        :param int width: The width of the bar.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                bar.set_width(200)

<!-- .. py:method:: get_width() -->

        Get the width of the bar.

        :return: The width of the bar.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                width = bar.get_width()

<!-- .. py:method:: set_height(height) -->

        Set the height of the bar.

        :param int height: The height of the bar.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                bar.set_height(30)

<!-- .. py:method:: get_height() -->

        Get the height of the bar.

        :return: The height of the bar.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                height = bar.get_height()

<!-- .. py:method:: align_to(obj, align, x, y) -->

        Align the bar to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                bar.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
