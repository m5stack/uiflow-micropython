# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *


title0 = None
label2 = None
label0 = None
label3 = None
label1 = None
label4 = None
label5 = None


def setup():
    global title0, label2, label0, label3, label1, label4, label5

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("IMU CoreS3 example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("Acc_z:", 1, 98, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("Acc_x:", 1, 32, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("Gyro_x:", 1, 135, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Acc_y:", 1, 66, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("Gyro_y:", 1, 168, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("Gyro_z:", 1, 198, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)


def loop():
    global title0, label2, label0, label3, label1, label4, label5
    M5.update()
    label0.setText(str((str("Acc_x:") + str(((Imu.getAccel())[0])))))
    label1.setText(str((str("Acc_y:") + str(((Imu.getAccel())[1])))))
    label2.setText(str((str("Acc_z:") + str(((Imu.getAccel())[2])))))
    label3.setText(str((str("Gyro_x:") + str(((Imu.getGyro())[0])))))
    label4.setText(str((str("Gyro_y:") + str(((Imu.getGyro())[1])))))
    label5.setText(str((str("Gyro_z:") + str(((Imu.getGyro())[2])))))


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
