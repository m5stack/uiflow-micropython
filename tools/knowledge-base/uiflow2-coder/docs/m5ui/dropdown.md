
# M5Dropdown

M5Dropdown is a widget that can be used to create dropdown menus in the user
interface. It allows users to select one option from a list of available options
with a compact dropdown interface.

> Important: **Available Fonts**: For `m5ui` widgets, use LVGL fonts such as `lv.font_montserrat_12`, `14`, `16`, `18`, `24`, `40`, `44`, and `48`. Some builds, such as Tab5, also include `20`, `22`, `30`, and `36`. The Alibaba CJK fonts are `M5.Lcd.FONTS` fonts for `M5.Lcd` / `M5.Widgets` drawing.
## MicroPython Example

#### Drop down in four directions

This example creates a drop down, up, left and right menus.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv

page0 = None
dropdown0 = None
dropdown1 = None
dropdown2 = None
dropdown3 = None

def setup():
    global page0, dropdown0, dropdown1, dropdown2, dropdown3

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    dropdown0 = m5ui.M5Dropdown(
        x=110,
        y=0,
        w=100,
        h=lv.SIZE_CONTENT,
        options=["option1", "option2"],
        direction=lv.DIR.BOTTOM,
        show_selected=True,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    dropdown1 = m5ui.M5Dropdown(
        x=111,
        y=212,
        w=100,
        h=lv.SIZE_CONTENT,
        options=["option1", "option2"],
        direction=lv.DIR.TOP,
        show_selected=True,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    dropdown2 = m5ui.M5Dropdown(
        x=220,
        y=106,
        w=100,
        h=lv.SIZE_CONTENT,
        options=["option1", "option2"],
        direction=lv.DIR.LEFT,
        show_selected=True,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    dropdown3 = m5ui.M5Dropdown(
        x=0,
        y=106,
        w=100,
        h=lv.SIZE_CONTENT,
        options=["option1", "option2"],
        direction=lv.DIR.RIGHT,
        show_selected=True,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    page0.screen_load()
    dropdown0.set_selected_highlight(True)
    dropdown1.set_selected_highlight(True)
    dropdown2.set_selected_highlight(True)
    dropdown3.set_selected_highlight(True)

def loop():
    global page0, dropdown0, dropdown1, dropdown2, dropdown3
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

#### M5Dropdown

## `M5Dropdown`
Create a dropdown object.

- Parameter `x`: The x position of the dropdown.
- Parameter `y`: The y position of the dropdown.
- Parameter `w`: The width of the dropdown.
- Parameter `h`: The height of the dropdown, default is `lv.SIZE_CONTENT`.
- Parameter `options`: A list of options to display in the dropdown.
- Parameter `direction`: The direction of the dropdown, can be `lv.DIR.LEFT`, `lv.DIR.RIGHT`, `lv.DIR.TOP`, or `lv.DIR.BOTTOM`.
- Parameter `show_selected`: Whether to highlight the selected option, default is `True`.
- Parameter `font`: The font used for the text in the dropdown, default is `lv.font_montserrat_14`.
- Parameter `parent`: The parent object for this dropdown, default is the active screen.

### `set_options`
Set the options for the dropdown.

- Parameter `options`: A list of options to display in the dropdown.

```python
dropdown_0.set_options(["option1", "option2", "option3"])
```

### `get_options`
Get the list of options in the dropdown.

- Returns: The list of options.
- Return type: list

### `add_option`
Add an option to the dropdown at a specific position.

- Parameter `option`: The option to add.
- Parameter `pos`: The position to insert the option at.

```python
dropdown_0.add_option("New Option", 1)
```

### `clear_options`
Clear all options in the dropdown.

```python
dropdown_0.clear_options()
```

### `get_selected_str`
Get the currently selected option as a string.

- Returns: The selected option as a string.

```python
selected_option = dropdown_0.get_selected_str()
```

### `set_dir`
Set the direction of the dropdown.

- Parameter `direction`: The direction of the dropdown, can be `lv.DIR.LEFT`, `lv.DIR.RIGHT`, `lv.DIR.TOP`, or `lv.DIR.BOTTOM`.

```python
dropdown_0.set_dir(lv.DIR.LEFT)
```

### `set_style_radius`
Set the radius of the dropdown's corners.

- Parameter `radius`: The radius of the corners in pixels.
- Parameter `part`: The part of the dropdown to apply the radius to, e.g., `lv.PART.MAIN`.

    None

```python
dropdown_0.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)
```

### `set_size`
Set the size of the dropdown.

- Parameter `w`: The width of the dropdown.
- Parameter `h`: The height of the dropdown.

```python
dropdown_0.set_size(150, 40)
```

### `set_flag(flag, value)`

        Set a flag on the object. If `value` is True, the flag is added; if False, the flag is removed.

        - Parameter `flag` (`int`): The flag to set.
        - Parameter `value` (`bool`): If True, the flag is added; if False, the flag is removed.
        - Returns: None

```python
dropdown_0.set_flag(lv.obj.FLAG.HIDDEN, True)
```
### `toggle_flag(flag)`

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        - Parameter `flag` (`int`): The flag to toggle.
        - Returns: None

```python
dropdown_0.toggle_flag(lv.obj.FLAG.HIDDEN)
```
### `set_state(state, value)`

        Set the state of the dropdown. If `value` is True, the state is set; if False, the state is unset.

        - Parameter `state` (`int`): The state to set.
        - Parameter `value` (`bool`): If True, the state is set; if False, the state is unset.
        - Returns: None

```python
dropdown_0.set_state(lv.STATE.CHECKED, True)
```
### `toggle_state(state)`

        Toggle the state of the dropdown. If the state is set, it is unset; if not set, it is set.

        - Parameter `state` (`int`): The state to toggle.
        - Returns: None

```python
dropdown_0.toggle_state(lv.STATE.CHECKED)
```
### `set_pos(x, y)`

        Set the position of the dropdown.

        - Parameter `x` (`int`): The x-coordinate of the dropdown.
        - Parameter `y` (`int`): The y-coordinate of the dropdown.
        - Returns: None

```python
dropdown_0.set_pos(100, 100)
```
### `set_x(x)`

        Set the x-coordinate of the dropdown.

        - Parameter `x` (`int`): The x-coordinate of the dropdown.
        - Returns: None

```python
dropdown_0.set_x(100)
```
### `set_y(y)`

        Set the y-coordinate of the dropdown.

        - Parameter `y` (`int`): The y-coordinate of the dropdown.
        - Returns: None

```python
dropdown_0.set_y(100)
```
### `set_width(width)`

        Set the width of the dropdown.

        - Parameter `width` (`int`): The width of the dropdown.
        - Returns: None

```python
dropdown_0.set_width(100)
```
### `get_width()`

        Get the width of the dropdown.

        - Returns: The width of the dropdown.
        - Return type: int

```python
dropdown_0.get_width()
```
### `set_height(height)`

        Set the height of the dropdown.

        - Parameter `height` (`int`): The height of the dropdown.
        - Returns: None

```python
dropdown_0.set_height(50)
```
### `get_height()`

        Get the height of the dropdown.

        - Returns: The height of the dropdown.
        - Return type: int

```python
dropdown_0.get_height()
```
### `align_to(obj, align, x, y)`

        Align the dropdown to another object.

        - Parameter `obj` (`lv.obj`): The object to align to.
        - Parameter `align` (`int`): The alignment type.
        - Parameter `x` (`int`): The x-offset from the aligned object.
        - Parameter `y` (`int`): The y-offset from the aligned object.
        - Returns: None

```python
dropdown_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
```
### `get_selected()`

        Get the index of the currently selected option.

        - Returns: The index of the selected option.
        - Return type: int

```python
selected_index = dropdown_0.get_selected()
```
### `set_selected_highlight(enable)`

        Enable or disable highlighting of the selected option.

        - Parameter `enable` (`bool`): True to enable highlighting, False to disable.
        - Returns: None

```python
dropdown_0.set_selected_highlight(True)
```
### `get_option_count()`

        Clear all options in a drop-down list.

        - Returns: The number of options in the dropdown.
        - Return type: int

```python
option_count = dropdown_0.get_option_count()
```
### `get_option_index(option)`

        Get the index of an option.

        - Parameter `option` (`str`): The option to find.
        - Returns: The index of the option, or -1 if not found.
        - Return type: int

```python
index = dropdown_0.get_option_index("Option 1")
if index != -1:
    print(f"Option found at index: {index}")
else:
    print("Option not found")
```
### `get_text()`

        Get text of the drop-down list's button.

        - Returns: The text of the dropdown button.
        - Return type: str

```python
text = dropdown_0.get_text()
print(f"Dropdown button text: {text}")
```
### `set_text(txt)`

        Set text of the drop-down list's button.

        - Parameter `txt` (`str`): The text to set for the dropdown button.
        - Returns: None

```python
dropdown_0.set_text("Select an option")
```
### `add_event_cb(handler, event, user_data)`

        Add an event callback to the dropdown. The callback will be called when the specified event occurs.

        - Parameter `handler` (`function`): The callback function to call.
        - Parameter `event` (`int`): The event to listen for.
        - Parameter `user_data` (`Any`): Optional user data to pass to the callback.
        - Returns: None

```python
def dropdown_0_value_changed_event(event_struct):
    global dropdown_0
    selected = dropdown_0.get_selected_str()
    print(f"Selected: {selected}")

def dropdown_0_event_handler(event_struct):
    global dropdown_0
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED:
        dropdown_0_value_changed_event(event_struct)
    return

dropdown_0.add_event_cb(dropdown_0_event_handler, lv.EVENT.ALL, None)
```
