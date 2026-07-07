<!-- .. currentmodule:: m5ui -->

# M5Msgbox

<!-- .. include:: ../refs/m5ui.msgbox.ref -->

M5Msgbox is a widget that can be used to create msgboxes in the user interface.

## UiFlow2 Example

#### msgbox event

Open the |msgbox_core2_example.m5f2| project in UiFlow2.

This example creates msgbox and associated with events.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### msgbox event

This example creates msgbox and associated with events.

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
msgbox0 = None
label_sfu = None
btn_apply = None
btn_cancel = None

import random

def btn_apply_clicked_event(event_struct):
    global page0, msgbox0, label_sfu, btn_apply, btn_cancel

    label_sfu.set_text(str((str("Hello ") + str((random.randint(1, 100))))))

def btn_cancel_clicked_event(event_struct):
    global page0, msgbox0, label_sfu, btn_apply, btn_cancel

    btn_apply.toggle_flag(lv.obj.FLAG.HIDDEN)

def btn_apply_event_handler(event_struct):
    global page0, msgbox0, label_sfu, btn_apply, btn_cancel
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_apply_clicked_event(event_struct)
    return

def btn_cancel_event_handler(event_struct):
    global page0, msgbox0, label_sfu, btn_apply, btn_cancel
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_cancel_clicked_event(event_struct)
    return

def setup():
    global page0, msgbox0, label_sfu, btn_apply, btn_cancel

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    msgbox0 = m5ui.M5Msgbox(title="Message Box", x=0, y=0, w=320, h=240, parent=page0)
    label_sfu = msgbox0.add_text("This is label_sfu")
    btn_apply = msgbox0.add_button(text="Apply", option="footer")
    btn_cancel = msgbox0.add_button(text="Cancel", option="footer")
    msgbox0.add_close_button()

    btn_apply.add_event_cb(btn_apply_event_handler, lv.EVENT.ALL, None)
    btn_cancel.add_event_cb(btn_cancel_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()

def loop():
    global page0, msgbox0, label_sfu, btn_apply, btn_cancel
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

#### M5Msgbox

## M5Msgbox
Create a msgbox object.

:param str title: The title of the msgbox.
:param int x: The x-coordinate of the msgbox.
:param int y: The y-coordinate of the msgbox.
:param int w: The width of the msgbox.
:param int h: The height of the msgbox.
:param lv.obj parent: The parent object to attach the msgbox to. If not specified, the msgbox will be attached to the default screen.

MicroPython Code Block:

    .. code-block:: python

        from m5ui import M5Msgbox
        import lvgl as lv

        m5ui.init()
        msgbox_0 = M5Msgbox(
            title="msgbox",
            x=0,
            y=0,
            w=320,
            h=240,
            parent=page0,
        )

### `add_text`
Add a text label to the msgbox.

:param str text: The text to display.
:param int text_c: The text color in hexadecimal format.
:param int text_opa: The text opacity (0-255).
:param int bg_c: The background color in hexadecimal format.
:param int bg_opa: The background opacity (0-255).
:param lv.font font: The font to use for the text.

:return: The created label object.
:rtype: m5ui.M5Label

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        text0 = msgbox_0.add_text(
            text="Hello World",
            text_c=0x212121,
            text_opa=255,
            bg_c=0xFFFFFF,
            bg_opa=255,
            font=lv.font_montserrat_14,
        )

### `add_button`
Add a button to the msgbox.

:param str icon: The icon to display on the button.
:param str text: The text to display on the button.
:param int bg_c: The background color in hexadecimal format.
:param int bg_opa: The background opacity (0-255).
:param int text_c: The text color in hexadecimal format.
:param int text_opa: The text opacity (0-255).
:param lv.font font: The font to use for the button text.
:param str option: The position of the button ("header" or "footer").

:return: The created button object.
:rtype: m5ui.M5Button

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        button0 = msgbox_0.add_button(
            icon=None,
            text="OK",
            bg_c=0x2196F3,
            bg_opa=255,
            text_c=0xFFFFFF,
            text_opa=255,
            font=lv.font_montserrat_14,
            option="footer",
        )

<!-- .. py:method:: add_close_button() -->

        Add a close button to the msgboxheader.

        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                msgbox_0.add_close_button()

<!-- .. py:method:: delete() -->

        Delete the item from the msgbox.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.delete()
                text_0.delete()

<!-- .. py:method:: set_text(txt) -->

        Set text of the msgbox button/label.

        :param str txt: The text to set for the msgbox button/label.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.set_text("Select an option")

                label_0.set_text("M5Stack")

<!-- .. py:method:: set_style_text_font(font, part) -->

        Set the font of the msgbox button/label text.

        :param lv.lv_font_t font: The font to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN | lv.STATE.DEFAULT)

                button_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN | lv.STATE.DEFAULT)

