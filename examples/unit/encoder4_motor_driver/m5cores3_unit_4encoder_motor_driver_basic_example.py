# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from unit import Encoder4MotorDriverUnit
from hardware import Pin
from hardware import I2C


page0 = None
button_stop = None
label_title = None
label_m1 = None
slider_m1 = None
slider_m2 = None
slider_m3 = None
slider_m4 = None
label_m4 = None
label_m3 = None
label_m2 = None
label_v1 = None
label_v4 = None
label_v3 = None
label_v2 = None
i2c0 = None
encoder4motordriver_0 = None
speed1 = None
speed2 = None
speed3 = None
speed4 = None
speed = None


def button_stop_short_clicked_event(event_struct):
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
        speed
    encoder4motordriver_0.stop_motor(Encoder4MotorDriverUnit.MOTOR_ALL)
    encoder4motordriver_0.set_rgb_color(0xCC0000)
    speed1 = 0
    speed2 = 0
    speed3 = 0
    speed4 = 0
    label_v1.set_text(str(speed1))
    label_v2.set_text(str(speed2))
    label_v3.set_text(str(speed3))
    label_v4.set_text(str(speed4))


def slider_m1_value_changed_event(event_struct):
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
        speed
    speed1 = slider_m1.get_value()
    encoder4motordriver_0.set_motor_pwm_duty(Encoder4MotorDriverUnit.MOTOR_1, speed1)
    label_v1.set_text(str(speed1))
    encoder4motordriver_0.set_rgb_color(0x009900)


def slider_m2_value_changed_event(event_struct):
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
        speed
    speed2 = slider_m2.get_value()
    encoder4motordriver_0.set_motor_pwm_duty(Encoder4MotorDriverUnit.MOTOR_2, speed2)
    label_v2.set_text(str(speed2))
    encoder4motordriver_0.set_rgb_color(0x009900)


def slider_m3_value_changed_event(event_struct):
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
        speed
    speed3 = slider_m3.get_value()
    encoder4motordriver_0.set_motor_pwm_duty(Encoder4MotorDriverUnit.MOTOR_3, speed3)
    label_v3.set_text(str(speed3))
    encoder4motordriver_0.set_rgb_color(0x009900)


def slider_m4_value_changed_event(event_struct):
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
        speed
    speed4 = slider_m4.get_value()
    encoder4motordriver_0.set_motor_pwm_duty(Encoder4MotorDriverUnit.MOTOR_4, speed4)
    label_v4.set_text(str(speed4))
    encoder4motordriver_0.set_rgb_color(0x009900)


def button_stop_event_handler(event_struct):
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
        speed
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button_stop_short_clicked_event(event_struct)
    return


def slider_m1_event_handler(event_struct):
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
        speed
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        slider_m1_value_changed_event(event_struct)
    return


def slider_m2_event_handler(event_struct):
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
        speed
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        slider_m2_value_changed_event(event_struct)
    return


def slider_m3_event_handler(event_struct):
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
        speed
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        slider_m3_value_changed_event(event_struct)
    return


def slider_m4_event_handler(event_struct):
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
        speed
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        slider_m4_value_changed_event(event_struct)
    return


def setup():
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
        speed

    M5.begin()
    Widgets.setRotation(0)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    button_stop = m5ui.M5Button(
        text="STOP",
        x=112,
        y=185,
        bg_c=0xF32121,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_title = m5ui.M5Label(
        "4Encoder Motor Control",
        x=12,
        y=5,
        text_c=0x079EE1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_m1 = m5ui.M5Label(
        "M1",
        x=4,
        y=42,
        text_c=0x079EE1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    slider_m1 = m5ui.M5Slider(
        x=55,
        y=45,
        w=205,
        h=11,
        mode=lv.slider.MODE.NORMAL,
        min_value=0,
        max_value=100,
        value=0,
        bg_c=0x2193F3,
        color=0x2193F3,
        parent=page0,
    )
    slider_m2 = m5ui.M5Slider(
        x=55,
        y=76,
        w=205,
        h=11,
        mode=lv.slider.MODE.NORMAL,
        min_value=0,
        max_value=100,
        value=0,
        bg_c=0x2193F3,
        color=0x2193F3,
        parent=page0,
    )
    slider_m3 = m5ui.M5Slider(
        x=56,
        y=107,
        w=205,
        h=11,
        mode=lv.slider.MODE.NORMAL,
        min_value=0,
        max_value=100,
        value=0,
        bg_c=0x2193F3,
        color=0x2193F3,
        parent=page0,
    )
    slider_m4 = m5ui.M5Slider(
        x=55,
        y=139,
        w=205,
        h=11,
        mode=lv.slider.MODE.NORMAL,
        min_value=0,
        max_value=100,
        value=0,
        bg_c=0x2193F3,
        color=0x2193F3,
        parent=page0,
    )
    label_m4 = m5ui.M5Label(
        "M4",
        x=4,
        y=136,
        text_c=0x079EE1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_m3 = m5ui.M5Label(
        "M3",
        x=3,
        y=104,
        text_c=0x079EE1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_m2 = m5ui.M5Label(
        "M2",
        x=4,
        y=73,
        text_c=0x079EE1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_v1 = m5ui.M5Label(
        "00",
        x=267,
        y=42,
        text_c=0x079EE1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_v4 = m5ui.M5Label(
        "00",
        x=267,
        y=136,
        text_c=0x079EE1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_v3 = m5ui.M5Label(
        "00",
        x=267,
        y=104,
        text_c=0x079EE1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_v2 = m5ui.M5Label(
        "00",
        x=267,
        y=73,
        text_c=0x079EE1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    button_stop.add_event_cb(button_stop_event_handler, lv.EVENT.ALL, None)
    slider_m1.add_event_cb(slider_m1_event_handler, lv.EVENT.ALL, None)
    slider_m2.add_event_cb(slider_m2_event_handler, lv.EVENT.ALL, None)
    slider_m3.add_event_cb(slider_m3_event_handler, lv.EVENT.ALL, None)
    slider_m4.add_event_cb(slider_m4_event_handler, lv.EVENT.ALL, None)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    encoder4motordriver_0 = Encoder4MotorDriverUnit(i2c0, 0x24)
    page0.screen_load()
    speed = 0
    encoder4motordriver_0.set_motor_mode(
        Encoder4MotorDriverUnit.MOTOR_ALL, Encoder4MotorDriverUnit.MODE_OPEN_LOOP
    )
    encoder4motordriver_0.set_rgb_color(0x009900)
    speed1 = 0
    speed2 = 0
    speed3 = 0
    speed4 = 0


def loop():
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
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
