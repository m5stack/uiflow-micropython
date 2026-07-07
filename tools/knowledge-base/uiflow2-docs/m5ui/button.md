<!-- .. currentmodule:: m5ui -->
<!-- .. _m5ui.M5Button: -->

# M5Button

<!-- .. include:: ../refs/m5ui.button.ref -->

M5Button is a widget that can be used to create buttons in the user interface. It can be used to trigger actions when clicked.

<!-- .. important:: -->

    **Available Fonts**: Only ``lv.font_montserrat_14``, ``lv.font_montserrat_16``, and ``lv.font_montserrat_24`` are available. Other sizes will cause ``AttributeError``.

## UiFlow2 Example

#### event button

Open the |cores3_button_event_example.m5f2| project in UiFlow2.

This example creates a button that triggers an event when clicked.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### event button

This example creates a button that triggers an event when clicked.

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
button0 = None
label0 = None

def button0_pressed_event(event_struct):
    global page0, button0, label0

    label0.set_text(str("pressed"))

def button0_released_event(event_struct):
    global page0, button0, label0

    label0.set_text(str("released"))

def button0_event_handler(event_struct):
    global page0, button0, label0
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button0_pressed_event(event_struct)
    if event == lv.EVENT.RELEASED and True:
        button0_released_event(event_struct)
    return

def setup():
    global page0, button0, label0

    M5.begin()
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    button0 = m5ui.M5Button(
        text="click me",
        x=117,
        y=102,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "label0",
        x=136,
        y=33,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    button0.add_event_cb(button0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()

def loop():
    global page0, button0, label0
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

#### M5Button

## M5Button
Create a button object.

:param str text: The text to display on the button.
:param int x: The x position of the button.
:param int y: The y position of the button.
:param int w: The width of the button. when set to 0, the button will automatically size to fit the text.
:param int h: The height of the button. when set to 0, the button will automatically size to fit the text.
:param int bg_c: The background color of the button in hexadecimal format.
:param int text_c: The text color of the button in hexadecimal format.
:param lv.lv_font_t font: The font to use for the button text.
:param lv.obj parent: The parent object to attach the button to. If not specified, the button will be attached to the default screen.

UiFlow2 Code Block:

    None

MicroPython Code Block:

    .. code-block:: python

        from m5ui import M5Button
        import lvgl as lv

        m5ui.init()
        button_0 = M5Button(text="Click Me", x=10, y=10, bg_c=0x2196F3, text_c=0xFFFFFF, parent=page0)

### `set_btn_text`
Set the text of the button.

:param str text: The text to set on the button.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        button_0.set_btn_text("Click Me")

### `set_style_radius`

### `get_btn_text`
Get the text of the button.

:return: The text of the button.
:rtype: str

UiFlow2 Code Block:

MicroPython Code Block:
    .. code-block:: python

        text = button_0.get_btn_text()

### `set_flag`

### `toggle_flag`

### `set_size`

### `set_height`

### `set_width`

### `set_shadow`

### `unset_shadow`

### `set_pressed_effect`

<!-- .. py:method:: set_flag(flag, value) -->

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.set_flag(lv.obj.FLAG.HIDDEN, True)

<!-- .. py:method:: toggle_flag(flag) -->

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.toggle_flag(lv.obj.FLAG.HIDDEN)

<!-- .. py:method:: set_state(state, value) -->

        Set the state of the button. If ``value`` is True, the state is set; if False, the state is unset.

        :param int state: The state to set.
        :param bool value: If True, the state is set; if False, the state is unset.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.set_state(lv.STATE.PRESSED, True)

<!-- .. py:method:: toggle_state(state) -->

        Toggle the state of the button. If the state is set, it is unset; if not set, it is set.

        :param int state: The state to toggle.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.toggle_state(lv.STATE.PRESSED)

<!-- .. py:method:: set_style_text_font(font, part) -->

        Set the font of the button text.

        :param lv.lv_font_t font: The font to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN | lv.STATE.DEFAULT)

<!-- .. py:method:: set_text_color(color, opa, part) -->

        Set the color of the button text.

        :param int color: The color to set.
        :param int opa: The opacity of the color. The value should be between 0 (transparent) and 255 (opaque).
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)
                button_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.PRESSED)

<!-- .. py:method:: set_bg_color(color, opa, part) -->

        Set the background color of the button.

        :param int color: The color to set.
        :param int opa: The opacity of the color. The value should be between 0 (transparent) and 255 (opaque).
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)
                button_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.PRESSED)

<!-- .. py:method:: set_pos(x, y) -->

        Set the position of the button.

        :param int x: The x-coordinate of the button.
        :param int y: The y-coordinate of the button.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.set_pos(100, 100)

<!-- .. py:method:: set_x(x) -->

        Set the x-coordinate of the button.

        :param int x: The x-coordinate of the button.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.set_x(100)

<!-- .. py:method:: set_y(y) -->

        Set the y-coordinate of the button.

        :param int y: The y-coordinate of the button.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.set_y(100)

<!-- .. py:method:: set_size(width, height) -->

        Set the size of the button.

        :param int width: The width of the button.
        :param int height: The height of the button.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.set_size(100, 50)

<!-- .. py:method:: set_width(width) -->

        Set the width of the button.

        :param int width: The width of the button.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.set_width(100)

<!-- .. py::method:: get_width() -->

        Get the width of the button.

        :return: The width of the button.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.get_width()

<!-- .. py:method:: set_height(height) -->

        Set the height of the button.

        :param int height: The height of the button.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.set_height(50)

<!-- .. py::method:: get_height() -->

        Get the height of the button.

        :return: The height of the button.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.get_height()

<!-- .. py:method:: align_to(obj, align, x, y) -->

        Align the button to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)

<!-- .. py:method:: set_style_radius(radius, part) -->

        Set the corner radius of the button.

        :param int radius: The radius to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)

<!-- .. py:method:: add_event_cb(handler, event, user_data) -->

        Add an event callback to the button. The callback will be called when the specified event occurs.

        :param function handler: The callback function to call.
        :param int event: The event to listen for.
        :param Any user_data: Optional user data to pass to the callback.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                def button_0_pressed_event(event_struct):
                    global button_0
                    button_0.set_bg_color(0x000000, 255, 0)

                def button_0_released_event(event_struct):
                    global button_0
                    button_0.set_bg_color(0xffffff, 255, 0)

                def button_0_clicked_event(event_struct):
                    global button_0
                    button_0.set_bg_color(0x000000, 255, 0)

                def button_0_event_handler(event_struct):
                    global button_0
                    event = event_struct.code
                    if event == lv.EVENT.PRESSED and True:
                        button_0_pressed_event(event_struct)
                    if event == lv.EVENT.RELEASED and True:
                        button_0_released_event(event_struct)
                    if event == lv.EVENT.CLICKED and True:
                        button_0_clicked_event(event_struct)
                    if event == lv.EVENT.LONG_PRESSED and True:
                        button_0_long_pressed_event(event_struct)
                    return

                page_0.add_event_cb(button_0_event_handler, lv.EVENT.ALL, None)
