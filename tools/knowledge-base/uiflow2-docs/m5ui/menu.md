<!-- .. currentmodule:: m5ui -->

# M5Menu

<!-- .. include:: ../refs/m5ui.menu.ref -->

M5Menu is a widget that can be used to create multi-level menus in the user interface.

## UiFlow2 Example

#### menu event

Open the |menu_core2_example.m5f2| project in UiFlow2.

This example creates a multi-level menus.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### menu event

This example creates a multi-level menus.

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
menu0 = None
Label1 = None
Label2 = None
Page_2 = None
Page2_Label1 = None
Page2_Label2 = None
Page_3 = None
Page3_Label = None
Page3_Switch = None

import random

def Page3_Switch_checked_event(event_struct):  # noqa: N802
    global \
        page0, \
        menu0, \
        Label1, \
        Label2, \
        Page_2, \
        Page2_Label1, \
        Page2_Label2, \
        Page_3, \
        Page3_Label, \
        Page3_Switch

    Page3_Label.set_text_color(random.randint(0x000000, 0xFFFFFF), 255, 0)

def Page3_Switch_unchecked_event(event_struct):  # noqa: N802
    global \
        page0, \
        menu0, \
        Label1, \
        Label2, \
        Page_2, \
        Page2_Label1, \
        Page2_Label2, \
        Page_3, \
        Page3_Label, \
        Page3_Switch

    Page3_Label.set_text_color(random.randint(0x000000, 0xFFFFFF), 255, 0)

def Page3_Switch_event_handler(event_struct):  # noqa: N802
    global \
        page0, \
        menu0, \
        Label1, \
        Label2, \
        Page_2, \
        Page2_Label1, \
        Page2_Label2, \
        Page_3, \
        Page3_Label, \
        Page3_Switch
    event = event_struct.code
    obj = event_struct.get_target_obj()
    if event == lv.EVENT.VALUE_CHANGED:
        if obj.has_state(lv.STATE.CHECKED):
            Page3_Switch_checked_event(event_struct)
        else:
            Page3_Switch_unchecked_event(event_struct)
    return

def setup():
    global \
        page0, \
        menu0, \
        Label1, \
        Label2, \
        Page_2, \
        Page2_Label1, \
        Page2_Label2, \
        Page_3, \
        Page3_Label, \
        Page3_Switch

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    menu0 = m5ui.M5Menu(x=0, y=0, w=320, h=240, parent=page0)
    menu0.set_page(menu0.main_page)
    Label1 = menu0.add_label("Label1")
    Label2 = menu0.add_label("Label2")
    menu0.set_mode_root_back_button(lv.menu.ROOT_BACK_BUTTON.ENABLED)
    menu0.set_mode_header(lv.menu.HEADER.TOP_FIXED)

    page0.screen_load()
    Label2.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN | lv.STATE.DEFAULT)
    Label2.set_text(str("Click me!!!!!!!!"))
    Page_2 = lv.menu_page(menu0, "Page2")
    menu0.set_load_page_event(Label2.cont, Page_2)
    Page2_Label1 = menu0.add_label("Label1", parent=Page_2)
    Page2_Label2 = menu0.add_label(
        "Label2 (Click me)",
        text_c=0xFF0000,
        text_opa=255,
        bg_c=0xFFFFFF,
        bg_opa=255,
        font=lv.font_montserrat_24,
        parent=Page_2,
    )
    Page_3 = lv.menu_page(menu0, "Page3")
    menu0.set_load_page_event(Page2_Label2.cont, Page_3)
    Page3_Label = menu0.add_label("A Label", parent=Page_3)
    Page3_Label.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN | lv.STATE.DEFAULT)
    Page3_Switch = menu0.add_switch(
        "A Switch",
        w=80,
        h=40,
        bg_c=0xE7E3E7,
        bg_opa=255,
        bg_c_checked=0x2196F3,
        bg_c_checked_opa=255,
        circle_c=0xFF9966,
        circle_opa=255,
        parent=Page_3,
    )
    Page3_Switch.add_event_cb(Page3_Switch_event_handler, lv.EVENT.ALL, None)

def loop():
    global \
        page0, \
        menu0, \
        Label1, \
        Label2, \
        Page_2, \
        Page2_Label1, \
        Page2_Label2, \
        Page_3, \
        Page3_Label, \
        Page3_Switch
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

#### M5Menu

## M5Menu
Create a list object.

:param int x: The x position of the menu.
:param int y: The y position of the menu.
:param int w: The width of the menu.
:param int h: The height of the menu.
:param str page_name: The name of the main page of the menu.
:param lv.obj parent: The parent object to attach the menu to. If not specified, the menu will be attached to the default screen.

UiFlow2 Code Block:

    None

MicroPython Code Block:

    .. code-block:: python

        from m5ui import M5Menu
        import lvgl as lv

        m5ui.init()
        menu0 = M5Menu(x=120, y=80, w=60, h=30, parent=page0)

### `add_label`
Add a label to the menu.

:param str text: The text to display on the label.
:param int text_c: The text color of the label.
:param int bg_c: The background color of the label.
:param int bg_opa: The background opacity of the label.
:param lv.font_t font: The font of the label.
:param lv.obj parent: The parent object to attach the label to. If not specified, the label will be attached to the main page of the menu.
:return: The created label object.
:rtype: :ref:`m5ui.M5Label <m5ui.M5Label>`

 UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        label0 = menu0.add_label("Hello, World!", text_c=0x212121, bg_c=0xFFFFFF, bg_opa=255, font=lv.font_montserrat_14, parent=menu0.main_page)

### `add_switch`
Add a switch to the menu.

:param str text: The text to display next to the switch.
:param int w: The width of the switch.
:param int h: The height of the switch.
:param int bg_c: The background color of the switch when unchecked.
:param int bg_c_checked: The background color of the switch when checked.
:param int circle_c: The color of the switch circle.
:param lv.obj parent: The parent object to attach the switch to. If not specified, the switch will be attached to the main page of the menu.
:return: The created switch object.
:rtype: :ref:`m5ui.M5Switch <m5ui.M5Switch>`

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        switch_0 = menu0.add_switch("Switch 1", w=50, h=20, bg_c=0xE7E3E7, bg_c_checked=0x0288FB, circle_c=0xFFFFFF, parent=menu0.main_page)

<!-- .. py:method:: set_page(page) -->

        Set main page for the menu.

        :param lv.obj page: The main page object.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                menu0.set_page(menu0.main_page)

<!-- .. py:method:: set_mode_header(mode) -->

        Set the mode header for the menu.

        :param int mode: The mode header text.

            Options:

                - ``lv.menu.HEADER.TOP_FIXED``
                - ``lv.menu.HEADER.TOP_UNFIXED``
                - ``lv.menu.HEADER.BOTTOM_FIXED``

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                menu0.set_mode_header(lv.menu.HEADER.TOP_FIXED)

<!-- .. py:method:: set_pos(x, y) -->

        Set the position of the menu.

        :param int x: The x-coordinate of the menu.
        :param int y: The y-coordinate of the menu.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                menu0.set_pos(100, 100)

<!-- .. py:method:: set_size(width, height) -->

        Set the size of the menu.

        :param int width: The width of the menu.
        :param int height: The height of the menu.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                menu0.set_size(100, 50)
