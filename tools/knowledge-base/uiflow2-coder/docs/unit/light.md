# Light Unit

Support the following products:

    Light

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from unit import LightUnit

label0 = None
light_0 = None

def setup():
    global label0, light_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 132, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    light_0 = LightUnit((36, 26))

def loop():
    global label0, light_0
    M5.update()
    label0.setText(str(light_0.get_digital_value()))

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

## class Light

## Constructors

### `class Light(IO1,IO2)`

    Create a Light object.

    The parameters are:
        - `IO1,IO2` Define digital and analog output pins.

## Methods

### `Light.get_digital_value()`

    Define digital and analog output pins.

### `Light.get_analog_value()`

    Gets the analog (returns 0-65535).

### `Light.get_ohm()`

    Gets the resistance value (returns an integer).
