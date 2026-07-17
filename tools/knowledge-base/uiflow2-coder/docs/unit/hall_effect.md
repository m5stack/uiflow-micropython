# Hall Effect Unit

Support the following products:

    HallEffect

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from unit import HallEffectUnit

rect0 = None
hall_effect_0 = None

def hall_effect_0_active_event(hall_effect):
    global rect0, hall_effect_0
    rect0.setColor(color=0xFF0000, fill_c=0xFF0000)

def hall_effect_0_negative_event(hall_effect):
    global rect0, hall_effect_0
    rect0.setColor(color=0x33FF33, fill_c=0x33FF33)

def setup():
    global rect0, hall_effect_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    rect0 = Widgets.Rectangle(145, 105, 30, 30, 0xFFFFFF, 0xFFFFFF)

    hall_effect_0 = HallEffectUnit((8, 9))
    hall_effect_0.set_callback(hall_effect_0_active_event, hall_effect_0.IRQ_ACTIVE)
    hall_effect_0.set_callback(hall_effect_0_negative_event, hall_effect_0.IRQ_NEGATIVE)
    hall_effect_0.enable_irq()
    rect0.setColor(color=0x33FF33, fill_c=0x33FF33)

def loop():
    global rect0, hall_effect_0
    M5.update()

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

## class HallEffectUnit

## Constructors

### `class HallEffectUnit(port: tuple)`

    Create a HallEffectUnit object.

    - Parameter `port` (`tuple`): Specify the port number according to the label on the unit.

## Methods

### `HallEffectUnit.get_status()`

    Get the status of the Hall Effect sensor.

### `HallEffectUnit.enable_irq()`

    Enable HAll Effect sensor interrupt.

### `HallEffectUnit.disable_irq()`

    Disable Hall Effect sensor interrupt.

### `HallEffectUnit.set_callback(handler, trigger=HallEffectUnit.IRQ_ACTIVE | HallEffectUnit.IRQ_NEGATIVE)`

    Set the callback function.

## Constants

### `HallEffectUnit.IRQ_ACTIVE`
          HallEffectUnit.IRQ_NEGATIVE

    used to set the trigger mode of the interrupt.
