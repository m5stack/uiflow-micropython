
# M5Roller

M5Roller is a widget that can be used to create a roller (spinner/wheel picker) in the
user interface. It provides a scrollable list of options that users can select from by
scrolling up or down, similar to iOS-style picker wheels.

## MicroPython Example

#### basic roller

This example demonstrates how to create a roller with multiple options and handle selection events.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv

page0 = None
roller0 = None

def setup():
    global page0, roller0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    roller0 = m5ui.M5Roller(
        x=110,
        y=71,
        w=100,
        h=0,
        options=[
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
        mode=lv.roller.MODE.INFINITE,
        selected=0,
        visible_row_count=3,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    page0.screen_load()
    print(roller0.get_options())

def loop():
    global page0, roller0
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

#### M5Roller

## `M5Roller`
Create a roller widget.

- Parameter `x` (`int`): X position of the widget.
- Parameter `y` (`int`): Y position of the widget.
- Parameter `w` (`int`): Width of the widget.
- Parameter `h` (`int`): Height of the widget.
- Parameter `options` (`list`): List of options to display in the roller.
- Parameter `mode` (`lv.roller.MODE`): Roller mode (default is NORMAL).
- Parameter `selected` (`int`): Index of the initially selected option.
- Parameter `visible_row_count` (`int`): Number of visible rows in the roller.
- Parameter `font` (`lv.font_t`): Font to use for the text in the roller.
- Parameter `parent`: Parent widget to attach this roller to (default is the active screen).
- Type of `parent`: lv.obj or None

    None

```python
from m5ui import M5Roller
import lvgl as lv
m5ui.init()
roller_0 = M5Roller(x=10, y=10, w=100, h=100, options=["Option 1", "Option 2"], mode=lv.roller.MODE.NORMAL, selected=0, visible_row_count=2, font=lv.font_montserrat_14, parent=page0)
```

### `set_options`
Set the options for the roller.

- Parameter `options` (`list`): List of options to display in the roller.
- Parameter `mode` (`lv.roller.MODE`): Roller mode (default is NORMAL).

```python
roller_0.set_options(["Option 1", "Option 2"], mode=lv.roller.MODE.NORMAL)
```

### `get_options`
Get the list of options in the dropdown.

- Returns: The list of options.
- Return type: list

```python
options = roller_0.get_options()
```

### `get_option_count`
Get the number of options in the roller.

- Returns: The number of options.
- Return type: int

```python
option_count = roller_0.get_option_count()
```

### `get_selected_str`
Get the currently selected option as a string.

- Returns: The selected option as a string.

```python
selected_option = roller_0.get_selected_str()
```

### `set_style_radius`
Set the corner radius of the slider components.

- Parameter `radius` (`int`): The radius to set.
- Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN, lv.PART.SELECTED).
- Returns: None

```python
roller_0.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)
roller_0.set_style_radius(10, lv.PART.SELECTED | lv.STATE.DEFAULT)
```

### `set_flag(flag, value)`

        Set a flag on the object. If `value` is True, the flag is added; if False, the flag is removed.

        - Parameter `flag` (`int`): The flag to set.
        - Parameter `value` (`bool`): If True, the flag is added; if False, the flag is removed.
        - Returns: None

```python
roller_0.set_flag(lv.obj.FLAG.HIDDEN, True)
```
### `toggle_flag(flag)`

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        - Parameter `flag` (`int`): The flag to toggle.
        - Returns: None

```python
roller_0.toggle_flag(lv.obj.FLAG.HIDDEN)
```
### `set_state(state, value)`

        Set the state of the roller. If `value` is True, the state is set; if False, the state is unset.

        - Parameter `state` (`int`): The state to set.
        - Parameter `value` (`bool`): If True, the state is set; if False, the state is unset.
        - Returns: None

```python
roller_0.set_state(lv.STATE.CHECKED, True)
```
### `toggle_state(state)`

        Toggle the state of the roller. If the state is set, it is unset; if not set, it is set.

        - Parameter `state` (`int`): The state to toggle.
        - Returns: None

```python
roller_0.toggle_state(lv.STATE.CHECKED)
```
### `event(callback, event, user_data=None)`

        Add an event callback to the roller. The callback will be called when the specified event occurs.

        - Parameter `callback`: The callback function to call.
        - Parameter `event` (`int`): The event to listen for.
        - Parameter `user_data`: Optional user data to pass to the callback.
        - Returns: None

```python
def roller_callback(event_obj):
    print("Roller value changed")

roller_0.event(roller_callback, lv.EVENT.VALUE_CHANGED)
```
### `set_bg_color(color, opa, part)`

        Set the background color of the roller.

        - Parameter `color` (`int`): The color to set.
        - Parameter `opa` (`int`): The opacity of the color.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
roller_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

roller_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.SELECTED | lv.STATE.DEFAULT)
```
### `set_border_color(color, opa, part)`

        Set the border color of the roller.

        - Parameter `color` (`int`): The color to set.
        - Parameter `opa` (`int`): The opacity of the color. The value should be between 0 (transparent) and 255 (opaque).
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
roller_0.set_border_color(lv.color_hex(0x2196F3), 255, lv.PART.MAIN | lv.STATE.DEFAULT)
roller_0.set_border_color(lv.color_hex(0x2196F3), 255, lv.PART.SELECTED | lv.STATE.DEFAULT)
```
### `set_style_border_width(width, part)`

        Set the border width of the roller.

        - Parameter `width` (`int`): The width to set.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
