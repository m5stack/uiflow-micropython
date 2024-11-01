# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import TimerPWRUnit
from hardware import *


label0 = None
label1 = None
label2 = None
label3 = None
label4 = None
label5 = None
label6 = None
label7 = None
label8 = None
rect0 = None
rect1 = None
label10 = None
rect2 = None
rect3 = None
label11 = None
label12 = None
label9 = None
i2c0 = None
timerpwr_0 = None


en = None


def timerpwr_0_btna_released_event(args):
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        rect0, \
        rect1, \
        label10, \
        rect2, \
        rect3, \
        label11, \
        label12, \
        label9, \
        i2c0, \
        timerpwr_0, \
        en
    print(timerpwr_0.get_button_status(0))
    rect1.setColor(color=0x00FF00, fill_c=0x00FF00)
    label11.setText(str("A"))
    label11.setColor(0x00FF00, 0x00FF00)


def timerpwr_0_btna_pressed_event(args):
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        rect0, \
        rect1, \
        label10, \
        rect2, \
        rect3, \
        label11, \
        label12, \
        label9, \
        i2c0, \
        timerpwr_0, \
        en
    print(timerpwr_0.get_button_status(0))
    rect1.setColor(color=0xFF0000, fill_c=0xFF0000)
    label11.setText(str("A"))
    label11.setColor(0xFF0000, 0xFF0000)


def timerpwr_0_btnb_released_event(args):
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        rect0, \
        rect1, \
        label10, \
        rect2, \
        rect3, \
        label11, \
        label12, \
        label9, \
        i2c0, \
        timerpwr_0, \
        en
    print(timerpwr_0.get_button_status(1))
    rect2.setColor(color=0x00FF00, fill_c=0x00FF00)
    label12.setText(str("B"))
    label12.setColor(0x00FF00, 0x00FF00)


def timerpwr_0_btnb_pressed_event(args):
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        rect0, \
        rect1, \
        label10, \
        rect2, \
        rect3, \
        label11, \
        label12, \
        label9, \
        i2c0, \
        timerpwr_0, \
        en
    print(timerpwr_0.get_button_status(1))
    rect2.setColor(color=0xFF0000, fill_c=0xFF0000)
    label12.setText(str("B"))
    label12.setColor(0xFF0000, 0xFF0000)


def timerpwr_0_usb_inserted_event(args):
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        rect0, \
        rect1, \
        label10, \
        rect2, \
        rect3, \
        label11, \
        label12, \
        label9, \
        i2c0, \
        timerpwr_0, \
        en
    rect0.setColor(color=0x00FF00, fill_c=0x00FF00)
    label10.setText(str("U"))
    label10.setColor(0x00FF00, 0x00FF00)


def timerpwr_0_usb_removed_event(args):
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        rect0, \
        rect1, \
        label10, \
        rect2, \
        rect3, \
        label11, \
        label12, \
        label9, \
        i2c0, \
        timerpwr_0, \
        en
    rect0.setColor(color=0xFF0000, fill_c=0xFF0000)
    label10.setText(str("U"))
    label10.setColor(0xFF0000, 0xFF0000)


def timerpwr_0_not_charging_event(args):
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        rect0, \
        rect1, \
        label10, \
        rect2, \
        rect3, \
        label11, \
        label12, \
        label9, \
        i2c0, \
        timerpwr_0, \
        en
    rect3.setColor(color=0xFF0000, fill_c=0xFF0000)
    label9.setText(str("C"))
    label9.setColor(0xFF0000, 0xFF0000)


def timerpwr_0_charging_event(args):
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        rect0, \
        rect1, \
        label10, \
        rect2, \
        rect3, \
        label11, \
        label12, \
        label9, \
        i2c0, \
        timerpwr_0, \
        en
    rect3.setColor(color=0x00FF00, fill_c=0x00FF00)
    label9.setText(str("C"))
    label9.setColor(0x00FF00, 0x00FF00)


def btnA_wasClicked_event(state):  # noqa: N802
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        rect0, \
        rect1, \
        label10, \
        rect2, \
        rect3, \
        label11, \
        label12, \
        label9, \
        i2c0, \
        timerpwr_0, \
        en
    timerpwr_0.sleep_cycle(0, 0, 30, 0, 0, 10)


