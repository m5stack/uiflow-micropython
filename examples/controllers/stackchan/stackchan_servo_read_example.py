import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time
from hardware.stackchan import StackChan


page0 = None
label_title = None
label_agnle_x = None
label_angle_y = None
stackchan = None
last_time = None
x_angle = None
y_angle = None


def setup():
    global page0, label_title, label_agnle_x, label_angle_y, stackchan, last_time, x_angle, y_angle

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    label_title = m5ui.M5Label(
        "Servo Read Example",
        x=34,
        y=10,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_agnle_x = m5ui.M5Label(
        "X-Axis Servo Angle:",
        x=10,
        y=80,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_angle_y = m5ui.M5Label(
        "Y-Axis Servo Angle:",
        x=10,
        y=125,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    stackchan = StackChan(i2c=1, uart=1)
    page0.screen_load()
    stackchan.set_servo_power(enable=True, settle_ms=500)
    stackchan.set_servo_torque(stackchan.SERVO_ID_X, enable=False)
    stackchan.set_servo_torque(stackchan.SERVO_ID_Y, enable=False)
    last_time = time.ticks_ms()


def loop():
    global page0, label_title, label_agnle_x, label_angle_y, stackchan, last_time, x_angle, y_angle
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        last_time = time.ticks_ms()
        x_angle = stackchan.get_servo_angle(stackchan.SERVO_ID_X)
        y_angle = stackchan.get_servo_angle(stackchan.SERVO_ID_Y)
        label_agnle_x.set_text(str((str("X-Axis Servo Angle: ") + str(x_angle))))
        label_angle_y.set_text(str((str("Y-Axis Servo Angle: ") + str(y_angle))))


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
