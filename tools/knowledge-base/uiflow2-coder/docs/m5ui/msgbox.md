
# M5Msgbox

M5Msgbox is a widget that can be used to create msgboxes in the user interface.

## MicroPython Example

#### msgbox event

This example creates msgbox and associated with events.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv

page0 = None
msgbox0 = None
label_sfu = None
btn_apply = None
btn_cancel = None

import random

def btn_apply_clicked_event(event_struct):
    global page0, msgbox0, label_sfu, btn_apply, btn_cancel

    label_sfu.set_text(str((str("Hello ") + str((random.randint(1, 100))))))

def btn_cancel_clicked_event(event_struct):
    global page0, msgbox0, label_sfu, btn_apply, btn_cancel

    btn_apply.toggle_flag(lv.obj.FLAG.HIDDEN)

def btn_apply_event_handler(event_struct):
    global page0, msgbox0, label_sfu, btn_apply, btn_cancel
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_apply_clicked_event(event_struct)
    return

def btn_cancel_event_handler(event_struct):
    global page0, msgbox0, label_sfu, btn_apply, btn_cancel
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_cancel_clicked_event(event_struct)
    return

def setup():
    global page0, msgbox0, label_sfu, btn_apply, btn_cancel

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    msgbox0 = m5ui.M5Msgbox(title="Message Box", x=0, y=0, w=320, h=240, parent=page0)
    label_sfu = msgbox0.add_text("This is label_sfu")
    btn_apply = msgbox0.add_button(text="Apply", option="footer")
    btn_cancel = msgbox0.add_button(text="Cancel", option="footer")
    msgbox0.add_close_button()

    btn_apply.add_event_cb(btn_apply_event_handler, lv.EVENT.ALL, None)
    btn_cancel.add_event_cb(btn_cancel_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()

def loop():
    global page0, msgbox0, label_sfu, btn_apply, btn_cancel
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

#### M5Msgbox

## `M5Msgbox`
Create a msgbox object.

- Parameter `title` (`str`): The title of the msgbox.
- Parameter `x` (`int`): The x-coordinate of the msgbox.
- Parameter `y` (`int`): The y-coordinate of the msgbox.
- Parameter `w` (`int`): The width of the msgbox.
- Parameter `h` (`int`): The height of the msgbox.
- Parameter `parent` (`lv.obj`): The parent object to attach the msgbox to. If not specified, the msgbox will be attached to the default screen.

```python
from m5ui import M5Msgbox
import lvgl as lv

m5ui.init()
msgbox_0 = M5Msgbox(
    title="msgbox",
    x=0,
    y=0,
    w=320,
    h=240,
    parent=page0,
)
```

### `add_text`
Add a text label to the msgbox.

- Parameter `text` (`str`): The text to display.
- Parameter `text_c` (`int`): The text color in hexadecimal format.
- Parameter `text_opa` (`int`): The text opacity (0-255).
- Parameter `bg_c` (`int`): The background color in hexadecimal format.
- Parameter `bg_opa` (`int`): The background opacity (0-255).
- Parameter `font` (`lv.font`): The font to use for the text.

- Returns: The created label object.
- Return type: m5ui.M5Label

```python
text0 = msgbox_0.add_text(
    text="Hello World",
    text_c=0x212121,
    text_opa=255,
    bg_c=0xFFFFFF,
    bg_opa=255,
    font=lv.font_montserrat_14,
)
```

### `add_button`
Add a button to the msgbox.

- Parameter `icon` (`str`): The icon to display on the button.
- Parameter `text` (`str`): The text to display on the button.
- Parameter `bg_c` (`int`): The background color in hexadecimal format.
- Parameter `bg_opa` (`int`): The background opacity (0-255).
- Parameter `text_c` (`int`): The text color in hexadecimal format.
- Parameter `text_opa` (`int`): The text opacity (0-255).
- Parameter `font` (`lv.font`): The font to use for the button text.
- Parameter `option` (`str`): The position of the button ("header" or "footer").

- Returns: The created button object.
- Return type: m5ui.M5Button

```python
button0 = msgbox_0.add_button(
    icon=None,
    text="OK",
    bg_c=0x2196F3,
    bg_opa=255,
    text_c=0xFFFFFF,
    text_opa=255,
    font=lv.font_montserrat_14,
    option="footer",
)
```

### `add_close_button()`

        Add a close button to the msgboxheader.

        - Returns: None

```python
msgbox_0.add_close_button()
```
### `delete()`

        Delete the item from the msgbox.

```python
button_0.delete()
text_0.delete()
```
### `set_text(txt)`

        Set text of the msgbox button/label.

        - Parameter `txt` (`str`): The text to set for the msgbox button/label.
        - Returns: None

```python
button_0.set_text("Select an option")

label_0.set_text("M5Stack")
```
### `set_style_text_font(font, part)`

        Set the font of the msgbox button/label text.

        - Parameter `font` (`lv.lv_font_t`): The font to set.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
label_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN | lv.STATE.DEFAULT)

