
# M5Window

M5Window is a widget that can be used to create windows in the user interface.

## MicroPython Example

#### window event

This example creates a window and associates it with events.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv

page0 = None
window0 = None
btn_lav = None
title_fmk = None
btn_nzk = None
btn_dkc = None
label_wgy = None

def btn_lav_clicked_event(event_struct):
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy

    label_wgy.set_text(str("Left Btn was clicked"))

def btn_nzk_clicked_event(event_struct):
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy

    label_wgy.set_text(str("Right Btn was clicked"))

def btn_dkc_clicked_event(event_struct):
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy

    window0.set_flag(lv.obj.FLAG.HIDDEN, True)

def btn_lav_event_handler(event_struct):
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_lav_clicked_event(event_struct)
    return

def btn_nzk_event_handler(event_struct):
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_nzk_clicked_event(event_struct)
    return

def btn_dkc_event_handler(event_struct):
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_dkc_clicked_event(event_struct)
    return

def setup():
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    window0 = m5ui.M5Win(x=0, y=0, w=320, h=240, parent=page0)
    btn_lav = window0.add_button(icon=lv.SYMBOL.LEFT, w=40)
    title_fmk = window0.add_title("This is a window")
    btn_nzk = window0.add_button(icon=lv.SYMBOL.RIGHT, w=40)
    btn_dkc = window0.add_button(icon=lv.SYMBOL.CLOSE, w=60)
    label_wgy = window0.add_text("This is label_wgy", x=0, y=0)

    btn_lav.add_event_cb(btn_lav_event_handler, lv.EVENT.ALL, None)
    btn_nzk.add_event_cb(btn_nzk_event_handler, lv.EVENT.ALL, None)
    btn_dkc.add_event_cb(btn_dkc_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()

def loop():
    global page0, window0, btn_lav, title_fmk, btn_nzk, btn_dkc, label_wgy
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

#### M5Win

## `M5Win`
Create a window object.

- Parameter `x` (`int`): The x position of the window.
- Parameter `y` (`int`): The y position of the window.
- Parameter `w` (`int`): The width of the window.
- Parameter `h` (`int`): The height of the window.
- Parameter `parent` (`lv.obj`): The parent object to attach the window to. If not specified, the window will be attached to the default screen.

    None

```python
from m5ui import M5Win
import lvgl as lv

m5ui.init()
win0 = M5Win(x=120, y=80, w=60, h=30, parent=page0)
```

### `add_title`
Add a title label to the window.

- Parameter `text` (`str`): The text to display on the window.
- Parameter `text_c` (`int`): The text color of the label in hexadecimal format.
- Parameter `text_opa` (`int`): The text opacity of the label (0-255).
- Parameter `bg_c` (`int`): The background color of the label in hexadecimal format.
- Parameter `bg_opa` (`int`): The background opacity of the label (0-255).
- Parameter `font` (`lv.font`): The font to use for the label.
- Returns: The created label object `m5ui.M5Label <m5ui.M5Label>`.
- Return type: lv.obj

```python
win0.add_title("A title", text_c=0x212121, text_opa=255, bg_c=0xE0E0E0, bg_opa=255, font=lv.font_montserrat_14)
```

### `add_text`
Add a text label to the window.

- Parameter `text` (`str`): The text to display on the window.
- Parameter `x` (`int`): The x position of the label.
- Parameter `y` (`int`): The y position of the label.
- Parameter `text_c` (`int`): The text color of the label in hexadecimal format.
- Parameter `text_opa` (`int`): The text opacity of the label (0-255).
- Parameter `bg_c` (`int`): The background color of the label in hexadecimal format.
- Parameter `bg_opa` (`int`): The background opacity of the label (0-255).
- Parameter `font` (`lv.font`): The font to use for the label.
- Returns: The created label object `m5ui.M5Label <m5ui.M5Label>`.
- Return type: lv.obj

```python
win0.add_text("A title", text_c=0x212121, text_opa=255, bg_c=0xF6F6F6, bg_opa=255, font=lv.font_montserrat_14)
```

### `add_button`
Add a button to the window.

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
win0.add_button(icon=lv.SYMBOL.BULLET, text_c=0xffffff, text_opa=255, bg_c=0x2196f3, bg_opa=255, font=lv.font_montserrat_14)

win0.add_button(text='M5', text_c=0xffffff, text_opa=255, bg_c=0x2196f3, bg_opa=255, font=lv.font_montserrat_14)
```

### `delete()`

        Delete the item from the window.

```python
label_0.delete()

button_0.delete()

text_0.delete()
```
### `set_text(txt)`

        Set text of the window button/label/title.

        - Parameter `txt` (`str`): The text to set for the window button/label/title.
        - Returns: None

```python
button_0.set_text("Select an option")

label_0.set_text("M5Stack")

title_0.set_text("Hello M5Stack")
```
### `set_style_text_font(font, part)`

        Set the font of the window button text.

        - Parameter `font` (`lv.lv_font_t`): The font to set.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
button_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN | lv.STATE.DEFAULT)
```
### `set_text_color(color, opa, part)`

        Set the color of the window button/label/title.

        - Parameter `color` (`int`): The color to set.
        - Parameter `opa` (`int`): The opacity of the color.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
button_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

label_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

title_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)
```
### `set_bg_color(color, opa, part)`

        Set the background color of the window button/label/title.

        - Parameter `color` (`int`): The color to set.
        - Parameter `opa` (`int`): The opacity of the color.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
button_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

label_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

title_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)
```
### `set_long_mode(mode)`

        Set the long mode of the window label/title.

        - Parameter `mode` (`int`): The long mode to set.

