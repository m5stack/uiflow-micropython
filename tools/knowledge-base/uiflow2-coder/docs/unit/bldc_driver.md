# BLDCDriver Unit

This library is the driver for Unit BLDCDriver.

Support the following products:

    Unit BLDCDriver

## MicroPython Example

#### Motor speed control

The example program gradually increases the motor speed and then stops the motor.

```python
import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from unit import BLDCDriverUnit
import time

title0 = None
label0 = None
label_speed = None
i2c0 = None
bldcdriver_0 = None
speed = None

def setup():
    global title0, label0, label_speed, i2c0, bldcdriver_0, speed
    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("BLDCDriver Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label0 = Widgets.Label("Speed: ", 35, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_speed = Widgets.Label("0", 115, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    bldcdriver_0 = BLDCDriverUnit(i2c0, 0x65)
    bldcdriver_0.set_mode(0)
    bldcdriver_0.set_open_loop_pwm(500)
    bldcdriver_0.set_rpm_int(0)
    speed = 0

def loop():
    global title0, label0, label_speed, i2c0, bldcdriver_0, speed
    M5.update()
    if speed < 300:
        speed = speed + 5
        label_speed.setText(str(speed))
        bldcdriver_0.set_rpm_int(speed)
        time.sleep_ms(100)
    else:
        bldcdriver_0.set_mode(1)
        label_speed.setText(str("0"))
        time.sleep_ms(500)

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

#### BLDCDriverUnit

## `BLDCDriverUnit`
Create an BLDCDriverUnit object.

- Parameter `i2c`: I2C port.
- Type of `i2c`: machine.I2C | PAHUBUnit
- Parameter `address`: BLDCDriverUnit Slave Address.
- Type of `address`: int  list  tuple

```python
from unit import BLDCDriverUnit

unit_bldcdriver_0 = BLDCDriverUnit(i2c0, 0x65)
```

### `get_current_mode`
Get the current mode setting.

- Returns: current mode.
- Return type: int

```python
unit_bldcdriver_0.get_current_mode()
```

### `set_mode`
Set the mode setting.

```python
unit_bldcdriver_0.set_mode(mode)
```

### `get_motor_current_direction`
Get the current direction setting.

- Returns: current direction.
- Return type: int

```python
unit_bldcdriver_0.get_motor_current_direction()
```

### `set_direction`
Set the direction.

- Parameter `model` (`int`): 0 forward, 1 backward.

```python
unit_bldcdriver_0.set_direction()
```

### `get_motor_current_model`
Get the motor current model setting.

- Returns: motor current model.
- Return type: int

```python
unit_bldcdriver_0.get_motor_current_model()
```

### `set_motor_model`
Set the motor model setting.

- Parameter `model` (`int`): 0 mean low speed, 1 mean high speed.

```python
unit_bldcdriver_0.set_motor_model(model)
```

### `get_motor_pole_pairs`
Get the pole pairs setting.

- Returns: motor pole pairs.
- Return type: int

```python
unit_bldcdriver_0.get_motor_pole_pairs()
```

### `set_pole_pairs`
Set pole pairs.

- Parameter `pole` (`int`): pole pairs, range: 0~255.

```python
unit_bldcdriver_0.set_pole_pairs(pole)
```

### `get_motor_status`
Get motor status.

- Returns: motor status.
- Return type: int

```python
unit_bldcdriver_0.get_motor_status()
```

### `get_open_loop_pwm`
Get the open loop pwm.

- Returns: open loop pwm.
- Return type: int

```python
unit_bldcdriver_0.get_open_loop_pwm()
```

### `set_open_loop_pwm`
Set the open loop pwm.

- Parameter `pwm` (`int`): open loop pwm., range: 0~2047.

```python
unit_bldcdriver_0.set_open_loop_pwm(pwm)
```

### `get_read_back_rpm_float`
Get the read back rpm in float.

- Returns: read back rpm.
- Return type: float

```python
unit_bldcdriver_0.get_read_back_rpm_float()
```

### `get_read_back_rpm_int`
Get the read back rpm in int.

- Returns: read back rpm.
- Return type: int

```python
unit_bldcdriver_0.get_read_back_rpm_int()
```

### `get_read_back_rpm_str`
Get the read back rpm in str.

- Returns: read back rpm.
- Return type: str

```python
unit_bldcdriver_0.get_read_back_rpm_str()
```

### `get_read_back_freq_float`
Get the read back frequency in float.

- Returns: read back frequency.
- Return type: float

```python
unit_bldcdriver_0.get_read_back_freq_float()
```

### `get_read_back_freq_int`
Get the read back frequency in int.

- Returns: read back frequency.
- Return type: int

```python
unit_bldcdriver_0.get_read_back_freq_int()
```

### `get_read_back_freq_str`
Get the read back frequency in str.

- Returns: read back frequency.
- Return type: str

```python
unit_bldcdriver_0.get_read_back_freq_str()
```

### `get_rpm_float`
Get the rpm in float.

- Returns: rpm.
- Return type: float

```python
unit_bldcdriver_0.get_rpm_float()
```

### `set_rpm_float`
Set the rpm in float.

- Parameter `rpm` (`float`): Revolutions per minute.

```python
unit_bldcdriver_0.set_rpm_float(rpm)
```

### `get_rpm_int`
Get the rpm in int.

- Returns: Revolutions per minute.
- Return type: int

```python
unit_bldcdriver_0.get_rpm_int()
```

### `set_rpm_int`
Set the rpm in int.

- Parameter `rpm` (`int`): Revolutions per minute.

```python
unit_bldcdriver_0.set_rpm_int(rpm)
```

### `get_pid_value`
Get the PID value.

This method retrieves the PID values from the specified register and returns them as a tuple.

- Returns: A tuple containing the PID values (proportional, integral, derivative).
- Return type: tuple[int, int, int]

```python
unit_bldcdriver_0.get_pid_value()
```

### `set_pid_value`
! Set the PID values (Proportional, Integral, Derivative).

This method sets the PID values to the specified register, which will control the motor's PID behavior.

- Parameter `p` (`int`): The proportional value.
- Parameter `i` (`int`): The integral value.
- Parameter `d` (`int`): The derivative value.

```python
unit_bldcdriver_0.set_pid_value(p, i, d)
```

### `save_data_in_flash`
Save motor data to flash.

```python
unit_bldcdriver_0.save_data_in_flash()
```

### `get_device_spec`
Get device firmware version and I2C address.

This method retrieves either the firmware version or the I2C address of the device based on the provided mode.

- Parameter `mode` (`int`): The mode to determine what information to fetch.
    - `0xFE`: Retrieve firmware version.
    - `0xFF`: Retrieve I2C address.

```python
unit_device.get_device_spec(mode)
```

### `set_i2c_address`
Set the I2C address.

- Parameter `addr` (`int`): The new I2C address, range: 1~127.

```python
unit_device.set_i2c_address(addr)
```
