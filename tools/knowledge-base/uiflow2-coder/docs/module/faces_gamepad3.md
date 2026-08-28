# Faces Gamepad3 Module

Faces Gamepad3 is an eight-button input module. Button states are active-low:
a cleared bit means that the button is pressed.

Support the following products:

    FacesGamepad3Module

## MicroPython Example

#### Button event display

Register one callback for each button that should be monitored, then call
`FacesGamepad3Module.tick` regularly from the main loop.

```python
import os, sys, io
import M5
from M5 import *
from module import FacesGamepad3Module

title0 = None
label0 = None
faces_gamepad3_0 = None

button_state = None

def faces_gamepad3_0_button_up_event(key_state):
    global title0, label0, faces_gamepad3_0, button_state
    button_state = key_state
    if button_state:
        label0.setText(str((str("Key: ") + str("Up Press"))))
    else:
        label0.setText(str((str("Key: ") + str("Up Release"))))

def faces_gamepad3_0_button_down_event(key_state):
    global title0, label0, faces_gamepad3_0, button_state
    button_state = key_state
    if button_state:
        label0.setText(str((str("Key: ") + str("Down Press"))))
    else:
        label0.setText(str((str("Key: ") + str("Down Release"))))

def setup():
    global title0, label0, faces_gamepad3_0, button_state

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "Faces Gamepad3 CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.Montserrat18
    )
    label0 = Widgets.Label("label0", 5, 104, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.Montserrat18)

    faces_gamepad3_0 = FacesGamepad3Module(address=0x08)
    faces_gamepad3_0.set_callback(faces_gamepad3_0.BUTTON_UP, faces_gamepad3_0_button_up_event)
    faces_gamepad3_0.set_callback(faces_gamepad3_0.BUTTON_DOWN, faces_gamepad3_0_button_down_event)
    label0.setText(str("Pls press key"))

def loop():
    global title0, label0, faces_gamepad3_0, button_state
    M5.update()
    faces_gamepad3_0.tick()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

## API

## `FacesGamepad3Module`
Create a Faces Gamepad3 Module object.

- Parameter `address` (`int`): I2C address. Default is `0x08`.

```python
from module import FacesGamepad3Module

faces_gamepad3 = FacesGamepad3Module()
```

### `get_key_state`
Read the active-low state of all eight buttons.

- Returns: Button state bitmask. A cleared bit means that button is pressed.
- Return type: int

```python
faces_gamepad3.get_key_state()
```

### `is_pressed`
Check whether a button or button combination is pressed.

- Parameter `button` (`int`): One or more `BUTTON_*` masks.
- Parameter `state` (`int`): Optional state previously returned by `get_key_state`.
- Returns: `True` when every selected button is pressed.
- Return type: bool

### `set_callback`
Set the callback for one button's state changes.

The callback receives `pressed`. Pass `None` to remove the callback.

- Parameter `button` (`int`): One `BUTTON_*` constant.
- Parameter `handler`: Callable accepting the pressed state, or `None`.

### `tick`
Poll once and invoke the callback for each changed button.

```python
faces_gamepad3.tick()
```

Gamepad button masks:

    - - Constant
      - Value
    - - `BUTTON_UP`
      - `0x01`
    - - `BUTTON_DOWN`
      - `0x02`
    - - `BUTTON_LEFT`
      - `0x04`
    - - `BUTTON_RIGHT`
      - `0x08`
    - - `BUTTON_A`
      - `0x10`
    - - `BUTTON_B`
      - `0x20`
    - - `BUTTON_SELECT`
      - `0x40`
    - - `BUTTON_START`
      - `0x80`
