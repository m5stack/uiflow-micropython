
# M5Arc

M5Arc is a widget that can be used to create arcs in the user interface. It can be used to display circular progress or other circular indicators.

## MicroPython Example

#### event arc

This example creates an arc that triggers an event when the value changes.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv

page0 = None
switch0 = None

def switch0_checked_event(event_struct):
    global page0, switch0

    print("switch0 checked")

def switch0_unchecked_event(event_struct):
    global page0, switch0

    print("switch0 unchecked")

def switch0_event_handler(event_struct):
    global page0, switch0
    event = event_struct.code
    obj = event_struct.get_target_obj()
    if event == lv.EVENT.VALUE_CHANGED:
        if obj.has_state(lv.STATE.CHECKED):
            switch0_checked_event(event_struct)
        else:
            switch0_unchecked_event(event_struct)
    return

def setup():
    global page0, switch0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    switch0 = m5ui.M5Switch(
        x=128,
        y=91,
        w=60,
        h=30,
        bg_c=0xE7E3E7,
        bg_c_checked=0x2196F3,
        circle_c=0xFFFFFF,
        parent=page0,
    )

    switch0.add_event_cb(switch0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    switch0.set_bg_color(0x666666, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    switch0.set_bg_color(0x33FF33, 255, lv.PART.INDICATOR | lv.STATE.CHECKED)

def loop():
    global page0, switch0
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

#### M5Arc

## `M5Arc`
Create a arc object.

- Parameter `x` (`int`): The x position of the arc.
- Parameter `y` (`int`): The y position of the arc.
- Parameter `w` (`int`): The width of the arc.
- Parameter `h` (`int`): The height of the arc.
- Parameter `value` (`int`): The initial value of the arc.
- Parameter `min_value` (`int`): The minimum value of the arc.
- Parameter `max_value` (`int`): The maximum value of the arc.
- Parameter `rotation` (`int`): The rotation of the arc in degrees.
- Parameter `bg_c` (`int`): The color of the arc in the off state in hexadecimal format.
- Parameter `bg_c_indicator` (`int`): The color of the arc in the on state in hexadecimal format.
- Parameter `bg_c_knob` (`int`): The color of the knob on the arc in hexadecimal format.
- Parameter `parent` (`lv.obj`): The parent object to attach the arc to. If not specified, the arc will be attached to the default screen.

    None

```python
from m5ui import M5Arc
import lvgl as lv

m5ui.init()
arc_0 = M5Arc(
    x=0,
    y=0,
    w=100,
    h=100,
    value=10,
    min_value=0,
    max_value=100,
    rotation=0,
    mode=lv.arc.MODE.REVERSE,
    bg_c=0xE7E3E7,
    bg_c_indicator=0x0288FB,
    bg_c_knob=0xE7E3E7,
    parent=page0,
)
```

### `set_arc_color`
Set the color of the arc.

- Parameter `color` (`int`): The color of the arc in hexadecimal format.
- Parameter `opa` (`int`): The opacity level (0-255).
- Parameter `part` (`int`): The part of the arc to apply the style to (e.g., lv.PART.MAIN | lv.STATE.DEFAULT).

```python
label_0.set_arc_color(0x2196F3, lv.PART.MAIN | lv.STATE.DEFAULT)
```

### `set_range`

### `set_style_radius`

### `set_rotation(rotation)`

        Set the rotation of the arc.

        - Parameter `rotation` (`int`): The rotation angle of the arc in degrees.

```python
arc_0.set_rotation(90)
```
### `set_value(value)`

        Set the value of the arc.

        - Parameter `value` (`int`): The value of the arc.

```python
arc_0.set_value(90)
```
### `get_value()`

        Get the value of the arc.

        - Returns: The value of the arc.
        - Return type: int

```python
arc_0.get_value()
```
### `set_range()`

        Set the range of the arc.

        - Parameter `min` (`int`): The minimum value of the arc.
        - Parameter `max` (`int`): The maximum value of the arc.

```python
arc_0.set_range(0, 100)
```
### `set_mode()`

        Set the mode of the arc.

        - Parameter `mode` (`int`): The mode of the arc.

            Option:
                - lv.arc.MODE.NORMAL: Normal mode.
                - lv.arc.MODE.REVERSE: Reverse mode.
                - lv.arc.MODE.SYMMETRICAL: Symmetrical mode.

```python
arc_0.set_mode(lv.ARC.MODE.NORMAL)
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

        Set the position of the arc.

        - Parameter `x` (`int`): The x-coordinate of the arc.
        - Parameter `y` (`int`): The y-coordinate of the arc.

```python
arc_0.set_pos(100, 100)
```
### `set_x(x)`

        Set the x-coordinate of the arc.

        - Parameter `x` (`int`): The x-coordinate of the arc.

```python
arc_0.set_x(100)
```
### `set_y(y)`

        Set the y-coordinate of the arc.

        - Parameter `y` (`int`): The y-coordinate of the arc.

```python
arc_0.set_y(100)
```
### `set_size(width, height)`

        Set the size of the arc.

        - Parameter `width` (`int`): The width of the arc.
        - Parameter `height` (`int`): The height of the arc.

```python
arc_0.set_size(100, 50)
```
### `align_to(obj, align, x, y)`

        Align the arc to another object.

        - Parameter `obj` (`lv.obj`): The object to align to.
        - Parameter `align` (`int`): The alignment type.
        - Parameter `x` (`int`): The x-offset from the aligned object.
        - Parameter `y` (`int`): The y-offset from the aligned object.

```python
arc_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
```
### `add_event_cb(handler, event, user_data)`

        Add an event callback to the arc. The callback will be called when the specified event occurs.

        - Parameter `handler` (`function`): The callback function to call.
        - Parameter `event` (`int`): The event to listen for.
        - Parameter `user_data` (`Any`): Optional user data to pass to the callback.

```python
def value_changed_event(event_struct):
    global page0, arc_0
    print("value changed:", arc_0.get_value())

arc_0.add_event_cb(value_changed_event, lv.EVENT.VALUE_CHANGED, None)
```
