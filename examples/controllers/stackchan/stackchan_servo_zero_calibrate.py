# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time
from hardware.stackchan import StackChan


page0 = None
label_title = None
button_save = None
label_angle_x = None
label_angle_y = None
label_tip = None
stackchan = None
x_angle = None
y_angle = None
last_time = None


def button_save_short_clicked_event(event_struct):
    global \
        page0, \
        label_title, \
        button_save, \
        label_angle_x, \
        label_angle_y, \
        label_tip, \
        stackchan, \
        x_angle, \
        y_angle, \
        last_time
    stackchan.set_servo_zero()
    label_tip.set_text(str("Tip: Calibration success"))
    Speaker.tone(1000, 100)
    last_time = time.ticks_ms()


def button_save_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        button_save, \
        label_angle_x, \
        label_angle_y, \
        label_tip, \
        stackchan, \
        x_angle, \
        y_angle, \
        last_time
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button_save_short_clicked_event(event_struct)
    return


def setup():
    global \
        page0, \
        label_title, \
        button_save, \
        label_angle_x, \
        label_angle_y, \
        label_tip, \
        stackchan, \
        x_angle, \
        y_angle, \
        last_time

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    label_title = m5ui.M5Label(
        "Servo Calibration",
        x=55,
        y=5,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    button_save = m5ui.M5Button(
        text="Save",
        x=128,
        y=195,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label_angle_x = m5ui.M5Label(
        "X-Axis Servo Angle:",
        x=10,
        y=130,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_angle_y = m5ui.M5Label(
        "Y-Axis Servo Angle:",
        x=8,
        y=160,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_tip = m5ui.M5Label(
        "Tip:Move by hand, tap Save.",
        x=33,
        y=70,
        text_c=0xD2E711,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )

    button_save.add_event_cb(button_save_event_handler, lv.EVENT.ALL, None)

    stackchan = StackChan(i2c=1, uart=1)
    page0.screen_load()
    stackchan.set_servo_power(enable=True, settle_ms=500)
    stackchan.set_servo_torque(stackchan.SERVO_ID_X, enable=False)
    stackchan.set_servo_torque(stackchan.SERVO_ID_Y, enable=False)
    Speaker.begin()
    Speaker.setVolumePercentage(0.6)
    Speaker.tone(1000, 100)
    last_time = time.ticks_ms()


def loop():
    global \
        page0, \
        label_title, \
        button_save, \
        label_angle_x, \
        label_angle_y, \
        label_tip, \
        stackchan, \
        x_angle, \
        y_angle, \
        last_time
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        last_time = time.ticks_ms()
        x_angle = stackchan.get_servo_angle(stackchan.SERVO_ID_X)
        y_angle = stackchan.get_servo_angle(stackchan.SERVO_ID_Y)
        label_angle_x.set_text(str((str("X-Axis Servo Angle:") + str(x_angle))))
        label_angle_y.set_text(str((str("Y-Axis Servo Angle:") + str(y_angle))))


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
