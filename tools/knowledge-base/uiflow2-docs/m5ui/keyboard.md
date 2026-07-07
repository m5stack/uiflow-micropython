<!-- .. currentmodule:: m5ui -->

# M5Keyboard

<!-- .. include:: ../refs/m5ui.keyboard.ref -->

M5Keyboard is a widget that can be used to create virtual keyboards in the user interface. It provides an on-screen keyboard that can be used for text input with support for different keyboard modes and layouts.

## UiFlow2 Example

#### basic keyboard

Open the |cores3_keyboard_basic_example.m5f2| project in UiFlow2.

This example demonstrates how to create a virtual keyboard and connect it to a text input area.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### basic keyboard

This example demonstrates how to create a virtual keyboard and connect it to a text input area.

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
textarea0 = None
keyboard0 = None

def textarea0_focused_event(event_struct):
    global page0, textarea0, keyboard0
    keyboard0.set_flag(lv.obj.FLAG.HIDDEN, False)

def textarea0_defocused_event(event_struct):
    global page0, textarea0, keyboard0
    keyboard0.set_flag(lv.obj.FLAG.HIDDEN, True)

def textarea0_event_handler(event_struct):
    global page0, textarea0, keyboard0
    event = event_struct.code
    if event == lv.EVENT.FOCUSED and True:
        textarea0_focused_event(event_struct)
    if event == lv.EVENT.DEFOCUSED and True:
        textarea0_defocused_event(event_struct)
    return

