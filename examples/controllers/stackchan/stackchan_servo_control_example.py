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
label_status = None
stackchan = None


def cleanup():
    global stackchan
    if stackchan is None:
        return
    try:
        stackchan.set_servo_x_pwm(0)
        time.sleep_ms(100)
        stackchan.set_servo_angle(stackchan.SERVO_ID_X, 0, 500, 0)
        stackchan.set_servo_angle(stackchan.SERVO_ID_Y, 45, 500, 0)
        time.sleep_ms(600)
        stackchan.set_servo_torque(stackchan.SERVO_ID_X, enable=False)
        stackchan.set_servo_torque(stackchan.SERVO_ID_Y, enable=False)
        stackchan.set_servo_power(enable=False)
    except Exception as e:
        print("StackChan cleanup failed:", e)


def setup():
    global page0, label_title, label_status, stackchan

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    label_title = m5ui.M5Label(
        "Servo Control Example",
        x=20,
        y=5,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_status = m5ui.M5Label(
        "--",
        x=153,
        y=115,
        text_c=0x0DC9F4,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )

    stackchan = StackChan(i2c=1, uart=1)
    page0.screen_load()
    Speaker.begin()
    Speaker.setVolumePercentage(0.5)
    # A previous run may have been interrupted while X was in PWM mode.
    # Power-cycle the servo rail before enabling torque to recover cleanly.
    stackchan.set_servo_power(enable=False, settle_ms=300)
    stackchan.set_servo_power(enable=True)
    stackchan.set_servo_torque(stackchan.SERVO_ID_X, enable=True)
    stackchan.set_servo_torque(stackchan.SERVO_ID_Y, enable=True)

    label_status.set_text(str("Center X/Y"))
    label_status.align_to(page0, lv.ALIGN.CENTER, 0, 0)
    stackchan.set_servo_angle(stackchan.SERVO_ID_X, 0, 1000, 0)
    stackchan.set_servo_angle(stackchan.SERVO_ID_Y, 45, 1000, 0)
    Speaker.tone(678, 300)
    time.sleep_ms(2000)

    label_status.set_text(str("Y tilt up"))
    label_status.align_to(page0, lv.ALIGN.CENTER, 0, 0)
    stackchan.set_servo_angle(stackchan.SERVO_ID_Y, 20, 1000, 0)
    time.sleep_ms(1800)

    label_status.set_text(str("Y tilt down"))
    label_status.align_to(page0, lv.ALIGN.CENTER, 0, 0)
    stackchan.set_servo_angle(stackchan.SERVO_ID_Y, 70, 1000, 0)
    time.sleep_ms(1800)

    label_status.set_text(str("Y back to center"))
    label_status.align_to(page0, lv.ALIGN.CENTER, 0, 0)
    stackchan.set_servo_angle(stackchan.SERVO_ID_Y, 45, 1000, 0)
    time.sleep_ms(1500)

    label_status.set_text(str("X rotate counterclockwise"))
    label_status.align_to(page0, lv.ALIGN.CENTER, 0, 0)
    stackchan.set_servo_x_pwm(-50)
    time.sleep_ms(3000)

    label_status.set_text(str("X rotate clockwise"))
    label_status.align_to(page0, lv.ALIGN.CENTER, 0, 0)
    stackchan.set_servo_x_pwm(50)
    time.sleep_ms(3000)

    label_status.set_text(str("X/Y back to center"))
    label_status.align_to(page0, lv.ALIGN.CENTER, 0, 0)
    stackchan.set_servo_x_pwm(0)
    time.sleep_ms(100)
    stackchan.set_servo_angle(stackchan.SERVO_ID_X, 0, 1000, 0)
    stackchan.set_servo_angle(stackchan.SERVO_ID_Y, 45, 1000, 0)


def loop():
    global page0, label_title, label_status, stackchan
    M5.update()


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        cleanup()
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
