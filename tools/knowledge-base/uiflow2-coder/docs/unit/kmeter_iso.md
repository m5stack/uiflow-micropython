# Kmeter ISO Unit

Supported Products:

    KmeterISOUnit

Micropython Example:
```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import KMeterISOUnit
import time

M5.begin()
i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
kmeter_iso_0 = KMeterISOUnit(i2c0, 0x66)
while True:
    if kmeteriso_0.is_ready():
        print(kmeteriso_0.get_thermocouple_temperature(0))
        print(kmeteriso_0.get_internal_temperature(0))
    time.sleep_ms(250)
```

## class KmeterISOUnit

## Constructors

### `class KmeterISOUnit(i2c, address=0x66)`

    - Parameter `i2c` (`object`): the I2C object.
    - Parameter `address` (`int`): 0x08 ~ 0x77.

## Methods

### `KmeterISOUnit.get_thermocouple_temperature(scale=0) -> float`

    Get the temperature of the thermocouple in the KmeterISO Unit. Returns a float value.

    `scale` accepts values of :py`KmeterISO.CELSIUS` or :py`KmeterISO.FAHRENHEIT`.

### `KmeterISOUnit.get_internal_temperature(scale=0) -> float`

    Get the internal temperature of the KmeterISO Unit. Returns a float value.

    `scale` accepts values of :py`KmeterISO.CELSIUS` or :py`KmeterISO.FAHRENHEIT`.

### `KmeterISOUnit.is_ready() -> bool`

    Check if the measurement result is ready.

### `KmeterISOUnit.get_thermocouple_temperature_string(scale=0) -> str`

    Get the temperature of the thermocouple in the KmeterISO Unit as a string with a sign.

    `scale` accepts values of :py`KmeterISO.CELSIUS` or :py`KmeterISO.FAHRENHEIT`.

### `KmeterISOUnit.get_internal_temperature_string(scale=0) -> str`

    Get the internal temperature of the KmeterISO Unit as a string with a sign.

    `scale` accepts values of :py`KmeterISO.CELSIUS` or :py`KmeterISO.FAHRENHEIT`.

### `KmeterISOUnit.get_device_spec(mode) -> int`

    Get the firmware version of the KmeterISO Unit. Returns an integer version number.

    - Parameter `mode` (`int`):

    int     mode
    0xFE    firmware version
    0xFF    i2c address

### `KmeterISOUnit.set_i2c_address(address) -> int`

    Set the i2c address can be changed by the user and this address should be between 0x08 and 0x77.

## Constants

### `KmeterISOUnit.CELSIUS`

    Celsius scale.

### `KmeterISOUnit.FAHRENHEIT`

    Fahrenheit scale.
