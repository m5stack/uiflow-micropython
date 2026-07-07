<!-- .. currentmodule:: m5ui -->
<!-- .. _m5ui.M5Label: -->

# M5Label

<!-- .. include:: ../refs/m5ui.label.ref -->

M5Label is a widget that can be used to create labels in the user interface. It can display text and can be styled with different fonts, colors, and sizes.

<!-- .. important:: -->

    **Available Fonts**: The firmware only includes these Montserrat fonts:

    - ``lv.font_montserrat_14`` (default)
    - ``lv.font_montserrat_16``
    - ``lv.font_montserrat_24``

    Other sizes (18, 20, 22, 28, etc.) are **not compiled** and will cause ``AttributeError``.

## UiFlow2 Example

#### scroll label

Open the |cores3_scroll_label_example.m5f2| project in UiFlow2.

This example demonstrates how to create a label that scrolls text in a circular manner.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### scroll label

This example demonstrates how to create a label that scrolls text in a circular manner.

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
label0 = None

def setup():
    global page0, label0

    M5.begin()
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    label0 = m5ui.M5Label(
        "It is a circularly scrolling text. ",
        x=60,
        y=110,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    page0.screen_load()
    label0.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)
    label0.set_width(150)
    label0.align_to(page0, lv.ALIGN.CENTER, 0, 0)

def loop():
    global page0, label0
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

#### M5Label

<!-- .. note:: -->

    Unlike ``M5Button`` and ``M5Chart``, the ``M5Label`` constructor does
    **not** accept ``w`` or ``h`` parameters. Label size is determined
    automatically by its text content. To explicitly set a label's width,
    call ``label.set_width(150)`` after creation.

## M5Label
Create a label object.

:param str text: The text to display on the label.
:param int x: The x position of the label.
:param int y: The y position of the label.
:param int text_c: The text color of the label in hexadecimal format.
:param int bg_c: The background color of the label in hexadecimal format.
:param int bg_opa: The background opacity of the label (0-255).
:param lv.lv_font_t font: The font to use for the button text.
:param lv.obj parent: The parent object to attach the button to. If not specified, the button will be attached to the default screen.

UiFlow2 Code Block:

    None

MicroPython Code Block:

    .. code-block:: python

        from m5ui import M5Label
        import lvgl as lv

        m5ui.init()
        label_0 = M5Label(text="Hello, World!", x=10, y=10, text_c=0x212121, bg_c=0xFFFFFF, bg_opa=0, font=lv.font_montserrat_14, parent=page0)

### `set_shadow`
Set a shadow for the label.

:param int color: The color of the shadow in hexadecimal format or an integer.
:param int opa: The opacity of the shadow (0-255).
:param int align: The alignment of the shadow relative to the label.
:param int offset_x: The horizontal offset of the shadow.
:param int offset_y: The vertical offset of the shadow.
:return: None

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        label_0.set_shadow(color=0x000000, opa=128, align=lv.ALIGN.BOTTOM_RIGHT, offset_x=5, offset_y=5)

### `unset_shadow`
Remove the shadow from the label.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        label_0.unset_shadow()

### `set_style_radius`

### `set_size`

<!-- .. py:method:: set_flag(flag, value) -->

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_0.set_flag(lv.obj.FLAG.HIDDEN, True)

<!-- .. py:method:: toggle_flag(flag) -->

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_0.toggle_flag(lv.obj.FLAG.HIDDEN)

<!-- .. py:method:: set_state(state, value) -->

        Set the state of the label. If ``value`` is True, the state is set; if False, the state is unset.

        :param int state: The state to set.
        :param bool value: If True, the state is set; if False, the state is unset.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_0.set_state(lv.STATE.PRESSED, True)

<!-- .. py:method:: toggle_state(state) -->

        Toggle the state of the label. If the state is set, it is unset; if not set, it is set.

        :param int state: The state to toggle.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_0.toggle_state(lv.STATE.PRESSED)

<!-- .. py:method:: set_style_text_font(font, part) -->

        Set the font of the label text.

        :param lv.lv_font_t font: The font to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN | lv.STATE.DEFAULT)

<!-- .. py:method:: set_text_color(color, opa, part) -->

        Set the color of the text.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

<!-- .. py:method:: set_bg_color(color, opa, part) -->

        Set the background color of the label.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

<!-- .. py:method:: set_pos(x, y) -->

        Set the position of the label.

        :param int x: The x-coordinate of the label.
        :param int y: The y-coordinate of the label.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_0.set_pos(100, 100)

<!-- .. py:method:: set_x(x) -->

        Set the x-coordinate of the label.

        :param int x: The x-coordinate of the label.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_0.set_x(100)

<!-- .. py:method:: set_y(y) -->

        Set the y-coordinate of the label.

        :param int y: The y-coordinate of the label.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_0.set_y(100)

<!-- .. py:method:: set_size(width, height) -->

        Set the size of the label.

        :param int width: The width of the label.
        :param int height: The height of the label.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_0.set_size(100, 50)

<!-- .. py:method:: set_width(width) -->

        Set the width of the label.

        :param int width: The width of the label.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_0.set_width(100)

<!-- .. py::method:: get_width() -->

        Get the width of the label.

        :return: The width of the label.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_0.get_width()

<!-- .. py:method:: align_to(obj, align, x, y) -->

        Align the label to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
