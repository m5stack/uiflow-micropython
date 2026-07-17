# DualKmeter Module

Supported Products:

     DualKmeter Module13.2

Micropython Example:
```python
import os, sys, io
import M5
from M5 import *
from module import DualKmeterModule

M5.begin()
km_0 = DualKmeterModule(address=0x11)
while True:
    if km_0.is_ready():
        print(km_0.get_thermocouple_temperature(scale=km_0.CELSIUS))
```

## class DualKmeterModule

## Constructors

### `class DualKmeterModule(address=0x11)`

    Create a DualKmeterModule object. `address` accepts values from 0x11 to 0x20.

## Methods

### `DualKmeterModule.get_thermocouple_temperature(scale=0) -> float`

    Get the temperature of the thermocouple in the DualKmeter Module. Returns a float value.

    `scale` accepts values of :py`DualKmeter.CELSIUS` or :py`DualKmeter.FAHRENHEIT`.

### `DualKmeterModule.get_kmeter_temperature(scale=0) -> float`

    Get the internal temperature of the DualKmeter Module. Returns a float value.

    `scale` accepts values of :py`DualKmeter.CELSIUS` or :py`DualKmeter.FAHRENHEIT`.

### `DualKmeterModule.get_kmeter_channel() -> int`

    Get the current thermocouple channel being used in the DualKmeter Module. `0` represents channel 1, and `1` represents channel 2.

### `DualKmeterModule.set_kmeter_channel(channel) -> None`

    Set the thermocouple channel to be used in the DualKmeter Module. `0` represents channel 1, and `1` represents channel 2.

### `DualKmeterModule.is_ready() -> bool`

    Check if the measurement result is ready.

### `DualKmeterModule.get_thermocouple_temperature_string(scale=0) -> str`

    Get the temperature of the thermocouple in the DualKmeter Module as a string with a sign.

    `scale` accepts values of :py`DualKmeter.CELSIUS` or :py`DualKmeter.FAHRENHEIT`.

### `DualKmeterModule.get_kmeter_temperature_string(scale=0) -> str`

    Get the internal temperature of the DualKmeter Module as a string with a sign.

    `scale` accepts values of :py`DualKmeter.CELSIUS` or :py`DualKmeter.FAHRENHEIT`.

### `DualKmeterModule.get_fw_ver() -> int`

    Get the firmware version of the DualKmeter Module. Returns an integer version number.

## Constants

### `DualKmeterModule.CELSIUS`

    Celsius scale.

### `DualKmeterModule.FAHRENHEIT`

    Fahrenheit scale.
