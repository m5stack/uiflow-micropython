# Atomic GPS Base

This is the driver library of ATOM GPS Base, which is used to obtain data from the
GPS module.

Support the following products:

    ATOM GPS         ATOM GPS Base

## MicroPython Example

#### get gps data

This example gets the GPS data of the ATOM GPS Base and displays it on the serial monitor.

```python
import os, sys, io
import M5
from M5 import *
from base import ATOMGPSBase
import time

title0 = None
base_gps = None

def setup():
    global title0, base_gps

    M5.begin()
    title0 = Widgets.Title("GPS Base", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)

    base_gps = ATOMGPSBase(2, port=(5, 6))
    base_gps.set_time_zone(0)

def loop():
    global title0, base_gps
    M5.update()
    print(base_gps.get_gps_time())
    print(base_gps.get_gps_date())
    print(base_gps.get_gps_date_time())
    print(base_gps.get_timestamp())
    print(base_gps.get_latitude())
    print(base_gps.get_longitude())
    print(base_gps.get_altitude())
    print(base_gps.get_satellite_num())
    print(base_gps.get_pos_quality())
    print(base_gps.get_corse_over_ground())
    print(base_gps.get_speed_over_ground())
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

#### ATOMGPSBase

## `ATOMGPSBase`
Create an ATOMGPSBase object.

- Parameter `id` (`int`): The UART ID to use (0, 1, or 2). Default is 2.
- Parameter `port`: A list or tuple containing the TX and RX pin numbers.
- Type of `port`: list | tuple
- Parameter `debug` (`bool`): Whether to enable debug mode. Default is False.

```python
from machine import UART
from base import ATOMGPSBase

gps = ATOMGPSBase(id=1, port=(16, 17))
```

### `get_antenna_state`
Get the state of the antenna.

- Returns: The current antenna state.
- Return type: str

```python
gps.get_antenna_state()
```

### `get_gps_time`
Get the current GPS time.

- Returns: The GPS time as a list of strings [hour, minute, second].
- Return type: list[str]

```python
gps.get_gps_time()
```

### `get_gps_date`
Get the current GPS date.

- Returns: The GPS date as a list of strings [day, month, year].
- Return type: list[str]

```python
gps.get_gps_date()
```

### `get_gps_date_time`
Get the current GPS date and time combined.

- Returns: The GPS date and time as a list of strings [year, month, day, hour, minute, second].
- Return type: list[str]

```python
gps.get_gps_date_time()
```

### `get_timestamp`
Get the timestamp of the current GPS time.

- Returns: The timestamp representing the current GPS time.
- Return type: int | float

```python
gps.get_timestamp()
```

### `get_latitude`
Get the current latitude.

- Returns: The current latitude.
- Return type: str

```python
gps.get_latitude()
```

### `get_longitude`
Get the current longitude.

- Returns: The current longitude.
- Return type: str

```python
gps.get_longitude()
```

### `get_altitude`
Get the current altitude.

- Returns: The current altitude.
- Return type: str

```python
gps.get_altitude()
```

### `get_satellite_num`
Get the number of satellites used for positioning.

- Returns: The number of satellites.
- Return type: str

```python
gps.get_satellite_num()
```

### `get_pos_quality`
Get the quality of the GPS position.

- Returns: The position quality indicator.
- Return type: str

```python
gps.get_pos_quality()
```

### `get_corse_over_ground`
Get the course over ground (COG).

- Returns: The course over ground in degrees.
- Return type: str

```python
gps.get_corse_over_ground()
```

### `get_speed_over_ground`
Get the speed over ground (SOG).

- Returns: The speed over ground in knots.
- Return type: str

```python
gps.get_speed_over_ground()
```

### `set_time_zone`
Set the time zone offset for the GPS time.

- Parameter `value` (`int`): The time zone offset value to set.

```python
gps.set_time_zone(8)
```

### `get_time_zone`
Get the current time zone offset.

- Returns: The current time zone offset.
- Return type: int

```python
gps.get_time_zone()
```

### `deinit`
Deinitialize the GPS unit, stopping any running tasks and releasing resources.

```python
gps.deinit()
```
