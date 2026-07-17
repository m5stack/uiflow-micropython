# Mini ToF-90° Unit

This is the driver library of Mini ToF-90° Unit, which is used to obtain data from the distance sensor.

Support the following products:

    ToF90Unit

## MicroPython Example

#### get distance value

This example gets the distance value of the Mini ToF-90° Unit and displays it on the screen.

```python
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

## **API**

#### ToF90Unit

## `ToF90Unit`
Create an VL53L0X object.

- Parameter `i2c` (`I2C`): The I2C bus the VL53L0X is connected to.
- Parameter `address` (`int`): The I2C address of VL53L0X. Default is 0x29.

```python
from unit import ToF90Unit

i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
tof_0 = ToF90Unit(i2c0)
```

#### VL53L0X

## `VL53L0X`
Create an VL53L0X object.

- Parameter `i2c` (`I2C`): The I2C bus the VL53L0X is connected to.
- Parameter `address` (`int`): The I2C address of VL53L0X. Default is 0x29.
- Parameter `io_timeout_ms` (`int`): The timeout for the I/O operations. Default is 0.

```python
from driver import VL53L0X

i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
vl53l0x_0 = VL53L0X(i2c0)
```

### `get_signal_rate_limit`

### `set_signal_rate_limit`

### `get_measurement_timing_budget`
Get the measurement timing budget in microseconds.

- Returns: The measurement timing budget in microseconds.
- Return type: int

```python
budget_ms = vl53l0x_0.get_measurement_timing_budget()
```

### `set_measurement_timing_budget`
Set the measurement timing budget in microseconds.

- Parameter `budget_us` (`int`): The measurement timing budget in microseconds(range 20000 - 200000).

```python
budget_ms = vl53l0x_0.get_measurement_timing_budget()
```

### `get_distance`
Perform a single reading of the range for an object in front of the sensor and return the distance in centimeters.

- Returns: The distance in centimeters.
- Return type: float

```python
distance = vl53l0x_0.get_distance()
```

### `get_range`
Perform a single reading of the range for an object in front of the sensor and return the distance in millimeters.

- Returns: The distance in millimeters.
- Return type: float

```python
distance = vl53l0x_0.get_range()
```

### `get_data_ready`
Get the data ready status of the sensor.

- Returns: The data ready status of the sensor.
- Return type: bool

```python
data_ready = vl53l0x_0.get_data_ready()
```

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

- Returns: The continuous mode status of the sensor.
- Return type: bool

```python
continuous_mode = vl53l0x_0.is_continuous_mode()
```

### `continuous_mode`
Activate the continuous mode manager

### `start_continuous`
Set the sensor to continuous mode.

```python
vl53l0x_0.start_continuous()
```

### `stop_continuous`
Set the sensor to single ranging mode.

```python
vl53l0x_0.stop_continuous()
```

### `set_address`
Set a new I2C address to the sensor.

- Parameter `new_address` (`int`): The 7-bit int that is to be assigned to the VL53L0X sensor.

```python
vl53l0x_0.set_address(0x2A)
```