roller_0.set_style_border_width(2, lv.PART.MAIN | lv.STATE.DEFAULT)
roller_0.set_style_border_width(2, lv.PART.SELECTED | lv.STATE.DEFAULT)
```
### `get_selected()`

        Get the index of the currently selected option.

        - Returns: The index of the selected option.
        - Return type: int

```python
selected_index = roller_0.get_selected()
```
### `set_visible_row_count(count)`

        Set the number of visible rows in the roller.

        - Parameter `count` (`int`): The number of visible rows.
        - Returns: None

```python
roller_0.set_visible_row_count(3)
```
### `set_pos(x, y)`

        Set the position of the roller.

        - Parameter `x` (`int`): The x-coordinate of the roller.
        - Parameter `y` (`int`): The y-coordinate of the roller.
        - Returns: None

```python
roller_0.set_pos(100, 50)
```
### `set_x(x)`

        Set the x-coordinate of the roller.

        - Parameter `x` (`int`): The x-coordinate of the roller.
        - Returns: None

```python
roller_0.set_x(100)
```
### `set_y(y)`

        Set the y-coordinate of the roller.

        - Parameter `y` (`int`): The y-coordinate of the roller.
        - Returns: None

```python
roller_0.set_y(50)
```
### `align_to(obj, align, x_ofs=0, y_ofs=0)`

        Align the roller to another object.

        - Parameter `obj` (`lv.obj`): The object to align to.
        - Parameter `align` (`int`): The alignment type.
        - Parameter `x_ofs` (`int`): The x-offset from the aligned object.
        - Parameter `y_ofs` (`int`): The y-offset from the aligned object.
        - Returns: None

```python
roller_0.align_to(other_obj, lv.ALIGN.CENTER, 0, 0)
```
### `set_size(w, h)`

        Set the size of the roller.

        - Parameter `w` (`int`): The width of the roller.
        - Parameter `h` (`int`): The height of the roller.
        - Returns: None

```python
roller_0.set_size(150, 120)
```
### `set_width(w)`

        Set the width of the roller.

        - Parameter `w` (`int`): The width of the roller.
        - Returns: None

```python
roller_0.set_width(150)
```
### `get_width()`

        Get the width of the roller.

        - Returns: The width of the roller.
        - Return type: int

```python
width = roller_0.get_width()
```
### `set_height(h)`

        Set the height of the roller.

        - Parameter `h` (`int`): The height of the roller.
        - Returns: None

```python
roller_0.set_height(120)
```
### `get_height()`

        Get the height of the roller.

        - Returns: The height of the roller.
        - Return type: int

```python
height = roller_0.get_height()
```
