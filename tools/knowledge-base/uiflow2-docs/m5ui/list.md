<!-- .. currentmodule:: m5ui -->

# M5List

<!-- .. include:: ../refs/m5ui.list.ref -->

M5List is a widget that can be used to create lists in user interfaces. It is basically a rectangle with vertical layout to which Buttons and Text can be added.

## UiFlow2 Example

#### list example

Open the |cores3_list_example.m5f2| project in UiFlow2.

This example demonstrates how to create a list that displays a series of items.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### list example

This example demonstrates how to create a list that displays a series of items.

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
list0 = None
File = None
New = None
Open = None
Save = None
Delete = None

def New_clicked_event(event_struct):  # noqa: N802
    global page0, list0, File, New, Open, Save, Delete

    print("New")

def Open_clicked_event(event_struct):  # noqa: N802
    global page0, list0, File, New, Open, Save, Delete

    print("Open")

def Save_clicked_event(event_struct):  # noqa: N802
    global page0, list0, File, New, Open, Save, Delete

    print("Save")

def Delete_clicked_event(event_struct):  # noqa: N802
    global page0, list0, File, New, Open, Save, Delete

    print("Delete")

def New_event_handler(event_struct):  # noqa: N802
    global page0, list0, File, New, Open, Save, Delete
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        New_clicked_event(event_struct)
    return

def Open_event_handler(event_struct):  # noqa: N802
    global page0, list0, File, New, Open, Save, Delete
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        Open_clicked_event(event_struct)
    return

def Save_event_handler(event_struct):  # noqa: N802
    global page0, list0, File, New, Open, Save, Delete
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        Save_clicked_event(event_struct)
    return

def Delete_event_handler(event_struct):  # noqa: N802
    global page0, list0, File, New, Open, Save, Delete
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        Delete_clicked_event(event_struct)
    return

def setup():
    global page0, list0, File, New, Open, Save, Delete

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    list0 = m5ui.M5List(x=-1, y=2, w=320, h=240, parent=page0)
    File = list0.add_text("File")
    New = list0.add_button(lv.SYMBOL.BULLET, "New")

    page0.screen_load()
    Open = list0.add_button(lv.SYMBOL.DIRECTORY, "Open")
    Save = list0.add_button(lv.SYMBOL.SAVE, "Save")
    Delete = list0.add_button(lv.SYMBOL.CLOSE, "Delete")

    New.add_event_cb(New_event_handler, lv.EVENT.ALL, None)
    Open.add_event_cb(Open_event_handler, lv.EVENT.ALL, None)
    Save.add_event_cb(Save_event_handler, lv.EVENT.ALL, None)
    Delete.add_event_cb(Delete_event_handler, lv.EVENT.ALL, None)

    New.set_text_color(0xFFFF00, 255, lv.PART.MAIN | lv.STATE.PRESSED)
    Open.set_text_color(0xFFFF00, 100, lv.PART.MAIN | lv.STATE.PRESSED)
    Save.set_text_color(0xFFFF00, 255, lv.PART.MAIN | lv.STATE.PRESSED)
    Delete.set_text_color(0xFFFF00, 255, lv.PART.MAIN | lv.STATE.PRESSED)

def loop():
    global page0, list0, File, New, Open, Save, Delete
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

#### M5List

## M5List
Create a list object.

:param int x: The x position of the list.
:param int y: The y position of the list.
:param int w: The width of the list.
:param int h: The height of the list.
:param lv.obj parent: The parent object to attach the list to. If not specified, the list will be attached to the default screen.

UiFlow2 Code Block:

    None

MicroPython Code Block:

    .. code-block:: python

        from m5ui import M5List
        import lvgl as lv

        m5ui.init()
        list_0 = M5List(x=120, y=80, w=60, h=30, parent=page0)

### `add_text`
Add a text label to the list.

:param str text: The text to display on the label.
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

        list_0.add_text("Item 1", text_c=0x000000, text_opa=255, bg_c=0xFFFFFF, bg_opa=255, font=lv.font_montserrat_14)

### `add_button`
Add a button to the list.

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

        list_0.add_button(lv.SYMBOL.BULLET, text="Home", h=40, bg_c=0xFFFFFF, text_c=0x000000, font=lv.font_montserrat_14)

<!-- .. py:method:: move_background() -->

        Move the background of the list to the end.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.move_background()
                text_0.move_background()

<!-- .. py:method:: move_foreground() -->

        Move the foreground of the list to the end.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.move_foreground()
                text_0.move_foreground()

<!-- .. py:method:: move_to_index(index) -->

        Move the item at the specified index to the end of the list.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.move_to_index(0)
                text_0.move_to_index(1)

<!-- .. py:method:: delete() -->

        Delete the item from the list.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                button_0.delete()
                text_0.delete()
