# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *


def setup():
    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    print((str("rotation: ") + str((M5.Lcd.getRotation()))))
    print((str("color depth: ") + str((M5.Lcd.getColorDepth()))))
    print((str((str("w: ") + str((M5.Lcd.width())))) + str((str("h:") + str((M5.Lcd.height()))))))
    M5.Lcd.setRotation(1)
    M5.Lcd.clear(0x000000)
    M5.Lcd.setTextColor(0x0000FF, 0x000000)
    M5.Lcd.setCursor(200, 3)
    M5.Lcd.printf("hello M5")
    M5.Lcd.print("hello M5", 0x6600CC)
    M5.Lcd.drawImage("/flash/res/img/default.png", 0, 0)
    M5.Lcd.drawQR("Hello", 220, 40, 100, 1)
    M5.Lcd.drawCircle(30, 80, 20, 0x3333FF)
    M5.Lcd.fillCircle(80, 80, 20, 0x009900)
    M5.Lcd.drawEllipse(60, 140, 50, 30, 0x00FF00)
    M5.Lcd.fillEllipse(60, 140, 30, 20, 0xFFFF00)
    M5.Lcd.drawLine(115, 10, 115, 60, 0xFF0000)
    M5.Lcd.drawRect(125, 10, 40, 30, 0xFF0000)
    M5.Lcd.fillRect(125, 50, 40, 30, 0x00FF00)
    M5.Lcd.drawTriangle(135, 150, 110, 190, 160, 190, 0x00FF00)
    M5.Lcd.fillTriangle(145, 150, 170, 190, 190, 150, 0x0000FF)
    M5.Lcd.drawArc(10, 180, 40, 45, 0, 90, 0xFFFF00)
    M5.Lcd.fillArc(20, 190, 40, 45, 0, 90, 0x00FFFF)


def loop():
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
