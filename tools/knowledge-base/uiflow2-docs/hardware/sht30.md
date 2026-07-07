# SHT30

<!-- .. include:: ../refs/hardware.sht30.ref -->

SHT30 is a sensor that can be used to measure temperature and humidity.

## UiFlow2 Example

#### get temperature and humidity

Open the |paper_sht30_example.m5f2| project in UiFlow2.

This example reads the temperature and humidity from the SHT30 sensor.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### get temperature and humidity

This example reads the temperature and humidity from the SHT30 sensor.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

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

Example output:

    None

## **API**

#### SHT30

## SHT30

## SHT30
Create a SHT30 object.

:param I2C i2c: The I2C bus object.
:param int delta_temp: The temperature delta to apply to measurements.
:param int delta_hum: The humidity delta to apply to measurements.
:param int i2c_address: The I2C address of the sensor.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from hardware import Pin
        from hardware import I2C
        from hardware import SHT30

        # Paper
        i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
        sht30 = SHT30(i2c0)

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

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        sht30.get_temperature()

### `get_humidity`
Get the relative humidity in percent.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        sht30.get_humidity()
