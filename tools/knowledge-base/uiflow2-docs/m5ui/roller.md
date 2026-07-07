<!-- .. currentmodule:: m5ui -->

# M5Roller

<!-- .. include:: ../refs/m5ui.roller.ref -->

M5Roller is a widget that can be used to create a roller (spinner/wheel picker) in the
user interface. It provides a scrollable list of options that users can select from by
scrolling up or down, similar to iOS-style picker wheels.

## UiFlow2 Example

#### basic roller

Open the |cores3_roller_basic_example.m5f2| project in UiFlow2.

This example demonstrates how to create a roller with multiple options and handle selection events.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### basic roller

This example demonstrates how to create a roller with multiple options and handle selection events.

MicroPython Code Block:

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv

page0 = None
roller0 = None

def setup():
    global page0, roller0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    roller0 = m5ui.M5Roller(
        x=110,
        y=71,
        w=100,
        h=0,
        options=[
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
        mode=lv.roller.MODE.INFINITE,
        selected=0,
        visible_row_count=3,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    page0.screen_load()
    print(roller0.get_options())

def loop():
    global page0, roller0
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

#### M5Roller

## M5Roller
Create a roller widget.

:param int x: X position of the widget.
:param int y: Y position of the widget.
:param int w: Width of the widget.
:param int h: Height of the widget.
:param list options: List of options to display in the roller.
:param lv.roller.MODE mode: Roller mode (default is NORMAL).
:param int selected: Index of the initially selected option.
:param int visible_row_count: Number of visible rows in the roller.
:param lv.font_t font: Font to use for the text in the roller.
:param parent: Parent widget to attach this roller to (default is the active screen).
:type parent: lv.obj or None

UiFlow2 Code Block:

    None

MicroPython Code Block:

    .. code-block:: python

        from m5ui import M5Roller
        import lvgl as lv
        m5ui.init()
        roller_0 = M5Roller(x=10, y=10, w=100, h=100, options=["Option 1", "Option 2"], mode=lv.roller.MODE.NORMAL, selected=0, visible_row_count=2, font=lv.font_montserrat_14, parent=page0)

### `set_options`
Set the options for the roller.

:param list options: List of options to display in the roller.
:param lv.roller.MODE mode: Roller mode (default is NORMAL).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        roller_0.set_options(["Option 1", "Option 2"], mode=lv.roller.MODE.NORMAL)

### `get_options`
Get the list of options in the dropdown.

:return: The list of options.
:rtype: list

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        options = roller_0.get_options()

### `get_option_count`
Get the number of options in the roller.

:return: The number of options.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        option_count = roller_0.get_option_count()

### `get_selected_str`
Get the currently selected option as a string.

:return: The selected option as a string.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        selected_option = roller_0.get_selected_str()

### `set_style_radius`
Set the corner radius of the slider components.

:param int radius: The radius to set.
:param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN, lv.PART.SELECTED).
:return: None

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        roller_0.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)
        roller_0.set_style_radius(10, lv.PART.SELECTED | lv.STATE.DEFAULT)

<!-- .. py:method:: set_flag(flag, value) -->

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                roller_0.set_flag(lv.obj.FLAG.HIDDEN, True)

<!-- .. py:method:: toggle_flag(flag) -->

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                roller_0.toggle_flag(lv.obj.FLAG.HIDDEN)

<!-- .. py:method:: set_state(state, value) -->

        Set the state of the roller. If ``value`` is True, the state is set; if False, the state is unset.

        :param int state: The state to set.
        :param bool value: If True, the state is set; if False, the state is unset.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                roller_0.set_state(lv.STATE.CHECKED, True)

<!-- .. py:method:: toggle_state(state) -->

        Toggle the state of the roller. If the state is set, it is unset; if not set, it is set.

        :param int state: The state to toggle.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                roller_0.toggle_state(lv.STATE.CHECKED)

<!-- .. py:method:: event(callback, event, user_data=None) -->

        Add an event callback to the roller. The callback will be called when the specified event occurs.

        :param callback: The callback function to call.
        :param int event: The event to listen for.
        :param user_data: Optional user data to pass to the callback.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                def roller_callback(event_obj):
                    print("Roller value changed")

                roller_0.event(roller_callback, lv.EVENT.VALUE_CHANGED)

<!-- .. py:method:: set_bg_color(color, opa, part) -->

        Set the background color of the roller.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                roller_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

                roller_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.SELECTED | lv.STATE.DEFAULT)

<!-- .. py:method:: set_border_color(color, opa, part) -->

        Set the border color of the roller.

        :param int color: The color to set.
        :param int opa: The opacity of the color. The value should be between 0 (transparent) and 255 (opaque).
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                roller_0.set_border_color(lv.color_hex(0x2196F3), 255, lv.PART.MAIN | lv.STATE.DEFAULT)
                roller_0.set_border_color(lv.color_hex(0x2196F3), 255, lv.PART.SELECTED | lv.STATE.DEFAULT)

<!-- .. py:method:: set_style_border_width(width, part) -->

        Set the border width of the roller.

        :param int width: The width to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                roller_0.set_style_border_width(2, lv.PART.MAIN | lv.STATE.DEFAULT)
                roller_0.set_style_border_width(2, lv.PART.SELECTED | lv.STATE.DEFAULT)

<!-- .. py:method:: get_selected() -->

        Get the index of the currently selected option.

        :return: The index of the selected option.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                selected_index = roller_0.get_selected()

<!-- .. py:method:: set_visible_row_count(count) -->

        Set the number of visible rows in the roller.

        :param int count: The number of visible rows.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                roller_0.set_visible_row_count(3)

<!-- .. py:method:: set_pos(x, y) -->

        Set the position of the roller.

        :param int x: The x-coordinate of the roller.
        :param int y: The y-coordinate of the roller.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                roller_0.set_pos(100, 50)

<!-- .. py:method:: set_x(x) -->

        Set the x-coordinate of the roller.

        :param int x: The x-coordinate of the roller.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                roller_0.set_x(100)

<!-- .. py:method:: set_y(y) -->

        Set the y-coordinate of the roller.

        :param int y: The y-coordinate of the roller.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                roller_0.set_y(50)

<!-- .. py:method:: align_to(obj, align, x_ofs=0, y_ofs=0) -->

        Align the roller to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x_ofs: The x-offset from the aligned object.
        :param int y_ofs: The y-offset from the aligned object.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                roller_0.align_to(other_obj, lv.ALIGN.CENTER, 0, 0)

<!-- .. py:method:: set_size(w, h) -->

        Set the size of the roller.

        :param int w: The width of the roller.
        :param int h: The height of the roller.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                roller_0.set_size(150, 120)

<!-- .. py:method:: set_width(w) -->

        Set the width of the roller.

        :param int w: The width of the roller.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                roller_0.set_width(150)

<!-- .. py:method:: get_width() -->

        Get the width of the roller.

        :return: The width of the roller.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                width = roller_0.get_width()

<!-- .. py:method:: set_height(h) -->

        Set the height of the roller.

        :param int h: The height of the roller.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                roller_0.set_height(120)

<!-- .. py:method:: get_height() -->

        Get the height of the roller.

        :return: The height of the roller.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                height = roller_0.get_height()
