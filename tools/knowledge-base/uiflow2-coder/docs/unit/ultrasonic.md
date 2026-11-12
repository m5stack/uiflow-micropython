# Ultrasonic Unit

Support the following products:

    Ultrasonic

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from unit import UltrasoundI2CUnit

label0 = None
i2c0 = None
ultrasonic_0 = None

def setup():
    global label0, i2c0, ultrasonic_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 132, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    ultrasonic_0 = UltrasoundI2CUnit(i2c0)

def loop():
    global label0, i2c0, ultrasonic_0
    M5.update()
    label0.setText(str(ultrasonic_0.get_target_distance(1)))

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

## class UltrasoundI2CUnit

## Constructors

Import with `from unit import UltrasoundI2CUnit`.

### `class UltrasoundI2CUnit(i2c, address=0x57)`

    Create a ULTRASONIC I2C object.

    The parameters is:
        - `i2c` is an initialized I2C bus or PAHUB port.
        - `address` is the I2C address (default 0x57).

## Methods

### `UltrasoundI2CUnit.get_target_distance()`

    Acquire transmitting distance
