# DCMotor Module

<!-- .. sku: M021 -->

<!-- .. include:: ../refs/module.dc_motor.ref -->

This library is the driver for Module DCMotor, and the module communicates via I2C.

Support the following products:

    |Module DCMotor|

## UiFlow2 Example

#### Speed Control

Open the |cores3_dc_motor_module_speed_control.m5f2| project in UiFlow2.

This example demonstrates the use of the DCMotor Module to control the speed of a DC motor and display the motor's encoder value in real-time.
The program automatically adjusts the motor speed, gradually increasing or decreasing the speed until it reaches the maximum or minimum value, then reverses the direction.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Speed Control

This example demonstrates the use of the DCMotor Module to control the speed of a DC motor and display the motor's encoder value in real-time.
The program automatically adjusts the motor speed, gradually increasing or decreasing the speed until it reaches the maximum or minimum value, then reverses the direction.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import DCMotorModule
import time

title0 = None
label_speed = None
label_speed_val = None
label_encoder = None
label_encoder_value = None
module_dcmotor_0 = None
last_time = None
direction = None
speed = None
encoder_value = None

def setup():
    global \
        title0, \
        label_speed, \
        label_speed_val, \
        label_encoder, \
        label_encoder_value, \
        module_dcmotor_0, \
        last_time, \
        direction, \
        speed, \
        encoder_value

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("DCMotor Control", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_speed = Widgets.Label("Speed:", 5, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    label_speed_val = Widgets.Label("0", 105, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    label_encoder = Widgets.Label(
        "Encoder Value:", 5, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24
    )
    label_encoder_value = Widgets.Label(
        "0", 203, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24
    )
    module_dcmotor_0 = DCMotorModule()
    module_dcmotor_0.clear_encoder(1)
    direction = True
    speed = 0

def loop():
    global \
        title0, \
        label_speed, \
        label_speed_val, \
        label_encoder, \
        label_encoder_value, \
        module_dcmotor_0, \
        last_time, \
        direction, \
        speed, \
        encoder_value
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) > 100:
        last_time = time.ticks_ms()
        if direction:
            speed = speed + 5
            if speed >= 255:
                direction = False
        else:
            speed = speed - 5
            if speed <= -255:
                direction = True
        module_dcmotor_0.set_motor_speed(1, speed)
        label_speed_val.setText(str(speed))
        encoder_value = module_dcmotor_0.get_encoder(1)
        label_encoder_value.setText(str(encoder_value))
        module_dcmotor_0.clear_encoder(1)

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

#### DCMotorModule

## DCMotorModule
Create an DCMotorModule object.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from module import DCMotorModule

        dcmotor_module = DCMotorModule()

### `set_motor_speed`
Set speed of motor.

:param int id: port num, range: 1~4
:param int speed: motor speed, range: -255~255

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        dcmotor_module.set_motor_speed(id, speed)

### `set_motor_speed_percent`
Set motor speed as a percentage.

:param int id: port num, range: 1~4.
:param float percent: motor speed percent, range: -100.0% ~ +100.0%.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        dcmotor_module.set_motor_speed_percent(id, percent)

### `get_encoder`
Get encoder count.

:param int id: port num, range: 1~4.
:returns: encoder count.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        dcmotor_module.get_encoder()

### `clear_encoder`
Clear encoder value.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        dcmotor_module.clear_encoder()