button_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN | lv.STATE.DEFAULT)
```
### `set_text_color(color, opa, part)`

        Set the color of the msgbox button/label.

        - Parameter `color` (`int`): The color to set.
        - Parameter `opa` (`int`): The opacity of the color.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
button_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

label_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)
```
### `set_bg_color(color, opa, part)`

        Set the background color of the msgbox label.

        - Parameter `color` (`int`): The color to set.
        - Parameter `opa` (`int`): The opacity of the color.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
button_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

label_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)
```
### `set_long_mode(mode)`

        Set the long mode of the msgbox label.

        - Parameter `mode` (`int`): The long mode to set.

```python
label_0.set_long_mode(lv.label.LONG_MODE.WRAP)
```
### `set_flag(flag, value)`

        Set a flag on the object. If `value` is True, the flag is added; if False, the flag is removed.

        - Parameter `flag` (`int`): The flag to set.
        - Parameter `value` (`bool`): If True, the flag is added; if False, the flag is removed.

```python
msgbox_0.set_flag(lv.obj.FLAG.HIDDEN, True)
```
### `set_pos(x, y)`

        Set the position of the msgbox.

        - Parameter `x` (`int`): The x-coordinate of the msgbox.
        - Parameter `y` (`int`): The y-coordinate of the msgbox.

```python
msgbox_0.set_pos(100, 100)
```
### `set_x(x)`

        Set the x-coordinate of the msgbox.

        - Parameter `x` (`int`): The x-coordinate of the msgbox.

```python
msgbox_0.set_x(100)
```
### `set_y(y)`

        Set the y-coordinate of the msgbox.

        - Parameter `y` (`int`): The y-coordinate of the msgbox.

```python
msgbox_0.set_y(100)
```
### `set_size(width, height)`

        Set the size of the msgbox.

        - Parameter `width` (`int`): The width of the msgbox.
        - Parameter `height` (`int`): The height of the msgbox.
        - Returns: None

```python
msgbox_0.set_size(100, 50)
```
### `align_to(obj, align, x, y)`

        Align the msgboxto another object.

        - Parameter `obj` (`lv.obj`): The object to align to.
        - Parameter `align` (`int`): The alignment type.
        - Parameter `x` (`int`): The x-offset from the aligned object.
        - Parameter `y` (`int`): The y-offset from the aligned object.

```python
msgbox_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
```
### `set_state(state, value)`

        Set the state of the bar. If `value` is True, the state is set; if False, the state is unset.

        - Parameter `state` (`int`): The state to set.
        - Parameter `value` (`bool`): If True, the state is set; if False, the state is unset.
        - Returns: None

```python
msgbox_0.set_state(lv.STATE.PRESSED, True)
```
### `toggle_flag(flag)`

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        - Parameter `flag` (`int`): The flag to toggle.
        - Returns: None

```python
msgbox_0.toggle_flag(lv.obj.FLAG.HIDDEN)
```
### `set_style_radius(radius, part)`

        Set the corner radius of the msgbox button.

        - Parameter `radius` (`int`): The radius to set.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
button_0.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)
```
### `set_shadow(color, opa, align, offset_x, offset_y)`

        Set a shadow for the label.

        - Parameter `color` (`int`): The color of the shadow in hexadecimal format or an integer.
        - Parameter `opa` (`int`): The opacity of the shadow (0-255).
        - Parameter `align` (`int`): The alignment of the shadow relative to the label.
        - Parameter `offset_x` (`int`): The horizontal offset of the shadow.
        - Parameter `offset_y` (`int`): The vertical offset of the shadow.
        - Returns: None

```python
label_0.set_shadow(color=0x000000, opa=128, align=lv.ALIGN.BOTTOM_RIGHT, offset_x=5, offset_y=5)
```
### `unset_shadow()`

        Remove the shadow from the label.

```python
label_0.unset_shadow()
```
### `get_text()`

        Get the text of the label.

        - Returns: The text of the label.
        - Return type: str

```python
label_0.get_text()
button_0.get_text()
```
### `toggle_state(state)`

        Toggle the state of the button. If the state is set, it is unset; if not set, it is set.

        - Parameter `state` (`int`): The state to toggle.
        - Returns: None

```python
button_0.toggle_state(lv.STATE.PRESSED)
```
### `add_event_cb(handler, event, user_data)`

        Add an event callback to the button. The callback will be called when the specified event occurs.

        - Parameter `handler` (`function`): The callback function to call.
        - Parameter `event` (`int`): The event to listen for.
        - Parameter `user_data` (`Any`): Optional user data to pass to the callback.
        - Returns: None

```python
def btn_ono_clicked_event(event_struct):
    global page0, msgbox_0, label_lkg, btn_ono, btn_pjm, label0

    print('hello M5')

def btn_ono_event_handler(event_struct):
    global page0, msgbox_0, label_lkg, btn_ono, btn_pjm, label0
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_ono_clicked_event(event_struct)
    return

btn_ono.add_event_cb(btn_ono_event_handler, lv.EVENT.ALL, None)
```
