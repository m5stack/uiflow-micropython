# Key Unit

Unit Key is a single mechanical key input unit with built-in RGB LED. The key
shaft adopts Blue switch with tactile bump and audible click features. Embedded
with one programable RGB LED - SK6812, supports 256 level brightness.
Two digital IOs are available for key status and LED control key status and
lighting control. Suitable for multiple HMI applications.

Support the following products:

    KeyUnit

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from unit import KeyUnit

label0 = None
key_0 = None

def key_0_wasPressed_event(state):  # noqa: N802
    global label0, key_0
    key_0.set_color(0x6600CC)
    label0.setText(str("pressed"))

def key_0_wasReleased_event(state):  # noqa: N802
    global label0, key_0
    key_0.set_color(0x33CC00)
    label0.setText(str("released"))

def setup():
    global label0, key_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 108, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    key_0 = KeyUnit((8, 9))
    key_0.setCallback(type=key_0.CB_TYPE.WAS_PRESSED, cb=key_0_wasPressed_event)
    key_0.setCallback(type=key_0.CB_TYPE.WAS_RELEASED, cb=key_0_wasReleased_event)

def loop():
    global label0, key_0
    M5.update()
    key_0.tick(None)

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

## class KeyUnit

## Constructors

### `class KeyUnit(port: tuple)`

    Initialize the KeyUnit.

    - Parameter `port` (`tuple`): The port to which the KeyUnit is connected. port[0]: key pin, port[1]: LEDs pin.

## Methods

### `KeyUnit.get_key_state() -> int`

    Get the state of the key.

    - Returns: 0: released, 1: pressed, 2: long pressed.

### `KeyUnit.set_color(color: int) -> None`

    Set the color of the LED.

    - Parameter `color` (`int`): The color of the LED.

### `KeyUnit.set_brightness(br: int) -> None`

    Set the brightness of the LED.

    - Parameter `br` (`int`): The brightness of the LED, range from 0 to 100.

### `KeyUnit.isHolding()`

    Returns whether the Button object is in a long press state.

### `KeyUnit.isPressed()`

    Returns whether the Button object is in a pressed state.

### `KeyUnit.isReleased()`

    Returns whether the Button object is in a released state.

### `KeyUnit.wasClicked()`

    Returns True when the Button object is briefly pressed and released.

### `KeyUnit.wasDoubleClicked()`

    Returns True when the Button object is double-clicked after a certain amount of time.

### `KeyUnit.wasHold()`

    Returns True when the Button object is held down for a certain amount of time.

### `KeyUnit.wasPressed()`

    Returns True when the Button object is pressed.

### `KeyUnit.wasReleased()`

    Returns True when the Button object is released.

### `KeyUnit.wasSingleClicked()`

    Returns True when the Button object is single-clicked after a certain amount of time.

## Event Handling

### `KeyUnit.setCallback(type:Callback_Type, cb)`

    Sets the event callback function.

## Constants

### `KeyUnit.CB_TYPE`

    A CB_TYPE object.

## class CB_TYPE

## Constants

### `CB_TYPE.WAS_CLICKED`

    Single click event type.

### `CB_TYPE.WAS_DOUBLECLICKED`

    Double click event type.

### `CB_TYPE.WAS_HOLD`

    Long press event type.

### `CB_TYPE.WAS_PRESSED`

    Press event type

### `CB_TYPE.WAS_RELEASED`

    Release event type
