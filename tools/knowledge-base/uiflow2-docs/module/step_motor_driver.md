
# StepMotorDriver Module

<!-- .. include:: ../refs/module.step_motor_driver.ref -->

StepMotor Driver Module 13.2 V1.1 is a stepper motor driver adapted to M5 main control, using STM32+HR8825 stepper motor drive scheme, providing 3-way bipolar stepper motor control interface.

Support the following products:

|StepMotorDriverModule|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import StepMotorDriverModule
import time

stepmotor_driver_0 = None

DIR = None

def setup():
    global stepmotor_driver_0, DIR

    M5.begin()
    Widgets.fillScreen(0x222222)

    stepmotor_driver_0 = StepMotorDriverModule(
        address=0x27, step_pin=(16, 12, 15), dir_pin=(17, 13, 0)
    )
    print(stepmotor_driver_0.get_all_limit_switch_state())
    print(stepmotor_driver_0.get_limit_switch_state(0))
    print(stepmotor_driver_0.get_fault_io_state(StepMotorDriverModule.MOTOR_X))
    print(stepmotor_driver_0.get_firmware_version())
    stepmotor_driver_0.reset_motor(
        StepMotorDriverModule.MOTOR_X, StepMotorDriverModule.MOTOR_STATE_ENABLE
    )
    stepmotor_driver_0.set_motor_state(StepMotorDriverModule.MOTOR_STATE_ENABLE)
    stepmotor_driver_0.set_microstep(StepMotorDriverModule.STEP_FULL)
    stepmotor_driver_0.set_motor_direction(StepMotorDriverModule.MOTOR_X, 1)
    stepmotor_driver_0.set_motor_pwm_freq(StepMotorDriverModule.MOTOR_X, 1000)
    stepmotor_driver_0.motor_control(StepMotorDriverModule.MOTOR_X, 1)
    DIR = 0

def loop():
    global stepmotor_driver_0, DIR
    M5.update()
    if DIR:
        stepmotor_driver_0.set_motor_direction(StepMotorDriverModule.MOTOR_X, 1)
    else:
        stepmotor_driver_0.set_motor_direction(StepMotorDriverModule.MOTOR_X, 0)
    DIR = not DIR
    time.sleep(2)

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

    |step_motor_driver.m5f2|

## class StepMotorDriverModule

## Constructors

<!-- .. class:: StepMotorDriverModule(address, step_pin, dir_pin) -->

    Initialize the StepMotorDriverModule.

    :param hex address: The I2C address of the device.
    :param tuple step_pin: The step pin (X, Y, Z) of the motor.
    :param tuple dir_pin: The dir pin (X, Y, Z) of the motor.

    UIFLOW2:

## Methods

<!-- .. method:: StepMotorDriverModule.reset_motor(motor_id, state) -->

    Reset the motor.

    :param  motor_id: The motor to reset.
        Options:
        - ``X``: StepMotorDriverModule.MOTOR_X
        - ``Y``: StepMotorDriverModule.MOTOR_Y
        - ``Z``: StepMotorDriverModule.MOTOR_Z
    :param bool state: The state of the motor.

    UIFLOW2:

<!-- .. method:: StepMotorDriverModule.set_motor_state(state) -->

    Enable or disable the motor.

    :param bool state: The state of the motor.

    UIFLOW2:

<!-- .. method:: StepMotorDriverModule.set_microstep(step) -->

    Set the microstep.

    :param  step: The microstep value.
        Options:
        - ``FULL``: StepMotorDriverModule.STEP_FULL
        - ``1/2``: StepMotorDriverModule.STEP1_2
        - ``1/4``: StepMotorDriverModule.STEP1_4
        - ``1/8``: StepMotorDriverModule.STEP1_8
        - ``1/16``: StepMotorDriverModule.STEP1_16
        - ``1/32``: StepMotorDriverModule.STEP1_32

    UIFLOW2:

