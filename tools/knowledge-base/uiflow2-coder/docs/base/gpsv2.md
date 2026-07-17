# Atomic GPS Base v2.0

This is the driver library for the Atomic GPS Base v2.0, which is used to get the GPS data.

Support the following products:

    Atom GPS Base v2.0

## MicroPython Example

#### get GPS data

This example demonstrates how to get the GPS data using Atomic GPS Base v2.0.

```python
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

## **API**

#### AtomicGPSV2Base

## `AtomicGPSV2Base`
Create an AtomicGPSV2Base object.

- Parameter `id` (`int`): The UART ID for communication with the GPS module. It can be 1, or 2.
- Parameter `port`: A list or tuple containing the TX and RX pins for UART communication.
- Type of `port`: list | tuple
- Parameter `verbose` (`bool`): Whether to print verbose output.

UIFlow Code Block:

```python
from base.gpsv2 import AtomicGPSV2Base

gps_0 = AtomicGPSV2Base(id=1, tx=5, rx=6)
```

## `ATGM336H`
Create an ATGM336H object.

- Parameter `id` (`int`): The UART ID for communication with the GPS module. It can be 1, or 2.
- Parameter `tx` (`int`): The TX pin is the pin that sends data to the GPS module.
- Parameter `rx` (`int`): The RX pin is the pin that receives data from the GPS module.
- Parameter `pps` (`int`): The PPS pin is the pin that receives the PPS signal from the GPS module.
- Parameter `verbose` (`bool`): Whether to print verbose output.

```python
from driver.atgm336h import ATGM336H

gps_0 = ATGM336H(id=2, tx=5, rx=6)
```

### `set_work_mode`
Set the working mode of the GPS module.

- Parameter `mode` (`int`): The mode to set, defined by the GPS module.

```python
gps_0.set_work_mode(7)
```

### `get_work_mode`
Get the current working mode of the GPS module.

- Returns: The current working mode of the GPS module.
- Return type: int

```python
gps_0.get_work_mode()
```

### `get_antenna_state`
Get the state of the antenna.

- Returns: The antenna state.
- Return type: str

```python
gps_0.get_antenna_state()
```

### `get_gps_time`
Get the current GPS time.

- Returns: The GPS time as a list of strings [hour, minute, second].
- Return type: list[str]

```python
gps_0.get_gps_time()
```

### `get_gps_date`
Get the current GPS date.

- Returns: The GPS date as a list of strings [year, month, day].
- Return type: list[str]

```python
gps_0.get_gps_date()
```

### `get_gps_date_time`
Get the current GPS date and time combined.

- Returns: The GPS date and time as a list of strings [year, month, day, hour, minute, second].
- Return type: list[str]

```python
gps_0.get_gps_date_time()
```

### `get_timestamp`
Get the timestamp of the current GPS time.

- Returns: The timestamp representing the current GPS time.
- Return type: int | float

```python
gps_0.get_timestamp()
```

### `get_latitude`
Get the current latitude.

- Returns: The current latitude in string format.
- Return type: str

```python
gps_0.get_latitude()
```

### `get_longitude`
Get the current longitude.

- Returns: The current longitude in string format.
- Return type: str

```python
gps_0.get_longitude()
```

### `get_altitude`
Get the current altitude.

- Returns: The current altitude in string format.
- Return type: str

```python
gps_0.get_altitude()
```

### `get_satellite_num`
Get the number of satellites used for positioning.

- Returns: The number of satellites.
- Return type: str

```python
gps_0.get_satellite_num()
```

### `get_pos_quality`
Get the quality of the GPS position.

- Returns: The position quality indicator.
- Return type: str

```python
gps_0.get_pos_quality()
```

### `get_corse_over_ground`

### `get_course_over_ground`
Get the course over ground (COG).

Note: Only data returned by the satellite is extracted. If the data does not display properly, it indicates that the satellite did not actually return that data.

- Returns: The course over ground in degrees.
- Return type: str

```python
gps_0.get_course_over_ground()
```

### `get_speed_over_ground`
Get the speed over ground (SOG).

- Returns: The speed over ground in knots.
- Return type: str

```python
gps_0.get_speed_over_ground()
```

### `set_time_zone`
Set the time zone offset for the GPS time.

- Parameter `value` (`int`): The time zone offset value to set.

```python
gps_0.set_time_zone(1)
```

### `get_time_zone`
Get the current time zone offset.

- Returns: The current time zone offset.
- Return type: int

```python
gps_0.get_time_zone()
```

### `deinit`
Deinitialize the GPS unit, stopping any running tasks and releasing resources.

```python
gps_0.deinit()
```
