# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
import time


label_imu = None
label_accel = None
label_gyro = None
label_acc_x = None
label_acc_y = None
label_acc_z = None
label_gyro_y = None
label_gyro_z = None
label_gyro_x = None
last_time = None
accel = None
gyro = None


def setup():
    global \
        label_imu, \
        label_accel, \
        label_gyro, \
        label_acc_x, \
        label_acc_y, \
        label_acc_z, \
        label_gyro_y, \
        label_gyro_z, \
        label_gyro_x, \
        last_time, \
        accel, \
        gyro
    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_imu = Widgets.Label("IMU", 46, 4, 1.0, 0x1BCDCD, 0x000000, Widgets.FONTS.DejaVu18)
    label_accel = Widgets.Label(
        "Accel(m/^2)", 5, 35, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_gyro = Widgets.Label(
        "Gyro(dps)", 17, 138, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_acc_x = Widgets.Label("X:", 5, 60, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_acc_y = Widgets.Label("Y:", 5, 85, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_acc_z = Widgets.Label("Z:", 5, 110, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_gyro_y = Widgets.Label("Y:", 5, 187, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_gyro_z = Widgets.Label("Z:", 5, 213, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_gyro_x = Widgets.Label("X:", 5, 163, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)


def loop():
    global \
        label_imu, \
        label_accel, \
        label_gyro, \
        label_acc_x, \
        label_acc_y, \
        label_acc_z, \
        label_gyro_y, \
        label_gyro_z, \
        label_gyro_x, \
        last_time, \
        accel, \
        gyro
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        last_time = time.ticks_ms()
        accel = Imu.getAccel()
        gyro = Imu.getGyro()
        label_acc_x.setText(str((str("X: ") + str((accel[0] * 9.8)))))
        label_acc_y.setText(str((str("Y: ") + str((accel[1] * 9.8)))))
        label_acc_z.setText(str((str("Z: ") + str((accel[2] * 9.8)))))
        label_gyro_x.setText(str((str("X: ") + str((gyro[0])))))
        label_gyro_y.setText(str((str("Y: ") + str((gyro[1])))))
        label_gyro_z.setText(str((str("Z: ") + str((gyro[2])))))


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
