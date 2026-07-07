# BLDCDriver Unit

<!-- .. sku: U181 -->

<!-- .. include:: ../refs/unit.bldc_driver.ref -->

This library is the driver for Unit BLDCDriver.

Support the following products:

    |Unit BLDCDriver|

## UiFlow2 Example

#### Motor speed control

Open the |cores3_bldc_driver_example.m5f2| project in UiFlow2.

The example program gradually increases the motor speed and then stops the motor.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Motor speed control

The example program gradually increases the motor speed and then stops the motor.

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

Example output:

    None

## **API**

#### BLDCDriverUnit

## BLDCDriverUnit
Create an BLDCDriverUnit object.

:param i2c: I2C port.
:type i2c: machine.I2C | PAHUBUnit
:param address: BLDCDriverUnit Slave Address.
:type address: int | list | tuple

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from unit import BLDCDriverUnit

        unit_bldcdriver_0 = BLDCDriverUnit(i2c0, 0x65)

### `get_current_mode`
Get the current mode setting.

:returns: current mode.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.get_current_mode()

### `set_mode`
Set the mode setting.

:param: int mode: 0 mean open loop, 1 mean close loop.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.set_mode(mode)

### `get_motor_current_direction`
Get the current direction setting.

:returns: current direction.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.get_motor_current_direction()

### `set_direction`
Set the direction.

:param int model: 0 forward, 1 backward.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.set_direction()

### `get_motor_current_model`
Get the motor current model setting.

:returns: motor current model.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.get_motor_current_model()

### `set_motor_model`
Set the motor model setting.

:param int model: 0 mean low speed, 1 mean high speed.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.set_motor_model(model)

### `get_motor_pole_pairs`
Get the pole pairs setting.

:returns: motor pole pairs.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.get_motor_pole_pairs()

### `set_pole_pairs`
Set pole pairs.

:param int pole: pole pairs, range: 0~255.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.set_pole_pairs(pole)

### `get_motor_status`
Get motor status.

:returns: motor status.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.get_motor_status()

### `get_open_loop_pwm`
Get the open loop pwm.

:returns: open loop pwm.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.get_open_loop_pwm()

### `set_open_loop_pwm`
Set the open loop pwm.

:param int pwm:  open loop pwm., range: 0~2047.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.set_open_loop_pwm(pwm)

### `get_read_back_rpm_float`
Get the read back rpm in float.

:returns: read back rpm.
:rtype: float

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.get_read_back_rpm_float()

### `get_read_back_rpm_int`
Get the read back rpm in int.

:returns: read back rpm.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.get_read_back_rpm_int()

### `get_read_back_rpm_str`
Get the read back rpm in str.

:returns: read back rpm.
:rtype: str

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.get_read_back_rpm_str()

### `get_read_back_freq_float`
Get the read back frequency in float.

:returns: read back frequency.
:rtype: float

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.get_read_back_freq_float()

### `get_read_back_freq_int`
Get the read back frequency in int.

:returns: read back frequency.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.get_read_back_freq_int()

### `get_read_back_freq_str`
Get the read back frequency in str.

:returns: read back frequency.
:rtype: str

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.get_read_back_freq_str()

### `get_rpm_float`
Get the rpm in float.

:returns: rpm.
:rtype: float

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.get_rpm_float()

### `set_rpm_float`
Set the rpm in float.

:param float rpm: Revolutions per minute.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.set_rpm_float(rpm)

### `get_rpm_int`
Get the rpm in int.

:returns: Revolutions per minute.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.get_rpm_int()

### `set_rpm_int`
Set the rpm in int.

:param int rpm: Revolutions per minute.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.set_rpm_int(rpm)

### `get_pid_value`
Get the PID value.

This method retrieves the PID values from the specified register and returns them as a tuple.

:returns: A tuple containing the PID values (proportional, integral, derivative).
:rtype: tuple[int, int, int]

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.get_pid_value()

### `set_pid_value`
! Set the PID values (Proportional, Integral, Derivative).

This method sets the PID values to the specified register, which will control the motor's PID behavior.

:param int p: The proportional value.
:param int i: The integral value.
:param int d: The derivative value.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.set_pid_value(p, i, d)

### `save_data_in_flash`
Save motor data to flash.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_bldcdriver_0.save_data_in_flash()

### `get_device_spec`
Get device firmware version and I2C address.

This method retrieves either the firmware version or the I2C address of the device based on the provided mode.

:param int mode: The mode to determine what information to fetch.
    - `0xFE`: Retrieve firmware version.
    - `0xFF`: Retrieve I2C address.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_device.get_device_spec(mode)

### `set_i2c_address`
Set the I2C address.

:param int addr: The new I2C address, range: 1~127.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_device.set_i2c_address(addr)
