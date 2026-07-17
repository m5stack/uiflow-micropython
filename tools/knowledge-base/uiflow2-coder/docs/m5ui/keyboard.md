
# M5Keyboard

M5Keyboard is a widget that can be used to create virtual keyboards in the user interface. It provides an on-screen keyboard that can be used for text input with support for different keyboard modes and layouts.

## MicroPython Example

#### basic keyboard

This example demonstrates how to create a virtual keyboard and connect it to a text input area.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv

page0 = None
textarea0 = None
keyboard0 = None

def textarea0_focused_event(event_struct):
    global page0, textarea0, keyboard0
    keyboard0.set_flag(lv.obj.FLAG.HIDDEN, False)

def textarea0_defocused_event(event_struct):
    global page0, textarea0, keyboard0
    keyboard0.set_flag(lv.obj.FLAG.HIDDEN, True)

def textarea0_event_handler(event_struct):
    global page0, textarea0, keyboard0
    event = event_struct.code
    if event == lv.EVENT.FOCUSED and True:
        textarea0_focused_event(event_struct)
    if event == lv.EVENT.DEFOCUSED and True:
        textarea0_defocused_event(event_struct)
    return

def setup():
    global page0, textarea0, keyboard0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    textarea0 = m5ui.M5TextArea(
        text="textarea0",
        placeholder="Placeholder...",
        x=10,
        y=30,
        w=300,
        h=70,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    keyboard0 = m5ui.M5Keyboard(
        x=0,
        y=120,
        w=320,
        h=120,
        mode=lv.keyboard.MODE.TEXT_LOWER,
        target_textarea=textarea0,
        parent=page0,
    )

    textarea0.add_event_cb(textarea0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()

def loop():
    global page0, textarea0, keyboard0
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

#### M5Keyboard

## `M5Keyboard`
Create a keyboard widget.

- Parameter `x` (`int`): The x position of the keyboard.
- Parameter `y` (`int`): The y position of the keyboard.
- Parameter `w` (`int`): The width of the keyboard.
- Parameter `h` (`int`): The height of the keyboard.
- Parameter `mode` (`int`): The keyboard mode, default is `lv.keyboard.MODE.TEXT_LOWER`.
- Parameter `target_textarea` (`lv.obj`): The target textarea to link with the keyboard.
- Parameter `parent` (`lv.obj`): The parent object, default is the active screen.

    None

```python
import m5ui
import lvgl as lv

m5ui.init()
keyboard = m5ui.M5Keyboard(x=0, y=120, w=320, h=100, target_textarea=None, parent=page0)
```

### `set_flag(flag, value)`

        Set a flag on the object. If `value` is True, the flag is added; if False, the flag is removed.

        - Parameter `flag` (`int`): The flag to set.
        - Parameter `value` (`bool`): If True, the flag is added; if False, the flag is removed.
        - Returns: None

```python
keyboard_0.set_flag(lv.obj.FLAG.HIDDEN, True)
```
### `toggle_flag(flag)`

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        - Parameter `flag` (`int`): The flag to toggle.
        - Returns: None

```python
keyboard_0.toggle_flag(lv.obj.FLAG.HIDDEN)
```
### `set_state(state, value)`

        Set the state of the keyboard. If `value` is True, the state is set; if False, the state is unset.

        - Parameter `state` (`int`): The state to set.
        - Parameter `value` (`bool`): If True, the state is set; if False, the state is unset.
        - Returns: None

```python
keyboard_0.set_state(lv.STATE.PRESSED, True)
```
### `toggle_state(state)`

        Toggle the state of the keyboard. If the state is set, it is unset; if not set, it is set.

        - Parameter `state` (`int`): The state to toggle.
        - Returns: None

```python
keyboard_0.toggle_state(lv.STATE.PRESSED)
```
### `add_event_cb(handler, event, user_data)`

        Add an event callback to the keyboard. The callback will be called when the specified event occurs.

        - Parameter `handler` (`function`): The callback function to call.
        - Parameter `event` (`int`): The event to listen for.
        - Parameter `user_data` (`Any`): Optional user data to pass to the callback.
        - Returns: None

```python
def keyboard_0_value_changed_event(event_struct):
    global page0, textarea0
    print("Key pressed")

def keyboard_0_ready_event(event_struct):
    global page0, textarea0
    print("Ready")

def keyboard_0_event_handler(event_struct):
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED:
        keyboard_0_value_changed_event(event_struct)
    elif event == lv.EVENT.READY:
        keyboard_0_ready_event(event_struct)
    return

keyboard_0.add_event_cb(keyboard_0_event_handler, lv.EVENT.ALL, None)
```
### `set_textarea(textarea)`

        Set the text area that this keyboard should control. When keys are pressed, the text will be entered into the specified text area.

        - Parameter `textarea` (`lv.textarea`): The text area object to connect to the keyboard.
        - Returns: None

```python
keyboard_0.set_textarea(textarea_0)
```
### `get_textarea()`

        Get the text area that is currently connected to this keyboard.

        - Returns: The connected text area object, or None if no text area is connected.
        - Return type: lv.textarea or None

```python
ta = keyboard_0.get_textarea()
```
### `set_mode(mode)`

        Set the keyboard mode to display different keyboard layouts.

        - Parameter `mode` (`int`): The keyboard mode to set.
        - Returns: None

        Available modes include:

            - lv.keyboard.MODE.TEXT_LOWER: 0.
            - lv.keyboard.MODE.TEXT_UPPER: 1.
            - lv.keyboard.MODE.SYMBOL: 2.
            - lv.keyboard.MODE.NUMBER: 3.

```python
keyboard_0.set_mode(lv.keyboard.MODE.TEXT_LOWER)
```
### `get_mode()`

        Get the current keyboard mode.

        - Returns: The current keyboard mode.
        - Return type: int

        Keyboard modes include:

            - lv.keyboard.MODE.TEXT_LOWER: 0.
            - lv.keyboard.MODE.TEXT_UPPER: 1.
            - lv.keyboard.MODE.SYMBOL: 2.
            - lv.keyboard.MODE.NUMBER: 3.

```python
mode = keyboard_0.get_mode()
```
### `set_popovers(en)`

        Enable or disable popovers for the keyboard. Popovers are additional UI elements that can be displayed when certain keys are pressed.

        - Parameter `en` (`bool`): If True, popovers are enabled; if False, they are disabled.
        - Returns: None

```python
keyboard_0.set_popovers(True)
```
### `get_selected_button()`

        Get the index of the last released button. This can be useful to determine which key was last pressed.

        - Returns: index of the last released button.
        - Return type: int

```python
btn = keyboard_0.get_selected_button()
```
### `get_button_text(btn_id)`

        Get the text of a button by its index.

        - Parameter `btn` (`int`): The index of the button.
        - Returns: The text of the button.
        - Return type: str

```python
keyboard_0.get_button_text(3)
```
### `set_pos(x, y)`

        Set the position of the keyboard.

        - Parameter `x` (`int`): The x-coordinate of the keyboard.
        - Parameter `y` (`int`): The y-coordinate of the keyboard.
        - Returns: None

```python
keyboard_0.set_pos(100, 100)
```
### `set_x(x)`

        Set the x-coordinate of the keyboard.

        - Parameter `x` (`int`): The x-coordinate of the keyboard.
        - Returns: None

```python
keyboard_0.set_x(100)
```
### `set_y(y)`

        Set the y-coordinate of the keyboard.

        - Parameter `y` (`int`): The y-coordinate of the keyboard.
        - Returns: None

```python
keyboard_0.set_y(100)
```
### `set_size(width, height)`

        Set the size of the keyboard.

        - Parameter `width` (`int`): The width of the keyboard.
        - Parameter `height` (`int`): The height of the keyboard.
        - Returns: None

```python
keyboard_0.set_size(300, 200)
```
### `set_width(width)`

        Set the width of the keyboard.

        - Parameter `width` (`int`): The width of the keyboard.
        - Returns: None

```python
keyboard_0.set_width(300)
```
### `get_width()`

        Get the width of the keyboard.

        - Returns: The width of the keyboard.
        - Return type: int

```python
width = keyboard_0.get_width()
```
### `set_height(height)`

        Set the height of the keyboard.

        - Parameter `height` (`int`): The height of the keyboard.
        - Returns: None

```python
keyboard_0.set_height(200)
```
### `get_height()`

        Get the height of the keyboard.

        - Returns: The height of the keyboard.
        - Return type: int

```python
height = keyboard_0.get_height()
```
### `align_to(obj, align, x, y)`

        Align the keyboard to another object.

        - Parameter `obj` (`lv.obj`): The object to align to.
        - Parameter `align` (`int`): The alignment type.
        - Parameter `x` (`int`): The x-offset from the aligned object.
        - Parameter `y` (`int`): The y-offset from the aligned object.
        - Returns: None

```python
keyboard_0.align_to(page_0, lv.ALIGN.BOTTOM_MID, 0, -10)
```
