<!-- .. currentmodule:: m5ui -->

# M5Checkbox

<!-- .. include:: ../refs/m5ui.checkbox.ref -->

M5Checkbox is a widget that can be used to create checkboxes in the user interface. It can be used to allow users to select or deselect options with a visual indicator.

## UiFlow2 Example

#### basic checkbox

Open the |cores3_checkbox_basic_example.m5f2| project in UiFlow2.

This example creates a basic checkbox that can be checked and unchecked.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### basic checkbox

This example creates a basic checkbox that can be checked and unchecked.

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
checkbox0 = None
checkbox1 = None
label0 = None

def checkbox0_checked_event(event_struct):
    global page0, checkbox0, checkbox1, label0
    label0.set_text(str("checked"))

def checkbox0_unchecked_event(event_struct):
    global page0, checkbox0, checkbox1, label0
    label0.set_text(str("unchecked"))

def checkbox0_event_handler(event_struct):
    global page0, checkbox0, checkbox1, label0
    event = event_struct.code
    obj = event_struct.get_target_obj()
    if event == lv.EVENT.VALUE_CHANGED:
        if obj.has_state(lv.STATE.CHECKED):
            checkbox0_checked_event(event_struct)
        else:
            checkbox0_unchecked_event(event_struct)
    return

def setup():
    global page0, checkbox0, checkbox1, label0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    checkbox0 = m5ui.M5Checkbox(
        title="checkbox0",
        value=False,
        x=77,
        y=106,
        title_c=0x212121,
        title_font=lv.font_montserrat_24,
        bullet_border_c=0x2193F3,
        bullet_bg_c=0xFFFFFF,
        parent=page0,
    )
    checkbox1 = m5ui.M5Checkbox(
        title="checkbox1",
        value=False,
        x=80,
        y=54,
        title_c=0x212121,
        title_font=lv.font_montserrat_24,
        bullet_border_c=0x2193F3,
        bullet_bg_c=0xFFFFFF,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "label0",
        x=124,
        y=153,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    checkbox0.add_event_cb(checkbox0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    checkbox1.set_state(lv.STATE.DISABLED, True)
    checkbox1.set_state(lv.STATE.CHECKED, True)

def loop():
    global page0, checkbox0, checkbox1, label0
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

#### M5Checkbox

## M5Checkbox
Create a checkbox object.

:param str title: The title text of the checkbox.
:param bool value: The initial checked state of the checkbox.
:param int x: The x position of the checkbox.
:param int y: The y position of the checkbox.
:param int title_c: The color of the title text in hexadecimal format.
:param lv.lv_font_t title_font: The font to use for the title text.
:param int bullet_border_c: The border color of the checkbox bullet in hexadecimal format.
:param int bullet_bg_c: The background color of the checkbox bullet in hexadecimal format.
:param lv.obj parent: The parent object to attach the checkbox to. If not specified, the checkbox will be attached to the default screen.

UiFlow2 Code Block:

    None

MicroPython Code Block:

    .. code-block:: python

        from m5ui import M5Checkbox
        import lvgl as lv
        m5ui.init()
        checkbox_0 = M5Checkbox(title="Check Me", value=True, x=10, y=10, title_c=0x2121, title_font=lv.font_montserrat_14, bullet_border_c=0x2196F3, bullet_bg_c=0xFFFFFF, parent=page0)

### `set_style_radius`

<!-- .. py:method:: set_flag(flag, value) -->

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                checkbox_0.set_flag(lv.obj.FLAG.HIDDEN, True)

<!-- .. py:method:: toggle_flag(flag) -->

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                checkbox_0.toggle_flag(lv.obj.FLAG.HIDDEN)

<!-- .. py:method:: set_state(state, value) -->

        Set the state of the checkbox. If ``value`` is True, the state is set; if False, the state is unset.

        :param int state: The state to set.
        :param bool value: If True, the state is set; if False, the state is unset.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                checkbox_0.set_state(lv.STATE.CHECKED, True)

<!-- .. py:method:: toggle_state(state) -->

        Toggle the state of the checkbox. If the state is set, it is unset; if not set, it is set.

        :param int state: The state to toggle.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                checkbox_0.toggle_state(lv.STATE.CHECKED)

<!-- .. py:method:: set_style_text_font(font, part) -->

        Set the font of the checkbox text.

        :param lv.lv_font_t font: The font to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                checkbox_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN | lv.STATE.DEFAULT)

<!-- .. py:method:: set_text_color(color, opa, part) -->

        Set the color of the checkbox text.

        :param int color: The color to set.
        :param int opa: The opacity of the color. The value should be between 0 (transparent) and 255 (opaque).
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                checkbox_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)
                checkbox_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.CHECKED)

