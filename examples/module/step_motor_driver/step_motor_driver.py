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
