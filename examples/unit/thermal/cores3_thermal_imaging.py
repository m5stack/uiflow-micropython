# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from unit import ThermalUnit
import math


i2c0 = None
thermal_0 = None
temp = None
min2 = None
max2 = None
color = None
ratio = None
r = None
templist = None
g = None
min_temp = None
b = None
max_temp = None
y = None
x = None
c = None


def temperature_to_color(temp, min2, max2):
    global color, ratio, r, templist, g, min_temp, b, max_temp, y, x, c, i2c0, thermal_0
    # Clamp the temperature value to be within the min2 and max2 range
    temp = min(max(temp, min2), max2)
    # Calculate the ratio of the temperature within the given range [0.0 - 1.0]
    ratio = (temp - min2) / (max2 - min2)
    # Red increases with temperature
    r = int(255 * ratio)
    # Green peaks in the middle of the range
    g = int(255 * ((1 - math.fabs(ratio - 0.5)) * 2))
    # Blue decreases with temperature
    b = int(255 * (1 - ratio))
    # Combine R, G, B into a single 24-bit color value (0xRRGGBB)
    color = r * 65536 + (g * 256 + b)
    # Return the color value
    return color


def setup():
    global \
        i2c0, \
        thermal_0, \
        temp, \
        color, \
        ratio, \
        min2, \
        max2, \
        r, \
        templist, \
        g, \
        min_temp, \
        b, \
        max_temp, \
        c, \
        x, \
        y

    M5.begin()
    Widgets.fillScreen(0x222222)
    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
    thermal_0 = ThermalUnit(i2c0)
    thermal_0.set_refresh_rate(1)
    M5.Lcd.clear(0x000000)


def loop():
    global \
        i2c0, \
        thermal_0, \
        temp, \
        color, \
        ratio, \
        min2, \
        max2, \
        r, \
        templist, \
        g, \
        min_temp, \
        b, \
        max_temp, \
        c, \
        x, \
        y
    M5.update()
    thermal_0.update_temperature_buffer()
    templist = thermal_0.get_temperature_buffer()
    min_temp = thermal_0.get_min_temperature
    max_temp = thermal_0.get_max_temperature
    M5.Lcd.setFont(M5.Lcd.FONTS.DejaVu18)
    M5.Lcd.fillRect(35, 10, 250, 20, 0x000000)
    M5.Lcd.setCursor(35, 10)
    M5.Lcd.print((str("min: ") + str(min_temp)), 0x3366FF)
    M5.Lcd.setCursor(165, 10)
    M5.Lcd.print((str("max: ") + str(max_temp)), 0xCC0000)
    for y in range(24):
        for x in range(32):
            c = temperature_to_color(templist[int((y * 32 + x) - 1)], 20, 40)
            M5.Lcd.fillRect(80 + x * 5, 60 + y * 5, 5, 5, c)


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
