# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import ODriveModule


odrive_0 = None


def setup():
    global odrive_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    odrive_0 = ODriveModule(2, (13, 5))
    print(odrive_0.get_velocity())
    print(odrive_0.get_vbus_voltage())
    print(odrive_0.get_phase_current())
    print(odrive_0.get_bus_current())
    print(odrive_0.get_encoder_shadow_count())
    print(odrive_0.get_encoder_pos_estimate())
    print(odrive_0.get_motor_temp())
    odrive_0.set_position(10, 1, 1)
    odrive_0.set_velocity(1, 1)
    odrive_0.set_current(1)
    odrive_0.set_gain(0.1, 0.1, 0.1)
    odrive_0.set_control_mode(ODriveModule.CONTROL_MODE_VOLTAGE_CONTROL)
    odrive_0.set_control_input_pos(0)
    odrive_0.trapezoidal_move(0)
    odrive_0.run_state(ODriveModule.AXIS_STATE_IDLE, 0)
    odrive_0.save_config()
    odrive_0.erase_config()
    odrive_0.set_default_config()
    odrive_0.check_error()
    odrive_0.reboot()


def loop():
    global odrive_0
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
