<!-- .. currentmodule:: m5ui -->

# M5Window

<!-- .. include:: ../refs/m5ui.win.ref -->

M5Window is a widget that can be used to create windows in the user interface.

## UiFlow2 Example

#### window event

Open the |window_core2_example.m5f2| project in UiFlow2.

This example creates a window and associates it with events.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### window event

This example creates a window and associates it with events.

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
window0 = None
btn_lav = None
title_fmk = None
btn_nzk = None
btn_dkc = None
label_wgy = None

def btn_lav_clicked_event(event_struct):
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy

    label_wgy.set_text(str("Left Btn was clicked"))

def btn_nzk_clicked_event(event_struct):
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy

    label_wgy.set_text(str("Right Btn was clicked"))

def btn_dkc_clicked_event(event_struct):
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy

    window0.set_flag(lv.obj.FLAG.HIDDEN, True)

def btn_lav_event_handler(event_struct):
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_lav_clicked_event(event_struct)
    return

def btn_nzk_event_handler(event_struct):
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_nzk_clicked_event(event_struct)
    return

def btn_dkc_event_handler(event_struct):
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_dkc_clicked_event(event_struct)
    return

def setup():
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    window0 = m5ui.M5Win(x=0, y=0, w=320, h=240, parent=page0)
    btn_lav = window0.add_button(icon=lv.SYMBOL.LEFT, w=40)
    title_fmk = window0.add_title("This is a window")
    btn_nzk = window0.add_button(icon=lv.SYMBOL.RIGHT, w=40)
    btn_dkc = window0.add_button(icon=lv.SYMBOL.CLOSE, w=60)
    label_wgy = window0.add_text("This is label_wgy", x=0, y=0)

    btn_lav.add_event_cb(btn_lav_event_handler, lv.EVENT.ALL, None)
    btn_nzk.add_event_cb(btn_nzk_event_handler, lv.EVENT.ALL, None)
    btn_dkc.add_event_cb(btn_dkc_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()

def loop():
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy
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

#### M5Win

## M5Win
Create a window object.

:param int x: The x position of the window.
:param int y: The y position of the window.
:param int w: The width of the window.
:param int h: The height of the window.
:param lv.obj parent: The parent object to attach the window to. If not specified, the window will be attached to the default screen.

UiFlow2 Code Block:

    None

MicroPython Code Block:

    .. code-block:: python

        from m5ui import M5Win
        import lvgl as lv

        m5ui.init()
        win0 = M5Win(x=120, y=80, w=60, h=30, parent=page0)

### `add_title`
Add a title label to the window.

:param str text: The text to display on the window.
:param int text_c: The text color of the label in hexadecimal format.
:param int text_opa: The text opacity of the label (0-255).
:param int bg_c: The background color of the label in hexadecimal format.
:param int bg_opa: The background opacity of the label (0-255).
:param lv.font font: The font to use for the label.
:return: The created label object :ref:`m5ui.M5Label <m5ui.M5Label>`.
:rtype: lv.obj

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        win0.add_title("A title", text_c=0x212121, text_opa=255, bg_c=0xE0E0E0, bg_opa=255, font=lv.font_montserrat_14)

### `add_text`
Add a text label to the window.

:param str text: The text to display on the window.
:param int x: The x position of the label.
:param int y: The y position of the label.
:param int text_c: The text color of the label in hexadecimal format.
:param int text_opa: The text opacity of the label (0-255).
:param int bg_c: The background color of the label in hexadecimal format.
:param int bg_opa: The background opacity of the label (0-255).
:param lv.font font: The font to use for the label.
:return: The created label object :ref:`m5ui.M5Label <m5ui.M5Label>`.
:rtype: lv.obj

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        win0.add_text("A title", text_c=0x212121, text_opa=255, bg_c=0xF6F6F6, bg_opa=255, font=lv.font_montserrat_14)

### `add_button`
Add a button to the window.

:param int icon: The icon to display on the button.
:param str text: The text to display on the button.
:param int h: The height of the button.
:param int bg_c: The background color of the button in hexadecimal format.
:param int bg_opa: The background opacity of the button (0-255).
:param int text_c: The text color of the button in hexadecimal format.
:param int text_opa: The text opacity of the button (0-255).
:param lv.font font: The font to use for the button text.
:return: The created button object :ref:`m5ui.M5Button <m5ui.M5Button>`.
:rtype: lv.obj

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        win0.add_button(icon=lv.SYMBOL.BULLET, text_c=0xffffff, text_opa=255, bg_c=0x2196f3, bg_opa=255, font=lv.font_montserrat_14)

        win0.add_button(text='M5', text_c=0xffffff, text_opa=255, bg_c=0x2196f3, bg_opa=255, font=lv.font_montserrat_14)

<!-- .. py:method:: delete() -->

        Delete the item from the window.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_0.delete()

                button_0.delete()

                text_0.delete()

<!-- .. py:method:: set_text(txt) -->

        Set text of the window button/label/title.

        :param str txt: The text to set for the window button/label/title.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.set_text("Select an option")

                label_0.set_text("M5Stack")

                title_0.set_text("Hello M5Stack")

<!-- .. py:method:: set_style_text_font(font, part) -->

        Set the font of the window button text.

        :param lv.lv_font_t font: The font to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN | lv.STATE.DEFAULT)

