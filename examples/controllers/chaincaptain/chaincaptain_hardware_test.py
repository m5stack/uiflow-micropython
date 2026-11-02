# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
import M5
from M5 import *

last_ms = 0
color_index = 0
colors = (0xFF0000, 0x00FF00, 0x0000FF, 0xFFFFFF, 0x000000)
port_a_on = False
port_b_on = False


def _text(y, label, value, color=0xFFFFFF):
    M5.Lcd.fillRect(8, y, 224, 18, 0x000000)
    M5.Lcd.setFont(M5.Lcd.FONTS.Montserrat12)
    M5.Lcd.setTextColor(0x888888, 0x000000)
    M5.Lcd.drawString(label, 8, y)
    M5.Lcd.setTextColor(color, 0x000000)
    M5.Lcd.drawString(str(value), 78, y)


def _set_port(port, enabled):
    try:
        Power.setExtOutput(enabled, port)
    except TypeError:
        Power.setExtOutput(enabled)


def setup():
    M5.begin()
    M5.Lcd.setRotation(0)
    M5.Lcd.clear(0x000000)
    M5.Lcd.setTextColor(0x26C6DA, 0x000000)
    M5.Lcd.setFont(M5.Lcd.FONTS.Montserrat18)
    M5.Lcd.drawString("ChainCaptain Test", 18, 8)
    M5.Lcd.setFont(M5.Lcd.FONTS.Montserrat12)
    M5.Lcd.drawString("A:PortA  B:Audio  C:PortB", 18, 30)
    Speaker.begin()
    Speaker.setVolumePercentage(0.8)


def loop():
    global last_ms, color_index, port_a_on, port_b_on
    M5.update()
    if BtnA.wasClicked():
        port_a_on = not port_a_on
        _set_port(Power.PORT.A, port_a_on)
    if BtnB.wasClicked():
        Speaker.setPA(True)
        Speaker.tone(880, 120)
    if BtnC.wasClicked():
        port_b_on = not port_b_on
        _set_port(Power.PORT.B, port_b_on)

    now = time.ticks_ms()
    if time.ticks_diff(now, last_ms) < 250:
        return
    last_ms = now
    M5.Lcd.fillRect(8, 52, 224, 20, colors[color_index])
    color_index = (color_index + 1) % len(colors)
    _text(82, "Board", M5.getBoard())
    _text(102, "VBUS", str(Power.getVBUSVoltage()) + " mV")
    _text(122, "BAT", str(Power.getBatteryVoltage()) + " mV")
    _text(
        142,
        "PortA",
        str(Power.getExtVoltage(Power.PORT.A)) + " mV " + ("ON" if port_a_on else "OFF"),
    )
    _text(
        162,
        "PortB",
        str(Power.getExtVoltage(Power.PORT.B)) + " mV " + ("ON" if port_b_on else "OFF"),
    )
    acc = Imu.getAccel()
    gyro = Imu.getGyro()
    _text(184, "ACC", "%.2f %.2f %.2f" % (acc[0], acc[1], acc[2]))
    _text(204, "GYRO", "%.1f %.1f %.1f" % (gyro[0], gyro[1], gyro[2]))


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
            print(e)
