# Mini ToF-90° Unit

<!-- .. sku: U196 -->

<!-- .. include:: ../refs/unit.tof90.ref -->

This is the driver library of Mini ToF-90° Unit, which is used to obtain data from the distance sensor.

Support the following products:

    |ToF90Unit|

## UiFlow2 Example

#### get distance value

Open the |tof90_core2_example.m5f2| project in UiFlow2.

This example gets the distance value of the Mini ToF-90° Unit and displays it on the screen.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### get distance value

This example gets the distance value of the Mini ToF-90° Unit and displays it on the screen.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from unit import ToF90Unit

title0 = None
label0 = None
label1 = None
i2c0 = None
minitof90_0 = None

def setup():
    global title0, label0, label1, i2c0, minitof90_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "Core2 Mini ToF-90  Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 2, 110, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", -85, 149, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    minitof90_0 = ToF90Unit(i2c0, 0x29)
    minitof90_0.start_continuous()

def loop():
    global title0, label0, label1, i2c0, minitof90_0
    M5.update()
    if minitof90_0.get_data_ready():
        label0.setText(str((str("Distance:") + str((str((minitof90_0.get_range())) + str("mm"))))))

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

#### ToF90Unit

## ToF90Unit
Create an VL53L0X object.

:param I2C i2c: The I2C bus the VL53L0X is connected to.
:param int address: The I2C address of VL53L0X. Default is 0x29.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from unit import ToF90Unit

        i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
        tof_0 = ToF90Unit(i2c0)

#### VL53L0X

## VL53L0X
Create an VL53L0X object.

:param I2C i2c: The I2C bus the VL53L0X is connected to.
:param int address: The I2C address of VL53L0X. Default is 0x29.
:param int io_timeout_ms: The timeout for the I/O operations. Default is 0.

MicroPython Code Block:

    .. code-block:: python

        from driver import VL53L0X

        i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
        vl53l0x_0 = VL53L0X(i2c0)

### `get_signal_rate_limit`

### `set_signal_rate_limit`

### `get_measurement_timing_budget`
Get the measurement timing budget in microseconds.

:returns: The measurement timing budget in microseconds.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        budget_ms = vl53l0x_0.get_measurement_timing_budget()

### `set_measurement_timing_budget`
Set the measurement timing budget in microseconds.

:param int budget_us: The measurement timing budget in microseconds(range 20000 - 200000).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        budget_ms = vl53l0x_0.get_measurement_timing_budget()

### `get_distance`
Perform a single reading of the range for an object in front of the sensor and return the distance in centimeters.

:returns: The distance in centimeters.
:rtype: float

MicroPython Code Block:

    .. code-block:: python

        distance = vl53l0x_0.get_distance()

### `get_range`
Perform a single reading of the range for an object in front of the sensor and return the distance in millimeters.

:returns: The distance in millimeters.
:rtype: float

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        distance = vl53l0x_0.get_range()

### `get_data_ready`
Get the data ready status of the sensor.

:returns: The data ready status of the sensor.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        data_ready = vl53l0x_0.get_data_ready()

### `do_range_measurement`
Perform a single reading of the range for an object in front of the
sensor, but without return the distance.

### `read_range`
Return a range reading in millimeters.
Note: Avoid calling this directly. If you do single mode, you need
to call `do_range_measurement` first. Or your program will stuck or
timeout occurred.

### `is_continuous_mode`
Get the continuous mode status of the sensor.

:returns: The continuous mode status of the sensor.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        continuous_mode = vl53l0x_0.is_continuous_mode()

### `continuous_mode`
Activate the continuous mode manager

### `start_continuous`
Set the sensor to continuous mode.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        vl53l0x_0.start_continuous()

### `stop_continuous`
Set the sensor to single ranging mode.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        vl53l0x_0.stop_continuous()

### `set_address`
Set a new I2C address to the sensor.

:param int new_address: The 7-bit int that is to be assigned to the VL53L0X sensor.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        vl53l0x_0.set_address(0x2A)
