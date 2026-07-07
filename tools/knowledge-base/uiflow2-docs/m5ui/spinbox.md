<!-- .. currentmodule:: m5ui -->

# M5Spinbox

<!-- .. include:: ../refs/m5ui.spinbox.ref -->

M5Spinbox is a widget that provides a numeric input interface with increment and decrement buttons.
It displays a numeric value that can be adjusted by clicking the + and - buttons or by typing directly.
The spinbox supports both integer and floating-point numbers with customizable digit count and decimal precision.

## UiFlow2 Example

#### basic spinbox

Open the |cores3_spinbox_basic_example.m5f2| project in UiFlow2.

This example demonstrates how to create a spinbox with customizable range and precision settings.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### basic spinbox

This example demonstrates how to create a spinbox with customizable range and precision settings.

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
spinbox0 = None
label0 = None

def spinbox0_value_changed_event(event_struct):
    global page0, spinbox0, label0
    label0.set_text(str(spinbox0.get_value()))

def spinbox0_event_handler(event_struct):
    global page0, spinbox0, label0
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        spinbox0_value_changed_event(event_struct)
    return

def setup():
    global page0, spinbox0, label0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    spinbox0 = m5ui.M5Spinbox(
        x=60,
        y=100,
        w=200,
        h=40,
        value=50,
        min_value=0,
        max_value=100,
        digit_count=5,
        prec=2,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "label0",
        x=138,
        y=166,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    spinbox0.add_event_cb(spinbox0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    spinbox0.set_border_color(0xFF0000, 255, lv.PART.MAIN | lv.STATE.DEFAULT)

def loop():
    global page0, spinbox0, label0
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

#### M5Spinbox

## M5Spinbox
Create a spinbox widget.

:param int x: The x position of the spinbox.
:param int y: The y position of the spinbox.
:param int w: The width of the spinbox.
:param int h: The height of the spinbox.
:param int value: The initial value of the spinbox.
:param int min_value: The minimum value of the spinbox.
:param int max_value: The maximum value of the spinbox.
:param int digit_count: The number of digits to display.
:param int prec: The number of decimal places.
:param lv.font_t font: The font to use for the spinbox.
:param lv.obj parent: The parent object of the spinbox.

### `set_state`
Set the state of the spinbox. If ``value`` is True, the state is set; if False, the state is unset.

:param int state: The state to set.
:param bool value: If True, the state is set; if False, the state is unset.
:return: None

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        spinbox_0.set_state(lv.STATE.DISABLED, True)

### `toggle_state`
Toggle the state of the spinbox. If the state is set, it is unset; if not set, it is set.

:param int state: The state to toggle.
:return: None

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        spinbox_0.toggle_state(lv.STATE.CHECKED)

### `set_size`
Set the size of the spinbox.

:param int width: The width of the spinbox.
:param int height: The height of the spinbox.
:return: None

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        spinbox_0.set_size(150, 40)

### `set_width`
Set the width of the spinbox.

:param int width: The width of the spinbox.
:return: None

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        spinbox_0.set_width(180)

### `set_height`
Set the height of the spinbox.

:param int height: The height of the spinbox.
:return: None

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        spinbox_0.set_height(50)

### `add_event_cb`
Add an event callback to the spinbox.

:param function handler: The callback function to call.
:param int event: The event to listen for.
:param Any user_data: Optional user data to pass to the callback.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        def spinbox0_value_changed_event(event_struct):
            global page0, spinbox0
            print("value changed:", spinbox0.get_value())

        def spinbox0_event_handler(event_struct):
        global page0, spinbox0
        event = event_struct.code
        if event == lv.EVENT.VALUE_CHANGED and True:
            spinbox0_value_changed_event(event_struct)
        return

        spinbox_0.add_event_cb(spinbox0_event_handler, lv.EVENT.ALL, None)

### `set_bg_color`
Set the background color and opacity for a given part of the object.

:param int color: The color to set, can be an integer (hex) or a lv.color object.
:param int opa: The opacity level (0-255).
:param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
:return: None

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        spinbox0.set_bg_color(0xFF0000, 255, lv.PART.MAIN | lv.STATE.DEFAULT)

### `set_border_color`
Set the border color and opacity for a given part of the object.

:param int color: The color to set, can be an integer (hex) or a lv.color object.
:param int opa: The opacity level (0-255).
:param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
:return: None

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        spinbox0.set_border_color(0xFF0000, 255, lv.PART.MAIN | lv.STATE.DEFAULT)

### `set_style_border_width`
Set the border width of the spinbox.

:param int w: The border width in pixels.
:param int part: The part of the spinbox to apply the border width to, e.g., `lv.PART.MAIN`.
:return: None

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        spinbox0.set_style_border_width(10, lv.PART.MAIN | lv.STATE.DEFAULT)

### `set_style_radius`
Set the radius of the spinbox's corners.

:param radius: The radius of the corners in pixels.
:param part: The part of the spinbox to apply the radius to, e.g., `lv.PART.MAIN`.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        dropdown_0.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)

### `set_digit_format`
Set the digit format of the spinbox.

:param digit_count: The total number of digits in the float representation.
:type digit_count: int
:param sep_pos: The position of the separator.
:type sep_pos: int

### `set_range`
Set the range of the spinbox.

:param min_value: The minimum value of the spinbox.
:type min_value: float | int
:param max_value: The maximum value of the spinbox.
:type max_value: float | int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        spinbox0.set_range(0, 100)

### `set_value`
Set the value of the spinbox.

:param value: The value to set.
:type value: float | int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        spinbox0.set_value(50)

### `get_value`
Get the current value of the spinbox.

:return: The current value.
:rtype: float | int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        spinbox0.get_value()

### `set_step`
Set the step value for the spinbox.

:param step: The step value to set.
:type step: float | int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        spinbox0.set_step(1)
        spinbox0.set_step(0.1)

### `value2raw`
Convert a float to an integer by removing the decimal point.

:param float value: The float value to convert.
:return: The converted integer value.
:rtype: int

### `raw2value`
Convert an integer to a float with a specified decimal point position.

:param int value: The integer value to convert.
:param int digit_count: The total number of digits in the float representation.
:param int sep_pos: The position of the decimal point.
:return: The converted float value.
:rtype: float

<!-- .. py:method:: set_flag(flag, value) -->

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                spinbox_0.set_flag(lv.obj.FLAG.HIDDEN, True)

<!-- .. py:method:: toggle_flag(flag) -->

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                spinbox_0.toggle_flag(lv.obj.FLAG.HIDDEN)

<!-- .. py:method:: set_pos(x, y) -->

        Set the position of the spinbox.

        :param int x: The x-coordinate of the spinbox.
        :param int y: The y-coordinate of the spinbox.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                spinbox_0.set_pos(100, 200)

<!-- .. py:method:: set_x(x) -->

        Set the x-coordinate of the spinbox.

        :param int x: The x-coordinate of the spinbox.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                spinbox_0.set_x(150)

<!-- .. py:method:: set_y(y) -->

        Set the y-coordinate of the spinbox.

        :param int y: The y-coordinate of the spinbox.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                spinbox_0.set_y(250)

<!-- .. py:method:: get_width() -->

        Get the width of the spinbox.

        :return: The width of the spinbox.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                width = spinbox_0.get_width()

<!-- .. py:method:: get_height() -->

        Get the height of the spinbox.

        :return: The height of the spinbox.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                height = spinbox_0.get_height()

<!-- .. py:method:: align_to(obj, align, x, y) -->

        Align the spinbox to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                spinbox_0.align_to(label_0, lv.ALIGN.OUT_BOTTOM_MID, 0, 10)
