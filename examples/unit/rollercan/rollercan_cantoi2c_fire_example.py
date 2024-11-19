# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import RollerCANUnit
from unit import CANUnit
from unit import ENVUnit


title0 = None
label5 = None
label7 = None
label0 = None
label6 = None
label1 = None
label2 = None
label3 = None
label4 = None
env3_0 = None
can_0 = None
rollercan_0 = None


output = None
mode = None


def btnb__event(state):
    global \
        title0, \
        label5, \
        label7, \
        label0, \
        label6, \
        label1, \
        label2, \
        label3, \
        label4, \
        env3_0, \
        can_0, \
        rollercan_0, \
        output, \
        mode
    output = output ^ (0x01 << 0)
    rollercan_0.set_motor_output_state(output)


def btna__event(state):
    global \
        title0, \
        label5, \
        label7, \
        label0, \
        label6, \
        label1, \
        label2, \
        label3, \
        label4, \
        env3_0, \
        can_0, \
        rollercan_0, \
        output, \
        mode
    mode = mode + 1
    if mode > 4:
        mode = 1
    rollercan_0.set_motor_mode(mode)


def btnc__event(state):
    global \
        title0, \
        label5, \
        label7, \
        label0, \
        label6, \
        label1, \
        label2, \
        label3, \
        label4, \
        env3_0, \
        can_0, \
        rollercan_0, \
        output, \
        mode
    label5.setText(str((str("temp:") + str((env3_0.read_temperature())))))
    label6.setText(str((str("humi:") + str((env3_0.read_pressure())))))


def setup():
    global \
        title0, \
        label5, \
        label7, \
        label0, \
        label6, \
        label1, \
        label2, \
        label3, \
        label4, \
        env3_0, \
        can_0, \
        rollercan_0, \
        output, \
        mode

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "RollerCAN CANToI2C Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label5 = Widgets.Label("temp:", 182, 66, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label7 = Widgets.Label("update env", 199, 213, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("mode:", 1, 63, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label6 = Widgets.Label("humi:", 182, 131, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("motor state:", 2, 108, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("speed:", 2, 152, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("mode", 40, 215, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("on/off", 126, 215, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb__event)
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna__event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc__event)

    can_0 = CANUnit((13, 15), CANUnit.NORMAL, baudrate=1000000)
    rollercan_0 = RollerCANUnit(can_0, address=0xA8, mode=RollerCANUnit.CAN_TO_I2C_MODE)
    env3_0 = ENVUnit(i2c=rollercan_0, type=3)
    rollercan_0.set_motor_output_state(0)
    output = 0
    mode = rollercan_0.get_motor_mode()
    label0.setText(str((str("mode:") + str(mode))))
    label1.setText(str((str("motor state:") + str(output))))


def loop():
    global \
        title0, \
        label5, \
        label7, \
        label0, \
        label6, \
        label1, \
        label2, \
        label3, \
        label4, \
        env3_0, \
        can_0, \
        rollercan_0, \
        output, \
        mode
    M5.update()
    label0.setText(str((str("mode:") + str(mode))))
    label1.setText(str((str("motor state:") + str(output))))
    if mode == 1:
        rollercan_0.set_motor_speed(20000)
        rollercan_0.set_speed_max_current(400)
        label2.setText(str((str("speed:") + str((rollercan_0.get_motor_speed_readback())))))
    elif mode == 2:
        rollercan_0.set_motor_position(1000)
        rollercan_0.set_position_max_current(400)
        label2.setText(str((str("position:") + str((rollercan_0.get_motor_position_readback())))))
    elif mode == 3:
        rollercan_0.set_motor_max_current(400)
        label2.setText(str((str("current:") + str((rollercan_0.get_motor_current_readback())))))
    elif mode == 4:
        label2.setText(str((str("encoder:") + str((rollercan_0.get_encoder_value())))))


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