def setup():
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        rect0, \
        rect1, \
        label10, \
        rect2, \
        rect3, \
        label11, \
        label12, \
        label9, \
        i2c0, \
        timerpwr_0, \
        en

    M5.begin()
    label0 = Widgets.Label("OUT", 13, 4, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu9)
    label1 = Widgets.Label("label1", 9, 24, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu9)
    label2 = Widgets.Label("label2", 9, 42, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu9)
    label3 = Widgets.Label("BAT", 54, 4, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu9)
    label4 = Widgets.Label("label4", 49, 24, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu9)
    label5 = Widgets.Label("label5", 49, 42, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu9)
    label6 = Widgets.Label("USB", 93, 4, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu9)
    label7 = Widgets.Label("label7", 88, 24, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu9)
    label8 = Widgets.Label("label8", 88, 42, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu9)
    rect0 = Widgets.Rectangle(6, 98, 24, 24, 0x00FF00, 0x00FF00)
    rect1 = Widgets.Rectangle(37, 98, 24, 24, 0x00FF00, 0x00FF00)
    label10 = Widgets.Label("U", 13, 103, 1.0, 0xFFFFFF, 0x00FF00, Widgets.FONTS.DejaVu12)
    rect2 = Widgets.Rectangle(67, 98, 24, 24, 0x00FF00, 0x00FF00)
    rect3 = Widgets.Rectangle(97, 98, 24, 24, 0x00FF00, 0x00FF00)
    label11 = Widgets.Label("A", 45, 103, 1.0, 0xFFFFFF, 0x00FF00, Widgets.FONTS.DejaVu12)
    label12 = Widgets.Label("B", 75, 103, 1.0, 0xFFFFFF, 0x00FF00, Widgets.FONTS.DejaVu12)
    label9 = Widgets.Label("C", 105, 103, 1.0, 0xFFFFFF, 0x00FF00, Widgets.FONTS.DejaVu12)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btnA_wasClicked_event)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    timerpwr_0 = TimerPWRUnit(i2c0, 0x56)
    timerpwr_0.set_callback(timerpwr_0.EVENT_BUTTONA_RELEASED, timerpwr_0_btna_released_event)
    timerpwr_0.set_callback(timerpwr_0.EVENT_BUTTONA_PRESSED, timerpwr_0_btna_pressed_event)
    timerpwr_0.set_callback(timerpwr_0.EVENT_BUTTONB_RELEASED, timerpwr_0_btnb_released_event)
    timerpwr_0.set_callback(timerpwr_0.EVENT_BUTTONB_PRESSED, timerpwr_0_btnb_pressed_event)
    timerpwr_0.set_callback(timerpwr_0.EVENT_USB_INSERTED, timerpwr_0_usb_inserted_event)
    timerpwr_0.set_callback(timerpwr_0.EVENT_USB_REMOVED, timerpwr_0_usb_removed_event)
    timerpwr_0.set_callback(timerpwr_0.EVENT_NOT_CHARGING, timerpwr_0_not_charging_event)
    timerpwr_0.set_callback(timerpwr_0.EVENT_CHARGING, timerpwr_0_charging_event)
    en = True
    timerpwr_0.set_wakeup_trigger(timerpwr_0.TRIG_ALL)
    timerpwr_0.set_sleep_trigger(timerpwr_0.TRIG_ALL)


def loop():
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        rect0, \
        rect1, \
        label10, \
        rect2, \
        rect3, \
        label11, \
        label12, \
        label9, \
        i2c0, \
        timerpwr_0, \
        en
    M5.update()
    label1.setText(str(timerpwr_0.get_grove_voltage()))
    label2.setText(str(timerpwr_0.get_battery_current()))
    label4.setText(str(timerpwr_0.get_battery_voltage()))
    label5.setText(str(timerpwr_0.get_battery_current()))
    label7.setText(str(timerpwr_0.get_usb_voltage()))
    label8.setText(str(timerpwr_0.get_usb_current()))
    timerpwr_0.tick()


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
