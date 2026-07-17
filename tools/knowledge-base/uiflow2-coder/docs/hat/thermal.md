# Thermal Hat

The following products are supported:

    ThermalHat

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from hat import ThermalHat

label0 = None
i2c0 = None
hat_thermal_0 = None

def setup():
    global label0, i2c0, hat_thermal_0

    M5.begin()
    label0 = Widgets.Label("label0", 39, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(26), sda=Pin(0), freq=100000)
    hat_thermal_0 = ThermalHat(i2c0, 0x33)

def loop():
    global label0, i2c0, hat_thermal_0
    M5.update()
    hat_thermal_0.update_temperature_buffer()
    label0.setText(str(hat_thermal_0.get_max_temperature))

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

## class ThermalHat

## Constructors

### `class ThermalHat(i2c, address: int = 0x33)`

    Create a ThermalHat object.

    - Parameter `i2c`: I2C object
    - Parameter `address`: the I2C address of the device. Default is 0x33.

ThermalHat class inherits ThermalUnit class, See `unit.ThermaltUnit.Methods <unit.ThermaltUnit.Methods>` for more details.
