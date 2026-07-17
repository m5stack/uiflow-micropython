# Kmeter Unit

The `Kmeter Unit` is a K-type thermocouple sensor with I2C communication interface. The hardware adopts ESP32-C3 main control + MAX31855KASA+T 14bit thermocouple digital conversion chip. The conversion chip supports thermocouple probes with a measuring range of -200°C to 1350°C.

Supported Products:

    Kmeter Unit

Micropython Example:
```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import KMeterUnit
import time

i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
kmeter_0 = KMeterUnit(i2c0, 0x66)
print(kmeter_0.get_firmware_version())
while True:
    print(kmeter_0.get_thermocouple_temperature(kmeter_0.CELSIUS))
    print(kmeter_0.get_internal_temperature(kmeter_0.CELSIUS))
    time.sleep_ms(250)
```

## class KmeterUnit

## Constructors

### `class KmeterUnit(i2c, address)`

    - Parameter `i2c` (`object`): the I2C object.
    - Parameter `address` (`int`): 0x08 ~ 0x77.

## Methods

### `KmeterUnit.get_thermocouple_temperature(scale) -> float`

    Get the temperature of the thermocouple in the Kmeter Unit. Returns a float value.

    - Parameter `scale` (`bool`): accepts values of :py`KmeterUnit.CELSIUS` or :py`KmeterUnit.FAHRENHEIT`.

### `KmeterUnit.get_internal_temperature(scale) -> float`

    Get the internal temperature of the Kmeter Unit. Returns a float value.

    - Parameter `scale` (`bool`): accepts values of :py`KmeterUnit.CELSIUS` or :py`KmeterUnit.FAHRENHEIT`.

### `KmeterUnit.get_sleep_time() -> int`

    Get the sleep time in seconds. Returns a int value.

    - Return: `int`: 0 ~ 65535.

### `KmeterUnit.get_firmware_version() -> float`

    Get the firmware version of the Kmeter Unit. Returns an integer version number.

    - Return: `float`

### `KmeterUnit.get_i2c_address() -> int`

    Get the i2c address of this device should be between 0x08 and 0x77.

    - Return: `int`: 0x08 ~ 0x77.

### `KmeterUnit.set_sleep_time(sleep) -> None`

    Set the sleep time in seconds.

    - Parameter `sleep` (`int`): 0 ~ 65535

### `KmeterUnit.set_wakeup_trigger(mode) -> str`

    set wakeup trigger mode in timer or i2c scl low level.

    - Parameter `mode` (`bool`): timer(True) or i2c scl low(False)

### `KmeterUnit.set_i2c_address(address) -> int`

    Set the i2c address can be changed by the user and this address should be between 0x08 and 0x77.

    - Parameter `address` (`int`): 0x08 ~ 0x77

## Constants

### `KmeterUnit.CELSIUS`

    Celsius scale.

### `KmeterUnit.FAHRENHEIT`

    Fahrenheit scale.
