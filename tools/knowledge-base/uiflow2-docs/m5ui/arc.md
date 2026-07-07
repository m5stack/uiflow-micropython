<!-- .. currentmodule:: m5ui -->

# M5Arc

<!-- .. include:: ../refs/m5ui.arc.ref -->

M5Arc is a widget that can be used to create arcs in the user interface. It can be used to display circular progress or other circular indicators.

## UiFlow2 Example

#### event arc

Open the |cores3_arc_event_example.m5f2| project in UiFlow2.

This example creates an arc that triggers an event when the value changes.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### event arc

This example creates an arc that triggers an event when the value changes.

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
switch0 = None

def switch0_checked_event(event_struct):
    global page0, switch0

    print("switch0 checked")

def switch0_unchecked_event(event_struct):
    global page0, switch0

    print("switch0 unchecked")

def switch0_event_handler(event_struct):
    global page0, switch0
    event = event_struct.code
    obj = event_struct.get_target_obj()
    if event == lv.EVENT.VALUE_CHANGED:
        if obj.has_state(lv.STATE.CHECKED):
            switch0_checked_event(event_struct)
        else:
            switch0_unchecked_event(event_struct)
    return

def setup():
    global page0, switch0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    switch0 = m5ui.M5Switch(
        x=128,
        y=91,
        w=60,
        h=30,
        bg_c=0xE7E3E7,
        bg_c_checked=0x2196F3,
        circle_c=0xFFFFFF,
        parent=page0,
    )

    switch0.add_event_cb(switch0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    switch0.set_bg_color(0x666666, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    switch0.set_bg_color(0x33FF33, 255, lv.PART.INDICATOR | lv.STATE.CHECKED)

def loop():
    global page0, switch0
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

#### M5Arc

## M5Arc
Create a arc object.

:param int x: The x position of the arc.
:param int y: The y position of the arc.
:param int w: The width of the arc.
:param int h: The height of the arc.
:param int value: The initial value of the arc.
:param int min_value: The minimum value of the arc.
:param int max_value: The maximum value of the arc.
:param int rotation: The rotation of the arc in degrees.
:param int bg_c: The color of the arc in the off state in hexadecimal format.
:param int bg_c_indicator: The color of the arc in the on state in hexadecimal format.
:param int bg_c_knob: The color of the knob on the arc in hexadecimal format.
:param lv.obj parent: The parent object to attach the arc to. If not specified, the arc will be attached to the default screen.

UiFlow2 Code Block:

    None

MicroPython Code Block:

    .. code-block:: python

        from m5ui import M5Arc
        import lvgl as lv

        m5ui.init()
        arc_0 = M5Arc(
            x=0,
            y=0,
            w=100,
            h=100,
            value=10,
            min_value=0,
            max_value=100,
            rotation=0,
            mode=lv.arc.MODE.REVERSE,
            bg_c=0xE7E3E7,
            bg_c_indicator=0x0288FB,
            bg_c_knob=0xE7E3E7,
            parent=page0,
        )

### `set_arc_color`
Set the color of the arc.

:param int color: The color of the arc in hexadecimal format.
:param int opa: The opacity level (0-255).
:param int part: The part of the arc to apply the style to (e.g., lv.PART.MAIN | lv.STATE.DEFAULT).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        label_0.set_arc_color(0x2196F3, lv.PART.MAIN | lv.STATE.DEFAULT)

### `set_range`

### `set_style_radius`

<!-- .. py:method:: set_rotation(rotation) -->

        Set the rotation of the arc.

        :param int rotation: The rotation angle of the arc in degrees.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                arc_0.set_rotation(90)

<!-- .. py:method:: set_value(value) -->

        Set the value of the arc.

        :param int value: The value of the arc.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                arc_0.set_value(90)

<!-- .. py:method:: get_value() -->

        Get the value of the arc.

        :return: The value of the arc.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                arc_0.get_value()

<!-- .. py:method:: set_range() -->

        Set the range of the arc.

        :param int min: The minimum value of the arc.
        :param int max: The maximum value of the arc.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                arc_0.set_range(0, 100)

<!-- .. py:method:: set_mode() -->

        Set the mode of the arc.

        :param int mode: The mode of the arc.

            Option:
                - lv.arc.MODE.NORMAL: Normal mode.
                - lv.arc.MODE.REVERSE: Reverse mode.
                - lv.arc.MODE.SYMMETRICAL: Symmetrical mode.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                arc_0.set_mode(lv.ARC.MODE.NORMAL)

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

        Set the position of the arc.

        :param int x: The x-coordinate of the arc.
        :param int y: The y-coordinate of the arc.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                arc_0.set_pos(100, 100)

<!-- .. py:method:: set_x(x) -->

        Set the x-coordinate of the arc.

        :param int x: The x-coordinate of the arc.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                arc_0.set_x(100)

<!-- .. py:method:: set_y(y) -->

        Set the y-coordinate of the arc.

        :param int y: The y-coordinate of the arc.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                arc_0.set_y(100)

<!-- .. py:method:: set_size(width, height) -->

        Set the size of the arc.

        :param int width: The width of the arc.
        :param int height: The height of the arc.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                arc_0.set_size(100, 50)

<!-- .. py:method:: align_to(obj, align, x, y) -->

        Align the arc to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                arc_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)

<!-- .. py:method:: add_event_cb(handler, event, user_data) -->

        Add an event callback to the arc. The callback will be called when the specified event occurs.

        :param function handler: The callback function to call.
        :param int event: The event to listen for.
        :param Any user_data: Optional user data to pass to the callback.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                def value_changed_event(event_struct):
                    global page0, arc_0
                    print("value changed:", arc_0.get_value())

                arc_0.add_event_cb(value_changed_event, lv.EVENT.VALUE_CHANGED, None)
