<!-- .. currentmodule:: m5ui -->

# M5ButtonMatrix

<!-- .. include:: ../refs/m5ui.buttonmatrix.ref -->

M5ButtonMatrix is a widget that can be used to create a matrix of buttons in the
user interface. It provides a flexible layout for displaying multiple buttons in
a grid format with support for different button configurations and text labels.

## UiFlow2 Example

#### basic buttonmatrix

Open the |cores3_buttonmatrix_basic_example.m5f2| project in UiFlow2.

This example demonstrates how to create a button matrix with custom labels and handle button press events.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### basic buttonmatrix

This example demonstrates how to create a button matrix with custom labels and handle button press events.

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
buttonmatrix0 = None
label0 = None
label1 = None

def buttonmatrix0_value_changed_event(event_struct):
    global page0, textarea0, buttonmatrix0, label0, label1
    label1.set_text(str(buttonmatrix0.get_button_text(buttonmatrix0.get_selected_button())))

def buttonmatrix0_event_handler(event_struct):
    global page0, textarea0, buttonmatrix0, label0, label1
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        buttonmatrix0_value_changed_event(event_struct)
    return

def setup():
    global page0, textarea0, buttonmatrix0, label0, label1

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    textarea0 = m5ui.M5TextArea(
        text="",
        placeholder="Placeholder...",
        x=24,
        y=15,
        w=150,
        h=70,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    buttonmatrix0 = m5ui.M5ButtonMatrix(
        ["0", "1", "2", "4", "\n", "5", "6", "7", "8", "9"],
        x=25,
        y=100,
        w=260,
        h=130,
        target_textarea=textarea0,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "last key:",
        x=189,
        y=15,
        text_c=0xC9C9C9,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label1 = m5ui.M5Label(
        "label1",
        x=203,
        y=42,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    buttonmatrix0.add_event_cb(buttonmatrix0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()

def loop():
    global page0, textarea0, buttonmatrix0, label0, label1
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

#### M5ButtonMatrix

## M5ButtonMatrix
Create a button matrix object.

:param list map: A list of button labels. Use "\\n" to create a new row.
:param int x: The x position of the button matrix.
:param int y: The y position of the button matrix.
:param int w: The width of the button matrix.
:param int h: The height of the button matrix.
:param m5ui.M5TextArea target_textarea: A M5TextArea to display the button text when a button is pressed.
:param lv.obj parent: The parent object to attach the button matrix to.

UiFlow2 Code Block:

    None

MicroPython Code Block:

    .. code-block:: python

        import m5ui
        import lvgl as lv

        m5ui.init()
        page0 = m5ui.M5Page()
        page0.screen_load()
        textarea0 = m5ui.M5TextArea(x=10, y=10, w=200, h=60, parent=page0)
        buttonmatrix_0 = m5ui.M5ButtonMatrix(
            ["0", "1", "2", "3", "4","\n", "5", "6", "7", "8", "9",],
            x=10, y=80, w=260, h=130,
            target_textarea=textarea0,
            parent=page0
        )

### `value_changed_event`

### `toggle_button_ctrl`
Toggle control flags for a specific button.

:param int btn_id: The button ID to toggle control flags for.
:param int ctrl: The control flags to toggle.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        buttonmatrix_0.toggle_button_ctrl(0, lv.buttonmatrix.CTRL.HIDDEN)

### `set_textarea`
Set a M5TextArea to display button text.

:param m5ui.M5TextArea textarea: The M5TextArea to set.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        buttonmatrix_0.set_textarea(textarea0)

### `get_textarea`
Get the currently set M5TextArea.

:return: The M5TextArea currently set for the button matrix.
:rtype: m5ui.M5TextArea

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        textarea = buttonmatrix_0.get_textarea()

### `get_selected_button`
Get the ID of the currently selected button.

:return: The ID of the currently selected button, or -1 if none is selected.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        selected_button = buttonmatrix_0.get_selected_button()

<!-- .. py:method:: set_flag(flag, value) -->

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                buttonmatrix_0.set_flag(lv.obj.FLAG.HIDDEN, True)

<!-- .. py:method:: toggle_flag(flag) -->

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                buttonmatrix_0.toggle_flag(lv.obj.FLAG.HIDDEN)

<!-- .. py:method:: set_state(state, value) -->

        Set the state of the buttonmatrix. If ``value`` is True, the state is set; if False, the state is unset.

        :param int state: The state to set.
        :param bool value: If True, the state is set; if False, the state is unset.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                buttonmatrix_0.set_state(lv.STATE.PRESSED, True)

<!-- .. py:method:: toggle_state(state) -->

        Toggle the state of the buttonmatrix. If the state is set, it is unset; if not set, it is set.

        :param int state: The state to toggle.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                buttonmatrix_0.toggle_state(lv.STATE.PRESSED)

<!-- .. py:method:: add_event_cb(handler, event, user_data) -->

        Add an event callback to the buttonmatrix. The callback will be called when the specified event occurs.

        :param function handler: The callback function to call.
        :param int event: The event to listen for.
        :param Any user_data: Optional user data to pass to the callback.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                def buttonmatrix_0_pressed_event(event_struct):
                    global page0
                    btn_id = buttonmatrix_0.get_selected_button()
                    print(f"Button {btn_id} pressed")

                def buttonmatrix_0_event_handler(event_struct):
                    event = event_struct.code
                    if event == lv.EVENT.VALUE_CHANGED:
                        buttonmatrix_0_pressed_event(event_struct)
                    return

                buttonmatrix_0.add_event_cb(buttonmatrix_0_event_handler, lv.EVENT.ALL, None)

<!-- .. py:method:: set_button_width(btn_id, width) -->

        Set the relative width of a specific button.

        :param int btn_id: The index of the button.
        :param int width: The relative width (1-7, where 1 is normal width).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                buttonmatrix_0.set_button_width(0, 2)  # Make first button twice as wide

<!-- .. py:method:: get_button_text(btn_id) -->

        Get the text of a specific button.

        :param int btn_id: The index of the button.
        :return: The text of the button.
        :rtype: str

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                text = buttonmatrix_0.get_button_text(0)

<!-- .. py:method:: clear_button_ctrl(btn_id, ctrl) -->

        Clear control flags for a specific button.

        :param int btn_id: The button ID to clear control flags for.
        :param int ctrl: The control flags to clear.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                buttonmatrix_0.clear_button_ctrl(0, lv.buttonmatrix.CTRL.HIDDEN)

<!-- .. py:method:: set_button_ctrl(btn_id, ctrl) -->

        Set control flags for a specific button.

        :param int btn_id: The button ID to set control flags for.
        :param int ctrl: The control flags to set.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                buttonmatrix_0.set_button_ctrl(0, lv.buttonmatrix.CTRL.HIDDEN)

<!-- .. py:method:: set_button_ctrl_all(ctrl) -->

        Set control flags for all buttons.

        :param int ctrl: The control flags to set for all buttons.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                buttonmatrix_0.set_button_ctrl_all(lv.buttonmatrix.CTRL.HIDDEN)

<!-- .. py:method:: clear_button_ctrl_all(ctrl) -->

        Clear control flags for all buttons.

        :param int ctrl: The control flags to clear for all buttons.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                buttonmatrix_0.clear_button_ctrl_all(lv.buttonmatrix.CTRL.HIDDEN)

<!-- .. py:method:: set_one_checked(btn_id) -->

        Set a specific button as checked.

        :param int btn_id: The button ID to set as checked.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                buttonmatrix_0.set_one_checked(0)

<!-- .. py:method:: set_pos(x, y) -->

        Set the position of the buttonmatrix.

        :param int x: The x-coordinate of the buttonmatrix.
        :param int y: The y-coordinate of the buttonmatrix.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                buttonmatrix_0.set_pos(100, 100)

<!-- .. py:method:: set_x(x) -->

        Set the x-coordinate of the buttonmatrix.

        :param int x: The x-coordinate of the buttonmatrix.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                buttonmatrix_0.set_x(100)

<!-- .. py:method:: set_y(y) -->

        Set the y-coordinate of the buttonmatrix.

        :param int y: The y-coordinate of the buttonmatrix.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                buttonmatrix_0.set_y(100)

<!-- .. py:method:: set_size(width, height) -->

        Set the size of the buttonmatrix.

        :param int width: The width of the buttonmatrix.
        :param int height: The height of the buttonmatrix.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                buttonmatrix_0.set_size(300, 200)

<!-- .. py:method:: set_width(width) -->

        Set the width of the buttonmatrix.

        :param int width: The width of the buttonmatrix.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                buttonmatrix_0.set_width(300)

<!-- .. py:method:: get_width() -->

        Get the width of the buttonmatrix.

        :return: The width of the buttonmatrix.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                width = buttonmatrix_0.get_width()

<!-- .. py:method:: set_height(height) -->

        Set the height of the buttonmatrix.

        :param int height: The height of the buttonmatrix.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                buttonmatrix_0.set_height(200)

<!-- .. py:method:: get_height() -->

        Get the height of the buttonmatrix.

        :return: The height of the buttonmatrix.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                height = buttonmatrix_0.get_height()

<!-- .. py:method:: align_to(obj, align, x, y) -->

        Align the buttonmatrix to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                buttonmatrix_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
