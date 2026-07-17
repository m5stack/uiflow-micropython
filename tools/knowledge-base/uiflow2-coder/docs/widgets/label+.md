
# class LabelPlus -- display remote text

The `LabelPlus` class extends the `Widgets.Label` class to provide additional functionalities for handling text with dynamic updates.

Currently only accepts strings in json format, and extracts data through `json_key`.

## MicroPython Example

#### Simple Usage

This example demonstrates how to create and manipulate a LabelPlus widget.

```python
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

## **API**

#### LabelPlus

## `LabelPlus`
Create a LabelPlus object that can fetch and display text from a URL.

- Parameter `text` (`str`): The initial text to display on the label.
- Parameter `x` (`int`): The x position of the label.
- Parameter `y` (`int`): The y position of the label.
- Parameter `size` (`int`): The font size of the label text.
- Parameter `text_color` (`int`): The text color of the label in hexadecimal format.
- Parameter `bg_color` (`int`): The background color of the label in hexadecimal format.
- Parameter `font`: The font to use for the label text.
- Parameter `url` (`str`): The URL to fetch data from.
- Parameter `period` (`int`): The update period in milliseconds. If set to 0, the label will not update automatically.
- Parameter `enable` (`bool`): Whether to enable automatic updates.
- Parameter `json_key` (`str`): The JSON key to extract from the fetched data.
- Parameter `error_msg` (`str`): The message to display in case of an error.
- Parameter `error_msg_color` (`int`): The text color to use when displaying an error message, in hexadecimal format.

    None

```python
from label_plus import LabelPlus

label_plus0 = LabelPlus("label_plus0", 7, 10, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18, "http://example.com", 3000, True, "title", "error", 0xFF0000)
```

### `deinit`

### `set_update_enable`
Enable or disable automatic updates.

- Parameter `enable` (`bool`): True to enable automatic updates, False to disable.

```python
label_plus0.set_update_enable(True)
```

### `set_update_period`
Set the update period for automatic updates.

- Parameter `period` (`int`): The update period in milliseconds.

```python
label_plus0.set_update_period(5000)
```

### `is_valid_data`
Check if the current data is valid (i.e., not an error message).

- Returns: True if the current data is valid, False otherwise.
- Return type: bool

```python
valid = label_plus0.is_valid_data()
```

### `get_data`
Get the current data displayed on the label.

- Returns: The current data.
- Return type: str

```python
data = label_plus0.get_data()
```

### `setColor`
Sets the text font color of the Label object.

- Parameter `fg_color` (`int`): The text color in hexadecimal format.
- Parameter `bg_color` (`int`): The background color in hexadecimal format.

```python
label_plus0.setColor(0xFFFFFF, 0x000000)
```

### `set_url`

### `update`

### `show_value_of_key`

### `setText(text)`

        Set the text of the LabelPlus widget.

        - Parameter `text` (`str`): The text to set on the label.

```python
label_plus_0.setText("New Text")
```
### `setCursor(x=0, y=0)`

        Sets the starting coordinates of the text cursor in the LabelPlus widget.

        - Parameter `x` (`int`): The x-coordinate of the cursor.
        - Parameter `y` (`int`): The y-coordinate of the cursor.

```python
label_plus_0.setCursor(10, 20)
```
### `setSize(size)`

        Sets the font size of the text in the LabelPlus widget.

        - Parameter `size` (`float`): The font size to set.

```python
label_plus_0.setSize(1.5)
```
### `setFont(font)`

        Sets the font of the text in the LabelPlus widget.

        - Parameter `supports built-in fonts and font files (for example, `.bin` (lvgl binary font format) or `.vlw` (Processing font format)). For the full list of built-in fonts, status, and device support, see` (`font:`): meth:`Display.setFont` . Widgets.FONTS uses the same font as M5.Display.

```python
label_plus_0.setFont(Widgets.FONTS.Montserrat12)
```
### `setVisible(visible)`

        Set the visible property of the LabelPlus widget.

        - Parameter `visible` (`bool`): True to make the label visible, False to hide it.

```python
label_plus_0.setVisible(True)
```