def setup():
    global page0, textarea0, keyboard0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    textarea0 = m5ui.M5TextArea(
        text="textarea0",
        placeholder="Placeholder...",
        x=10,
        y=30,
        w=300,
        h=70,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    keyboard0 = m5ui.M5Keyboard(
        x=0,
        y=120,
        w=320,
        h=120,
        mode=lv.keyboard.MODE.TEXT_LOWER,
        target_textarea=textarea0,
        parent=page0,
    )

    textarea0.add_event_cb(textarea0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()

def loop():
    global page0, textarea0, keyboard0
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

#### M5Keyboard

## M5Keyboard
Create a keyboard widget.

:param int x: The x position of the keyboard.
:param int y: The y position of the keyboard.
:param int w: The width of the keyboard.
:param int h: The height of the keyboard.
:param int mode: The keyboard mode, default is `lv.keyboard.MODE.TEXT_LOWER`.
:param lv.obj target_textarea: The target textarea to link with the keyboard.
:param lv.obj parent: The parent object, default is the active screen.

UiFlow2 Code Block:

    None

MicroPython Code Block:

    .. code-block:: python

        import m5ui
        import lvgl as lv

        m5ui.init()
        keyboard = m5ui.M5Keyboard(x=0, y=120, w=320, h=100, target_textarea=None, parent=page0)

<!-- .. py:method:: set_flag(flag, value) -->

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                keyboard_0.set_flag(lv.obj.FLAG.HIDDEN, True)

<!-- .. py:method:: toggle_flag(flag) -->

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                keyboard_0.toggle_flag(lv.obj.FLAG.HIDDEN)

<!-- .. py:method:: set_state(state, value) -->

        Set the state of the keyboard. If ``value`` is True, the state is set; if False, the state is unset.

        :param int state: The state to set.
        :param bool value: If True, the state is set; if False, the state is unset.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                keyboard_0.set_state(lv.STATE.PRESSED, True)

<!-- .. py:method:: toggle_state(state) -->

        Toggle the state of the keyboard. If the state is set, it is unset; if not set, it is set.

        :param int state: The state to toggle.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                keyboard_0.toggle_state(lv.STATE.PRESSED)

<!-- .. py:method:: add_event_cb(handler, event, user_data) -->

        Add an event callback to the keyboard. The callback will be called when the specified event occurs.

        :param function handler: The callback function to call.
        :param int event: The event to listen for.
        :param Any user_data: Optional user data to pass to the callback.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                def keyboard_0_value_changed_event(event_struct):
                    global page0, textarea0
                    print("Key pressed")

                def keyboard_0_ready_event(event_struct):
                    global page0, textarea0
                    print("Ready")

                def keyboard_0_event_handler(event_struct):
                    event = event_struct.code
                    if event == lv.EVENT.VALUE_CHANGED:
                        keyboard_0_value_changed_event(event_struct)
                    elif event == lv.EVENT.READY:
                        keyboard_0_ready_event(event_struct)
                    return

                keyboard_0.add_event_cb(keyboard_0_event_handler, lv.EVENT.ALL, None)

<!-- .. py:method:: set_textarea(textarea) -->

        Set the text area that this keyboard should control. When keys are pressed, the text will be entered into the specified text area.

        :param lv.textarea textarea: The text area object to connect to the keyboard.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                keyboard_0.set_textarea(textarea_0)

<!-- .. py:method:: get_textarea() -->

        Get the text area that is currently connected to this keyboard.

        :return: The connected text area object, or None if no text area is connected.
        :rtype: lv.textarea or None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                ta = keyboard_0.get_textarea()

<!-- .. py:method:: set_mode(mode) -->

        Set the keyboard mode to display different keyboard layouts.

        :param int mode: The keyboard mode to set.
        :return: None

        Available modes include:

            - lv.keyboard.MODE.TEXT_LOWER: 0.
            - lv.keyboard.MODE.TEXT_UPPER: 1.
            - lv.keyboard.MODE.SYMBOL: 2.
            - lv.keyboard.MODE.NUMBER: 3.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                keyboard_0.set_mode(lv.keyboard.MODE.TEXT_LOWER)

<!-- .. py:method:: get_mode() -->

        Get the current keyboard mode.

        :return: The current keyboard mode.
        :rtype: int

        Keyboard modes include:

            - lv.keyboard.MODE.TEXT_LOWER: 0.
            - lv.keyboard.MODE.TEXT_UPPER: 1.
            - lv.keyboard.MODE.SYMBOL: 2.
            - lv.keyboard.MODE.NUMBER: 3.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                mode = keyboard_0.get_mode()

<!-- .. py:method:: set_popovers(en) -->

        Enable or disable popovers for the keyboard. Popovers are additional UI elements that can be displayed when certain keys are pressed.

        :param bool en: If True, popovers are enabled; if False, they are disabled.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                keyboard_0.set_popovers(True)

<!-- .. py:method:: get_selected_button() -->

        Get the index of the last released button. This can be useful to determine which key was last pressed.

        :return: index of the last released button.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                btn = keyboard_0.get_selected_button()

<!-- .. py:method:: get_button_text(btn_id) -->

        Get the text of a button by its index.

        :param int btn: The index of the button.
        :return: The text of the button.
        :rtype: str

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                keyboard_0.get_button_text(3)

<!-- .. py:method:: set_pos(x, y) -->

        Set the position of the keyboard.

        :param int x: The x-coordinate of the keyboard.
        :param int y: The y-coordinate of the keyboard.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                keyboard_0.set_pos(100, 100)

<!-- .. py:method:: set_x(x) -->

        Set the x-coordinate of the keyboard.

        :param int x: The x-coordinate of the keyboard.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                keyboard_0.set_x(100)

<!-- .. py:method:: set_y(y) -->

        Set the y-coordinate of the keyboard.

        :param int y: The y-coordinate of the keyboard.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                keyboard_0.set_y(100)

<!-- .. py:method:: set_size(width, height) -->

        Set the size of the keyboard.

        :param int width: The width of the keyboard.
        :param int height: The height of the keyboard.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                keyboard_0.set_size(300, 200)

<!-- .. py:method:: set_width(width) -->

        Set the width of the keyboard.

        :param int width: The width of the keyboard.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                keyboard_0.set_width(300)

<!-- .. py:method:: get_width() -->

        Get the width of the keyboard.

        :return: The width of the keyboard.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                width = keyboard_0.get_width()

<!-- .. py:method:: set_height(height) -->

        Set the height of the keyboard.

        :param int height: The height of the keyboard.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                keyboard_0.set_height(200)

<!-- .. py:method:: get_height() -->

        Get the height of the keyboard.

        :return: The height of the keyboard.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                height = keyboard_0.get_height()

<!-- .. py:method:: align_to(obj, align, x, y) -->

        Align the keyboard to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                keyboard_0.align_to(page_0, lv.ALIGN.BOTTOM_MID, 0, -10)
