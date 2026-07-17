
# M5Spinner

M5Spinner is a spinning arc over a ring, typically used to show some type of activity is in progress.

## MicroPython Example

#### spinner

This example shows a spinning arc over a ring.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv

page0 = None
spinner0 = None

def setup():
    global page0, spinner0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    spinner0 = m5ui.M5Spinner(
        x=71,
        y=81,
        w=100,
        h=100,
        anim_t=10000,
        angle=180,
        bg_c=0xE7E3E7,
        bg_c_indicator=0x2193F3,
        parent=page0,
    )

    page0.screen_load()

def loop():
    global page0, spinner0
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

#### M5Spinner

## `M5Spinner`
Create a spinner object.

- Parameter `x` (`int`): The x position of the spinner.
- Parameter `y` (`int`): The y position of the spinner.
- Parameter `w` (`int`): The width of the spinner.
- Parameter `h` (`int`): The height of the spinner.
- Parameter `anim_t` (`int`): The animation time in milliseconds.
- Parameter `angle` (`int`): The angle of the spinner in degrees.
- Parameter `bg_c` (`int`): The background color of the spinner in hexadecimal format.
- Parameter `bg_c_indicator` (`int`): The indicator color of the spinner in hexadecimal format.
- Parameter `parent` (`lv.obj`): The parent object to attach the spinner to. If not specified, the spinner will be attached to the default screen.

    None

```python
from m5ui import M5Spinner
import lvgl as lv

m5ui.init()
spinner_0 = M5Spinner(x=120, y=80, w=60, h=30, anim_t=1000, angle=180, bg_c=0xE7E3E7, bg_c_indicator=0x0288FB, parent=page0)
```

### `set_spinner_color`
Set the color of the spinner.

- Parameter `color` (`int`): The color of the spinner in hexadecimal format.
- Parameter `opa` (`int`): The opacity of the color (0-255).
- Parameter `part` (`int`): The part of the spinner to set the color for.

```python
spinner_0.set_spinner_color(0x2196F3, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
```

### `set_flag(flag, value)`

        Set a flag on the object. If `value` is True, the flag is added; if False, the flag is removed.

        - Parameter `flag` (`int`): The flag to set.
        - Parameter `value` (`bool`): If True, the flag is added; if False, the flag is removed.
        - Returns: None

```python
spinner_0.set_flag(lv.obj.FLAG.HIDDEN, True)
```
### `set_pos(x, y)`

        Set the position of the spinner.

        - Parameter `x` (`int`): The x-coordinate of the spinner.
        - Parameter `y` (`int`): The y-coordinate of the spinner.

```python
spinner_0.set_pos(100, 100)
```
### `set_x(x)`

        Set the x-coordinate of the spinner.

        - Parameter `x` (`int`): The x-coordinate of the spinner.

```python
spinner_0.set_x(100)
```
### `set_y(y)`

        Set the y-coordinate of the spinner.

        - Parameter `y` (`int`): The y-coordinate of the spinner.

```python
spinner_0.set_y(100)
```
### `set_size(width, height)`

        Set the size of the spinner.

        - Parameter `width` (`int`): The width of the spinner.
        - Parameter `height` (`int`): The height of the spinner.

```python
spinner_0.set_size(100, 50)
```
### `align_to(obj, align, x, y)`

        Align the spinner to another object.

        - Parameter `obj` (`lv.obj`): The object to align to.
        - Parameter `align` (`int`): The alignment type.
        - Parameter `x` (`int`): The x-offset from the aligned object.
        - Parameter `y` (`int`): The y-offset from the aligned object.

```python
spinner_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
```
### `set_anim_params(anim_t, angle)`

        Set the animation parameters of the spinner.

        - Parameter `anim_t` (`int`): The animation time in milliseconds.
        - Parameter `angle` (`int`): The angle of the spinner in degrees.

```python
spinner_0.set_anim_params(1000, 180)
```
