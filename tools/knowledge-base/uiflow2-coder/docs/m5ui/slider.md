
# M5Slider

M5Slider is a widget that can be used to create sliders in the user interface. It allows users to select a value from a range by dragging a handle along a track.

## MicroPython Example

#### basic slider

This example creates a basic slider that can be used to select values from 0 to 100.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv

page0 = None
slider0 = None
label0 = None

def slider0_value_changed_event(event_struct):
    global page0, slider0, label0
    label0.set_text(str(slider0.get_value()))

def slider0_event_handler(event_struct):
    global page0, slider0, label0
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        slider0_value_changed_event(event_struct)
    return

def setup():
    global page0, slider0, label0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    slider0 = m5ui.M5Slider(
        x=60,
        y=110,
        w=200,
        h=19,
        mode=lv.slider.MODE.NORMAL,
        min_value=0,
        max_value=100,
        value=25,
        bg_c=0x2193F3,
        color=0x2193F3,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "25",
        x=151,
        y=142,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    slider0.add_event_cb(slider0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()

def loop():
    global page0, slider0, label0
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

#### M5Slider

## `M5Slider`
Create a slider widget.

- Parameter `x`: The x position of the slider.
- Parameter `y`: The y position of the slider.
- Parameter `w`: The width of the slider.
- Parameter `h`: The height of the slider.
- Parameter `mode`: only `lv.slider.MODE.NORMAL` is supported.
- Parameter `min_value`: The minimum value of the slider.
- Parameter `max_value`: The maximum value of the slider.
- Parameter `value`: The initial value of the slider.
- Parameter `bg_c`: The background color of the slider.
- Parameter `color`: The color of the slider indicator.
- Parameter `parent`: The parent object of the slider. If not specified, it will be set to the active screen.

    None

```python
from m5ui import M5Slider
import lvgl as lv

slider_0 = M5Slider(x=50, y=50, w=200, h=20, min_value=0, max_value=100, value=25)
```

### `set_value`
Set the value of the slider.

- Parameter `value` (`int`): The value to set.
- Parameter `anim` (`bool`): Whether to animate the change.
- Returns: None

```python
slider_0.set_value(50, True)
```

### `set_range`
Set the range of the slider.

- Parameter `min_value` (`int`): The minimum value of the range.
- Parameter `max_value` (`int`): The maximum value of the range.
- Returns: None

```python
slider_0.set_range(0, 200)
```

### `set_style_radius`

### `set_flag(flag, value)`

        Set a flag on the object. If `value` is True, the flag is added; if False, the flag is removed.

        - Parameter `flag` (`int`): The flag to set.
        - Parameter `value` (`bool`): If True, the flag is added; if False, the flag is removed.
        - Returns: None

```python
slider_0.set_flag(lv.obj.FLAG.HIDDEN, True)
```
### `toggle_flag(flag)`

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        - Parameter `flag` (`int`): The flag to toggle.
        - Returns: None

```python
slider_0.toggle_flag(lv.obj.FLAG.HIDDEN)
```
### `set_state(state, value)`

        Set the state of the slider. If `value` is True, the state is set; if False, the state is unset.

        - Parameter `state` (`int`): The state to set.
        - Parameter `value` (`bool`): If True, the state is set; if False, the state is unset.
        - Returns: None

```python
slider_0.set_state(lv.STATE.PRESSED, True)
```
### `toggle_state(state)`

        Toggle the state of the slider. If the state is set, it is unset; if not set, it is set.

        - Parameter `state` (`int`): The state to toggle.
        - Returns: None

```python
slider_0.toggle_state(lv.STATE.PRESSED)
```
### `add_event_cb(handler, event, user_data)`

        Add an event callback to the slider. The callback will be called when the specified event occurs.

        - Parameter `handler` (`function`): The callback function to call.
        - Parameter `event` (`int`): The event to listen for.
        - Parameter `user_data` (`Any`): Optional user data to pass to the callback.
        - Returns: None

```python
def slider_0_value_changed_event(event_struct):
    global slider_0
    value = slider_0.get_value()
    print(f"Slider value changed to: {value}")

def slider_0_event_handler(event_struct):
    global slider_0
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED:
        slider_0_value_changed_event(event_struct)
    return

slider_0.add_event_cb(slider_0_event_handler, lv.EVENT.ALL, None)
```
### `set_bg_color(color, opa, part)`

        Set the background color of the slider.

        - Parameter `color` (`int`): The color to set.
        - Parameter `opa` (`int`): The opacity of the color. The value should be between 0 (transparent) and 255 (opaque).
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN, lv.PART.INDICATOR).
        - Returns: None

```python
slider_0.set_bg_color(lv.color_hex(0x2196F3), 255, lv.PART.INDICATOR | lv.STATE.DEFAULT)
```
### `set_style_radius(radius, part)`

        Set the corner radius of the slider components.

        - Parameter `radius` (`int`): The radius to set.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN, lv.PART.KNOB).
        - Returns: None

