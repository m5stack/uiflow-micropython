<!-- .. currentmodule:: m5ui -->

# M5Dropdown

<!-- .. include:: ../refs/m5ui.dropdown.ref -->

M5Dropdown is a widget that can be used to create dropdown menus in the user
interface. It allows users to select one option from a list of available options
with a compact dropdown interface.

<!-- .. important:: -->

    **Available Fonts**: Only ``lv.font_montserrat_14``, ``lv.font_montserrat_16``, and ``lv.font_montserrat_24`` are available.

## UiFlow2 Example

#### Drop down in four directions

Open the |cores3_dropdown_directions_example.m5f2| project in UiFlow2.

This example creates a drop down, up, left and right menus.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Drop down in four directions

This example creates a drop down, up, left and right menus.

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
dropdown0 = None
dropdown1 = None
dropdown2 = None
dropdown3 = None

def setup():
    global page0, dropdown0, dropdown1, dropdown2, dropdown3

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    dropdown0 = m5ui.M5Dropdown(
        x=110,
        y=0,
        w=100,
        h=lv.SIZE_CONTENT,
        options=["option1", "option2"],
        direction=lv.DIR.BOTTOM,
        show_selected=True,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    dropdown1 = m5ui.M5Dropdown(
        x=111,
        y=212,
        w=100,
        h=lv.SIZE_CONTENT,
        options=["option1", "option2"],
        direction=lv.DIR.TOP,
        show_selected=True,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    dropdown2 = m5ui.M5Dropdown(
        x=220,
        y=106,
        w=100,
        h=lv.SIZE_CONTENT,
        options=["option1", "option2"],
        direction=lv.DIR.LEFT,
        show_selected=True,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    dropdown3 = m5ui.M5Dropdown(
        x=0,
        y=106,
        w=100,
        h=lv.SIZE_CONTENT,
        options=["option1", "option2"],
        direction=lv.DIR.RIGHT,
        show_selected=True,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    page0.screen_load()
    dropdown0.set_selected_highlight(True)
    dropdown1.set_selected_highlight(True)
    dropdown2.set_selected_highlight(True)
    dropdown3.set_selected_highlight(True)

def loop():
    global page0, dropdown0, dropdown1, dropdown2, dropdown3
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

#### M5Dropdown

## M5Dropdown
Create a dropdown object.

:param x: The x position of the dropdown.
:param y: The y position of the dropdown.
:param w: The width of the dropdown.
:param h: The height of the dropdown, default is `lv.SIZE_CONTENT`.
:param options: A list of options to display in the dropdown.
:param direction: The direction of the dropdown, can be `lv.DIR.LEFT`, `lv.DIR.RIGHT`, `lv.DIR.TOP`, or `lv.DIR.BOTTOM`.
:param show_selected: Whether to highlight the selected option, default is `True`.
:param font: The font used for the text in the dropdown, default is `lv.font_montserrat_14`.
:param parent: The parent object for this dropdown, default is the active screen.

### `set_options`
Set the options for the dropdown.

:param options: A list of options to display in the dropdown.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        dropdown_0.set_options(["option1", "option2", "option3"])

### `get_options`
Get the list of options in the dropdown.

:return: The list of options.
:rtype: list

### `add_option`
Add an option to the dropdown at a specific position.

:param option: The option to add.
:param pos: The position to insert the option at.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        dropdown_0.add_option("New Option", 1)

### `clear_options`
Clear all options in the dropdown.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        dropdown_0.clear_options()

### `get_selected_str`
Get the currently selected option as a string.

:return: The selected option as a string.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        selected_option = dropdown_0.get_selected_str()

### `set_dir`
Set the direction of the dropdown.

:param direction: The direction of the dropdown, can be `lv.DIR.LEFT`, `lv.DIR.RIGHT`, `lv.DIR.TOP`, or `lv.DIR.BOTTOM`.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        dropdown_0.set_dir(lv.DIR.LEFT)

### `set_style_radius`
Set the radius of the dropdown's corners.

:param radius: The radius of the corners in pixels.
:param part: The part of the dropdown to apply the radius to, e.g., `lv.PART.MAIN`.

UiFlow2 Code Block:

    None

MicroPython Code Block:

    .. code-block:: python

        dropdown_0.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)

### `set_size`
Set the size of the dropdown.

:param w: The width of the dropdown.
:param h: The height of the dropdown.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        dropdown_0.set_size(150, 40)

<!-- .. py:method:: set_flag(flag, value) -->

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                dropdown_0.set_flag(lv.obj.FLAG.HIDDEN, True)

<!-- .. py:method:: toggle_flag(flag) -->

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                dropdown_0.toggle_flag(lv.obj.FLAG.HIDDEN)

<!-- .. py:method:: set_state(state, value) -->

        Set the state of the dropdown. If ``value`` is True, the state is set; if False, the state is unset.

        :param int state: The state to set.
        :param bool value: If True, the state is set; if False, the state is unset.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                dropdown_0.set_state(lv.STATE.CHECKED, True)

<!-- .. py:method:: toggle_state(state) -->

        Toggle the state of the dropdown. If the state is set, it is unset; if not set, it is set.

        :param int state: The state to toggle.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                dropdown_0.toggle_state(lv.STATE.CHECKED)

<!-- .. py:method:: set_pos(x, y) -->

        Set the position of the dropdown.

        :param int x: The x-coordinate of the dropdown.
        :param int y: The y-coordinate of the dropdown.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                dropdown_0.set_pos(100, 100)

<!-- .. py:method:: set_x(x) -->

        Set the x-coordinate of the dropdown.

        :param int x: The x-coordinate of the dropdown.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                dropdown_0.set_x(100)

<!-- .. py:method:: set_y(y) -->

        Set the y-coordinate of the dropdown.

        :param int y: The y-coordinate of the dropdown.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                dropdown_0.set_y(100)

<!-- .. py:method:: set_width(width) -->

        Set the width of the dropdown.

        :param int width: The width of the dropdown.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                dropdown_0.set_width(100)

<!-- .. py:method:: get_width() -->

        Get the width of the dropdown.

        :return: The width of the dropdown.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                dropdown_0.get_width()

<!-- .. py:method:: set_height(height) -->

        Set the height of the dropdown.

        :param int height: The height of the dropdown.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                dropdown_0.set_height(50)

<!-- .. py:method:: get_height() -->

        Get the height of the dropdown.

        :return: The height of the dropdown.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                dropdown_0.get_height()

<!-- .. py:method:: align_to(obj, align, x, y) -->

        Align the dropdown to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                dropdown_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)

<!-- .. py:method:: get_selected() -->

        Get the index of the currently selected option.

        :return: The index of the selected option.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                selected_index = dropdown_0.get_selected()

<!-- .. py:method:: set_selected_highlight(enable) -->

        Enable or disable highlighting of the selected option.

        :param bool enable: True to enable highlighting, False to disable.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                dropdown_0.set_selected_highlight(True)

<!-- .. py:method:: get_option_count() -->

        Clear all options in a drop-down list.

        :return: The number of options in the dropdown.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                option_count = dropdown_0.get_option_count()

<!-- .. py:method:: get_option_index(option) -->

        Get the index of an option.

        :param str option: The option to find.
        :return: The index of the option, or -1 if not found.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                index = dropdown_0.get_option_index("Option 1")
                if index != -1:
                    print(f"Option found at index: {index}")
                else:
                    print("Option not found")

<!-- .. py:method:: get_text() -->

        Get text of the drop-down list's button.

        :return: The text of the dropdown button.
        :rtype: str

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                text = dropdown_0.get_text()
                print(f"Dropdown button text: {text}")

<!-- .. py:method:: set_text(txt) -->

        Set text of the drop-down list's button.

        :param str txt: The text to set for the dropdown button.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                dropdown_0.set_text("Select an option")

<!-- .. py:method:: add_event_cb(handler, event, user_data) -->

        Add an event callback to the dropdown. The callback will be called when the specified event occurs.

        :param function handler: The callback function to call.
        :param int event: The event to listen for.
        :param Any user_data: Optional user data to pass to the callback.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                def dropdown_0_value_changed_event(event_struct):
                    global dropdown_0
                    selected = dropdown_0.get_selected_str()
                    print(f"Selected: {selected}")

                def dropdown_0_event_handler(event_struct):
                    global dropdown_0
                    event = event_struct.code
                    if event == lv.EVENT.VALUE_CHANGED:
                        dropdown_0_value_changed_event(event_struct)
                    return

                dropdown_0.add_event_cb(dropdown_0_event_handler, lv.EVENT.ALL, None)
