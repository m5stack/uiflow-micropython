# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time


page0 = None
label_title = None
label_vbus = None
label_battery = None
label_charging = None
label_port_a = None
label_charge_control = None
label_action = None
label_vbus_name = None
label_battery_name = None
label_charging_name = None
label_port_a_name = None
label_charge_control_name = None
button_port_a = None
button_charge = None


port_a_enabled = None
charge_enabled = None


def button_port_a_clicked_event(event_struct):
    global \
        page0, \
        label_title, \
        label_vbus, \
        label_battery, \
        label_charging, \
        label_port_a, \
        label_charge_control, \
        label_action, \
        label_vbus_name, \
        label_battery_name, \
        label_charging_name, \
        label_port_a_name, \
        label_charge_control_name, \
        button_port_a, \
        button_charge, \
        port_a_enabled, \
        charge_enabled
    port_a_enabled = not port_a_enabled
    if port_a_enabled:
        Power.setExtOutput(True, 1)
    else:
        Power.setExtOutput(False, 1)
    if port_a_enabled:
        button_port_a.set_btn_text(str("PORT A: ON"))
        label_port_a.set_text(str("ON"))
    else:
        button_port_a.set_btn_text(str("PORT A: OFF"))
        label_port_a.set_text(str("OFF"))
    label_action.set_text(str("Port A 5V updated"))


def button_charge_clicked_event(event_struct):
    global \
        page0, \
        label_title, \
        label_vbus, \
        label_battery, \
        label_charging, \
        label_port_a, \
        label_charge_control, \
        label_action, \
        label_vbus_name, \
        label_battery_name, \
        label_charging_name, \
        label_port_a_name, \
        label_charge_control_name, \
        button_port_a, \
        button_charge, \
        port_a_enabled, \
        charge_enabled
    charge_enabled = not charge_enabled
    if charge_enabled:
        Power.setBatteryCharge(True)
    else:
        Power.setBatteryCharge(False)
    if charge_enabled:
        button_charge.set_btn_text(str("CHARGE: ON"))
        label_charge_control.set_text(str("ON"))
    else:
        button_charge.set_btn_text(str("CHARGE: OFF"))
        label_charge_control.set_text(str("OFF"))
    label_action.set_text(str("Charge control updated"))


def button_port_a_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_vbus, \
        label_battery, \
        label_charging, \
        label_port_a, \
        label_charge_control, \
        label_action, \
        label_vbus_name, \
        label_battery_name, \
        label_charging_name, \
        label_port_a_name, \
        label_charge_control_name, \
        button_port_a, \
        button_charge, \
        port_a_enabled, \
        charge_enabled
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button_port_a_clicked_event(event_struct)
    return


def button_charge_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_vbus, \
        label_battery, \
        label_charging, \
        label_port_a, \
        label_charge_control, \
        label_action, \
        label_vbus_name, \
        label_battery_name, \
        label_charging_name, \
        label_port_a_name, \
        label_charge_control_name, \
        button_port_a, \
        button_charge, \
        port_a_enabled, \
        charge_enabled
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button_charge_clicked_event(event_struct)
    return


def setup():
    global \
        page0, \
        label_title, \
        label_vbus, \
        label_battery, \
        label_charging, \
        label_port_a, \
        label_charge_control, \
        label_action, \
        label_vbus_name, \
        label_battery_name, \
        label_charging_name, \
        label_port_a_name, \
        label_charge_control_name, \
        button_port_a, \
        button_charge, \
        port_a_enabled, \
        charge_enabled

    M5.begin()
    Widgets.setRotation(0)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x080808)
    label_title = m5ui.M5Label(
        "Power",
        x=24,
        y=18,
        text_c=0xF1F5F7,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_vbus = m5ui.M5Label(
        "---- mV",
        x=284,
        y=82,
        text_c=0xF1F5F7,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_battery = m5ui.M5Label(
        "---- mV",
        x=284,
        y=124,
        text_c=0xF1F5F7,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_charging = m5ui.M5Label(
        "--",
        x=284,
        y=166,
        text_c=0xF1F5F7,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_port_a = m5ui.M5Label(
        "OFF",
        x=284,
        y=208,
        text_c=0xF1F5F7,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_charge_control = m5ui.M5Label(
        "ON",
        x=284,
        y=250,
        text_c=0xF1F5F7,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_action = m5ui.M5Label(
        "Power controls ready",
        x=24,
        y=342,
        text_c=0xA9BAC4,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_vbus_name = m5ui.M5Label(
        "USB VBUS",
        x=24,
        y=82,
        text_c=0xA9BAC4,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_battery_name = m5ui.M5Label(
        "Battery",
        x=24,
        y=124,
        text_c=0xA9BAC4,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_charging_name = m5ui.M5Label(
        "Charging",
        x=24,
        y=166,
        text_c=0xA9BAC4,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_port_a_name = m5ui.M5Label(
        "Port A 5 V",
        x=24,
        y=208,
        text_c=0xA9BAC4,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_charge_control_name = m5ui.M5Label(
        "Charge control",
        x=24,
        y=250,
        text_c=0xA9BAC4,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    button_port_a = m5ui.M5Button(
        text="PORT A: OFF",
        x=24,
        y=388,
        bg_c=0x245A85,
        text_c=0xF1F5F7,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    button_charge = m5ui.M5Button(
        text="CHARGE: ON",
        x=252,
        y=388,
        bg_c=0x245A85,
        text_c=0xF1F5F7,
        font=lv.font_montserrat_18,
        parent=page0,
    )

    button_port_a.add_event_cb(button_port_a_event_handler, lv.EVENT.ALL, None)
    button_charge.add_event_cb(button_charge_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    Power.setExtOutput(False, 1)
    Power.setBatteryCharge(True)
    port_a_enabled = False
    charge_enabled = True
    button_port_a.set_size(204, 64)
    button_charge.set_size(204, 64)


def loop():
    global \
        page0, \
        label_title, \
        label_vbus, \
        label_battery, \
        label_charging, \
        label_port_a, \
        label_charge_control, \
        label_action, \
        label_vbus_name, \
        label_battery_name, \
        label_charging_name, \
        label_port_a_name, \
        label_charge_control_name, \
        button_port_a, \
        button_charge, \
        port_a_enabled, \
        charge_enabled
    M5.update()
    label_vbus.set_text(str((str("") + str((str((Power.getVBUSVoltage())) + str(" mV"))))))
    label_battery.set_text(str((str("") + str((str((Power.getBatteryVoltage())) + str(" mV"))))))
    if Power.isCharging():
        label_charging.set_text(str("YES"))
        label_battery.set_text_color(0x8EDA91, 255, 0)
    else:
        label_charging.set_text(str("NO"))
        label_battery.set_text_color(0xF1F5F7, 255, 0)
    time.sleep_ms(500)


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
