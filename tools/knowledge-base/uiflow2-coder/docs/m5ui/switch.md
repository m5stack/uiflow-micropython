
# M5Switch

M5Switch is a widget that can be used to create switch in the user interface. It can be used to trigger actions when checked and uncheked.

## MicroPython Example

#### event switch

This example creates a switch that triggers an event when checked and uncheked.

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

#### M5Switch

## `M5Switch`
Create a switch object.

- Parameter `x` (`int`): The x position of the switch.
- Parameter `y` (`int`): The y position of the switch.
- Parameter `w` (`int`): The width of the switch.
- Parameter `h` (`int`): The height of the switch.
- Parameter `bg_c` (`int`): The color of the switch in the off state in hexadecimal format.
- Parameter `bg_c_checked` (`int`): The color of the switch in the on state in hexadecimal format.
- Parameter `circle_c` (`int`): This color refers to the color of the circle on the switch in hexadecimal format.
- Parameter `parent` (`lv.obj`): The parent object to attach the switch to. If not specified, the switch will be attached to the default screen.

    None

```python
from m5ui import M5Switch
import lvgl as lv

m5ui.init()
switch_0 = M5Switch(x=120, y=80, w=60, h=30, bg_c=0xE7E3E7, color=0x2196F3, parent=page0)
```

### `set_direction`
Set the direction of the switch.

- Parameter `direction` (`int`): The direction of the switch.

    Options:

        - 0: Horizontal
        - 1: Vertical

UIFlow2 Code Block:

```python
switch_0.set_direction(0)  # Set to horizontal
switch_0.set_direction(1)  # Set to vertical
```

### `set_size`

### `set_style_radius`

### `set_bg_color(color, opa, part)`

        Set the background color of the switch.

        - Parameter `color` (`int`): The color to set.
        - Parameter `opa` (`int`): The opacity of the color. The value should be between 0 (transparent) and 255 (opaque).
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).

```python
switch_0.set_bg_color(0xE7E3E7, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
switch_0.set_bg_color(0x2196F3, 255, lv.PART.INDICATOR | lv.STATE.CHECKED)
```
### `set_state(state, value)`

        Set the state of the Switch.

        - Parameter `state` (`int`): The state to set.
        - Parameter `value` (`bool`): If True, the state is set; if False, the state is unset.

```python
switch_0.set_state(lv.STATE.CHECKED, True)
```
### `has_state(state)`

        Get the state of the Switch.

        - Parameter `state` (`int`): The state to get.
        - Returns: True if the state is set, False otherwise.
        - Return type: bool

```python
switch_0.has_state(lv.STATE.CHECKED)
```
### `set_pos(x, y)`

        Set the position of the switch.

        - Parameter `x` (`int`): The x-coordinate of the switch.
        - Parameter `y` (`int`): The y-coordinate of the switch.

```python
switch_0.set_pos(100, 100)
```
### `set_x(x)`

        Set the x-coordinate of the switch.

        - Parameter `x` (`int`): The x-coordinate of the switch.

```python
switch_0.set_x(100)
```
### `set_y(y)`

        Set the y-coordinate of the switch.

        - Parameter `y` (`int`): The y-coordinate of the switch.

```python
switch_0.set_y(100)
```
### `set_size(width, height)`

        Set the size of the switch.

        - Parameter `width` (`int`): The width of the switch.
        - Parameter `height` (`int`): The height of the switch.

```python
switch_0.set_size(100, 50)
```
### `set_width(width)`

        Set the width of the switch.

        - Parameter `width` (`int`): The width of the switch.

```python
switch_0.set_width(100)
```
### `get_width()`

        Get the width of the switch.

        - Returns: The width of the switch.
        - Return type: int

```python
switch_0.get_width()
```
### `set_height(height)`

        Set the height of the switch.

        - Parameter `height` (`int`): The height of the switch.

```python
switch_0.set_height(50)
```
### `get_height()`

        Get the height of the switch.

        - Returns: The height of the switch.
        - Return type: int

```python
switch_0.get_height()
```
### `align_to(obj, align, x, y)`

        Align the switch to another object.

        - Parameter `obj` (`lv.obj`): The object to align to.
        - Parameter `align` (`int`): The alignment type.
        - Parameter `x` (`int`): The x-offset from the aligned object.
        - Parameter `y` (`int`): The y-offset from the aligned object.

```python
switch_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
```
### `add_event_cb(handler, event, user_data)`

        Add an event callback to the switch. The callback will be called when the specified event occurs.

        - Parameter `handler` (`function`): The callback function to call.
        - Parameter `event` (`int`): The event to listen for.
        - Parameter `user_data` (`Any`): Optional user data to pass to the callback.

```python
def switch0_checked_event(event_struct):
    global page0, button0
    print("checked")

def switch0_unchecked_event(event_struct):
    global page0, button0
    print("unchecked")

def switch0_event_handler(event_struct):
    global page0, button0
    event = event_struct.code
    obj = event_struct.get_target_obj()
    if event == lv.EVENT.VALUE_CHANGED:
        if obj.has_state(lv.STATE.CHECKED):
            switch0_checked_event(event_struct)
        else:
            switch0_unchecked_event(event_struct)
    return

switch_0.add_event_cb(switch0_event_handler, lv.EVENT.ALL, None)
```
