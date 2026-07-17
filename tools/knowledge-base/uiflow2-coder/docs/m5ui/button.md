
# M5Button

M5Button is a widget that can be used to create buttons in the user interface. It can be used to trigger actions when clicked.

> Important: **Available Fonts**: For `m5ui` widgets, use LVGL fonts such as `lv.font_montserrat_12`, `14`, `16`, `18`, `24`, `40`, `44`, and `48`. Some builds, such as Tab5, also include `20`, `22`, `30`, and `36`. Check optional sizes with `hasattr()` before using them in cross-board examples. The Alibaba CJK fonts are `M5.Lcd.FONTS` fonts for `M5.Lcd` / `M5.Widgets` drawing.
## MicroPython Example

#### event button

This example creates a button that triggers an event when clicked.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv

page0 = None
button0 = None
label0 = None

def button0_pressed_event(event_struct):
    global page0, button0, label0

    label0.set_text(str("pressed"))

def button0_released_event(event_struct):
    global page0, button0, label0

    label0.set_text(str("released"))

def button0_event_handler(event_struct):
    global page0, button0, label0
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button0_pressed_event(event_struct)
    if event == lv.EVENT.RELEASED and True:
        button0_released_event(event_struct)
    return

def setup():
    global page0, button0, label0

    M5.begin()
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    button0 = m5ui.M5Button(
        text="click me",
        x=117,
        y=102,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "label0",
        x=136,
        y=33,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    button0.add_event_cb(button0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()

def loop():
    global page0, button0, label0
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

#### M5Button

## `M5Button`
Create a button object.

- Parameter `text` (`str`): The text to display on the button.
- Parameter `x` (`int`): The x position of the button.
- Parameter `y` (`int`): The y position of the button.
- Parameter `w` (`int`): The width of the button. when set to 0, the button will automatically size to fit the text.
- Parameter `h` (`int`): The height of the button. when set to 0, the button will automatically size to fit the text.
- Parameter `bg_c` (`int`): The background color of the button in hexadecimal format.
- Parameter `text_c` (`int`): The text color of the button in hexadecimal format.
- Parameter `font` (`lv.lv_font_t`): The font to use for the button text.
- Parameter `parent` (`lv.obj`): The parent object to attach the button to. If not specified, the button will be attached to the default screen.

    None

```python
from m5ui import M5Button
import lvgl as lv

m5ui.init()
button_0 = M5Button(text="Click Me", x=10, y=10, bg_c=0x2196F3, text_c=0xFFFFFF, parent=page0)
```

### `set_btn_text`
Set the text of the button.

- Parameter `text` (`str`): The text to set on the button.

```python
button_0.set_btn_text("Click Me")
```

### `set_style_radius`

### `get_btn_text`
Get the text of the button.

- Returns: The text of the button.
- Return type: str

```python
text = button_0.get_btn_text()
```

### `set_flag`

### `toggle_flag`

### `set_size`

### `set_height`

### `set_width`

### `set_shadow`

### `unset_shadow`

### `set_pressed_effect`

### `set_flag(flag, value)`

        Set a flag on the object. If `value` is True, the flag is added; if False, the flag is removed.

        - Parameter `flag` (`int`): The flag to set.
        - Parameter `value` (`bool`): If True, the flag is added; if False, the flag is removed.
        - Returns: None

```python
button_0.set_flag(lv.obj.FLAG.HIDDEN, True)
```
### `toggle_flag(flag)`

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        - Parameter `flag` (`int`): The flag to toggle.
        - Returns: None

```python
button_0.toggle_flag(lv.obj.FLAG.HIDDEN)
```
### `set_state(state, value)`

        Set the state of the button. If `value` is True, the state is set; if False, the state is unset.

        - Parameter `state` (`int`): The state to set.
        - Parameter `value` (`bool`): If True, the state is set; if False, the state is unset.
        - Returns: None

```python
button_0.set_state(lv.STATE.PRESSED, True)
```
### `toggle_state(state)`

        Toggle the state of the button. If the state is set, it is unset; if not set, it is set.

        - Parameter `state` (`int`): The state to toggle.
        - Returns: None

```python
button_0.toggle_state(lv.STATE.PRESSED)
```
### `set_style_text_font(font, part)`

        Set the font of the button text.

        - Parameter `font` (`lv.lv_font_t`): The font to set.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
button_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN | lv.STATE.DEFAULT)
```
### `set_text_color(color, opa, part)`

        Set the color of the button text.

        - Parameter `color` (`int`): The color to set.
        - Parameter `opa` (`int`): The opacity of the color. The value should be between 0 (transparent) and 255 (opaque).
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
button_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)
button_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.PRESSED)
```
### `set_bg_color(color, opa, part)`

        Set the background color of the button.

        - Parameter `color` (`int`): The color to set.
        - Parameter `opa` (`int`): The opacity of the color. The value should be between 0 (transparent) and 255 (opaque).
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
button_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)
button_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.PRESSED)
```
### `set_pos(x, y)`

        Set the position of the button.

        - Parameter `x` (`int`): The x-coordinate of the button.
        - Parameter `y` (`int`): The y-coordinate of the button.
        - Returns: None

```python
button_0.set_pos(100, 100)
```
### `set_x(x)`

        Set the x-coordinate of the button.

        - Parameter `x` (`int`): The x-coordinate of the button.
        - Returns: None

```python
button_0.set_x(100)
```
### `set_y(y)`

        Set the y-coordinate of the button.

        - Parameter `y` (`int`): The y-coordinate of the button.
        - Returns: None

```python
button_0.set_y(100)
```
### `set_size(width, height)`

        Set the size of the button.

        - Parameter `width` (`int`): The width of the button.
        - Parameter `height` (`int`): The height of the button.
        - Returns: None

```python
button_0.set_size(100, 50)
```
### `set_width(width)`

        Set the width of the button.

        - Parameter `width` (`int`): The width of the button.
        - Returns: None

```python
button_0.set_width(100)
```
### `get_width()`

        Get the width of the button.

        - Returns: The width of the button.
        - Return type: int

```python
button_0.get_width()
```
### `set_height(height)`

        Set the height of the button.

        - Parameter `height` (`int`): The height of the button.
        - Returns: None

```python
button_0.set_height(50)
```
### `get_height()`

        Get the height of the button.

        - Returns: The height of the button.
        - Return type: int

```python
button_0.get_height()
```
### `align_to(obj, align, x, y)`

        Align the button to another object.

        - Parameter `obj` (`lv.obj`): The object to align to.
        - Parameter `align` (`int`): The alignment type.
        - Parameter `x` (`int`): The x-offset from the aligned object.
        - Parameter `y` (`int`): The y-offset from the aligned object.
        - Returns: None

```python
button_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
```
### `set_style_radius(radius, part)`

        Set the corner radius of the button.

        - Parameter `radius` (`int`): The radius to set.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
button_0.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)
```
### `add_event_cb(handler, event, user_data)`

        Add an event callback to the button. The callback will be called when the specified event occurs.

        - Parameter `handler` (`function`): The callback function to call.
        - Parameter `event` (`int`): The event to listen for.
        - Parameter `user_data` (`Any`): Optional user data to pass to the callback.
        - Returns: None

```python
def button_0_pressed_event(event_struct):
    global button_0
    button_0.set_bg_color(0x000000, 255, 0)

def button_0_released_event(event_struct):
    global button_0
    button_0.set_bg_color(0xffffff, 255, 0)

def button_0_clicked_event(event_struct):
    global button_0
    button_0.set_bg_color(0x000000, 255, 0)

def button_0_event_handler(event_struct):
    global button_0
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button_0_pressed_event(event_struct)
    if event == lv.EVENT.RELEASED and True:
        button_0_released_event(event_struct)
    if event == lv.EVENT.CLICKED and True:
        button_0_clicked_event(event_struct)
    if event == lv.EVENT.LONG_PRESSED and True:
        button_0_long_pressed_event(event_struct)
    return

page_0.add_event_cb(button_0_event_handler, lv.EVENT.ALL, None)
```
