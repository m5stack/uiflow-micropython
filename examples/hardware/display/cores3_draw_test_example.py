# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *


def setup():
    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)

    print((str("rotation: ") + str((M5.Display.getRotation()))))
    print(
        (
            str((str("w: ") + str((M5.Display.width()))))
            + str((str("h:") + str((M5.Display.height()))))
        )
    )
    M5.Display.setRotation(1)
    M5.Display.clear(0x000000)
    M5.Display.setTextColor(0x0000FF, 0x000000)
    M5.Display.setCursor(200, 3)
    M5.Display.printf("hello M5")
    M5.Display.print("hello M5", 0x6600CC)
    M5.Display.drawImage("/flash/res/img/default.png", 0, 0)
    M5.Display.drawQR("Hello", 220, 40, 100, 1)
    M5.Display.drawCircle(30, 80, 20, 0x3333FF)
    M5.Display.fillCircle(80, 80, 20, 0x009900)
    M5.Display.drawEllipse(60, 140, 50, 30, 0x00FF00)
    M5.Display.fillEllipse(60, 140, 30, 20, 0xFFFF00)
    M5.Display.drawLine(115, 10, 115, 60, 0xFF0000)
    M5.Display.drawRect(125, 10, 40, 30, 0xFF0000)
    M5.Display.fillRect(125, 50, 40, 30, 0x00FF00)
    M5.Display.drawTriangle(135, 150, 110, 190, 160, 190, 0x00FF00)
    M5.Display.fillTriangle(145, 150, 170, 190, 190, 150, 0x0000FF)
    M5.Display.drawArc(10, 180, 40, 45, 0, 90, 0xFFFF00)
    M5.Display.fillArc(20, 190, 40, 45, 0, 90, 0x00FFFF)


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
