# Fan v1.1 Module

<!-- .. sku: M013-V11 -->

<!-- .. include:: ../refs/module.fan.ref -->

This is the driver library of Fan Module, which is used to control the fan.

Support the following products:

    |FAN|

## UiFlow2 Example

#### control module fan v1.1

Open the |fan_cores3_example.m5f2| project in UiFlow2.

Initializes the fan module, sets the fan status, PWM frequency and duty cycle, and displays the fan status, speed, PWM frequency and duty cycle on the screen in real time. When the user touches the screen, the fan status toggles on/off.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### control module fan v1.1

Initializes the fan module, sets the fan status, PWM frequency and duty cycle, and displays the fan status, speed, PWM frequency and duty cycle on the screen in real time. When the user touches the screen, the fan status toggles on/off.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import FanModule
import time

title0 = None
label0 = None
label1 = None
label2 = None
label3 = None
fan_v11_0 = None

def setup():
    global title0, label0, label1, label2, label3, fan_v11_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "FanModuleV1.1 CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 0, 57, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 0, 94, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 0, 133, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("label3", 0, 168, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    fan_v11_0 = FanModule(address=0x18)
    fan_v11_0.set_fan_state(True)
    fan_v11_0.set_pwm_frequency(0)
    fan_v11_0.set_pwm_duty_cycle(80)

def loop():
    global title0, label0, label1, label2, label3, fan_v11_0
    M5.update()
    label0.setText(str((str("Fan State:") + str((fan_v11_0.get_fan_state())))))
    label1.setText(str((str("Fan PWM Freq:") + str((fan_v11_0.get_single_frequency())))))
    label2.setText(str((str("Fan PWM duty cycle:") + str((fan_v11_0.get_pwm_duty_cycle())))))
    label3.setText(str((str("Fan rpm:") + str((fan_v11_0.get_fan_rpm())))))
    if M5.Touch.getCount():
        fan_v11_0.set_fan_state(not (fan_v11_0.get_fan_state()))
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

#### FanModule

## FanModule
### `set_fan_state`
Set the fan state to on or off.

:param bool state: The state of the fan.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        fan_v11_0.set_fan_state(True)

### `get_fan_state`
Get current fan state.

:returns: The current fan state.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        fan_v11_0.get_fan_state()

### `set_pwm_frequency`
Set the PWM frequency of the fan.

:param int freq: The PWM frequency of the fan.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        fan_v11_0.set_pwm_frequency(2)

### `get_pwm_frequency`
Get current PWM frequency.

:returns: The current PWM frequency.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        fan_v11_0.get_pwm_frequency()

### `set_pwm_duty_cycle`
Set the PWM duty cycle of the fan.

:param int duty_cycle: The PWM duty cycle of the fan.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        fan_v11_0.set_pwm_duty_cycle(50)

### `get_pwm_duty_cycle`
Get current PWM duty cycle.

:returns: The current PWM duty cycle.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        fan_v11_0.get_pwm_duty_cycle()

### `get_fan_rpm`
Get current fan RPM.

:returns: The current fan RPM.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        fan_v11_0.get_fan_rpm()

### `get_single_frequency`
Get current single frequency.

:returns: The current single frequency.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        fan_v11_0.get_single_frequency()

### `write_flash`
Save the current configuration(fan status, PWM frequency, and PWM duty cycle) to the flash.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        fan_v11_0.write_flash()

### `get_firmware_version`
Get current firmware version.

:returns: The current firmware version.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        fan_v11_0.get_firmware_version()

### `get_i2c_address`
Get current I2C address.

:returns: The current I2C address.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        fan_v11_0.get_i2c_address()

### `set_i2c_address`
Set the I2C address of the fan.

:param int addr: The I2C address of the fan.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        fan_v11_0.set_i2c_address(0x18)
