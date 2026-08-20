# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None
label_title = None
label_acc_title = None
label_acc_x = None
label_acc_y = None
label_acc_z = None
label_gyro_title = None
label_gyro_x = None
label_gyro_y = None
label_gyro_z = None
label_footer = None


accel = None
gyro = None
acc_x = None
acc_y = None
acc_z = None
gyro_x = None
gyro_y = None
gyro_z = None


def setup():
    global \
        page0, \
        label_title, \
        label_acc_title, \
        label_acc_x, \
        label_acc_y, \
        label_acc_z, \
        label_gyro_title, \
        label_gyro_x, \
        label_gyro_y, \
        label_gyro_z, \
        label_footer, \
        accel, \
        gyro, \
        acc_x, \
        acc_y, \
        acc_z, \
        gyro_x, \
        gyro_y, \
        gyro_z

    M5.begin()
    Widgets.setRotation(3)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x101820)
    label_title = m5ui.M5Label(
        "IMU Example",
        x=465,
        y=30,
        text_c=0x2EAD65,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_acc_title = m5ui.M5Label(
        "Accelerometer",
        x=140,
        y=125,
        text_c=0x9FB3C8,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_acc_x = m5ui.M5Label(
        "X: -- g",
        x=120,
        y=220,
        text_c=0xF4F7FA,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_acc_y = m5ui.M5Label(
        "Y: -- g",
        x=120,
        y=350,
        text_c=0xF4F7FA,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_acc_z = m5ui.M5Label(
        "Z: -- g",
        x=120,
        y=480,
        text_c=0xF4F7FA,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_gyro_title = m5ui.M5Label(
        "Gyroscope",
        x=825,
        y=125,
        text_c=0x9FB3C8,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_gyro_x = m5ui.M5Label(
        "X: -- dps",
        x=760,
        y=220,
        text_c=0xF4F7FA,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_gyro_y = m5ui.M5Label(
        "Y: -- dps",
        x=760,
        y=350,
        text_c=0xF4F7FA,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_gyro_z = m5ui.M5Label(
        "Z: -- dps",
        x=760,
        y=480,
        text_c=0xF4F7FA,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_footer = m5ui.M5Label(
        "Live data",
        x=535,
        y=610,
        text_c=0x9FB3C8,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )

    page0.screen_load()


def loop():
    global \
        page0, \
        label_title, \
        label_acc_title, \
        label_acc_x, \
        label_acc_y, \
        label_acc_z, \
        label_gyro_title, \
        label_gyro_x, \
        label_gyro_y, \
        label_gyro_z, \
        label_footer, \
        accel, \
        gyro, \
        acc_x, \
        acc_y, \
        acc_z, \
        gyro_x, \
        gyro_y, \
        gyro_z
    M5.update()
    accel = Imu.getAccel()
    gyro = Imu.getGyro()
    acc_x = accel[0]
    acc_y = accel[1]
    acc_z = accel[2]
    gyro_x = gyro[0]
    gyro_y = gyro[1]
    gyro_z = gyro[2]
    label_acc_x.set_text(str((str("X: ") + str((str(acc_x) + str(" g"))))))
    label_acc_y.set_text(str((str("Y: ") + str((str(acc_y) + str(" g"))))))
    label_acc_z.set_text(str((str("Z: ") + str((str(acc_z) + str(" g"))))))
    label_gyro_x.set_text(str((str("X: ") + str((str(gyro_x) + str(" dps"))))))
    label_gyro_y.set_text(str((str("Y: ") + str((str(gyro_y) + str(" dps"))))))
    label_gyro_z.set_text(str((str("Z: ") + str((str(gyro_z) + str(" dps"))))))


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
