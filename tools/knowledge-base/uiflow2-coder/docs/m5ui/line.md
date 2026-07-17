
# M5Line

M5Line is a widget that can be used to create lines in the user interface. It can be used to draw shapes and connect points.

## MicroPython Example

#### points connect

This example creates a line that connects multiple points.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv

page0 = None
line0 = None

def setup():
    global page0, line0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    line0 = m5ui.M5Line(
        points=[5, 5, 70, 70, 120, 10, 180, 60, 190, 70, 200, 80, 210, 90, 220, 100],
        width=7,
        color=0x2196F3,
        rounded=True,
        parent=page0,
    )

    page0.screen_load()

def loop():
    global page0, line0
    M5.update()
    if M5.Touch.getCount():
        line0.add_point(M5.Touch.getX(), M5.Touch.getY())

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

#### M5Line

## `M5Line`
Create a line object.

- Parameter `points` (`list`): A list of points where each point is a pair of x and y coordinates.
- Parameter `width` (`int`): The width of the line.
- Parameter `color` (`int`): The color of the line in hexadecimal format.
- Parameter `rounded` (`bool`): If True, the line will have rounded ends; otherwise, it will have square ends.
- Parameter `parent` (`lv.obj`): The parent object to attach the line to. If not specified, the line will be attached to the default screen.

```python
from m5ui import M5Line
import lvgl as lv

m5ui.init()
line_0 = M5Line(
    points=[5, 5, 70, 70, 120, 10, 180, 60, 240, 20],
    width=2,
    color=0x2196F3,
    rounded=True,
    parent=page0,
)
```

### `set_points`
Set the points of the line.

- Parameter `points` (`list`): A list of points where each point is a pair of x and y coordinates.

```python
line_0.set_points([0, 0, 100, 100, 200, 50])
```

### `add_point`
Add a point to the line end.

- Parameter `x` (`int`): The x position of the point.
- Parameter `y` (`int`): The y position of the point.

```python
line_0.add_point(100, 100)
```

### `set_style_radius`

### `set_line_color(color, opa, part)`

        Set the color of the line.

        - Parameter `color` (`int`): The color to set.
        - Parameter `opa` (`int`): The opacity of the color.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).

```python
line_0.set_line_color(0xFF0000, 255, lv.PART.MAIN)
```
### `set_style_line_width(width,  part)`

        Set the width of the line.

        - Parameter `width` (`int`): The width to set.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).

```python
line_0.set_style_line_width(2, lv.PART.MAIN)
```
### `set_flag(flag, value)`

        Set a flag on the object. If `value` is True, the flag is added; if False, the flag is removed.

        - Parameter `flag` (`int`): The flag to set.
        - Parameter `value` (`bool`): If True, the flag is added; if False, the flag is removed.
        - Returns: None

```python
button_0.set_flag(lv.obj.FLAG.HIDDEN, True)
```
### `set_pos(x, y)`

        Set the position of the line.

        - Parameter `x` (`int`): The x-coordinate of the line.
        - Parameter `y` (`int`): The y-coordinate of the line.

```python
line_0.set_pos(100, 100)
```
### `set_x(x)`

        Set the x-coordinate of the line.

        - Parameter `x` (`int`): The x-coordinate of the line.

```python
line_0.set_x(100)
```
### `set_y(y)`

        Set the y-coordinate of the line.

        - Parameter `y` (`int`): The y-coordinate of the line.

```python
line_0.set_y(100)
```
### `align_to(obj, align, x, y)`

        Align the line to another object.

        - Parameter `obj` (`lv.obj`): The object to align to.
        - Parameter `align` (`int`): The alignment type.
        - Parameter `x` (`int`): The x-offset from the aligned object.
        - Parameter `y` (`int`): The y-offset from the aligned object.

```python
line_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
```
