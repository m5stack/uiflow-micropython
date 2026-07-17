# EARTH Unit

Support the following products:

    EARTH

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from unit import EarthUnit

label0 = None
earth_0 = None

def setup():
    global label0, earth_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 132, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    earth_0 = EarthUnit((36, 26))

def loop():
    global label0, earth_0
    M5.update()
    label0.setText(str(earth_0.get_digital_value()))

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

## class Earth

## Constructors

### `class Earth(port)`

    Create an Earth object.

    The parameters is:
        - `port` Is the pin number of the port

## Methods

### `EARTH.get_analog_value()`

    This method allows you to read the analog captured by EARTH and return an integer value. The value ranges from 0 to 65535.

### `EARTH.get_digital_value()`

    This method allows you to read the amount of numbers collected by EARTH and return an integer value. The value ranges from 0 to 1.

### `EARTH.get_voltage_mv()`

    This method allows you to read the voltage value collected by EARTH and return an integer value. It ranges from 0 to 3300.

### `EARTH.humidity()`

    This method allows you to read the voltage value collected by EARTH and return a floating-point value. Range 0.0 to 1.0.

### `EARTH.set_calibrate()`

    This method allows setting the maximum (0-3300) and minimum (0-3300) values for calibrating the EARTH sensor.