<!-- .. py:method:: set_text_color(color, opa, part) -->

        Set the color of the msgbox button/label.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

                label_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

<!-- .. py:method:: set_bg_color(color, opa, part) -->

        Set the background color of the msgbox label.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

                label_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

<!-- .. py:method:: set_long_mode(mode) -->

        Set the long mode of the msgbox label.

        :param int mode: The long mode to set.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_0.set_long_mode(lv.label.LONG_MODE.WRAP)

<!-- .. py:method:: set_flag(flag, value) -->

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                msgbox_0.set_flag(lv.obj.FLAG.HIDDEN, True)

<!-- .. py:method:: set_pos(x, y) -->

        Set the position of the msgbox.

        :param int x: The x-coordinate of the msgbox.
        :param int y: The y-coordinate of the msgbox.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                msgbox_0.set_pos(100, 100)

<!-- .. py:method:: set_x(x) -->

        Set the x-coordinate of the msgbox.

        :param int x: The x-coordinate of the msgbox.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                msgbox_0.set_x(100)

<!-- .. py:method:: set_y(y) -->

        Set the y-coordinate of the msgbox.

        :param int y: The y-coordinate of the msgbox.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                msgbox_0.set_y(100)

<!-- .. py:method:: set_size(width, height) -->

        Set the size of the msgbox.

        :param int width: The width of the msgbox.
        :param int height: The height of the msgbox.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                msgbox_0.set_size(100, 50)

<!-- .. py:method:: align_to(obj, align, x, y) -->

        Align the msgboxto another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                msgbox_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)

<!-- .. py:method:: set_state(state, value) -->

        Set the state of the bar. If ``value`` is True, the state is set; if False, the state is unset.

        :param int state: The state to set.
        :param bool value: If True, the state is set; if False, the state is unset.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                msgbox_0.set_state(lv.STATE.PRESSED, True)

<!-- .. py:method:: toggle_flag(flag) -->

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                msgbox_0.toggle_flag(lv.obj.FLAG.HIDDEN)

<!-- .. py:method:: set_style_radius(radius, part) -->

        Set the corner radius of the msgbox button.

        :param int radius: The radius to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)

<!-- .. py:method:: set_shadow(color, opa, align, offset_x, offset_y) -->

        Set a shadow for the label.

        :param int color: The color of the shadow in hexadecimal format or an integer.
        :param int opa: The opacity of the shadow (0-255).
        :param int align: The alignment of the shadow relative to the label.
        :param int offset_x: The horizontal offset of the shadow.
        :param int offset_y: The vertical offset of the shadow.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_0.set_shadow(color=0x000000, opa=128, align=lv.ALIGN.BOTTOM_RIGHT, offset_x=5, offset_y=5)

<!-- .. py:method:: unset_shadow() -->

        Remove the shadow from the label.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_0.unset_shadow()

<!-- .. py:method:: get_text() -->

        Get the text of the label.

        :return: The text of the label.
        :rtype: str

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_0.get_text()
                button_0.get_text()

<!-- .. py:method:: toggle_state(state) -->

        Toggle the state of the button. If the state is set, it is unset; if not set, it is set.

        :param int state: The state to toggle.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.toggle_state(lv.STATE.PRESSED)

<!-- .. py:method:: add_event_cb(handler, event, user_data) -->

        Add an event callback to the button. The callback will be called when the specified event occurs.

        :param function handler: The callback function to call.
        :param int event: The event to listen for.
        :param Any user_data: Optional user data to pass to the callback.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                def btn_ono_clicked_event(event_struct):
                    global page0, msgbox_0, label_lkg, btn_ono, btn_pjm, label0

                    print('hello M5')

                def btn_ono_event_handler(event_struct):
                    global page0, msgbox_0, label_lkg, btn_ono, btn_pjm, label0
                    event = event_struct.code
                    if event == lv.EVENT.CLICKED and True:
                        btn_ono_clicked_event(event_struct)
                    return

                btn_ono.add_event_cb(btn_ono_event_handler, lv.EVENT.ALL, None)
