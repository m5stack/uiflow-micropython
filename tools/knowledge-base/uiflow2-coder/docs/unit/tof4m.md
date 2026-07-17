# ToF4M Unit

This is the driver library of ToF4M Unit, which is used to obtain distance data from the
VL53L1CXV0FY sensor.

Support the following products:

    ToF4M

## MicroPython Example

#### get distance value

This example gets the distance value of the ToF4M Unit and displays it on the screen.

```python
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

## **API**

#### TOF4MUnit

## `TOF4MUnit`
`TOF4MUnit` is an alias of `VL53L1X` in `m5stack/libs/driver/vl53l1x.py`.

Create a VL53L1X object.

- Parameter `i2c` (`I2C`): The I2C bus the ToF4M Unit is connected to.
- Parameter `address` (`int`): The I2C address of the device. Default is 0x29.

```python
from hardware import I2C
from unit import TOFUnit

i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
tof_0 = TOFUnit(i2c0)
```

### `get_model_info`

### `get_distance`
The distance in units of millimeters.

- Returns: Distance in millimeters or None if measurement is invalid.
- Return type: int or None

```python
distance = tof_0.get_distance
```

### `set_continuous_start_measurement`
Starts continuous measure operation.

```python
tof_0.set_continuous_start_measurement()
```

### `set_continuous_stop_measurement`
Stops measure operation.

```python
tof_0.set_continuous_stop_measurement()
```

### `clear_interrupt`

### `get_data_ready`
Returns true if new data is ready, otherwise false.

- Returns: True if new data is ready.
- Return type: bool

```python
if tof_0.get_data_ready:
    distance = tof_0.get_distance
```

### `get_measurement_timing_budget`
Get measurement duration in milliseconds.

- Returns: The timing budget in milliseconds.
- Return type: int

```python
budget = tof_0.get_measurement_timing_budget
```

### `set_measurement_timing_budget`
Set the measurement timing budget in milliseconds.

- Parameter `val` (`int`): Timing budget in milliseconds.

```python
tof_0.set_measurement_timing_budget(100)
```

### `get_distance_mode`
Get the distance mode.

- Returns: distance mode(1=short, 2=long).
- Return type: int

```python
mode = tof_0.get_distance_mode
```

### `set_distance_mode`
Set the distance mode.

- Parameter `mode` (`int`): 1=short, 2=long.

```python
tof_0.set_distance_mode(2)  # Long distance mode
```

### `set_i2c_address`
Set a new I2C address to the instantiated object.

- Parameter `new_address` (`int`): The new I2C address.

```python
tof_0.set_i2c_address(42)
```

#### VL53L1CXV0FY

## `VL53L1X`
Create a VL53L1X object.

- Parameter `i2c` (`I2C`): The I2C bus the ToF4M Unit is connected to.
- Parameter `address` (`int`): The I2C address of the device. Default is 0x29.

```python
from hardware import I2C
from unit import TOFUnit

i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
tof_0 = TOFUnit(i2c0)
```

### `get_model_info`

### `get_distance`
The distance in units of millimeters.

- Returns: Distance in millimeters or None if measurement is invalid.
- Return type: int or None

```python
distance = tof_0.get_distance
```

### `set_continuous_start_measurement`
Starts continuous measure operation.

```python
tof_0.set_continuous_start_measurement()
```

### `set_continuous_stop_measurement`
Stops measure operation.

```python
tof_0.set_continuous_stop_measurement()
```

### `clear_interrupt`

### `get_data_ready`
Returns true if new data is ready, otherwise false.

- Returns: True if new data is ready.
- Return type: bool

```python
if tof_0.get_data_ready:
    distance = tof_0.get_distance
```

### `get_measurement_timing_budget`
Get measurement duration in milliseconds.

- Returns: The timing budget in milliseconds.
- Return type: int

```python
budget = tof_0.get_measurement_timing_budget
```

### `set_measurement_timing_budget`
Set the measurement timing budget in milliseconds.

- Parameter `val` (`int`): Timing budget in milliseconds.

```python
tof_0.set_measurement_timing_budget(100)
```

### `get_distance_mode`
Get the distance mode.

- Returns: distance mode(1=short, 2=long).
- Return type: int

```python
mode = tof_0.get_distance_mode
```

### `set_distance_mode`
Set the distance mode.

- Parameter `mode` (`int`): 1=short, 2=long.

```python
tof_0.set_distance_mode(2)  # Long distance mode
```

### `set_i2c_address`
Set a new I2C address to the instantiated object.

- Parameter `new_address` (`int`): The new I2C address.

```python
tof_0.set_i2c_address(42)
```
