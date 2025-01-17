# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from base import ATOMEchoBase


i2c1 = None
base_echo = None


def setup():
    global i2c1, base_echo

    M5.begin()
    i2c1 = I2C(1, scl=Pin(39), sda=Pin(38), freq=100000)
    base_echo = ATOMEchoBase(i2c1, 0x18, 1, 44100, 8, 6, 7, 5)
    base_echo.speaker.playWavFile("/flash/res/audio/66.wav")


def loop():
    global i2c1, base_echo
    M5.update()


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
