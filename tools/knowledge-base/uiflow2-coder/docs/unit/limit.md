
# Limit Unit

The Unit Limit is a travel switch unit that provides a limit trigger signal to the MCU or other master peripherals by pulling the digital signal interface from 3.3V high to 0V low when the switch handle is closed by an external force. It is suitable for all kinds of moving machinery and equipment to control its stroke and carry out terminal limit protection.

Support the following products:

LimitUnit

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from unit import LIMITUnit

title0 = None
label1 = None
label0 = None
limit_0 = None

def setup():
    global title0, label1, label0, limit_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "LimitUnit Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "Button State:", 395, 150, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label(
        "Limit Counter Value:", 1, 102, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    limit_0 = LIMITUnit((33, 32), True, type=2)
    limit_0.count_reset()

def loop():
    global title0, label1, label0, limit_0
    M5.update()
    label0.setText(str((str("Limit Counter Value:") + str((limit_0.count_value)))))

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

## class LIMITUnit

## Constructors

Import with `from unit import LIMITUnit`.

### `class LIMITUnit(port, active_low=True, type=1)`

    Initialize a LIMITUnit with the specified port, active-low configuration, and operation mode.

    - Parameter `port` (`tuple`): Pin tuple; port[0] is the GPIO connected to the limit switch.
    - Parameter `active_low` (`bool`): Determines whether the limit signal is active-low. Default is True.
    - Parameter `type` (`int`): Operation mode: 1 (switch, default) or 2 (edge counter).

## Methods

### `LIMITUnit.count_reset()`

    Reset the count value to zero.

### `LIMITUnit.isHolding()`

    Check if the limit is currently being held.

### `LIMITUnit.setCallback(type, cb)`

    Set a callback function for a specified limit event type.

    - Parameter `type`: The event type (e.g., WAS_CLICKED, WAS_DOUBLECLICKED).
    - Parameter `cb`: The callback function to be executed for the event.

### `LIMITUnit.tick(pin)`

    Monitor the state transitions of a limit based on its pin state and trigger appropriate handlers.
