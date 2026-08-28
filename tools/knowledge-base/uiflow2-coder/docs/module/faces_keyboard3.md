# Faces Keyboard3 Module

Faces Keyboard3 is a keyboard input module with mapped-character Normal mode
and raw-matrix Direct mode. In Direct mode, the callback receives a tuple of
currently pressed key names and the two keyboard LEDs can be controlled.

Support the following products:

    FacesKeyboard3Module

## MicroPython Example

#### Normal mode key events

Normal mode maps key presses to character codes. Direct mode reports a tuple
of currently pressed matrix-key names and also allows LED control.

```python
import os, sys, io
import M5
from M5 import *
from module import FacesKeyboard3Module

title0 = None
label0 = None
faces_keyboard3_0 = None

normal_args = None

def faces_keyboard3_0_normal_event(args):
    global title0, label0, faces_keyboard3_0, normal_args
    normal_args = chr(args)
    label0.setText(str((str("Key: ") + str(normal_args))))

def setup():
    global title0, label0, faces_keyboard3_0, normal_args

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "Faces Keyboard3 CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.Montserrat18
    )
    label0 = Widgets.Label("label0", 3, 110, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.Montserrat18)

    faces_keyboard3_0 = FacesKeyboard3Module(address=0x08)
    faces_keyboard3_0.set_callback(faces_keyboard3_0_normal_event)
    faces_keyboard3_0.set_mode(FacesKeyboard3Module.NORMAL)

def loop():
    global title0, label0, faces_keyboard3_0, normal_args
    M5.update()
    faces_keyboard3_0.tick()

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

## `FacesKeyboard3Module`
Create a Faces Keyboard3 Module object.

- Parameter `address` (`int`): I2C address. Default is `0x08`.

```python
from module import FacesKeyboard3Module

faces_keyboard3 = FacesKeyboard3Module()
```

### `get_mode`
Get the current keyboard operating mode.

`NORMAL` (`0x00`) maps key presses to characters; `DIRECT`
(`0x01`) reports matrix key names.

```python
faces_keyboard3.get_mode()
```

### `set_mode`
Set mapped-character or raw-matrix operating mode.

- Parameter `mode` (`int`): `NORMAL` or `DIRECT`.

```python
faces_keyboard3.set_mode(faces_keyboard3.DIRECT)
```

### `set_led_effect`
Set a keyboard LED effect in Direct mode.

Effects correspond to the keyboard firmware states and LED patterns:

- `LED_EFFECT_1`: `aA` single press; left LED stays on.
- `LED_EFFECT_2`: `aA` double-press lock; left LED blinks every 500 ms.
- `LED_EFFECT_3`: `ALT` active; left LED blinks every 150 ms.
- `LED_EFFECT_4`: `FN` single press; right LED stays on.
- `LED_EFFECT_5`: `FN` double-press lock; right LED blinks every 500 ms.
- `LED_EFFECT_6`: `SYM` double-press lock; right LED blinks every 150 ms.
- `LED_EFFECT_7`: `SYM` single press; LEDs alternate every 500 ms.
- `LED_EFFECT_8`: External effect; LEDs alternate every 200 ms.

- Parameter `effect` (`int`): One of the `LED_EFFECT_*` constants.

```python
faces_keyboard3.set_led_effect(faces_keyboard3.LED_EFFECT_1)
```

### `set_led`
Set the left and right LEDs directly in Direct mode.

```python
faces_keyboard3.set_led(True, False)
```

### `set_callback`
Set the key callback.

In Normal mode, the callback receives an integer key code. In Direct
mode, it receives a tuple containing the currently pressed key names.
Pass `None` to disable the callback.

- Parameter `handler`: Callable accepting the key event value, or `None`.

### `tick`
Poll once and schedule the callback for a new key event.

```python
faces_keyboard3.tick()
```

Keyboard LED constants:

    - - Constant
      - Value
      - Description
    - - `LED_EFFECT_OFF`
      - `0x00`
      - Disable the preset effect
    - - `LED_EFFECT_1`
      - `0x01`
      - Left LED stays on
    - - `LED_EFFECT_2`
      - `0x02`
      - Left LED blinks slowly
    - - `LED_EFFECT_3`
      - `0x03`
      - Left LED blinks quickly
    - - `LED_EFFECT_4`
      - `0x04`
      - Right LED stays on
    - - `LED_EFFECT_5`
      - `0x05`
      - Right LED blinks slowly
    - - `LED_EFFECT_6`
      - `0x06`
      - Right LED blinks quickly
    - - `LED_EFFECT_7`
      - `0x07`
      - Left and right LEDs alternate slowly
    - - `LED_EFFECT_8`
      - `0x08`
      - Left and right LEDs alternate quickly

In Normal mode, `KEY_BACKSPACE` is `0x08`, `KEY_ENTER` is `0x0D`, and
`KEY_DELETE` is `0x7F`. LED effects and manual LED states are available
only in Direct mode.