```python
label_0.set_long_mode(lv.label.LONG_MODE.WRAP)
```
### `set_flag(flag, value)`

        Set a flag on the object. If `value` is True, the flag is added; if False, the flag is removed.

        - Parameter `flag` (`int`): The flag to set.
        - Parameter `value` (`bool`): If True, the flag is added; if False, the flag is removed.

```python
window_0.set_flag(lv.obj.FLAG.HIDDEN, True)
```
### `set_pos(x, y)`

        Set the position of the window.

        - Parameter `x` (`int`): The x-coordinate of the window.
        - Parameter `y` (`int`): The y-coordinate of the window.

```python
window_0.set_pos(100, 100)
```
### `set_x(x)`

        Set the x-coordinate of the window.

        - Parameter `x` (`int`): The x-coordinate of the window.

```python
window_0.set_x(100)
```
### `set_y(y)`

        Set the y-coordinate of the window.

        - Parameter `y` (`int`): The y-coordinate of the window.

```python
window_0.set_y(100)
```
### `set_size(width, height)`

        Set the size of the window.

        - Parameter `width` (`int`): The width of the window.
        - Parameter `height` (`int`): The height of the window.
        - Returns: None

```python
window_0.set_size(100, 50)
```
### `align_to(obj, align, x, y)`

        Align the windowto another object.

        - Parameter `obj` (`lv.obj`): The object to align to.
        - Parameter `align` (`int`): The alignment type.
        - Parameter `x` (`int`): The x-offset from the aligned object.
        - Parameter `y` (`int`): The y-offset from the aligned object.

```python
window_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
```
### `set_state(state, value)`

        Set the state of the bar. If `value` is True, the state is set; if False, the state is unset.

        - Parameter `state` (`int`): The state to set.
        - Parameter `value` (`bool`): If True, the state is set; if False, the state is unset.
        - Returns: None

```python
window_0.set_state(lv.STATE.PRESSED, True)
```
### `toggle_flag(flag)`

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        - Parameter `flag` (`int`): The flag to toggle.
        - Returns: None

```python
window_0.toggle_flag(lv.obj.FLAG.HIDDEN)
```
### `set_style_radius(radius, part)`

        Set the corner radius of the window button.

        - Parameter `radius` (`int`): The radius to set.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
button_0.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)
```
### `set_shadow(color, opa, align, offset_x, offset_y)`

        Set a shadow for the label/title.

        - Parameter `color` (`int`): The color of the shadow in hexadecimal format or an integer.
        - Parameter `opa` (`int`): The opacity of the shadow (0-255).
        - Parameter `align` (`int`): The alignment of the shadow relative to the label/title.
        - Parameter `offset_x` (`int`): The horizontal offset of the shadow.
        - Parameter `offset_y` (`int`): The vertical offset of the shadow.
        - Returns: None

```python
label_0.set_shadow(color=0x000000, opa=128, align=lv.ALIGN.BOTTOM_RIGHT, offset_x=5, offset_y=5)
```
### `unset_shadow()`

        Remove the shadow from the label/title.

```python
label_0.unset_shadow()
```
### `get_text()`

        Get the text of the button/label/title.

        - Returns: The text of the button/label/title.
        - Return type: str

```python
button_0.get_text()

label_0.get_text()

text_0.get_text()
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
    global page0, window_0, label_lkg, btn_ono, btn_pjm, label0

    print('hello M5')

def btn_ono_event_handler(event_struct):
    global page0, window_0, label_lkg, btn_ono, btn_pjm, label0
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_ono_clicked_event(event_struct)
    return

btn_ono.add_event_cb(btn_ono_event_handler, lv.EVENT.ALL, None)
```
