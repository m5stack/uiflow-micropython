import os, sys, io
import M5
from M5 import *
from hardware import *
from hat import MiniEncoderCHat


title0 = None
circle0 = None
circle1 = None
circle2 = None
label0 = None
i2c0 = None
i2c1 = None
hat_miniencoderc_0 = None


import math

angle = None
x = None
y = None
direction = None
big_radius = None
small_radius = None


# Describe this function...
def move_small_circle():
    global \
        angle, \
        x, \
        y, \
        direction, \
        big_radius, \
        small_radius, \
        title0, \
        circle0, \
        circle1, \
        circle2, \
        label0, \
        i2c0, \
        i2c1, \
        hat_miniencoderc_0
    angle = ((hat_miniencoderc_0.get_rotary_value()) / 58) * 360
    x = big_radius * math.cos(angle / 180.0 * math.pi)
    y = big_radius * math.sin(angle / 180.0 * math.pi)
    circle0.setCursor(x=67, y=120)
    circle2.setCursor(x=(67 + (int(x))), y=(120 + (int(y))))


def setup():
    global \
        title0, \
        circle0, \
        circle1, \
        circle2, \
        label0, \
        i2c0, \
        i2c1, \
        hat_miniencoderc_0, \
        angle, \
        x, \
        y, \
        direction, \
        big_radius, \
        small_radius

    M5.begin()
    title0 = Widgets.Title("Mini Encoder", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    circle0 = Widgets.Circle(67, 120, 50, 0xFFFFFF, 0x000000)
    circle1 = Widgets.Circle(67, 120, 10, 0x00FF00, 0x00FF00)
    circle2 = Widgets.Circle(117, 120, 6, 0xFFFFFF, 0xFFFFFF)
    label0 = Widgets.Label("Count: 0", 4, 213, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    i2c1 = I2C(1, scl=Pin(26), sda=Pin(0), freq=100000)
    hat_miniencoderc_0 = MiniEncoderCHat(i2c0, 0x42)
    big_radius = 50
    small_radius = 6


def loop():
    global \
        title0, \
        circle0, \
        circle1, \
        circle2, \
        label0, \
        i2c0, \
        i2c1, \
        hat_miniencoderc_0, \
        angle, \
        x, \
        y, \
        direction, \
        big_radius, \
        small_radius
    M5.update()
    if hat_miniencoderc_0.get_rotary_status():
        direction = hat_miniencoderc_0.get_rotary_increments()
        move_small_circle()
        if direction < 0:
            hat_miniencoderc_0.fill_color(0xFF0000)
            label0.setText(str((str("Count: ") + str((hat_miniencoderc_0.get_rotary_value())))))
        elif direction > 0:
            hat_miniencoderc_0.fill_color(0x33FF33)
            label0.setText(str((str("Count: ") + str((hat_miniencoderc_0.get_rotary_value())))))
    else:
        hat_miniencoderc_0.fill_color(0x000000)
    if hat_miniencoderc_0.get_button_status():
        circle1.setColor(color=0xFF0000, fill_c=0xFF0000)
        move_small_circle()
        hat_miniencoderc_0.reset_rotary_value()
    else:
        circle1.setColor(color=0x00FF00, fill_c=0x00FF00)


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
