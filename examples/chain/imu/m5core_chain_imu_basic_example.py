# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from chain import ChainBus
from chain import IMUChain
import time


title = None
accel_caption = None
accel_unit = None
x_caption = None
accel_x = None
y_caption = None
accel_y = None
z_caption = None
accel_z = None
gyro_caption = None
gyro_unit = None
gyro_x = None
gyro_y = None
gyro_z = None
temperature = None
bus2 = None
chain_imu_0 = None
accel = None
gyro = None
last_time = None


def setup():
    global \
        title, \
        accel_caption, \
        accel_unit, \
        x_caption, \
        accel_x, \
        y_caption, \
        accel_y, \
        z_caption, \
        accel_z, \
        gyro_caption, \
        gyro_unit, \
        gyro_x, \
        gyro_y, \
        gyro_z, \
        temperature, \
        bus2, \
        chain_imu_0, \
        accel, \
        gyro, \
        last_time

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x10171D)
    title = Widgets.Label("Chain IMU", 112, 8, 1.0, 0x4CD7D0, 0x10171D, Widgets.FONTS.Montserrat18)
    accel_caption = Widgets.Label(
        "Acceleration", 12, 43, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    accel_unit = Widgets.Label(
        "m/s2", 200, 43, 1.0, 0x63A8FF, 0x10171D, Widgets.FONTS.Montserrat14
    )
    x_caption = Widgets.Label("X", 12, 65, 1.0, 0xFFB454, 0x10171D, Widgets.FONTS.Montserrat14)
    accel_x = Widgets.Label("--.--", 12, 86, 1.0, 0xF2F6F8, 0x10171D, Widgets.FONTS.Montserrat24)
    y_caption = Widgets.Label("Y", 113, 65, 1.0, 0x63D08C, 0x10171D, Widgets.FONTS.Montserrat14)
    accel_y = Widgets.Label("--.--", 113, 86, 1.0, 0xF2F6F8, 0x10171D, Widgets.FONTS.Montserrat24)
    z_caption = Widgets.Label("Z", 214, 65, 1.0, 0x63A8FF, 0x10171D, Widgets.FONTS.Montserrat14)
    accel_z = Widgets.Label("--.--", 214, 86, 1.0, 0xF2F6F8, 0x10171D, Widgets.FONTS.Montserrat24)
    gyro_caption = Widgets.Label(
        "Angular velocity", 12, 131, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    gyro_unit = Widgets.Label(
        "rad/s", 200, 131, 1.0, 0x4CD7D0, 0x10171D, Widgets.FONTS.Montserrat14
    )
    gyro_x = Widgets.Label("--.--", 12, 157, 1.0, 0x4CD7D0, 0x10171D, Widgets.FONTS.Montserrat24)
    gyro_y = Widgets.Label("--.--", 113, 157, 1.0, 0x4CD7D0, 0x10171D, Widgets.FONTS.Montserrat24)
    gyro_z = Widgets.Label("--.--", 214, 157, 1.0, 0x4CD7D0, 0x10171D, Widgets.FONTS.Montserrat24)
    temperature = Widgets.Label(
        "Temperature  --.- C", 12, 212, 1.0, 0xFFB454, 0x10171D, Widgets.FONTS.Montserrat14
    )

    bus2 = ChainBus(2, tx=21, rx=22)
    chain_imu_0 = IMUChain(bus2, 1)
    title.setCursor(
        x=(int((320 - (M5.Display.textWidth("Chain IMU", Widgets.FONTS.Montserrat18))) / 2)), y=8
    )
    last_time = 0


def loop():
    global \
        title, \
        accel_caption, \
        accel_unit, \
        x_caption, \
        accel_x, \
        y_caption, \
        accel_y, \
        z_caption, \
        accel_z, \
        gyro_caption, \
        gyro_unit, \
        gyro_x, \
        gyro_y, \
        gyro_z, \
        temperature, \
        bus2, \
        chain_imu_0, \
        accel, \
        gyro, \
        last_time
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        accel = chain_imu_0.read_accel()
        gyro = chain_imu_0.read_gyro()
        accel_x.setText(str(round(accel[0], 2)))
        gyro_x.setText(str(round(gyro[0], 2)))
        accel_y.setText(str(round(accel[1], 2)))
        gyro_y.setText(str(round(gyro[1], 2)))
        accel_z.setText(str(round(accel[2], 2)))
        gyro_z.setText(str(round(gyro[2], 2)))
        temperature.setText(
            str(
                (
                    str((str("Temperature  ") + str((round(chain_imu_0.read_temperature(), 1)))))
                    + str(" C")
                )
            )
        )
        last_time = time.ticks_ms()
    time.sleep_ms(10)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            bus2.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
