
# M5Bar

M5Bar is a widget that can be used to create progress bars in the user interface. It displays values within a specified range using a visual bar indicator. The bar can be customized with different colors, gradients, and can optionally display the current value as text.

## MicroPython Example

#### Temperature meter

This example demonstrates how to create a temperature meter that shows the current temperature.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from hardware import I2C
from hardware import Pin
from unit import ENVPROUnit
import time

page0 = None
bar0 = None
label0 = None
i2c0 = None
envpro_0 = None

def setup():
    global page0, bar0, label0, i2c0, envpro_0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    bar0 = m5ui.M5Bar(
        x=148,
        y=21,
        w=20,
        h=200,
        min_value=0,
        max_value=50,
        value=25,
        bg_c=0x2193F3,
        color=0x2193F3,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "label0",
        x=181,
        y=112,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    envpro_0 = ENVPROUnit(i2c0)
    page0.screen_load()
    bar0.set_bg_grad_color(
        0xFF0000, 255, 0x0000FF, 255, lv.GRAD_DIR.VER, lv.PART.INDICATOR | lv.STATE.DEFAULT
    )

def loop():
    global page0, bar0, label0, i2c0, envpro_0
    M5.update()
    bar0.set_value(int(envpro_0.get_temperature()), True)
    label0.set_text(str(envpro_0.get_temperature()))
    time.sleep(1)

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

#### M5Bar

## `M5Bar`
Initialize a new M5Bar widget.

- Parameter `x` (`int`): The x-coordinate of the bar.
- Parameter `y` (`int`): The y-coordinate of the bar.
- Parameter `w` (`int`): The width of the bar.
- Parameter `h` (`int`): The height of the bar.
- Parameter `min_value` (`int`): The minimum value of the bar range.
- Parameter `max_value` (`int`): The maximum value of the bar range.
- Parameter `value` (`int`): The initial value of the bar.
- Parameter `is_show_value` (`bool`): Whether to display the current value as text.
- Parameter `bg_c` (`int`): The background color of the bar.
- Parameter `color` (`int`): The indicator color of the bar.
- Parameter `parent` (`lv.obj`): The parent object. If None, uses the active screen.
- Returns: None

    None

```python
bar = M5Bar(x=50, y=50, w=200, h=30, min_value=0, max_value=100, value=50)
```

### `set_value`
Set the current value of the bar.

- Parameter `value` (`int`): The value to set.
- Parameter `anim_enable` (`bool`): Whether to enable animation when changing the value.
- Returns: None

```python
bar.set_value(75, True)
```

### `set_range`
Set the value range of the bar.

- Parameter `min_value` (`int`): The minimum value.
- Parameter `max_value` (`int`): The maximum value.
- Returns: None

```python
bar.set_range(0, 200)
```

### `set_style_radius`

### `get_value()`

        Get the current value of the bar.

        - Returns: The current value of the bar.
        - Return type: int

```python
current_value = bar.get_value()
```
### `get_min_value()`

        Get the minimum value of the bar range.

        - Returns: The minimum value.
        - Return type: int

```python
min_val = bar.get_min_value()
```
### `get_max_value()`

        Get the maximum value of the bar range.

        - Returns: The maximum value.
        - Return type: int

```python
max_val = bar.get_max_value()
```
### `set_flag(flag, value)`

        Set a flag on the object. If `value` is True, the flag is added; if False, the flag is removed.

        - Parameter `flag` (`int`): The flag to set.
        - Parameter `value` (`bool`): If True, the flag is added; if False, the flag is removed.
        - Returns: None

```python
bar.set_flag(lv.obj.FLAG.HIDDEN, True)
```
### `toggle_flag(flag)`

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        - Parameter `flag` (`int`): The flag to toggle.
        - Returns: None

```python
bar.toggle_flag(lv.obj.FLAG.HIDDEN)
```
### `set_state(state, value)`

        Set the state of the bar. If `value` is True, the state is set; if False, the state is unset.

        - Parameter `state` (`int`): The state to set.
        - Parameter `value` (`bool`): If True, the state is set; if False, the state is unset.
        - Returns: None

```python
bar.set_state(lv.STATE.PRESSED, True)
```
### `toggle_state(state)`

        Toggle the state of the bar. If the state is set, it is unset; if not set, it is set.

        - Parameter `state` (`int`): The state to toggle.
        - Returns: None

```python
bar.toggle_state(lv.STATE.PRESSED)
```
### `set_bg_color(color, opa, part)`

        Set the background color of the bar.

        - Parameter `color` (`int`): The color to set.
        - Parameter `opa` (`int`): The opacity of the color.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
bar.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

bar.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.INDICATOR | lv.STATE.DEFAULT)
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
### `set_pos(x, y)`

        Set the position of the bar.

        - Parameter `x` (`int`): The x-coordinate of the bar.
        - Parameter `y` (`int`): The y-coordinate of the bar.
        - Returns: None

```python
bar.set_pos(100, 100)
```
### `set_x(x)`

        Set the x-coordinate of the bar.

        - Parameter `x` (`int`): The x-coordinate of the bar.
        - Returns: None

```python
bar.set_x(100)
```
### `set_y(y)`

        Set the y-coordinate of the bar.

        - Parameter `y` (`int`): The y-coordinate of the bar.
        - Returns: None

```python
bar.set_y(100)
```
### `set_size(width, height)`

        Set the size of the bar.

        - Parameter `width` (`int`): The width of the bar.
        - Parameter `height` (`int`): The height of the bar.
        - Returns: None

```python
bar.set_size(200, 30)
```
### `set_width(width)`

        Set the width of the bar.

        - Parameter `width` (`int`): The width of the bar.
        - Returns: None

```python
bar.set_width(200)
```
### `get_width()`

        Get the width of the bar.

        - Returns: The width of the bar.
        - Return type: int

```python
width = bar.get_width()
```
### `set_height(height)`

        Set the height of the bar.

        - Parameter `height` (`int`): The height of the bar.
        - Returns: None

```python
bar.set_height(30)
```
### `get_height()`

        Get the height of the bar.

        - Returns: The height of the bar.
        - Return type: int

```python
height = bar.get_height()
```
### `align_to(obj, align, x, y)`

        Align the bar to another object.

        - Parameter `obj` (`lv.obj`): The object to align to.
        - Parameter `align` (`int`): The alignment type.
        - Parameter `x` (`int`): The x-offset from the aligned object.
        - Parameter `y` (`int`): The y-offset from the aligned object.
        - Returns: None

```python
bar.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
```
