<!-- .. currentmodule:: m5ui -->
<!-- .. _m5ui.M5Switch: -->

# M5Switch

<!-- .. include:: ../refs/m5ui.switch.ref -->

M5Switch is a widget that can be used to create switch in the user interface. It can be used to trigger actions when checked and uncheked.

## UiFlow2 Example

#### event switch

Open the |cores3_switch_event_example.m5f2| project in UiFlow2.

This example creates a switch that triggers an event when checked and uncheked.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### event switch

This example creates a switch that triggers an event when checked and uncheked.

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

#### M5Switch

## M5Switch
Create a switch object.

:param int x: The x position of the switch.
:param int y: The y position of the switch.
:param int w: The width of the switch.
:param int h: The height of the switch.
:param int bg_c: The color of the switch in the off state in hexadecimal format.
:param int bg_c_checked: The color of the switch in the on state in hexadecimal format.
:param int circle_c: This color refers to the color of the circle on the switch in hexadecimal format.
:param lv.obj parent: The parent object to attach the switch to. If not specified, the switch will be attached to the default screen.

UiFlow2 Code Block:

    None

MicroPython Code Block:

    .. code-block:: python

        from m5ui import M5Switch
        import lvgl as lv

        m5ui.init()
        switch_0 = M5Switch(x=120, y=80, w=60, h=30, bg_c=0xE7E3E7, color=0x2196F3, parent=page0)

### `set_direction`
Set the direction of the switch.

:param int direction: The direction of the switch.

    Options:

        - 0: Horizontal
        - 1: Vertical

UIFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        switch_0.set_direction(0)  # Set to horizontal
        switch_0.set_direction(1)  # Set to vertical

### `set_size`

### `set_style_radius`

<!-- .. py:method:: set_bg_color(color, opa, part) -->

        Set the background color of the switch.

        :param int color: The color to set.
        :param int opa: The opacity of the color. The value should be between 0 (transparent) and 255 (opaque).
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                switch_0.set_bg_color(0xE7E3E7, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
                switch_0.set_bg_color(0x2196F3, 255, lv.PART.INDICATOR | lv.STATE.CHECKED)

<!-- .. py:method:: set_state(state, value) -->

        Set the state of the Switch.

        :param int state: The state to set.
        :param bool value: If True, the state is set; if False, the state is unset.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                switch_0.set_state(lv.STATE.CHECKED, True)

<!-- .. py:method:: has_state(state) -->

        Get the state of the Switch.

        :param int state: The state to get.
        :return: True if the state is set, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                switch_0.has_state(lv.STATE.CHECKED)

<!-- .. py:method:: set_pos(x, y) -->

        Set the position of the switch.

        :param int x: The x-coordinate of the switch.
        :param int y: The y-coordinate of the switch.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                switch_0.set_pos(100, 100)

<!-- .. py:method:: set_x(x) -->

        Set the x-coordinate of the switch.

        :param int x: The x-coordinate of the switch.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                switch_0.set_x(100)

<!-- .. py:method:: set_y(y) -->

        Set the y-coordinate of the switch.

        :param int y: The y-coordinate of the switch.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                switch_0.set_y(100)

<!-- .. py:method:: set_size(width, height) -->

        Set the size of the switch.

        :param int width: The width of the switch.
        :param int height: The height of the switch.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                switch_0.set_size(100, 50)

<!-- .. py:method:: set_width(width) -->

        Set the width of the switch.

        :param int width: The width of the switch.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                switch_0.set_width(100)

<!-- .. py::method:: get_width() -->

        Get the width of the switch.

        :return: The width of the switch.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                switch_0.get_width()

<!-- .. py:method:: set_height(height) -->

        Set the height of the switch.

        :param int height: The height of the switch.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                switch_0.set_height(50)

<!-- .. py::method:: get_height() -->

        Get the height of the switch.

        :return: The height of the switch.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                switch_0.get_height()

<!-- .. py:method:: align_to(obj, align, x, y) -->

        Align the switch to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                switch_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)

<!-- .. py:method:: add_event_cb(handler, event, user_data) -->

        Add an event callback to the switch. The callback will be called when the specified event occurs.

        :param function handler: The callback function to call.
        :param int event: The event to listen for.
        :param Any user_data: Optional user data to pass to the callback.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                def switch0_checked_event(event_struct):
                    global page0, button0
                    print("checked")

                def switch0_unchecked_event(event_struct):
                    global page0, button0
                    print("unchecked")

                def switch0_event_handler(event_struct):
                    global page0, button0
                    event = event_struct.code
                    obj = event_struct.get_target_obj()
                    if event == lv.EVENT.VALUE_CHANGED:
                        if obj.has_state(lv.STATE.CHECKED):
                            switch0_checked_event(event_struct)
                        else:
                            switch0_unchecked_event(event_struct)
                    return

                switch_0.add_event_cb(switch0_event_handler, lv.EVENT.ALL, None)