<!-- .. py:method:: set_bg_color(color, opa, part) -->

        Set the background color of the checkbox indicator.

        :param int color: The color to set.
        :param int opa: The opacity of the color. The value should be between 0 (transparent) and 255 (opaque).
        :param int part: The part of the object to apply the style to (e.g., lv.PART.INDICATOR).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                checkbox_0.set_bg_color(lv.color_hex(0xFFFFFF), 255, lv.PART.INDICATOR | lv.STATE.DEFAULT)
                checkbox_0.set_bg_color(lv.color_hex(0x2196F3), 255, lv.PART.INDICATOR | lv.STATE.CHECKED)

<!-- .. py:method:: set_border_color(color, opa, part) -->

        Set the border color of the checkbox indicator.

        :param int color: The color to set.
        :param int opa: The opacity of the color. The value should be between 0 (transparent) and 255 (opaque).
        :param int part: The part of the object to apply the style to (e.g., lv.PART.INDICATOR).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                checkbox_0.set_border_color(lv.color_hex(0x2196F3), 255, lv.PART.INDICATOR | lv.STATE.DEFAULT)

<!-- .. py:method:: set_pos(x, y) -->

        Set the position of the checkbox.

        :param int x: The x-coordinate of the checkbox.
        :param int y: The y-coordinate of the checkbox.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                checkbox_0.set_pos(100, 100)

<!-- .. py:method:: set_x(x) -->

        Set the x-coordinate of the checkbox.

        :param int x: The x-coordinate of the checkbox.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                checkbox_0.set_x(100)

<!-- .. py:method:: set_y(y) -->

        Set the y-coordinate of the checkbox.

        :param int y: The y-coordinate of the checkbox.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                checkbox_0.set_y(100)

<!-- .. py:method:: set_size(width, height) -->

        Set the size of the checkbox.

        :param int width: The width of the checkbox.
        :param int height: The height of the checkbox.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                checkbox_0.set_size(100, 50)

<!-- .. py:method:: set_width(width) -->

        Set the width of the checkbox.

        :param int width: The width of the checkbox.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                checkbox_0.set_width(100)

<!-- .. py:method:: get_width() -->

        Get the width of the checkbox.

        :return: The width of the checkbox.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                checkbox_0.get_width()

<!-- .. py:method:: set_height(height) -->

        Set the height of the checkbox.

        :param int height: The height of the checkbox.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                checkbox_0.set_height(50)

<!-- .. py:method:: get_height() -->

        Get the height of the checkbox.

        :return: The height of the checkbox.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                checkbox_0.get_height()

<!-- .. py:method:: align_to(obj, align, x, y) -->

        Align the checkbox to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                checkbox_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)

<!-- .. py:method:: set_style_radius(radius, part) -->

        Set the corner radius of the checkbox indicator.

        :param int radius: The radius to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.INDICATOR).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                checkbox_0.set_style_radius(10, lv.PART.INDICATOR | lv.STATE.DEFAULT)

<!-- .. py:method:: set_text(text) -->

        Set the text of the checkbox.

        :param str text: The text to set.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                checkbox_0.set_text("Checkbox")

<!-- .. py:method:: get_text() -->

        Get the text of the checkbox.

        :return: The text of the checkbox.
        :rtype: str

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                checkbox_0.get_text()

<!-- .. py:method:: add_event_cb(handler, event, user_data) -->

        Add an event callback to the checkbox. The callback will be called when the specified event occurs.

        :param function handler: The callback function to call.
        :param int event: The event to listen for.
        :param Any user_data: Optional user data to pass to the callback.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                def checkbox_0_checked_event(event_struct):
                    global checkbox_0
                    print("Checkbox checked!")

                def checkbox_0_unchecked_event(event_struct):
                    global checkbox_0
                    print("Checkbox unchecked!")

                def checkbox_0_event_handler(event_struct):
                    global checkbox_0
                    event = event_struct.code
                    if event == lv.EVENT.VALUE_CHANGED and checkbox_0.has_state(lv.STATE.CHECKED):
                        checkbox_0_checked_event(event_struct)
                    elif event == lv.EVENT.VALUE_CHANGED and not checkbox_0.has_state(lv.STATE.CHECKED):
                        checkbox_0_unchecked_event(event_struct)
                    return

                checkbox_0.add_event_cb(checkbox_0_event_handler, lv.EVENT.ALL, None)
