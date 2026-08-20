# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv


page0 = None
label_title = None
button_port_a = None
button_port_usb = None
button_charge = None
label_battery = None
label_current = None
label_charging = None


port_a = None
port_usb = None
charge_enabled = None
battery_level = None
battery_voltage = None
battery_current = None


def button_port_a_pressed_event(event_struct):
    global \
        page0, \
        label_title, \
        button_port_a, \
        button_port_usb, \
        button_charge, \
        label_battery, \
        label_current, \
        label_charging, \
        port_a, \
        port_usb, \
        charge_enabled, \
        battery_level, \
        battery_voltage, \
        battery_current
    if port_a:
        port_a = False
        Power.setExtOutput(False, M5.Power.PORT.A)
        button_port_a.set_btn_text(str("PORT.A OFF"))
        button_port_a.set_bg_color(0x5F6B75, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    else:
        port_a = True
        Power.setExtOutput(True, M5.Power.PORT.A)
        button_port_a.set_btn_text(str("PORT.A ON"))
        button_port_a.set_bg_color(0x2EAD65, 255, lv.PART.MAIN | lv.STATE.DEFAULT)


def button_port_usb_pressed_event(event_struct):
    global \
        page0, \
        label_title, \
        button_port_a, \
        button_port_usb, \
        button_charge, \
        label_battery, \
        label_current, \
        label_charging, \
        port_a, \
        port_usb, \
        charge_enabled, \
        battery_level, \
        battery_voltage, \
        battery_current
    if port_usb:
        port_usb = False
        Power.setExtOutput(False, M5.Power.PORT.USB)
        button_port_usb.set_btn_text(str("USB Type-A OFF"))
        button_port_usb.set_bg_color(0x5F6B75, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    else:
        port_usb = True
        Power.setExtOutput(True, M5.Power.PORT.USB)
        button_port_usb.set_btn_text(str("USB Type-A ON"))
        button_port_usb.set_bg_color(0x2EAD65, 255, lv.PART.MAIN | lv.STATE.DEFAULT)


def button_charge_pressed_event(event_struct):
    global \
        page0, \
        label_title, \
        button_port_a, \
        button_port_usb, \
        button_charge, \
        label_battery, \
        label_current, \
        label_charging, \
        port_a, \
        port_usb, \
        charge_enabled, \
        battery_level, \
        battery_voltage, \
        battery_current
    if charge_enabled:
        charge_enabled = False
        Power.setBatteryCharge(False)
        button_charge.set_btn_text(str("CHARGE OFF"))
        button_charge.set_bg_color(0x5F6B75, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    else:
        charge_enabled = True
        Power.setBatteryCharge(True)
        button_charge.set_btn_text(str("CHARGE ON"))
        button_charge.set_bg_color(0x2EAD65, 255, lv.PART.MAIN | lv.STATE.DEFAULT)


def button_port_a_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        button_port_a, \
        button_port_usb, \
        button_charge, \
        label_battery, \
        label_current, \
        label_charging, \
        port_a, \
        port_usb, \
        charge_enabled, \
        battery_level, \
        battery_voltage, \
        battery_current
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button_port_a_pressed_event(event_struct)
    return


def button_port_usb_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        button_port_a, \
        button_port_usb, \
        button_charge, \
        label_battery, \
        label_current, \
        label_charging, \
        port_a, \
        port_usb, \
        charge_enabled, \
        battery_level, \
        battery_voltage, \
        battery_current
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button_port_usb_pressed_event(event_struct)
    return


def button_charge_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        button_port_a, \
        button_port_usb, \
        button_charge, \
        label_battery, \
        label_current, \
        label_charging, \
        port_a, \
        port_usb, \
        charge_enabled, \
        battery_level, \
        battery_voltage, \
        battery_current
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button_charge_pressed_event(event_struct)
    return


def setup():
    global \
        page0, \
        label_title, \
        button_port_a, \
        button_port_usb, \
        button_charge, \
        label_battery, \
        label_current, \
        label_charging, \
        port_a, \
        port_usb, \
        charge_enabled, \
        battery_level, \
        battery_voltage, \
        battery_current

    M5.begin()
    Widgets.setRotation(3)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x101820)
    label_title = m5ui.M5Label(
        "Power Example",
        x=465,
        y=35,
        text_c=0x1976D2,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    button_port_a = m5ui.M5Button(
        text="PORT.A OFF",
        x=70,
        y=160,
        bg_c=0x5F6B75,
        text_c=0xF4F7FA,
        font=lv.font_montserrat_40,
        parent=page0,
    )
    button_port_usb = m5ui.M5Button(
        text="USB Type-A OFF",
        x=70,
        y=310,
        bg_c=0x5F6B75,
        text_c=0xF4F7FA,
        font=lv.font_montserrat_40,
        parent=page0,
    )
    button_charge = m5ui.M5Button(
        text="CHARGE ON",
        x=70,
        y=460,
        bg_c=0x2EAD65,
        text_c=0xF4F7FA,
        font=lv.font_montserrat_40,
        parent=page0,
    )
    label_battery = m5ui.M5Label(
        "Battery: --%   -.--- V",
        x=600,
        y=210,
        text_c=0xF4F7FA,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_current = m5ui.M5Label(
        "Current: -- mA",
        x=600,
        y=330,
        text_c=0xF4F7FA,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_charging = m5ui.M5Label(
        "Charging: --",
        x=600,
        y=450,
        text_c=0x9FB3C8,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )

    button_port_a.add_event_cb(button_port_a_event_handler, lv.EVENT.ALL, None)
    button_port_usb.add_event_cb(button_port_usb_event_handler, lv.EVENT.ALL, None)
    button_charge.add_event_cb(button_charge_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    Power.setBatteryCharge(True)
    port_a = False
    port_usb = False
    charge_enabled = True
    battery_level = Power.getBatteryLevel()
    battery_voltage = Power.getBatteryVoltage()
    battery_current = Power.getBatteryCurrent()
    label_current.set_text(str((str("Current: ") + str((str(battery_current) + str(" mA"))))))
    label_battery.set_text(
        str(
            (
                str("Battery: ")
                + str(
                    (
                        str(battery_level)
                        + str((str("%   ") + str((str((battery_voltage / 1000)) + str(" V")))))
                    )
                )
            )
        )
    )
    if battery_current > 10:
        label_charging.set_text(str("Charging: YES"))
        label_battery.set_text_color(0x2EAD65, 255, 0)
        label_charging.set_text_color(0x2EAD65, 255, 0)
    else:
        label_charging.set_text(str("Charging: NO"))
        label_battery.set_text_color(0xF4F7FA, 255, 0)
        label_charging.set_text_color(0x9FB3C8, 255, 0)


def loop():
    global \
        page0, \
        label_title, \
        button_port_a, \
        button_port_usb, \
        button_charge, \
        label_battery, \
        label_current, \
        label_charging, \
        port_a, \
        port_usb, \
        charge_enabled, \
        battery_level, \
        battery_voltage, \
        battery_current
    M5.update()
    battery_level = Power.getBatteryLevel()
    battery_voltage = Power.getBatteryVoltage()
    battery_current = Power.getBatteryCurrent()
    label_current.set_text(str((str("Current: ") + str((str(battery_current) + str(" mA"))))))
    label_battery.set_text(
        str(
            (
                str("Battery: ")
                + str(
                    (
                        str(battery_level)
                        + str((str("%   ") + str((str((battery_voltage / 1000)) + str(" V")))))
                    )
                )
            )
        )
    )
    if battery_current > 10:
        label_charging.set_text(str("Charging: YES"))
        label_battery.set_text_color(0x2EAD65, 255, 0)
        label_charging.set_text_color(0x2EAD65, 255, 0)
    else:
        label_charging.set_text(str("Charging: NO"))
        label_battery.set_text_color(0xF4F7FA, 255, 0)
        label_charging.set_text_color(0x9FB3C8, 255, 0)


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
