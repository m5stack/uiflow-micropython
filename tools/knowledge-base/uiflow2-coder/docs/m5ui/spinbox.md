
# M5Spinbox

M5Spinbox is a widget that provides a numeric input interface with increment and decrement buttons.
It displays a numeric value that can be adjusted by clicking the + and - buttons or by typing directly.
The spinbox supports both integer and floating-point numbers with customizable digit count and decimal precision.

## MicroPython Example

#### basic spinbox

This example demonstrates how to create a spinbox with customizable range and precision settings.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv

page0 = None
spinbox0 = None
label0 = None

def spinbox0_value_changed_event(event_struct):
    global page0, spinbox0, label0
    label0.set_text(str(spinbox0.get_value()))

def spinbox0_event_handler(event_struct):
    global page0, spinbox0, label0
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        spinbox0_value_changed_event(event_struct)
    return

def setup():
    global page0, spinbox0, label0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    spinbox0 = m5ui.M5Spinbox(
        x=60,
        y=100,
        w=200,
        h=40,
        value=50,
        min_value=0,
        max_value=100,
        digit_count=5,
        prec=2,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "label0",
        x=138,
        y=166,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    spinbox0.add_event_cb(spinbox0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    spinbox0.set_border_color(0xFF0000, 255, lv.PART.MAIN | lv.STATE.DEFAULT)

def loop():
    global page0, spinbox0, label0
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

#### M5Spinbox

## `M5Spinbox`
Create a spinbox widget.

- Parameter `x` (`int`): The x position of the spinbox.
- Parameter `y` (`int`): The y position of the spinbox.
- Parameter `w` (`int`): The width of the spinbox.
- Parameter `h` (`int`): The height of the spinbox.
- Parameter `value` (`int`): The initial value of the spinbox.
- Parameter `min_value` (`int`): The minimum value of the spinbox.
- Parameter `max_value` (`int`): The maximum value of the spinbox.
- Parameter `digit_count` (`int`): The number of digits to display.
- Parameter `prec` (`int`): The number of decimal places.
- Parameter `font` (`lv.font_t`): The font to use for the spinbox.
- Parameter `parent` (`lv.obj`): The parent object of the spinbox.

### `set_state`
Set the state of the spinbox. If `value` is True, the state is set; if False, the state is unset.

- Parameter `state` (`int`): The state to set.
- Parameter `value` (`bool`): If True, the state is set; if False, the state is unset.
- Returns: None

```python
spinbox_0.set_state(lv.STATE.DISABLED, True)
```

### `toggle_state`
Toggle the state of the spinbox. If the state is set, it is unset; if not set, it is set.

- Parameter `state` (`int`): The state to toggle.
- Returns: None

```python
spinbox_0.toggle_state(lv.STATE.CHECKED)
```

### `set_size`
Set the size of the spinbox.

- Parameter `width` (`int`): The width of the spinbox.
- Parameter `height` (`int`): The height of the spinbox.
- Returns: None

```python
spinbox_0.set_size(150, 40)
```

### `set_width`
Set the width of the spinbox.

- Parameter `width` (`int`): The width of the spinbox.
- Returns: None

```python
spinbox_0.set_width(180)
```

### `set_height`
Set the height of the spinbox.

- Parameter `height` (`int`): The height of the spinbox.
- Returns: None

```python
spinbox_0.set_height(50)
```

### `add_event_cb`
Add an event callback to the spinbox.

- Parameter `handler` (`function`): The callback function to call.
- Parameter `event` (`int`): The event to listen for.
- Parameter `user_data` (`Any`): Optional user data to pass to the callback.

```python
def spinbox0_value_changed_event(event_struct):
    global page0, spinbox0
    print("value changed:", spinbox0.get_value())

def spinbox0_event_handler(event_struct):
global page0, spinbox0
event = event_struct.code
if event == lv.EVENT.VALUE_CHANGED and True:
    spinbox0_value_changed_event(event_struct)
return

spinbox_0.add_event_cb(spinbox0_event_handler, lv.EVENT.ALL, None)
```

### `set_bg_color`
Set the background color and opacity for a given part of the object.

- Parameter `color` (`int`): The color to set, can be an integer (hex) or a lv.color object.
- Parameter `opa` (`int`): The opacity level (0-255).
- Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
- Returns: None

```python
spinbox0.set_bg_color(0xFF0000, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
```

### `set_border_color`
Set the border color and opacity for a given part of the object.

- Parameter `color` (`int`): The color to set, can be an integer (hex) or a lv.color object.
- Parameter `opa` (`int`): The opacity level (0-255).
- Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
- Returns: None

```python
spinbox0.set_border_color(0xFF0000, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
```

### `set_style_border_width`
Set the border width of the spinbox.

- Parameter `w` (`int`): The border width in pixels.
- Parameter `part` (`int`): The part of the spinbox to apply the border width to, e.g., `lv.PART.MAIN`.
- Returns: None

```python
spinbox0.set_style_border_width(10, lv.PART.MAIN | lv.STATE.DEFAULT)
```

### `set_style_radius`
Set the radius of the spinbox's corners.

- Parameter `radius`: The radius of the corners in pixels.
- Parameter `part`: The part of the spinbox to apply the radius to, e.g., `lv.PART.MAIN`.

```python
dropdown_0.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)
```

### `set_digit_format`
Set the digit format of the spinbox.

- Parameter `digit_count`: The total number of digits in the float representation.
- Type of `digit_count`: int
- Parameter `sep_pos`: The position of the separator.
- Type of `sep_pos`: int

### `set_range`
Set the range of the spinbox.

- Parameter `min_value`: The minimum value of the spinbox.
- Type of `min_value`: float | int
- Parameter `max_value`: The maximum value of the spinbox.
- Type of `max_value`: float | int

```python
spinbox0.set_range(0, 100)
```

### `set_value`
Set the value of the spinbox.

- Parameter `value`: The value to set.
- Type of `value`: float | int

```python
spinbox0.set_value(50)
```

### `get_value`
Get the current value of the spinbox.

- Returns: The current value.
- Return type: float | int

```python
spinbox0.get_value()
```

### `set_step`
Set the step value for the spinbox.

- Parameter `step`: The step value to set.
- Type of `step`: float | int

```python
spinbox0.set_step(1)
spinbox0.set_step(0.1)
```

### `value2raw`
Convert a float to an integer by removing the decimal point.

- Parameter `value` (`float`): The float value to convert.
- Returns: The converted integer value.
- Return type: int

### `raw2value`
Convert an integer to a float with a specified decimal point position.

- Parameter `value` (`int`): The integer value to convert.
- Parameter `digit_count` (`int`): The total number of digits in the float representation.
- Parameter `sep_pos` (`int`): The position of the decimal point.
- Returns: The converted float value.
- Return type: float

### `set_flag(flag, value)`

        Set a flag on the object. If `value` is True, the flag is added; if False, the flag is removed.

        - Parameter `flag` (`int`): The flag to set.
        - Parameter `value` (`bool`): If True, the flag is added; if False, the flag is removed.
        - Returns: None

```python
spinbox_0.set_flag(lv.obj.FLAG.HIDDEN, True)
```
### `toggle_flag(flag)`

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        - Parameter `flag` (`int`): The flag to toggle.
        - Returns: None

```python
spinbox_0.toggle_flag(lv.obj.FLAG.HIDDEN)
```
### `set_pos(x, y)`

        Set the position of the spinbox.

        - Parameter `x` (`int`): The x-coordinate of the spinbox.
        - Parameter `y` (`int`): The y-coordinate of the spinbox.
        - Returns: None

```python
spinbox_0.set_pos(100, 200)
```
### `set_x(x)`

        Set the x-coordinate of the spinbox.

        - Parameter `x` (`int`): The x-coordinate of the spinbox.
        - Returns: None

```python
spinbox_0.set_x(150)
```
### `set_y(y)`

        Set the y-coordinate of the spinbox.

        - Parameter `y` (`int`): The y-coordinate of the spinbox.
        - Returns: None

```python
spinbox_0.set_y(250)
```
### `get_width()`

        Get the width of the spinbox.

        - Returns: The width of the spinbox.
        - Return type: int

```python
width = spinbox_0.get_width()
```
### `get_height()`

        Get the height of the spinbox.

        - Returns: The height of the spinbox.
        - Return type: int

```python
height = spinbox_0.get_height()
```
### `align_to(obj, align, x, y)`

        Align the spinbox to another object.

        - Parameter `obj` (`lv.obj`): The object to align to.
        - Parameter `align` (`int`): The alignment type.
        - Parameter `x` (`int`): The x-offset from the aligned object.
        - Parameter `y` (`int`): The y-offset from the aligned object.
        - Returns: None

```python
spinbox_0.align_to(label_0, lv.ALIGN.OUT_BOTTOM_MID, 0, 10)
```
