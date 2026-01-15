# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import time


label_title = None
label_5vout = None
label_usb = None
label_bat = None
label_tip = None
label_state = None
label_vout = None
vout_flag = None
charge = None
last_time = None
usb_vol = None
bat_vol = None
vout_vol = None
vout_state = None


def btna_click_event_cb(state):
    global \
        label_title, \
        label_5vout, \
        label_usb, \
        label_bat, \
        label_tip, \
        label_state, \
        label_vout, \
        vout_flag, \
        charge, \
        last_time, \
        usb_vol, \
        bat_vol, \
        vout_vol, \
        vout_state
    vout_flag = not vout_flag
    if vout_flag:
        Power.setExtOutput(True)
        print("turn on the output")
    else:
        Power.setExtOutput(False)
        print("turn off the output")


def btnb_click_event_cb(state):
    global \
        label_title, \
        label_5vout, \
        label_usb, \
        label_bat, \
        label_tip, \
        label_state, \
        label_vout, \
        vout_flag, \
        charge, \
        last_time, \
        usb_vol, \
        bat_vol, \
        vout_vol, \
        vout_state
    charge = not charge
    if charge:
        print("set charge")
        Power.setBatteryCharge(True)
    else:
        print("no charge")
        Power.setBatteryCharge(False)


def setup():
    global \
        label_title, \
        label_5vout, \
        label_usb, \
        label_bat, \
        label_tip, \
        label_state, \
        label_vout, \
        vout_flag, \
        charge, \
        last_time, \
        usb_vol, \
        bat_vol, \
        vout_vol, \
        vout_state
    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label("Power", 36, 5, 1.0, 0x13BDDE, 0x000000, Widgets.FONTS.DejaVu18)
    label_5vout = Widgets.Label(
        "OUT:----mV", 5, 85, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_usb = Widgets.Label("USB:----mV", 5, 35, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_bat = Widgets.Label("Bat:----mV", 5, 60, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_tip = Widgets.Label(
        "BtnA Control", 5, 210, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_state = Widgets.Label("ON", 31, 152, 1.0, 0x00FF00, 0x000000, Widgets.FONTS.DejaVu40)
    label_vout = Widgets.Label("5V OUT", 28, 125, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_click_event_cb)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_click_event_cb)

    Power.setBatteryCharge(True)
    Power.setExtOutput(False)
    charge = True
    label_bat.setColor(0x33CC00, 0x000000)


def loop():
    global \
        label_title, \
        label_5vout, \
        label_usb, \
        label_bat, \
        label_tip, \
        label_state, \
        label_vout, \
        vout_flag, \
        charge, \
        last_time, \
        usb_vol, \
        bat_vol, \
        vout_vol, \
        vout_state
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 1000:
        last_time = time.ticks_ms()
        usb_vol = Power.getVBUSVoltage()
        bat_vol = Power.getBatteryVoltage()
        vout_vol = Power.getExtVoltage(M5.Power.PORT.A)
        vout_state = Power.getExtOutput()
        if Power.isCharging():
            label_bat.setColor(0x33CC00, 0x000000)
        else:
            label_bat.setColor(0xFFFFFF, 0x000000)
        if vout_state:
            label_state.setCursor(x=32, y=152)
            label_state.setText(str("ON"))
            label_state.setColor(0x33CC00, 0x000000)
        else:
            label_state.setCursor(x=24, y=152)
            label_state.setText(str("OFF"))
            label_state.setColor(0x666666, 0x000000)
        label_usb.setText(str((str("USB:") + str((str(usb_vol) + str("mV"))))))
        label_bat.setText(str((str("Bat:") + str((str(bat_vol) + str("mV"))))))
        label_5vout.setText(str((str("Out:") + str((str(vout_vol) + str("mV"))))))


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
