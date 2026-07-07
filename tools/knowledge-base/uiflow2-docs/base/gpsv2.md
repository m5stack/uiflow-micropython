# Atomic GPS Base v2.0

<!-- .. sku: A134-V2 -->

<!-- .. include:: ../refs/base.gpsv2.ref -->

This is the driver library for the Atomic GPS Base v2.0, which is used to get the GPS data.

Support the following products:

    |Atom GPS Base v2.0|

## UiFlow2 Example

#### get GPS data

Open the |base_gpsv2_atom_example.m5f2| project in UiFlow2.

This example demonstrates how to get the GPS data using Atomic GPS Base v2.0.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### get GPS data

This example demonstrates how to get the GPS data using Atomic GPS Base v2.0.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import RGB
from base import AtomicGPSV2Base
import time

rgb = None
base_gpsv2 = None

def setup():
    global rgb, base_gpsv2

    M5.begin()
    rgb = RGB()
    rgb.set_screen([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    rgb.set_brightness(20)
    rgb.fill_color(0x33FF33)
    base_gpsv2 = AtomicGPSV2Base(2, port=(22, 19))
    base_gpsv2.set_work_mode(7)
    base_gpsv2.set_time_zone(0)

def loop():
    global rgb, base_gpsv2
    M5.update()
    print((str("longitude:") + str((base_gpsv2.get_longitude()))))
    print((str("altitude:") + str((base_gpsv2.get_altitude()))))
    print((str("latitude:") + str((base_gpsv2.get_latitude()))))
    time.sleep(1)

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

#### AtomicGPSV2Base

## AtomicGPSV2Base
Create an AtomicGPSV2Base object.

:param int id: The UART ID for communication with the GPS module. It can be 1, or 2.
:param port: A list or tuple containing the TX and RX pins for UART communication.
:type port: list | tuple
:param bool verbose: Whether to print verbose output.

UIFlow Code Block:

MicroPython Code Block:

    .. code-block:: python

        from base.gpsv2 import AtomicGPSV2Base

        gps_0 = AtomicGPSV2Base(id=1, tx=5, rx=6)

## ATGM336H
Create an ATGM336H object.

:param int id: The UART ID for communication with the GPS module. It can be 1, or 2.
:param int tx: The TX pin is the pin that sends data to the GPS module.
:param int rx: The RX pin is the pin that receives data from the GPS module.
:param int pps: The PPS pin is the pin that receives the PPS signal from the GPS module.
:param bool verbose: Whether to print verbose output.

MicroPython Code Block:

    .. code-block:: python

        from driver.atgm336h import ATGM336H

        gps_0 = ATGM336H(id=2, tx=5, rx=6)

### `set_work_mode`
Set the working mode of the GPS module.

:param int mode: The mode to set, defined by the GPS module.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        gps_0.set_work_mode(7)

### `get_work_mode`
Get the current working mode of the GPS module.

:returns: The current working mode of the GPS module.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        gps_0.get_work_mode()

### `get_antenna_state`
Get the state of the antenna.

:returns: The antenna state.
:rtype: str

MicroPython Code Block:

    .. code-block:: python

        gps_0.get_antenna_state()

### `get_gps_time`
Get the current GPS time.

:returns: The GPS time as a list of strings [hour, minute, second].
:rtype: list[str]

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        gps_0.get_gps_time()

### `get_gps_date`
Get the current GPS date.

:returns: The GPS date as a list of strings [year, month, day].
:rtype: list[str]

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        gps_0.get_gps_date()

### `get_gps_date_time`
Get the current GPS date and time combined.

:returns: The GPS date and time as a list of strings [year, month, day, hour, minute, second].
:rtype: list[str]

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        gps_0.get_gps_date_time()

### `get_timestamp`
Get the timestamp of the current GPS time.

:returns: The timestamp representing the current GPS time.
:rtype: int | float

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        gps_0.get_timestamp()

### `get_latitude`
Get the current latitude.

:returns: The current latitude in string format.
:rtype: str

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        gps_0.get_latitude()

### `get_longitude`
Get the current longitude.

:returns: The current longitude in string format.
:rtype: str

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        gps_0.get_longitude()

### `get_altitude`
Get the current altitude.

:returns: The current altitude in string format.
:rtype: str

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        gps_0.get_altitude()

### `get_satellite_num`
Get the number of satellites used for positioning.

:returns: The number of satellites.
:rtype: str

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        gps_0.get_satellite_num()

### `get_pos_quality`
Get the quality of the GPS position.

:returns: The position quality indicator.
:rtype: str

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        gps_0.get_pos_quality()

### `get_corse_over_ground`

### `get_course_over_ground`
Get the course over ground (COG).

Note: Only data returned by the satellite is extracted. If the data does not display properly, it indicates that the satellite did not actually return that data.

:returns: The course over ground in degrees.
:rtype: str

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        gps_0.get_course_over_ground()

### `get_speed_over_ground`
Get the speed over ground (SOG).

:returns: The speed over ground in knots.
:rtype: str

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        gps_0.get_speed_over_ground()

### `set_time_zone`
Set the time zone offset for the GPS time.

:param int value: The time zone offset value to set.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        gps_0.set_time_zone(1)

### `get_time_zone`
Get the current time zone offset.

:returns: The current time zone offset.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        gps_0.get_time_zone()

### `deinit`
Deinitialize the GPS unit, stopping any running tasks and releasing resources.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        gps_0.deinit()
