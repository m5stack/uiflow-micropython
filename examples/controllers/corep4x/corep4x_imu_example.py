# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time


page0 = None
label_title = None
label_subtitle = None
label_acc_x = None
label_acc_y = None
label_acc_z = None
label_gyro_x = None
label_gyro_y = None
label_gyro_z = None
label_gyro_title = None
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
        label_subtitle, \
        label_acc_x, \
        label_acc_y, \
        label_acc_z, \
        label_gyro_x, \
        label_gyro_y, \
        label_gyro_z, \
        label_gyro_title, \
        accel, \
        gyro, \
        acc_x, \
        acc_y, \
        acc_z, \
        gyro_x, \
        gyro_y, \
        gyro_z

    M5.begin()
    Widgets.setRotation(0)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x080808)
    label_title = m5ui.M5Label(
        "IMU",
        x=24,
        y=18,
        text_c=0xF1F5F7,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_subtitle = m5ui.M5Label(
        "Accel (g)",
        x=199,
        y=82,
        text_c=0xA9BAC4,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_acc_x = m5ui.M5Label(
        "X: -- g",
        x=48,
        y=116,
        text_c=0x45D483,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_acc_y = m5ui.M5Label(
        "Y: -- g",
        x=48,
        y=156,
        text_c=0x45D483,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_acc_z = m5ui.M5Label(
        "Z: -- g",
        x=48,
        y=196,
        text_c=0x45D483,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_gyro_x = m5ui.M5Label(
        "X: -- dps",
        x=48,
        y=300,
        text_c=0xFFD04D,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_gyro_y = m5ui.M5Label(
        "Y: -- dps",
        x=48,
        y=340,
        text_c=0xFFD04D,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_gyro_z = m5ui.M5Label(
        "Z: -- dps",
        x=48,
        y=380,
        text_c=0xFFD04D,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_gyro_title = m5ui.M5Label(
        "Gyro (dps)",
        x=192,
        y=266,
        text_c=0xA9BAC4,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )

    page0.screen_load()


def loop():
    global \
        page0, \
        label_title, \
        label_subtitle, \
        label_acc_x, \
        label_acc_y, \
        label_acc_z, \
        label_gyro_x, \
        label_gyro_y, \
        label_gyro_z, \
        label_gyro_title, \
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
    time.sleep_ms(200)


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
