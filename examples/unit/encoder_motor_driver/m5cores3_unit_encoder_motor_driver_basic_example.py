# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from unit import EncoderMotorDriverUnit
from hardware import Pin
from hardware import I2C


page0 = None
label_title = None
button_speed_up = None
button_speed_down = None
label_speed = None
button_stop = None
i2c0 = None
encodermotordriver_0 = None
speed = None


def button_stop_short_clicked_event(event_struct):
    global \
        page0, \
        label_title, \
        button_speed_up, \
        button_speed_down, \
        label_speed, \
        button_stop, \
        i2c0, \
        encodermotordriver_0, \
        speed
    speed = 0
    encodermotordriver_0.set_motor_pwm_duty(speed)
    label_speed.set_text(str(speed))


def button_speed_up_short_clicked_event(event_struct):
    global \
        page0, \
        label_title, \
        button_speed_up, \
        button_speed_down, \
        label_speed, \
        button_stop, \
        i2c0, \
        encodermotordriver_0, \
        speed
    if speed < 80:
        speed = speed + 20
    else:
        speed = 0
    encodermotordriver_0.set_motor_pwm_duty(speed)
    label_speed.set_text(str(speed))


def button_speed_down_short_clicked_event(event_struct):
    global \
        page0, \
        label_title, \
        button_speed_up, \
        button_speed_down, \
        label_speed, \
        button_stop, \
        i2c0, \
        encodermotordriver_0, \
        speed
    if speed > -80:
        speed = speed - 20
    else:
        speed = 0
    encodermotordriver_0.set_motor_pwm_duty(speed)
    label_speed.set_text(str(speed))


def button_stop_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        button_speed_up, \
        button_speed_down, \
        label_speed, \
        button_stop, \
        i2c0, \
        encodermotordriver_0, \
        speed
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button_stop_short_clicked_event(event_struct)
    return


def button_speed_up_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        button_speed_up, \
        button_speed_down, \
        label_speed, \
        button_stop, \
        i2c0, \
        encodermotordriver_0, \
        speed
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button_speed_up_short_clicked_event(event_struct)
    return


def button_speed_down_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        button_speed_up, \
        button_speed_down, \
        label_speed, \
        button_stop, \
        i2c0, \
        encodermotordriver_0, \
        speed
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button_speed_down_short_clicked_event(event_struct)
    return


def setup():
    global \
        page0, \
        label_title, \
        button_speed_up, \
        button_speed_down, \
        label_speed, \
        button_stop, \
        i2c0, \
        encodermotordriver_0, \
        speed

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    label_title = m5ui.M5Label(
        "Encoder Motor Control",
        x=20,
        y=5,
        text_c=0x079EE1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    button_speed_up = m5ui.M5Button(
        text="+",
        x=50,
        y=165,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    button_speed_down = m5ui.M5Button(
        text="-",
        x=230,
        y=165,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_speed = m5ui.M5Label(
        "00",
        x=132,
        y=75,
        text_c=0x079EE1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_40,
        parent=page0,
    )
    button_stop = m5ui.M5Button(
        text="STOP",
        x=112,
        y=165,
        bg_c=0xF32121,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    button_stop.add_event_cb(button_stop_event_handler, lv.EVENT.ALL, None)
    button_speed_up.add_event_cb(button_speed_up_event_handler, lv.EVENT.ALL, None)
    button_speed_down.add_event_cb(button_speed_down_event_handler, lv.EVENT.ALL, None)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    encodermotordriver_0 = EncoderMotorDriverUnit(i2c0, 0x2F)
    speed = 0
    encodermotordriver_0.set_motor_pwm_duty(speed)
    page0.screen_load()


def loop():
    global \
        page0, \
        label_title, \
        button_speed_up, \
        button_speed_down, \
        label_speed, \
        button_stop, \
        i2c0, \
        encodermotordriver_0, \
        speed
    M5.update()


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
