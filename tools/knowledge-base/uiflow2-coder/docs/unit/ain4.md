
# AIN4-20mA Unit

The following products are supported:

AIN4_20MAUnit

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from unit import AIN4_20MAUnit

title0 = None
label0 = None
label1 = None
i2c0 = None
ain4_20ma_0 = None

def setup():
    global title0, label0, label1, i2c0, ain4_20ma_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("AIN 4-20mA Unit Test", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("CH1 Current:", 1, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("CH1 ADC:", 1, 96, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    ain4_20ma_0 = AIN4_20MAUnit(i2c0, 0x55)
    ain4_20ma_0.set_cal_current(20)

def loop():
    global title0, label0, label1, i2c0, ain4_20ma_0
    M5.update()
    label0.setText(str((str("CH1 Current:") + str((ain4_20ma_0.get_current_value())))))
    label1.setText(str((str("CH1 ADC:") + str((ain4_20ma_0.get_adc_raw_value())))))

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

## class AIN4_20MAUnit

## Constructors

### `class AIN4_20MAUnit(i2c, address)`

    Init I2C port & UNIT AIN 4-20mA I2C Address.

    - Parameter `i2c` (`I2C`): I2C port to use.
    - Parameter `address` (`intlisttuple`): I2C address of the Unit AIN4-20mA.

## Methods

### `AIN4_20MAUnit.get_adc_raw_value() -> int`

    Retrieves the raw ADC value from the channel.

    - Returns: Raw ADC value as a 12-bit integer.

### `AIN4_20MAUnit.get_current_value() -> float`

    Retrieves the current value (in mA) from the channel.

    - Returns: Current value in milliamperes (mA).

### `AIN4_20MAUnit.set_cal_current(val)`

    Sets the calibration current for the specified channel.

    - Parameter `val` (`int`): The calibration current value, ranging from 4 to 20 mA.

### `AIN4_20MAUnit.get_firmware_version() -> int`

    Retrieves the firmware version of the AIN 4-20mA unit.

    - Returns: Firmware version.

### `AIN4_20MAUnit.get_i2c_address() -> str`

    Retrieves the current I2C address of the AIN 4-20mA unit.

    - Returns: I2C address as a string in hexadecimal format.

### `AIN4_20MAUnit.set_i2c_address(addr)`

    Sets a new I2C address for the AIN 4-20mA unit.

    - Parameter `addr` (`int`): The new I2C address, must be between 0x08 and 0x77.