```python
slider_0.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)
```
### `set_bg_grad_color(color, opa, grad_color, grad_opd, grad_dir, part)`

        Set the background gradient color of the bar.

        - Parameter `color` (`int`): The start color of the gradient, can be an integer (RGB).
        - Parameter `opa` (`int`): The opacity of the start color (0-255).
        - Parameter `grad_color` (`int`): The end color of the gradient, can be an integer (RGB).
        - Parameter `grad_opd` (`int`): The opacity of the end color (0-255).
        - Parameter `grad_dir` (`int`): The direction of the gradient (e.g., lv.GRAD_DIR.VER).
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
bar.set_bg_grad_color(0x00FF00, 255, 0xFF0000, 255, lv.GRAD_DIR.HOR, lv.PART.MAIN | lv.STATE.DEFAULT)
bar.set_bg_grad_color(0x00FF00, 255, 0xFF0000, 255, lv.GRAD_DIR.HOR, lv.PART.INDICATOR | lv.STATE.DEFAULT)
```
### `get_value()`

        Get the current value of the slider.

        - Returns: The current value of the slider.
        - Return type: int

```python
value = slider_0.get_value()
```
### `set_mode(mode)`

        Set the mode of the slider.

### `get_min_value()`

        Get the minimum value of the slider range.

        - Returns: The minimum value of the slider range.
        - Return type: int

```python
min_value = slider_0.get_min_value()
```
### `get_max_value()`

        Get the maximum value of the slider range.

        - Returns: The maximum value of the slider range.
        - Return type: int

```python
max_value = slider_0.get_max_value()
```
### `set_pos(x, y)`

        Set the position of the slider.

        - Parameter `x` (`int`): The x-coordinate of the slider.
        - Parameter `y` (`int`): The y-coordinate of the slider.
        - Returns: None

```python
slider_0.set_pos(100, 100)
```
### `set_x(x)`

        Set the x-coordinate of the slider.

        - Parameter `x` (`int`): The x-coordinate of the slider.
        - Returns: None

```python
slider_0.set_x(100)
```
### `set_y(y)`

        Set the y-coordinate of the slider.

        - Parameter `y` (`int`): The y-coordinate of the slider.
        - Returns: None

```python
slider_0.set_y(100)
```
### `align_to(obj, align, x, y)`

        Align the slider to another object.

        - Parameter `obj` (`lv.obj`): The object to align to.
        - Parameter `align` (`int`): The alignment type.
        - Parameter `x` (`int`): The x-offset from the aligned object.
        - Parameter `y` (`int`): The y-offset from the aligned object.
        - Returns: None

```python
slider_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
```
### `set_size(width, height)`

        Set the size of the slider.

        - Parameter `width` (`int`): The width of the slider.
        - Parameter `height` (`int`): The height of the slider.
        - Returns: None

```python
slider_0.set_size(200, 20)
```
### `set_width(width)`

        Set the width of the slider.

        - Parameter `width` (`int`): The width of the slider.
        - Returns: None

```python
slider_0.set_width(200)
```
### `get_width()`

        Get the width of the slider.

        - Returns: The width of the slider.
        - Return type: int

```python
slider_0.get_width()
```
### `set_height(height)`

        Set the height of the slider.

        - Parameter `height` (`int`): The height of the slider.
        - Returns: None

```python
slider_0.set_height(20)
```
### `get_height()`

        Get the height of the slider.

        - Returns: The height of the slider.
        - Return type: int

```python
slider_0.get_height()
```
