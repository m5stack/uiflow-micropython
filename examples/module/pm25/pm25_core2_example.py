# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import PM25Module
import time


title0 = None
label9 = None
label0 = None
label10 = None
label1 = None
label2 = None
label3 = None
label4 = None
label5 = None
label6 = None
label7 = None
label8 = None
pm25_0 = None


def setup():
    global \
        title0, \
        label9, \
        label0, \
        label10, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        pm25_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("PM2.5 Module Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label9 = Widgets.Label("Temp:", 191, 26, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("PM1.0 Env:", 1, 26, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label10 = Widgets.Label("Humi:", 191, 52, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("PM2.5 Env:", 1, 52, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("PM10 Env:", 1, 77, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label(
        "Particles 0.3um:", 1, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label4 = Widgets.Label(
        "Particles 0.5um:", 1, 124, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label5 = Widgets.Label(
        "Particles 1.0um:", 1, 145, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label6 = Widgets.Label(
        "Particles 2.5um:", 1, 167, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label7 = Widgets.Label(
        "Particles 5um:", 1, 189, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label8 = Widgets.Label(
        "Particles 10um:", 1, 210, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    pm25_0 = PM25Module(2)
    pm25_0.set_module_mode(0)
    pm25_0.set_module_power(True)
    print(pm25_0.get_module_power())


def loop():
    global \
        title0, \
        label9, \
        label0, \
        label10, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        pm25_0
    M5.update()
    pm25_0.request_air_data()
    pm25_0.refresh_data()
    label0.setText(str((str("PM1.0 Env:") + str((pm25_0.get_pm_data(3))))))
    label1.setText(str((str("PM2.5 Env:") + str((pm25_0.get_pm_data(4))))))
    label2.setText(str((str("PM10 Env:") + str((pm25_0.get_pm_data(5))))))
    label3.setText(str((str("Particles 0.3um:") + str((pm25_0.get_pm_data(6))))))
    label4.setText(str((str("Particles 0.5um:") + str((pm25_0.get_pm_data(7))))))
    label5.setText(str((str("Particles 1.0um:") + str((pm25_0.get_pm_data(8))))))
    label6.setText(str((str("Particles 2.5um:") + str((pm25_0.get_pm_data(9))))))
    label7.setText(str((str("Particles 5um:") + str((pm25_0.get_pm_data(10))))))
    label8.setText(str((str("Particles 10um:") + str((pm25_0.get_pm_data(11))))))
    label9.setText(str((str("Temp:") + str((pm25_0.get_temperature())))))
    label10.setText(str((str("Humi:") + str((pm25_0.get_humidity())))))
    time.sleep_ms(100)


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
