<!-- .. currentmodule:: Widgets -->

# class LabelPlus -- display remote text

The `LabelPlus` class extends the `Widgets.Label` class to provide additional functionalities for handling text with dynamic updates.

Currently only accepts strings in json format, and extracts data through ``json_key``.

<!-- .. include:: ../refs/widgets.label+.ref -->

## UiFlow2 Example

#### Simple Usage

Open the |cores3_labelplus_example.m5f2| project in UiFlow2.

This example demonstrates how to create and manipulate a LabelPlus widget.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Simple Usage

This example demonstrates how to create and manipulate a LabelPlus widget.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from label_plus import LabelPlus

label_plus0 = None

en = None

def btnPWR_wasClicked_event(state):  # noqa: N802
    global label_plus0, en
    en = not en
    if en:
        label_plus0.set_update_enable(True)
    else:
        label_plus0.set_update_enable(False)

def setup():
    global label_plus0, en

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    label_plus0 = LabelPlus(
        "label_plus0",
        24,
        31,
        1.0,
        0xFFFFFF,
        0x222222,
        Widgets.FONTS.DejaVu18,
        "http://192.168.8.200:8000/data",
        3000,
        True,
        "data",
        "error",
        0xFF0000,
    )

    BtnPWR.setCallback(type=BtnPWR.CB_TYPE.WAS_CLICKED, cb=btnPWR_wasClicked_event)

    en = True

def loop():
    global label_plus0, en
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

```

Example output:

    None

## **API**

#### LabelPlus

## LabelPlus
Create a LabelPlus object that can fetch and display text from a URL.

:param str text: The initial text to display on the label.
:param int x: The x position of the label.
:param int y: The y position of the label.
:param int size: The font size of the label text.
:param int text_color: The text color of the label in hexadecimal format.
:param int bg_color: The background color of the label in hexadecimal format.
:param font: The font to use for the label text.
:param str url: The URL to fetch data from.
:param int period: The update period in milliseconds. If set to 0, the label will not update automatically.
:param bool enable: Whether to enable automatic updates.
:param str json_key: The JSON key to extract from the fetched data.
:param str error_msg: The message to display in case of an error.
:param int error_msg_color: The text color to use when displaying an error message, in hexadecimal format.

UiFlow2 Code Block:

    None

MicroPython Code Block:

    .. code-block:: python

        from label_plus import LabelPlus

        label_plus0 = LabelPlus("label_plus0", 7, 10, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18, "http://example.com", 3000, True, "title", "error", 0xFF0000)

### `deinit`

### `set_update_enable`
Enable or disable automatic updates.

:param bool enable: True to enable automatic updates, False to disable.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        label_plus0.set_update_enable(True)

### `set_update_period`
Set the update period for automatic updates.

:param int period: The update period in milliseconds.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        label_plus0.set_update_period(5000)

### `is_valid_data`
Check if the current data is valid (i.e., not an error message).

:return: True if the current data is valid, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        valid = label_plus0.is_valid_data()

### `get_data`
Get the current data displayed on the label.

:return: The current data.
:rtype: str

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        data = label_plus0.get_data()

### `setColor`
Sets the text font color of the Label object.

:param int fg_color: The text color in hexadecimal format.
:param int bg_color: The background color in hexadecimal format.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        label_plus0.setColor(0xFFFFFF, 0x000000)

### `set_url`

### `update`

### `show_value_of_key`

<!-- .. py:method:: setText(text) -->

        Set the text of the LabelPlus widget.

        :param str text: The text to set on the label.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_plus_0.setText("New Text")

<!-- .. py:method:: setCursor(x=0, y=0) -->

        Sets the starting coordinates of the text cursor in the LabelPlus widget.

        :param int x: The x-coordinate of the cursor.
        :param int y: The y-coordinate of the cursor.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_plus_0.setCursor(10, 20)

<!-- .. py:method:: setSize(size) -->

        Sets the font size of the text in the LabelPlus widget.

        :param float size: The font size to set.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_plus_0.setSize(1.5)

<!-- .. py:method:: setFont(font) -->

        Sets the font of the text in the LabelPlus widget.

        :param font: supports built-in fonts and font files (for example, ``.bin`` (lvgl binary font format) or ``.vlw`` (Processing font format)). For the full list of built-in fonts, status, and device support, see :meth:`Display.setFont` . Widgets.FONTS uses the same font as M5.Display.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_plus_0.setFont(Widgets.FONTS.Montserrat12)

<!-- .. py:method:: setVisible(visible) -->

        Set the visible property of the LabelPlus widget.

        :param bool visible: True to make the label visible, False to hide it.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                label_plus_0.setVisible(True)