<!-- .. method:: StepMotorDriverModule.set_motor_pwm_freq(motor_id, freq) -->

    Set the motor pwm freq.

    :param  motor_id: The motor to set the freq.
        Options:
        - ``X``: StepMotorDriverModule.MOTOR_X
        - ``Y``: StepMotorDriverModule.MOTOR_Y
        - ``Z``: StepMotorDriverModule.MOTOR_Z
    :param int freq: The freq value.

    UIFLOW2:

<!-- .. method:: StepMotorDriverModule.set_motor_direction(motor_id, direction) -->

    Set the motor direction.

    :param  motor_id: The motor to set the direction.
        Options:
        - ``X``: StepMotorDriverModule.MOTOR_X
        - ``Y``: StepMotorDriverModule.MOTOR_Y
        - ``Z``: StepMotorDriverModule.MOTOR_Z
    :param bool direction: The direction value.
        Options:
        - ``Positive``: 1
        - ``Negative``: 0

    UIFLOW2:

<!-- .. method:: StepMotorDriverModule.get_all_limit_switch_state() -->

    Get all io state.

    UIFLOW2:

<!-- .. method:: StepMotorDriverModule.get_limit_switch_state(switch_id) -->

    Get the io state.

    :param int switch_id: The io id.

    UIFLOW2:

<!-- .. method:: StepMotorDriverModule.get_fault_io_state(motor_id) -->

    Get the fault io state.

    :param int motor_id: The motor id.
        Options:
        - ``X``: StepMotorDriverModule.MOTOR_X
        - ``Y``: StepMotorDriverModule.MOTOR_Y
        - ``Z``: StepMotorDriverModule.MOTOR_Z

    UIFLOW2:

<!-- .. method:: StepMotorDriverModule.motor_control(motor_id, state) -->

    Control the motor to rotate/stop.

    :param  motor_id: The motor id.
        Options:
        - ``X``: StepMotorDriverModule.MOTOR_X
        - ``Y``: StepMotorDriverModule.MOTOR_Y
        - ``Z``: StepMotorDriverModule.MOTOR_Z
    :param bool state: The state value.
        Options:
        - ``Rotate``: 1
        - ``Stop``: 0

    UIFLOW2:

<!-- .. method:: StepMotorDriverModule.get_firmware_version() -->

    Get the firmware version.

    UIFLOW2:

<!-- .. method:: StepMotorDriverModule.set_i2c_address(new_address) -->

    Set the i2c address.

    :param int new_address: The new address.

    UIFLOW2:

## Constants

<!-- .. data:: StepMotorDriverModule.MOTOR_X -->
<!-- .. data:: StepMotorDriverModule.MOTOR_Y -->
<!-- .. data:: StepMotorDriverModule.MOTOR_Z -->

    Motor IDs

<!-- .. data:: StepMotorDriverModule.MOTOR_STATE_ENABLE -->
<!-- .. data:: StepMotorDriverModule.MOTOR_STATE_DISABLE -->

    Motor states

<!-- .. data:: StepMotorDriverModule.INPUT_REG -->
<!-- .. data:: StepMotorDriverModule.OUTPUT_REG -->
<!-- .. data:: StepMotorDriverModule.POLINV_REG -->
<!-- .. data:: StepMotorDriverModule.CONFIG_REG -->
<!-- .. data:: StepMotorDriverModule.FAULT_REG -->
<!-- .. data:: StepMotorDriverModule.RESET_REG -->
<!-- .. data:: StepMotorDriverModule.FIRM_REG -->
<!-- .. data:: StepMotorDriverModule.I2C_REG -->

    Register addresses

<!-- .. data:: StepMotorDriverModule.STEP_FULL -->
<!-- .. data:: StepMotorDriverModule.STEP1_2 -->
<!-- .. data:: StepMotorDriverModule.STEP1_4 -->
<!-- .. data:: StepMotorDriverModule.STEP1_8 -->
<!-- .. data:: StepMotorDriverModule.STEP1_16 -->
<!-- .. data:: StepMotorDriverModule.STEP1_32 -->

    Microstep values
