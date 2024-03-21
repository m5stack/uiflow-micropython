# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from hardware import sdcard


label0 = None
label1 = None
label3 = None
label2 = None
label4 = None


dir2 = None
ret = None


# Describe this function...
def test_chg_dir():
    global dir2, ret, label0, label1, label3, label2, label4
    os.chdir("/sd")
    dir2 = os.getcwd()
    label0.setText(str((str("test chg: ") + str((dir2 == "/sd")))))


# Describe this function...
def test_mkdir():
    global dir2, ret, label0, label1, label3, label2, label4
    os.mkdir("/sd/test")
    os.rename("/sd/test", "/sd/test1")
    os.rmdir("/sd/test1")
    label1.setText(str((str("test mkdir: ") + str(True))))


# Describe this function...
def test_isexist():
    global dir2, ret, label0, label1, label3, label2, label4
    os.mkdir("/sd/test")
    os.mkdir("/sd/test/test1")
    dir2 = os.listdir("/sd/test")
    ret = "test1" in os.listdir("/sd/test")
    label4.setText(str((str("test isexist: ") + str(ret))))
    os.rmdir("/sd/test/test1")
    os.rmdir("/sd/test")


# Describe this function...
def test_isfile():
    global dir2, ret, label0, label1, label3, label2, label4
    os.mkdir("/sd/test")
    os.mkdir("/sd/test/test1")
    ret = not (os.stat("/sd/test/test1")[0] == 0x8000)
    label2.setText(str((str("test isfile: ") + str(ret))))
    os.rmdir("/sd/test/test1")
    os.rmdir("/sd/test")


# Describe this function...
def test_isdir():
    global dir2, ret, label0, label1, label3, label2, label4
    os.mkdir("/sd/test")
    os.mkdir("/sd/test/test1")
    ret = os.stat("/sd/test/test1")[0] == 0x4000
    label3.setText(str((str("test isdir: ") + str(ret))))
    os.rmdir("/sd/test/test1")
    os.rmdir("/sd/test")


def setup():
    global label0, label1, label3, label2, label4, dir2, ret

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Text", 10, 20, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Text", 10, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("Text", 10, 140, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("Text", 10, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("Text", 10, 180, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    sdcard.SDCard(slot=2, width=1, sck=36, miso=35, mosi=37, cs=4, freq=2000000)
    test_chg_dir()
    test_mkdir()
    test_isfile()
    test_isdir()
    test_isexist()


def loop():
    global label0, label1, label3, label2, label4, dir2, ret
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
