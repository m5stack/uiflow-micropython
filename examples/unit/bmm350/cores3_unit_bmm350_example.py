# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from unit import BMM350Unit
from hardware import Pin
from hardware import I2C
import time



page0 = None
label_title = None
label_status = None
label_heading = None
label_x = None
label_y = None
label_z = None
label_temperature = None
button_calibrate = None
i2c0 = None
bmm350_0 = None
magnetic = None
calibration_result = None
temperature = None
heading = None
mag_x = None
mag_y = None
mag_z = None


def button_calibrate_short_clicked_event(event_struct):
    global page0, label_title, label_status, label_heading, label_x, label_y, label_z, label_temperature, button_calibrate, i2c0, bmm350_0, magnetic, calibration_result, temperature, heading, mag_x, mag_y, mag_z
    if bmm350_0.is_calibrating():
        try:
            calibration_result = bmm350_0.stop_calibration()
            label_status.set_text(str('Complete'))
            button_calibrate.set_btn_text(str('Calibrate'))
        except:
            label_status.set_text(str('Incomplete'))
            button_calibrate.set_btn_text(str('Retry'))

    else:
        if not (bmm350_0.is_calibrating()):
            bmm350_0.start_calibration()
            label_status.set_text(str('Calibrating'))
            button_calibrate.set_btn_text(str('Finish'))


def button_calibrate_event_handler(event_struct):
    global page0, label_title, label_status, label_heading, label_x, label_y, label_z, label_temperature, button_calibrate, i2c0, bmm350_0, magnetic, calibration_result, temperature, heading, mag_x, mag_y, mag_z
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button_calibrate_short_clicked_event(event_struct)
    return

def setup():
    global page0, label_title, label_status, label_heading, label_x, label_y, label_z, label_temperature, button_calibrate, i2c0, bmm350_0, magnetic, calibration_result, temperature, heading, mag_x, mag_y, mag_z

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x111820)
    label_title = m5ui.M5Label("BMM350 Unit", x=76, y=9, text_c=0x58D6C7, bg_c=0x111820, bg_opa=0, font=lv.font_montserrat_24, parent=page0)
    label_status = m5ui.M5Label("Ready", x=215, y=138, text_c=0x95A4B3, bg_c=0x111820, bg_opa=0, font=lv.font_montserrat_14, parent=page0)
    label_heading = m5ui.M5Label("Heading: ---.-", x=86, y=70, text_c=0xFFFFFF, bg_c=0x111820, bg_opa=0, font=lv.font_montserrat_24, parent=page0)
    label_x = m5ui.M5Label("X: ----.-- uT", x=10, y=140, text_c=0xFF6B6B, bg_c=0x111820, bg_opa=0, font=lv.font_montserrat_14, parent=page0)
    label_y = m5ui.M5Label("Y: ----.-- uT", x=10, y=160, text_c=0x58D68D, bg_c=0x111820, bg_opa=0, font=lv.font_montserrat_14, parent=page0)
    label_z = m5ui.M5Label("Z: ----.-- uT", x=10, y=180, text_c=0x5DADE2, bg_c=0x111820, bg_opa=0, font=lv.font_montserrat_14, parent=page0)
    label_temperature = m5ui.M5Label("Temp: --.- degC", x=10, y=205, text_c=0xE8EDF2, bg_c=0x111820, bg_opa=0, font=lv.font_montserrat_14, parent=page0)
    button_calibrate = m5ui.M5Button(text="Calibrate", x=180, y=173, bg_c=0x147D73, text_c=0xFFFFFF, font=lv.font_montserrat_14, parent=page0)

    button_calibrate.add_event_cb(button_calibrate_event_handler, lv.EVENT.ALL, None)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
    bmm350_0 = BMM350Unit(i2c0)
    page0.screen_load()


def loop():
    global page0, label_title, label_status, label_heading, label_x, label_y, label_z, label_temperature, button_calibrate, i2c0, bmm350_0, magnetic, calibration_result, temperature, heading, mag_x, mag_y, mag_z
    M5.update()
    magnetic = bmm350_0.get_mag()
    temperature = bmm350_0.get_temperature()
    heading = bmm350_0.get_heading()
    mag_x = magnetic[0]
    mag_y = magnetic[1]
    mag_z = magnetic[2]
    label_heading.set_text(str((str('Heading: ') + str((int(heading))))))
    label_x.set_text(str((str('X: ') + str(((str(mag_x) + str(' uT')))))))
    label_y.set_text(str((str('Y: ') + str(((str(mag_y) + str(' uT')))))))
    label_z.set_text(str((str('Z: ') + str(((str(mag_z) + str(' uT')))))))
    label_temperature.set_text(str((str('Temp: ') + str(((str((int(temperature))) + str(' degC')))))))
    time.sleep_ms(50)


if __name__ == '__main__':
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
