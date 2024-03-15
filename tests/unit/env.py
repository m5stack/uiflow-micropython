# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# UNIT ENVUnit
import M5
import time
from M5 import *
from machine import Pin, I2C
from unit.env import ENVUnit

label0 = None
label1 = None
label2 = None
env = None


def setup():
    global label0, label1, label2, env
    M5.begin()
    label0 = Widgets.Label("Text", 9, 15, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Text", 9, 50, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("Text", 9, 85, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    # ATOMS3 PortA
    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    env = ENVUnit(i2c=i2c0, type=2)


def loop():
    global label0, label1, label2, env
    label0.setText("T:" + str(env.read_temperature()))
    label1.setText("H:" + str(env.read_humidity()))
    label2.setText("P:" + str(env.read_pressure()))
    time.sleep(1)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except Exception as ex:
        # error handler
        raise ex
