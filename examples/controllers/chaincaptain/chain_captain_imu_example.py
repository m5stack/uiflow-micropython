# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
import time


label_imu = None
label_mag_x = None
label_mag_y = None
label_acc_x = None
label_acc_y = None
label_acc_z = None
label_gyro_y = None
label_gyro_z = None
label_gyro_x = None
label_mag_z = None


last_time = None
accel = None
gyro = None
mag = None


def setup():
    global \
        label_imu, \
        label_mag_x, \
        label_mag_y, \
        label_acc_x, \
        label_acc_y, \
        label_acc_z, \
        label_gyro_y, \
        label_gyro_z, \
        label_gyro_x, \
        label_mag_z, \
        last_time, \
        accel, \
        gyro, \
        mag

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_imu = Widgets.Label("IMU", 98, 4, 1.0, 0x1BCDCD, 0x000000, Widgets.FONTS.Montserrat18)
    label_mag_x = Widgets.Label(
        "Mag X:", 10, 168, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_mag_y = Widgets.Label(
        "Mag Y:", 11, 190, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_acc_x = Widgets.Label(
        "Acc X:", 17, 27, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_acc_y = Widgets.Label(
        "Acc Y:", 18, 50, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_acc_z = Widgets.Label(
        "Acc Z:", 17, 74, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_gyro_y = Widgets.Label(
        "Gyro Y:", 10, 120, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_gyro_z = Widgets.Label(
        "Gyro Z:", 8, 142, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_gyro_x = Widgets.Label(
        "Gyro X:", 8, 97, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_mag_z = Widgets.Label(
        "Mag Z:", 10, 212, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    last_time = 0


def loop():
    global \
        label_imu, \
        label_mag_x, \
        label_mag_y, \
        label_acc_x, \
        label_acc_y, \
        label_acc_z, \
        label_gyro_y, \
        label_gyro_z, \
        label_gyro_x, \
        label_mag_z, \
        last_time, \
        accel, \
        gyro, \
        mag
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        last_time = time.ticks_ms()
        accel = Imu.getAccel()
        gyro = Imu.getGyro()
        mag = Imu.getMag()
        label_acc_x.setText(str((str("Acc X: ") + str((accel[0] * 9.8)))))
        label_acc_y.setText(str((str("Acc Y: ") + str((accel[1] * 9.8)))))
        label_acc_z.setText(str((str("Acc Z: ") + str((accel[2] * 9.8)))))
        label_gyro_x.setText(str((str("Gyro X: ") + str((gyro[0])))))
        label_gyro_y.setText(str((str("Gyro Y: ") + str((gyro[1])))))
        label_gyro_z.setText(str((str("Gyro Z: ") + str((gyro[2])))))
        label_mag_x.setText(str((str("Mag X: ") + str((mag[0])))))
        label_mag_y.setText(str((str("Mag Y: ") + str((mag[1])))))
        label_mag_z.setText(str((str("Mag Z: ") + str((mag[2])))))


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
