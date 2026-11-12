
# Button Unit

BUTTON is a single button Unit. The button status can be detected by the input pin by simply capturing the high/low electrical level. With the default active-low configuration, pressing the button produces a low signal and releasing it produces a high signal.

Support the following products:

ButtonUnit

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from unit import ButtonUnit

title0 = None
label1 = None
label0 = None
button_0 = None

def setup():
    global title0, label1, label0, button_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "ButtonUnit Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "Button State:", 395, 150, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label(
        "Button Counter Value:", 1, 102, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    button_0 = ButtonUnit((33, 32), True, type=2)

def loop():
    global title0, label1, label0, button_0
    M5.update()
    label0.setText(str((str("Button Counter Value:") + str((button_0.count_value)))))

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

## class ButtonUnit

## Constructors

### `class ButtonUnit(port, active_low=True, type=SWITCH)`

    Initialize the button input. ButtonUnit is an alias of LIMITUnit.

    - Parameter `port` (`tuple`): Grove GPIO tuple; the input uses the first pin, `port[0]`.
    - Parameter `active_low` (`bool`): Whether a low signal means pressed. Default is True.
    - Parameter `type` (`int`): `SWITCH` (default) or `COUNTER`, imported from `unit.limit`.

    The input enables `Pin.PULL_UP` internally. There is no
    `pullup_active` constructor argument.

```python
from unit import ButtonUnit
from unit.limit import SWITCH, COUNTER

button = ButtonUnit((33, 32), active_low=True, type=SWITCH)
```

## Methods

### `ButtonUnit.count_reset()`

    Reset the count value to zero.

### `ButtonUnit.isHolding()`

    Check if the button is currently being held.

### `ButtonUnit.setCallback(type, cb)`

    Set a callback function for a specified button event type.

    - Parameter `type`: The event type (e.g., WAS_CLICKED, WAS_DOUBLECLICKED).
    - Parameter `cb`: The callback function to be executed for the event.

### `ButtonUnit.tick(pin)`

    Monitor the state transitions of a button based on its pin state and trigger appropriate handlers.
