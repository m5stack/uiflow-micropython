# Hbridge Unit

<!-- .. sku: U160 -->

<!-- .. sku: U160-V11 -->

<!-- .. include:: ../refs/unit.hbridge.ref -->

This library is the driver for Unit HBridge. Only version v1.1 supports current measurement.

Support the following products:

    =================== ====================
    |Unit HBridge|      |Unit HBridge v1.1|
    =================== ====================

## UiFlow2 Example

#### Motor speed and rotate direction control

Open the |cores3_hbridge_motor_control.m5f2| project in UiFlow2.

This example demonstrates how to control the motor's speed and switch its rotation direction.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Motor speed and rotate direction control

This example demonstrates how to control the motor's speed and switch its rotation direction.

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
from unit import HbridgeUnit
import time

title0 = None
label0 = None
label_speed = None
i2c0 = None
hbridge_0 = None
speed = None
dir2 = None

def setup():
    global title0, label0, label_speed, i2c0, hbridge_0, speed, dir2
    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("HBridge Motor Control", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label0 = Widgets.Label("Speed:", 35, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_speed = Widgets.Label("0", 110, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    hbridge_0 = HbridgeUnit(i2c0, 0x20)
    hbridge_0.set_pwm_freq(1000)
    speed = 0
    hbridge_0.set_direction(0)
    dir2 = True

def loop():
    global title0, label0, label_speed, i2c0, hbridge_0, speed, dir2
    M5.update()
    speed = speed + 1
    label0.setText(str(speed))
    if speed > 99:
        speed = 0
        dir2 = not dir2
        if dir2:
            hbridge_0.set_direction(1)
        else:
            hbridge_0.set_direction(2)
        time.sleep_ms(1000)
    hbridge_0.set_percentage_pwm(speed, 8)
    time.sleep_ms(50)

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

#### HbridgeUnit

## HbridgeUnit
Create an HbridgeUnit object.

:param i2c: I2C port.
:type i2c: machine.I2C | PAHUBUnit
:param address: HbridgeUnit Slave Address.
:type address: int | list | tuple

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from unit import HbridgeUnit

        unit_hbridge_0 = HbridgeUnit(i2c0, 0x20)

### `init_i2c_address`

### `get_driver_config`
Get driver config.

:param int reg:

:returns: driver config.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_hbridge_0.get_driver_config(reg)

### `set_direction`
Set direction

This method controls the motor's movement direction or stops it.

:param int dir: Direction control parameter:
    - 0: Stop
    - 1: Forward
    - 2: Reverse

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_hbridge_0.set_direction(dir)

### `set_8bit_pwm`
Set 8-bit pwm duty cycle

:param int duty: PWM duty, range: 0~255

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_hbridge_0.set_8bit_pwm(duty)

### `set_16bit_pwm`
Set 16-bit pwm duty cycle

:param int duty: pwm duty, range: 0~65535

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_hbridge_0.set_16bit_pwm(duty)

### `set_percentage_pwm`
Set the PWM output based on percentage.

:param int duty: PWM duty cycle as a percentage (0 to 100).
:param int res: PWM resolution (8 or 16 bits), default is 8.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_hbridge_0.set_percentage_pwm(duty, reg)

### `set_pwm_freq`
Set PWM frequency.

:param int freq: The PWM frequnecy.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_hbridge_0.set_pwm_freq(freq)

### `get_adc_value`
Get ADC value.

This method retrieves the ADC value based on the specified resolution.
It supports both 8-bit and 16-bit ADC resolutions. If `raw` is set to `1`,
the raw ADC value is returned. Otherwise, the corresponding voltage is
calculated and returned.

:param int raw: If 1, returns the raw ADC value. If 0, returns the voltage
                (calculated based on ADC value).
:param int res: ADC resolution (8 or 16 bits). Default is 8 bits.

:returns: The raw ADC value or the calculated voltage, depending on `raw`.
:rtype: float or int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_hbridge_0.get_adc_value(raw, res)

### `get_vin_current`
Get the input voltage current (unit: A).

:returns: The input voltage current value.
:rtype: float

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_hbridge_0.get_vin_current()

### `get_device_status`
Get device status.

get firmware version and i2c address.

:param int mode: 0xFE and 0xFF

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_hbridge_0.get_device_status(mode)

### `write_mem_list`

### `read_reg`

### `map`

### `deinit`
