
# GRBL Module

<!-- .. include:: ../refs/module.grbl.ref -->

GRBL 13.2 is a three-axis stepper motor driver module in the M5Stack stacking module series. It uses an ATmega328P-AU controller with three sets of DRV8825PWPR stepper motor driver chip control ways, which can drive three bipolar steppers at the same time.

Support the following products:

|GRBLModule|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import GRBLModule

grbl_0 = None

def setup():
    global grbl_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    grbl_0 = GRBLModule(address=0x70)
    print(grbl_0.get_message())
    print(grbl_0.get_status())
    print(grbl_0.get_idle_state())
    print(grbl_0.get_lock_state())
    grbl_0.set_mode(GRBLModule.MODE_ABSOLUTE)
    grbl_0.unlock()
    grbl_0.turn(5, 5, 10, 5)
    grbl_0.wait_idle()
    grbl_0.lock()

def loop():
    global grbl_0
    M5.update()

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

UIFLOW2 Example:

<!-- .. only:: builder_html -->

    |grbl_example.m5f2|

## class GRBLModule

## Constructors

<!-- .. class:: GRBLModule(address) -->

    Initialize the GRBLModule.

    :param hex address: The I2C address of the device.

    UIFLOW2:

## Methods

<!-- .. method:: GRBLModule.g_code(command) -->

    Send the G-code command.

    :param  command: The G-code command.

    UIFLOW2:

<!-- .. method:: GRBLModule.get_code_time(code) -->

    Get the time of the code.

    :return (int): The estimated time of the command.
    :param  code: The G-code command

    UIFLOW2:

<!-- .. method:: GRBLModule.turn(x, y, z, speed) -->

    Turn the motor to a specific position.

    :param  x: The position of the X motor, 1.6&#x3D;360°.
    :param  y: The position of the Y motor, 1.6&#x3D;360°.
    :param  z: The position of the Z motor, 1.6&#x3D;360°.
    :param  speed: The speed of the motor.

    UIFLOW2:

<!-- .. method:: GRBLModule.set_mode(mode) -->

    Set the mode of the motor.

    :param  mode: The mode of the motor.
        Options:
        - ``Absolute``: GRBLModule.MODE_ABSOLUTE
        - ``Relative``: GRBLModule.MODE_RELATIVE

    UIFLOW2:

<!-- .. method:: GRBLModule.init(x_step, y_step, z_step, acc) -->

    Initialize the motor.

    :param  x_step: The step of the X motor.
    :param  y_step: The step of the Y motor.
    :param  z_step: The step of the Z motor.
    :param  acc: The acceleration of the motor.

    UIFLOW2:

<!-- .. method:: GRBLModule.flush() -->

    Flush the buffer.

    UIFLOW2:

<!-- .. method:: GRBLModule.get_message() -->

    Get the message.

    :return (str): The message string.

    UIFLOW2:

<!-- .. method:: GRBLModule.get_status() -->

    Get the status.

    :return (str): The status string.

    UIFLOW2:

<!-- .. method:: GRBLModule.get_idle_state() -->

    Get the idle state.

    :return (bool): The idle state.

    UIFLOW2:

<!-- .. method:: GRBLModule.get_lock_state() -->

    Get the lock state.

    :return (bool): The lock state.

    UIFLOW2:

<!-- .. method:: GRBLModule.wait_idle() -->

    Wait until the motor is idle.

    UIFLOW2:

<!-- .. method:: GRBLModule.unlock_alarm_state() -->

    Unlock the alarm state.

    UIFLOW2:

<!-- .. method:: GRBLModule.lock() -->

    Lock the motor.

    UIFLOW2:

<!-- .. method:: GRBLModule.unlock() -->

    Unlock the motor.

    UIFLOW2:

## Constants

<!-- .. data:: GRBLModule.MODE_ABSOLUTE -->
<!-- .. data:: GRBLModule.MODE_RELATIVE -->

    Motor mode
