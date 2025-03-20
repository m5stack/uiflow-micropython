# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import CommuModuleCAN
from module import CommuModuleRS485
from module import CommuModuleI2C
from hardware import Pin


title0 = None
label0 = None
label1 = None
label2 = None
commu_0 = None
commu_1 = None
commu_2 = None


def setup():
    global title0, label0, label1, label2, commu_0, commu_1, commu_2

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "COMMUModule Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("CAN Rec:", 1, 77, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("RS485 Rec:", 1, 121, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("I2C List:", 1, 166, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    commu_0 = CommuModuleCAN(0x00, baudrate=16)
    commu_1 = CommuModuleRS485(2, baudrate=115200, bits=8, parity=None, stop=1, tx=14, rx=13)
    commu_2 = CommuModuleI2C(0, scl=Pin(22), sda=Pin(21), freq=100000)


def loop():
    global title0, label0, label1, label2, commu_0, commu_1, commu_2
    M5.update()
    if commu_0.any():
        label0.setText(str((str("CAN Rec:") + str((commu_0.recv())))))
    if BtnA.isPressed():
        commu_0.send("uiflow2", 0, extframe=False)
    elif BtnB.isPressed():
        label2.setText(str((str("I2C List:") + str((commu_2.scan())))))
    if commu_1.any():
        label1.setText(str((str("RS485 Rec:") + str((commu_1.read())))))


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
