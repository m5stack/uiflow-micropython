
# M5TextArea

M5TextArea is a widget that can be used to create text input areas in the user interface. It allows users to input and edit multi-line text with support for placeholders, scrolling, and various styling options.

## MicroPython Example

#### basic textarea

This example demonstrates how to add text content to a text box and clear the content of the text box using a button.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time

page0 = None
textarea0 = None
button0 = None

line = None

def button0_clicked_event(event_struct):
    global page0, textarea0, button0, line

    textarea0.set_text("")
    line = 1

def button0_event_handler(event_struct):
    global page0, textarea0, button0, line
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button0_clicked_event(event_struct)
    return

def setup():
    global page0, textarea0, button0, line

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    textarea0 = m5ui.M5TextArea(
        text="",
        placeholder="Placeholder...",
        x=19,
        y=26,
        w=266,
        h=124,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    button0 = m5ui.M5Button(
        text="clear text",
        x=22,
        y=172,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    button0.add_event_cb(button0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    line = 1

def loop():
    global page0, textarea0, button0, line
    M5.update()
    textarea0.add_text(str((str("line") + str(line))))
    time.sleep(1)
    line = (line if isinstance(line, (int, float)) else 0) + 1

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

#### M5TextArea

## `M5TextArea`
Create a text area widget.

- Parameter `text` (`str`): Initial text content of the text area.
- Parameter `placeholder` (`str`): Placeholder text when the text area is empty.
- Parameter `x` (`int`): X position of the text area.
- Parameter `y` (`int`): Y position of the text area.
- Parameter `w` (`int`): Width of the text area.
- Parameter `h` (`int`): Height of the text area.
- Parameter `font` (`lv.font_t`): Font used for the text.
- Parameter `bg_c` (`int`): Background color of the text area.
- Parameter `border_c` (`int`): Border color of the text area.
- Parameter `text_c` (`int`): Text color of the text area.
- Parameter `parent` (`lv.obj`): Parent object of the text area. If not specified, it will be set to the active screen.

### `set_one_line`
Set whether the textarea should be single line or multi-line.

- Parameter `text` (`bool`): True for single line, False for multi-line.
- Returns: None

```python
textarea_0.set_one_line(True)
```

### `set_style_radius`

### `set_max_length`

### `set_flag(flag, value)`

        Set a flag on the object. If `value` is True, the flag is added; if False, the flag is removed.

        - Parameter `flag` (`int`): The flag to set.
        - Parameter `value` (`bool`): If True, the flag is added; if False, the flag is removed.
        - Returns: None

```python
textarea_0.set_flag(lv.obj.FLAG.HIDDEN, True)
```
### `toggle_flag(flag)`

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        - Parameter `flag` (`int`): The flag to toggle.
        - Returns: None

```python
textarea_0.toggle_flag(lv.obj.FLAG.HIDDEN)
```
### `set_state(state, value)`

        Set the state of the textarea. If `value` is True, the state is set; if False, the state is unset.

        - Parameter `state` (`int`): The state to set.
        - Parameter `value` (`bool`): If True, the state is set; if False, the state is unset.
        - Returns: None

```python
textarea_0.set_state(lv.STATE.PRESSED, True)
```
### `toggle_state(state)`

        Toggle the state of the textarea. If the state is set, it is unset; if not set, it is set.

        - Parameter `state` (`int`): The state to toggle.
        - Returns: None

```python
textarea_0.toggle_state(lv.STATE.PRESSED)
```
### `add_event_cb(handler, event, user_data)`

        Add an event callback to the slider. The callback will be called when the specified event occurs.

        - Parameter `handler` (`function`): The callback function to call.
        - Parameter `event` (`int`): The event to listen for.
        - Parameter `user_data` (`Any`): Optional user data to pass to the callback.
        - Returns: None

```python
def textarea_0_ready_event(event_struct):
    global page0, button0
    print("released")

def textarea_0_value_changed_event(event_struct):
    global page0, button0
    print("value changed")

def textarea_0_focused_event(event_struct):
    global page0, button0
    print("focused")

def textarea_0_defocused_event(event_struct):
    global page0, button0
    print("focused")

def textarea_0_event_handler(event_struct):
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        textarea_0_value_changed_event(event_struct)
    elif event == lv.EVENT.READY and True:
        textarea_0_ready_event(event_struct) # 单行模式下才会触发
    elif event == lv.EVENT.FOCUSED:
        textarea_0_focused_event(event_struct)
    elif event == lv.EVENT.DEFOCUSED:
        textarea_0_defocused_event(event_struct)
    return

textarea_0.add_event_cb(textarea_0_event_handler, lv.EVENT.ALL, None)
```
### `set_bg_color(color, opa, part)`

        Set the background color of the textarea.

        - Parameter `color` (`int`): The color to set.
        - Parameter `opa` (`int`): The opacity of the color.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
textarea_0.set_bg_color(lv.color_hex(0xFFFFFF), 255, lv.PART.MAIN | lv.STATE.DEFAULT)
```
### `set_style_radius(radius, part)`

        Set the corner radius of the slider components.

        - Parameter `radius` (`int`): The radius to set.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
slider_0.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)
```
### `set_border_color(color, opa, part)`

        Set the border color of the textarea.

        - Parameter `color` (`int`): The color to set.
        - Parameter `opa` (`int`): The opacity of the color.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
textarea_0.set_border_color(lv.color_hex(0xE0E0E0), 255, lv.PART.MAIN | lv.STATE.DEFAULT)
```
### `set_style_border_width(width, part)`

        Set the border width of the textarea.

        - Parameter `width` (`int`): The width to set.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
textarea_0.set_style_border_width(2, lv.PART.MAIN | lv.STATE.DEFAULT)
```
### `set_placeholder_text(text)`

        Set the placeholder text that appears when the textarea is empty.

        - Parameter `text` (`str`): The placeholder text to set.
        - Returns: None

```python
textarea_0.set_placeholder_text("Enter text here...")
```
### `set_text_color(color, opa, part)`

        Set the color of the text.

        - Parameter `color` (`int`): The color to set.
        - Parameter `opa` (`int`): The opacity of the color.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
textarea_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)
```
### `set_style_text_font(font, part)`

        Set the font of the textarea text.

        - Parameter `font` (`lv.font_t`): The font to set.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
textarea_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN | lv.STATE.DEFAULT)
```
### `set_style_text_align(align, part)`

        Set the text alignment of the textarea.

        - Parameter `align` (`int`): The alignment to set (e.g., lv.TEXT_ALIGN.LEFT, lv.TEXT_ALIGN.CENTER).
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
textarea_0.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN | lv.STATE.DEFAULT)
```
### `set_text(text)`

        Set the text content of the textarea.

        - Parameter `text` (`str`): The text to set.
        - Returns: None

```python
textarea_0.set_text("Hello World")
textarea_0.set_text("") # Clear the text content
```
### `get_text()`

        Get the current text content of the textarea.

        - Returns: The current text content.
        - Return type: str

```python
text = textarea_0.get_text()
```
### `add_text(text)`

        Add text to the current content of the textarea.

        - Parameter `text` (`str`): The text to add.
        - Returns: None

```python
textarea_0.add_text(" Additional text")
```
### `set_max_length(length)`

        Set the maximum length of text that can be entered in the textarea.

        - Parameter `length` (`int`): The maximum length of text.
        - Returns: None

```python
textarea_0.set_max_length(256)
```
### `set_password_mode(en)`

        Set whether the textarea should be in password mode (i.e., characters are hidden).

        - Parameter `en` (`bool`): True to enable password mode, False to disable.
        - Returns: None

```python
textarea_0.set_password_mode(True)
```
### `set_accepted_chars(chars)`

        Set the characters that are accepted in the textarea. Only these characters can be entered.

        - Parameter `chars` (`str`): The string of accepted characters.
        - Returns: None

```python
textarea_0.set_accepted_chars("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
```
### `set_pos(x, y)`

        Set the position of the textarea.

        - Parameter `x` (`int`): The x-coordinate of the textarea.
        - Parameter `y` (`int`): The y-coordinate of the textarea.
        - Returns: None

```python
textarea_0.set_pos(100, 100)
```
### `set_x(x)`

        Set the x-coordinate of the textarea.

        - Parameter `x` (`int`): The x-coordinate of the textarea.
        - Returns: None

```python
textarea_0.set_x(100)
```
### `set_y(y)`

        Set the y-coordinate of the textarea.

        - Parameter `y` (`int`): The y-coordinate of the textarea.
        - Returns: None

```python
textarea_0.set_y(100)
```
### `align_to(obj, align, x, y)`

        Align the textarea to another object.

        - Parameter `obj` (`lv.obj`): The object to align to.
        - Parameter `align` (`int`): The alignment type.
        - Parameter `x` (`int`): The x-offset from the aligned object.
        - Parameter `y` (`int`): The y-offset from the aligned object.
        - Returns: None

```python
textarea_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
```
### `set_size(width, height)`

        Set the size of the textarea.

        - Parameter `width` (`int`): The width of the textarea.
        - Parameter `height` (`int`): The height of the textarea.
        - Returns: None

```python
textarea_0.set_size(200, 100)
```
### `set_width(width)`

        Set the width of the textarea.

        - Parameter `width` (`int`): The width of the textarea.
        - Returns: None

```python
textarea_0.set_width(200)
```
### `set_height(height)`

        Set the height of the textarea.

        - Parameter `height` (`int`): The height of the textarea.
        - Returns: None

```python
textarea_0.set_height(100)
```
### `get_width()`

        Get the width of the textarea.

        - Returns: The width of the textarea.
        - Return type: int

```python
width = textarea_0.get_width()
```
### `get_height()`

        Get the height of the textarea.

        - Returns: The height of the textarea.
        - Return type: int

```python
height = textarea_0.get_height()
```
