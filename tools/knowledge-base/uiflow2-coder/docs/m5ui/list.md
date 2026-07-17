
# M5List

M5List is a widget that can be used to create lists in user interfaces. It is basically a rectangle with vertical layout to which Buttons and Text can be added.

## MicroPython Example

#### list example

This example demonstrates how to create a list that displays a series of items.

```python
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

## **API**

#### M5List

## `M5List`
Create a list object.

- Parameter `x` (`int`): The x position of the list.
- Parameter `y` (`int`): The y position of the list.
- Parameter `w` (`int`): The width of the list.
- Parameter `h` (`int`): The height of the list.
- Parameter `parent` (`lv.obj`): The parent object to attach the list to. If not specified, the list will be attached to the default screen.

    None

```python
from m5ui import M5List
import lvgl as lv

m5ui.init()
list_0 = M5List(x=120, y=80, w=60, h=30, parent=page0)
```

### `add_text`
Add a text label to the list.

- Parameter `text` (`str`): The text to display on the label.
- Parameter `text_c` (`int`): The text color of the label in hexadecimal format.
- Parameter `text_opa` (`int`): The text opacity of the label (0-255).
- Parameter `bg_c` (`int`): The background color of the label in hexadecimal format.
- Parameter `bg_opa` (`int`): The background opacity of the label (0-255).
- Parameter `font` (`lv.font`): The font to use for the label.
- Returns: The created label object `m5ui.M5Label <m5ui.M5Label>`.
- Return type: lv.obj

```python
list_0.add_text("Item 1", text_c=0x000000, text_opa=255, bg_c=0xFFFFFF, bg_opa=255, font=lv.font_montserrat_14)
```

### `add_button`
Add a button to the list.

- Parameter `icon` (`int`): The icon to display on the button.
- Parameter `text` (`str`): The text to display on the button.
- Parameter `h` (`int`): The height of the button.
- Parameter `bg_c` (`int`): The background color of the button in hexadecimal format.
- Parameter `bg_opa` (`int`): The background opacity of the button (0-255).
- Parameter `text_c` (`int`): The text color of the button in hexadecimal format.
- Parameter `text_opa` (`int`): The text opacity of the button (0-255).
- Parameter `font` (`lv.font`): The font to use for the button text.
- Returns: The created button object `m5ui.M5Button <m5ui.M5Button>`.
- Return type: lv.obj

```python
list_0.add_button(lv.SYMBOL.BULLET, text="Home", h=40, bg_c=0xFFFFFF, text_c=0x000000, font=lv.font_montserrat_14)
```

### `move_background()`

        Move the background of the list to the end.

```python
button_0.move_background()
text_0.move_background()
```
### `move_foreground()`

        Move the foreground of the list to the end.

```python
button_0.move_foreground()
text_0.move_foreground()
```
### `move_to_index(index)`

        Move the item at the specified index to the end of the list.

```python
button_0.move_to_index(0)
text_0.move_to_index(1)
```
### `delete()`

        Delete the item from the list.

```python
button_0.delete()
text_0.delete()
```
