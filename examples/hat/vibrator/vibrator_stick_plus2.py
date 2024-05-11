import os, sys, io
import M5
from M5 import *
from hat import VibratorHat
from hardware import *


title0 = None
freq_label = None
duty_label = None
label0 = None
label1 = None
label2 = None
line0 = None
line1 = None
line2 = None
hat_vibrator_0 = None


import math

width = None
duty_w = None
duty = None
freq = None


# Describe this function...
def draw_pwm():
    global \
        width, \
        duty_w, \
        duty, \
        freq, \
        title0, \
        freq_label, \
        duty_label, \
        label0, \
        label1, \
        label2, \
        line0, \
        line1, \
        line2, \
        hat_vibrator_0
    if duty == 0:
        width = 55 - (freq - 10)
        print(width)
        line0.setPoints(x0=(67 - width), y0=160, x1=67, y1=160)
        line2.setPoints(x0=67, y0=160, x1=67, y1=160)
        line1.setPoints(x0=67, y0=160, x1=(67 + width), y1=160)
    else:
        width = 55 - (freq - 10)
        duty_w = math.ceil((width + width) * (duty / 100))
        line0.setPoints(x0=12, y0=130, x1=(12 + duty_w), y1=130)
        line2.setPoints(x0=(12 + duty_w), y0=130, x1=(12 + duty_w), y1=160)
        line1.setPoints(
            x0=(12 + duty_w), y0=160, x1=((12 + duty_w) + ((width + width) - duty_w)), y1=160
        )


def setup():
    global \
        title0, \
        freq_label, \
        duty_label, \
        label0, \
        label1, \
        label2, \
        line0, \
        line1, \
        line2, \
        hat_vibrator_0, \
        width, \
        duty_w, \
        duty, \
        freq

    M5.begin()
    Widgets.fillScreen(0xFFFFFF)
    title0 = Widgets.Title("VIBRATOR", 18, 0xFFFFFF, 0xF5A41D, Widgets.FONTS.DejaVu18)
    freq_label = Widgets.Label("Freq: 00", 2, 32, 1.0, 0xF5A41D, 0xFFFFFF, Widgets.FONTS.DejaVu18)
    duty_label = Widgets.Label("Duty: 00", 2, 64, 1.0, 0xF5A41D, 0xFFFFFF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label(
        "Long Press Turn OFF", 18, 192, 1.0, 0xF5A41D, 0xFFFFFF, Widgets.FONTS.DejaVu9
    )
    label1 = Widgets.Label("Duty", 84, 100, 1.0, 0xF5A41D, 0xFFFFFF, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("Freq", 47, 213, 1.0, 0xF5A41D, 0xFFFFFF, Widgets.FONTS.DejaVu18)
    line0 = Widgets.Line(12, 130, 67, 130, 0xF5A41D)
    line1 = Widgets.Line(67, 160, 122, 160, 0xF5A41D)
    line2 = Widgets.Line(67, 130, 67, 160, 0xF5A41D)

    hat_vibrator_0 = VibratorHat(port=(26, 0))
    freq = 10
    duty = 0
    freq_label.setText(str((str("Freq: ") + str(freq))))
    duty_label.setText(str((str("Duty: ") + str(duty))))
    draw_pwm()
    hat_vibrator_0.once(freq=10, duty=50, duration=50)


def loop():
    global \
        title0, \
        freq_label, \
        duty_label, \
        label0, \
        label1, \
        label2, \
        line0, \
        line1, \
        line2, \
        hat_vibrator_0, \
        width, \
        duty_w, \
        duty, \
        freq
    M5.update()
    if BtnA.wasClicked():
        freq = freq + 1
        if freq > 55:
            freq = 10
        freq_label.setText(str((str("Freq: ") + str(freq))))
        draw_pwm()
        hat_vibrator_0.set_freq(freq)
    if BtnB.wasClicked():
        duty = duty + 1
        duty = duty % 100
        duty_label.setText(str((str("Duty: ") + str(duty))))
        draw_pwm()
        hat_vibrator_0.set_duty(duty)
    if BtnA.isHolding():
        duty = 0
        draw_pwm()
        hat_vibrator_0.turn_off()


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