<!-- .. py:method:: set_text_color(color, opa, part) -->

        Set the color of the window button/label/title.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

                label_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

                title_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

<!-- .. py:method:: set_bg_color(color, opa, part) -->

        Set the background color of the window button/label/title.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

                label_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

                title_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

<!-- .. py:method:: set_long_mode(mode) -->

        Set the long mode of the window label/title.

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

                window_0.set_flag(lv.obj.FLAG.HIDDEN, True)

<!-- .. py:method:: set_pos(x, y) -->

        Set the position of the window.

        :param int x: The x-coordinate of the window.
        :param int y: The y-coordinate of the window.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                window_0.set_pos(100, 100)

<!-- .. py:method:: set_x(x) -->

        Set the x-coordinate of the window.

        :param int x: The x-coordinate of the window.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                window_0.set_x(100)

<!-- .. py:method:: set_y(y) -->

        Set the y-coordinate of the window.

        :param int y: The y-coordinate of the window.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                window_0.set_y(100)

<!-- .. py:method:: set_size(width, height) -->

        Set the size of the window.

        :param int width: The width of the window.
        :param int height: The height of the window.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                window_0.set_size(100, 50)

<!-- .. py:method:: align_to(obj, align, x, y) -->

        Align the windowto another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                window_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)

<!-- .. py:method:: set_state(state, value) -->

        Set the state of the bar. If ``value`` is True, the state is set; if False, the state is unset.

        :param int state: The state to set.
        :param bool value: If True, the state is set; if False, the state is unset.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                window_0.set_state(lv.STATE.PRESSED, True)

<!-- .. py:method:: toggle_flag(flag) -->

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                window_0.toggle_flag(lv.obj.FLAG.HIDDEN)

<!-- .. py:method:: set_style_radius(radius, part) -->

        Set the corner radius of the window button.

        :param int radius: The radius to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)

<!-- .. py:method:: set_shadow(color, opa, align, offset_x, offset_y) -->

        Set a shadow for the label/title.

        :param int color: The color of the shadow in hexadecimal format or an integer.
        :param int opa: The opacity of the shadow (0-255).
        :param int align: The alignment of the shadow relative to the label/title.
        :param int offset_x: The horizontal offset of the shadow.
        :param int offset_y: The vertical offset of the shadow.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_0.set_shadow(color=0x000000, opa=128, align=lv.ALIGN.BOTTOM_RIGHT, offset_x=5, offset_y=5)

<!-- .. py:method:: unset_shadow() -->

        Remove the shadow from the label/title.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_0.unset_shadow()

<!-- .. py:method:: get_text() -->

        Get the text of the button/label/title.

        :return: The text of the button/label/title.
        :rtype: str

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.get_text()

                label_0.get_text()

                text_0.get_text()

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
                    global page0, window_0, label_lkg, btn_ono, btn_pjm, label0

                    print('hello M5')

                def btn_ono_event_handler(event_struct):
                    global page0, window_0, label_lkg, btn_ono, btn_pjm, label0
                    event = event_struct.code
                    if event == lv.EVENT.CLICKED and True:
                        btn_ono_clicked_event(event_struct)
                    return

                btn_ono.add_event_cb(btn_ono_event_handler, lv.EVENT.ALL, None)
