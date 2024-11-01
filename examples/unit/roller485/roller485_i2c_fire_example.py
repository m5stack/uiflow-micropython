# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import Roller485Unit


title0 = None
label0 = None
label1 = None
label2 = None
label3 = None
label4 = None
i2c1 = None
roller485_0 = None


output = None
mode = None


def btn_b_was_clicked_event(state):
    global title0, label0, label1, label2, label3, label4, i2c1, roller485_0, output, mode
    output = output ^ (0x01 << 0)
    roller485_0.set_motor_output_state(output)


def btn_a_was_clicked_event(state):
    global title0, label0, label1, label2, label3, label4, i2c1, roller485_0, output, mode
    mode = mode + 1
    if mode > 4:
        mode = 1


def setup():
    global title0, label0, label1, label2, label3, label4, i2c1, roller485_0, output, mode

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("Roller485 I2C Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("mode:", 1, 63, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("motor state:", 2, 108, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("speed:", 2, 152, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("mode", 40, 215, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("on/off", 126, 215, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btn_b_was_clicked_event)
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btn_a_was_clicked_event)

    i2c1 = I2C(1, scl=Pin(22), sda=Pin(21), freq=100000)
    roller485_0 = Roller485Unit(i2c1, address=0x64, mode=Roller485Unit.I2C_MODE)
    roller485_0.set_motor_output_state(0)
    output = roller485_0.get_motor_output_state()
    mode = roller485_0.get_motor_mode()
    label0.setText(str((str("mode:") + str(mode))))
    label1.setText(str((str("motor state:") + str(output))))


def loop():
    global title0, label0, label1, label2, label3, label4, i2c1, roller485_0, output, mode
    M5.update()
    label0.setText(str((str("mode:") + str(mode))))
    label1.setText(str((str("motor state:") + str(output))))
    if mode == 1:
        roller485_0.set_motor_speed(20000)
        roller485_0.set_speed_max_current(400)
        label2.setText(str((str("speed:") + str((roller485_0.get_motor_speed_readback())))))
    elif mode == 2:
        roller485_0.set_motor_position(1000)
        roller485_0.set_position_max_current(400)
        label2.setText(str((str("position:") + str((roller485_0.get_motor_position_readback())))))
    elif mode == 3:
        roller485_0.set_motor_max_current(400)
        label2.setText(str((str("current:") + str((roller485_0.get_motor_current_readback())))))
    elif mode == 4:
        label2.setText(str((str("encoder:") + str((roller485_0.get_encoder_value())))))
    roller485_0.set_motor_mode(mode)


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
