# ToF4M Unit

<!-- .. sku: U056 -->

<!-- .. include:: ../refs/unit.tof4m.ref -->

This is the driver library of ToF4M Unit, which is used to obtain distance data from the
VL53L1CXV0FY sensor.

Support the following products:

    |ToF4M|

## UiFlow2 Example

#### get distance value

Open the |tof4m_core_example.m5f2| project in UiFlow2.

This example gets the distance value of the ToF4M Unit and displays it on the screen.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### get distance value

This example gets the distance value of the ToF4M Unit and displays it on the screen.

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
from unit import TOF4MUnit

title0 = None
label1 = None
i2c1 = None
tof4m_0 = None

distance = None

def setup():
    global title0, label1, i2c1, tof4m_0, distance

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("ToF4MUnit CoreS3 Test", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 1, 121, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c1 = I2C(1, scl=Pin(22), sda=Pin(21), freq=100000)
    tof4m_0 = TOF4MUnit(i2c1, 0x29)
    tof4m_0.set_distance_mode(2)
    tof4m_0.set_measurement_timing_budget(500)
    tof4m_0.set_continuous_start_measurement()

def loop():
    global title0, label1, i2c1, tof4m_0, distance
    M5.update()
    if tof4m_0.get_data_ready:
        label1.setText(str((str("Distance:") + str((str(distance) + str("mm"))))))

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

#### TOF4MUnit

## TOF4MUnit
<!-- Failed to find class TOF4MUnit in /tmp/mr462_split/m5stack/libs/unit/tof4m.py -->

#### VL53L1CXV0FY

## VL53L1X
Create a VL53L1X object.

:param I2C i2c: The I2C bus the ToF4M Unit is connected to.
:param int address: The I2C address of the device. Default is 0x29.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from hardware import I2C
        from unit import TOFUnit

        i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
        tof_0 = TOFUnit(i2c0)

### `get_model_info`

### `get_distance`
The distance in units of millimeters.

:returns: Distance in millimeters or None if measurement is invalid.
:rtype: int or None

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        distance = tof_0.get_distance

### `set_continuous_start_measurement`
Starts continuous measure operation.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        tof_0.set_continuous_start_measurement()

### `set_continuous_stop_measurement`
Stops measure operation.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        tof_0.set_continuous_stop_measurement()

### `clear_interrupt`

### `get_data_ready`
Returns true if new data is ready, otherwise false.

:returns: True if new data is ready.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        if tof_0.get_data_ready:
            distance = tof_0.get_distance

### `get_measurement_timing_budget`
Get measurement duration in milliseconds.

:returns: The timing budget in milliseconds.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        budget = tof_0.get_measurement_timing_budget

### `set_measurement_timing_budget`
Set the measurement timing budget in milliseconds.

:param int val: Timing budget in milliseconds.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        tof_0.set_measurement_timing_budget(100)

### `get_distance_mode`
Get the distance mode.

:returns: distance mode(1=short, 2=long).
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        mode = tof_0.get_distance_mode

### `set_distance_mode`
Set the distance mode.

:param int mode: 1=short, 2=long.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        tof_0.set_distance_mode(2)  # Long distance mode

### `set_i2c_address`
Set a new I2C address to the instantiated object.

:param int new_address: The new I2C address.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        tof_0.set_i2c_address(42)
