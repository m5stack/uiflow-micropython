# SHT30

SHT30 is a sensor that can be used to measure temperature and humidity.

## MicroPython Example

#### get temperature and humidity

This example reads the temperature and humidity from the SHT30 sensor.

```python
import os, sys, io
import M5
from M5 import *
from hardware import SHT30

sht30 = None

def setup():
    global sht30

    M5.begin()
    Widgets.fillScreen(0xEEEEEE)

    sht30 = SHT30()

def loop():
    global sht30
    M5.update()
    print((str("Humidity:") + str((sht30.get_humidity()))))
    print((str("Temperature:") + str((sht30.get_temperature()))))

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

## **API**

#### SHT30

## `SHT30`

## `SHT30`
Create a SHT30 object.

- Parameter `i2c` (`I2C`): The I2C bus object.
- Parameter `delta_temp` (`int`): The temperature delta to apply to measurements.
- Parameter `delta_hum` (`int`): The humidity delta to apply to measurements.
- Parameter `i2c_address` (`int`): The I2C address of the sensor.

```python
from hardware import Pin
from hardware import I2C
from hardware import SHT30

# Paper
i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
sht30 = SHT30(i2c0)
```

### `is_present`

### `set_delta`

### `send_cmd`

### `clear_status`

### `reset`

### `status`

### `measure`

### `measure_int`

### `get_temperature`
Get the temperature in Celsius.

```python
sht30.get_temperature()
```

### `get_humidity`
Get the relative humidity in percent.

```python
sht30.get_humidity()
```
