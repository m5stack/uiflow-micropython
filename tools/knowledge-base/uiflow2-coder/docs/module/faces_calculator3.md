# Faces Calculator3 Module

Faces Calculator3 is a calculator keypad module. It reports released key
codes through a callback and uses I2C address `0x08` by default.

Support the following products:

    FacesCalculator3Module

## MicroPython Example

#### Key event display

Call `FacesCalculator3Module.tick` regularly from the main loop to poll
for new key events.

```python
import os, sys, io
import M5
from M5 import *
from module import FacesCalculator3Module

title0 = None
label0 = None
faces_calculator3_0 = None

event_args = None

def faces_calculator3_0_key_event(args):
    global title0, label0, faces_calculator3_0, event_args
    event_args = chr(args)
    label0.setText(str((str("Key: ") + str(event_args))))

def setup():
    global title0, label0, faces_calculator3_0, event_args

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "Faces Calculator3 CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.Montserrat18
    )
    label0 = Widgets.Label("label0", 1, 112, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.Montserrat18)

    faces_calculator3_0 = FacesCalculator3Module(address=0x08)
    faces_calculator3_0.set_callback(faces_calculator3_0_key_event)

def loop():
    global title0, label0, faces_calculator3_0, event_args
    M5.update()
    faces_calculator3_0.tick()

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

## `FacesCalculator3Module`
Create a Faces Calculator3 Module object.

- Parameter `address` (`int`): I2C address. Default is `0x08`.

```python
from module import FacesCalculator3Module

faces_calculator3 = FacesCalculator3Module()
```

### `set_callback`
Set the callback for key events.

The callback receives the released key code. Pass `None` to disable it.

- Parameter `handler`: Callable accepting one key code, or `None`.

### `tick`
Poll once and invoke the callback when a key event is available.

```python
faces_calculator3.tick()
```

Calculator key constants:

    - - Constant
      - Value
      - Key
    - - `KEY_BACKSPACE`
      - `0x08`
      - Backspace
    - - `KEY_ENTER`
      - `0x0D`
      - Enter
    - - `KEY_AC`
      - `0x41`
      - All clear
    - - `KEY_MEMORY`
      - `0x4D`
      - Memory
    - - `KEY_PERCENT`
      - `0x25`
      - Percent
    - - `KEY_DIVIDE`
      - `0x2F`
      - Divide
    - - `KEY_MULTIPLY`
      - `0x2A`
      - Multiply
    - - `KEY_MINUS`
      - `0x2D`
      - Minus
    - - `KEY_PLUS`
      - `0x2B`
      - Plus
    - - `KEY_SIGN`
      - `0x60`
      - Sign
    - - `KEY_EQUAL`
      - `0x3D`
      - Equal
