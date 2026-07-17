
# M5ButtonMatrix

M5ButtonMatrix is a widget that can be used to create a matrix of buttons in the
user interface. It provides a flexible layout for displaying multiple buttons in
a grid format with support for different button configurations and text labels.

## MicroPython Example

#### basic buttonmatrix

This example demonstrates how to create a button matrix with custom labels and handle button press events.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv

page0 = None
textarea0 = None
buttonmatrix0 = None
label0 = None
label1 = None

def buttonmatrix0_value_changed_event(event_struct):
    global page0, textarea0, buttonmatrix0, label0, label1
    label1.set_text(str(buttonmatrix0.get_button_text(buttonmatrix0.get_selected_button())))

def buttonmatrix0_event_handler(event_struct):
    global page0, textarea0, buttonmatrix0, label0, label1
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        buttonmatrix0_value_changed_event(event_struct)
    return

def setup():
    global page0, textarea0, buttonmatrix0, label0, label1

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    textarea0 = m5ui.M5TextArea(
        text="",
        placeholder="Placeholder...",
        x=24,
        y=15,
        w=150,
        h=70,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    buttonmatrix0 = m5ui.M5ButtonMatrix(
        ["0", "1", "2", "4", "\n", "5", "6", "7", "8", "9"],
        x=25,
        y=100,
        w=260,
        h=130,
        target_textarea=textarea0,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "last key:",
        x=189,
        y=15,
        text_c=0xC9C9C9,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label1 = m5ui.M5Label(
        "label1",
        x=203,
        y=42,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    buttonmatrix0.add_event_cb(buttonmatrix0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()

def loop():
    global page0, textarea0, buttonmatrix0, label0, label1
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

#### M5ButtonMatrix

## `M5ButtonMatrix`
Create a button matrix object.

- Parameter `map` (`list`): A list of button labels. Use "\\n" to create a new row.
- Parameter `x` (`int`): The x position of the button matrix.
- Parameter `y` (`int`): The y position of the button matrix.
- Parameter `w` (`int`): The width of the button matrix.
- Parameter `h` (`int`): The height of the button matrix.
- Parameter `target_textarea` (`m5ui.M5TextArea`): A M5TextArea to display the button text when a button is pressed.
- Parameter `parent` (`lv.obj`): The parent object to attach the button matrix to.

    None

```python
import m5ui
import lvgl as lv

m5ui.init()
page0 = m5ui.M5Page()
page0.screen_load()
textarea0 = m5ui.M5TextArea(x=10, y=10, w=200, h=60, parent=page0)
buttonmatrix_0 = m5ui.M5ButtonMatrix(
    ["0", "1", "2", "3", "4","\n", "5", "6", "7", "8", "9",],
    x=10, y=80, w=260, h=130,
    target_textarea=textarea0,
    parent=page0
)
```

### `value_changed_event`

### `toggle_button_ctrl`
Toggle control flags for a specific button.

- Parameter `btn_id` (`int`): The button ID to toggle control flags for.
- Parameter `ctrl` (`int`): The control flags to toggle.

```python
buttonmatrix_0.toggle_button_ctrl(0, lv.buttonmatrix.CTRL.HIDDEN)
```

### `set_textarea`
Set a M5TextArea to display button text.

- Parameter `textarea` (`m5ui.M5TextArea`): The M5TextArea to set.

```python
buttonmatrix_0.set_textarea(textarea0)
```

### `get_textarea`
Get the currently set M5TextArea.

- Returns: The M5TextArea currently set for the button matrix.
- Return type: m5ui.M5TextArea

```python
textarea = buttonmatrix_0.get_textarea()
```

### `get_selected_button`
Get the ID of the currently selected button.

- Returns: The ID of the currently selected button, or -1 if none is selected.
- Return type: int

```python
selected_button = buttonmatrix_0.get_selected_button()
```

### `set_flag(flag, value)`

        Set a flag on the object. If `value` is True, the flag is added; if False, the flag is removed.

        - Parameter `flag` (`int`): The flag to set.
        - Parameter `value` (`bool`): If True, the flag is added; if False, the flag is removed.
        - Returns: None

```python
buttonmatrix_0.set_flag(lv.obj.FLAG.HIDDEN, True)
```
### `toggle_flag(flag)`

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        - Parameter `flag` (`int`): The flag to toggle.
        - Returns: None

```python
buttonmatrix_0.toggle_flag(lv.obj.FLAG.HIDDEN)
```
### `set_state(state, value)`

        Set the state of the buttonmatrix. If `value` is True, the state is set; if False, the state is unset.

        - Parameter `state` (`int`): The state to set.
        - Parameter `value` (`bool`): If True, the state is set; if False, the state is unset.
        - Returns: None

```python
buttonmatrix_0.set_state(lv.STATE.PRESSED, True)
```
### `toggle_state(state)`

        Toggle the state of the buttonmatrix. If the state is set, it is unset; if not set, it is set.

        - Parameter `state` (`int`): The state to toggle.
        - Returns: None

```python
buttonmatrix_0.toggle_state(lv.STATE.PRESSED)
```
### `add_event_cb(handler, event, user_data)`

        Add an event callback to the buttonmatrix. The callback will be called when the specified event occurs.

        - Parameter `handler` (`function`): The callback function to call.
        - Parameter `event` (`int`): The event to listen for.
        - Parameter `user_data` (`Any`): Optional user data to pass to the callback.
        - Returns: None

```python
def buttonmatrix_0_pressed_event(event_struct):
    global page0
    btn_id = buttonmatrix_0.get_selected_button()
    print(f"Button {btn_id} pressed")

def buttonmatrix_0_event_handler(event_struct):
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED:
        buttonmatrix_0_pressed_event(event_struct)
    return

buttonmatrix_0.add_event_cb(buttonmatrix_0_event_handler, lv.EVENT.ALL, None)
```
### `set_button_width(btn_id, width)`

        Set the relative width of a specific button.

        - Parameter `btn_id` (`int`): The index of the button.
        - Parameter `width` (`int`): The relative width (1-7, where 1 is normal width).
        - Returns: None

```python
buttonmatrix_0.set_button_width(0, 2)  # Make first button twice as wide
```
### `get_button_text(btn_id)`

        Get the text of a specific button.

        - Parameter `btn_id` (`int`): The index of the button.
        - Returns: The text of the button.
        - Return type: str

```python
text = buttonmatrix_0.get_button_text(0)
```
### `clear_button_ctrl(btn_id, ctrl)`

        Clear control flags for a specific button.

        - Parameter `btn_id` (`int`): The button ID to clear control flags for.
        - Parameter `ctrl` (`int`): The control flags to clear.

```python
buttonmatrix_0.clear_button_ctrl(0, lv.buttonmatrix.CTRL.HIDDEN)
```
### `set_button_ctrl(btn_id, ctrl)`

        Set control flags for a specific button.

        - Parameter `btn_id` (`int`): The button ID to set control flags for.
        - Parameter `ctrl` (`int`): The control flags to set.

```python
buttonmatrix_0.set_button_ctrl(0, lv.buttonmatrix.CTRL.HIDDEN)
```
### `set_button_ctrl_all(ctrl)`

        Set control flags for all buttons.

        - Parameter `ctrl` (`int`): The control flags to set for all buttons.

```python
buttonmatrix_0.set_button_ctrl_all(lv.buttonmatrix.CTRL.HIDDEN)
```
### `clear_button_ctrl_all(ctrl)`

        Clear control flags for all buttons.

        - Parameter `ctrl` (`int`): The control flags to clear for all buttons.

```python
buttonmatrix_0.clear_button_ctrl_all(lv.buttonmatrix.CTRL.HIDDEN)
```
### `set_one_checked(btn_id)`

        Set a specific button as checked.

        - Parameter `btn_id` (`int`): The button ID to set as checked.

```python
buttonmatrix_0.set_one_checked(0)
```
### `set_pos(x, y)`

        Set the position of the buttonmatrix.

        - Parameter `x` (`int`): The x-coordinate of the buttonmatrix.
        - Parameter `y` (`int`): The y-coordinate of the buttonmatrix.
        - Returns: None

```python
buttonmatrix_0.set_pos(100, 100)
```
### `set_x(x)`

        Set the x-coordinate of the buttonmatrix.

        - Parameter `x` (`int`): The x-coordinate of the buttonmatrix.
        - Returns: None

```python
buttonmatrix_0.set_x(100)
```
### `set_y(y)`

        Set the y-coordinate of the buttonmatrix.

        - Parameter `y` (`int`): The y-coordinate of the buttonmatrix.
        - Returns: None

```python
buttonmatrix_0.set_y(100)
```
### `set_size(width, height)`

        Set the size of the buttonmatrix.

        - Parameter `width` (`int`): The width of the buttonmatrix.
        - Parameter `height` (`int`): The height of the buttonmatrix.
        - Returns: None

```python
buttonmatrix_0.set_size(300, 200)
```
### `set_width(width)`

        Set the width of the buttonmatrix.

        - Parameter `width` (`int`): The width of the buttonmatrix.
        - Returns: None

```python
buttonmatrix_0.set_width(300)
```
### `get_width()`

        Get the width of the buttonmatrix.

        - Returns: The width of the buttonmatrix.
        - Return type: int

```python
width = buttonmatrix_0.get_width()
```
### `set_height(height)`

        Set the height of the buttonmatrix.

        - Parameter `height` (`int`): The height of the buttonmatrix.
        - Returns: None

```python
buttonmatrix_0.set_height(200)
```
### `get_height()`

        Get the height of the buttonmatrix.

        - Returns: The height of the buttonmatrix.
        - Return type: int

```python
height = buttonmatrix_0.get_height()
```
### `align_to(obj, align, x, y)`

        Align the buttonmatrix to another object.

        - Parameter `obj` (`lv.obj`): The object to align to.
        - Parameter `align` (`int`): The alignment type.
        - Parameter `x` (`int`): The x-offset from the aligned object.
        - Parameter `y` (`int`): The y-offset from the aligned object.
        - Returns: None

```python
buttonmatrix_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
```
