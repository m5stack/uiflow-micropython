# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import switchc6


page0 = None
switch0 = None
label0 = None
label1 = None
label2 = None
label3 = None
switchc6_controller = None


switchc6_target_mac = None
switchc6_onoff = None
switchc6_voltage = None


def switch0_checked_event(event_struct):
    global \
        page0, \
        switch0, \
        label0, \
        label1, \
        label2, \
        label3, \
        switchc6_controller, \
        switchc6_target_mac, \
        switchc6_onoff, \
        switchc6_voltage
    switchc6_controller.toggle_switch("E4B3-2386-18B8", timeout=2000)


def switchc6_controller_off_event(args):
    global \
        page0, \
        switch0, \
        label0, \
        label1, \
        label2, \
        label3, \
        switchc6_controller, \
        switchc6_target_mac, \
        switchc6_onoff, \
        switchc6_voltage
    _, switchc6_target_mac, switchc6_onoff, switchc6_voltage = args
    label0.set_text(str(switchc6_target_mac))
    label1.set_text(str(switchc6_onoff))
    label2.set_text(str(switchc6_voltage))


def switch0_unchecked_event(event_struct):
    global \
        page0, \
        switch0, \
        label0, \
        label1, \
        label2, \
        label3, \
        switchc6_controller, \
        switchc6_target_mac, \
        switchc6_onoff, \
        switchc6_voltage
    switchc6_controller.set_switch("E4B3-2386-18B8", False, timeout=2000)


def switchc6_controller_on_event(args):
    global \
        page0, \
        switch0, \
        label0, \
        label1, \
        label2, \
        label3, \
        switchc6_controller, \
        switchc6_target_mac, \
        switchc6_onoff, \
        switchc6_voltage
    _, switchc6_target_mac, switchc6_onoff, switchc6_voltage = args
    label0.set_text(str(switchc6_target_mac))
    label1.set_text(str(switchc6_onoff))
    label2.set_text(str(switchc6_voltage))


def switch0_event_handler(event_struct):
    global \
        page0, \
        switch0, \
        label0, \
        label1, \
        label2, \
        label3, \
        switchc6_controller, \
        switchc6_target_mac, \
        switchc6_onoff, \
        switchc6_voltage
    event = event_struct.code
    obj = event_struct.get_target_obj()
    if event == lv.EVENT.VALUE_CHANGED:
        if obj.has_state(lv.STATE.CHECKED):
            switch0_checked_event(event_struct)
        else:
            switch0_unchecked_event(event_struct)
    return


def setup():
    global \
        page0, \
        switch0, \
        label0, \
        label1, \
        label2, \
        label3, \
        switchc6_controller, \
        switchc6_target_mac, \
        switchc6_onoff, \
        switchc6_voltage

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    switch0 = m5ui.M5Switch(
        x=76,
        y=49,
        w=154,
        h=77,
        bg_c=0xE7E3E7,
        bg_c_checked=0x2196F3,
        circle_c=0xFFFFFF,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "label0",
        x=19,
        y=151,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label1 = m5ui.M5Label(
        "label1",
        x=17,
        y=173,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label2 = m5ui.M5Label(
        "label2",
        x=17,
        y=195,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label3 = m5ui.M5Label(
        "label3",
        x=18,
        y=217,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    switch0.add_event_cb(switch0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    switchc6_controller = switchc6.SwitchC6Controller(
        ["E4B3-2386-18B8"], wifi_channel=0, verbose=False
    )
    switchc6_controller.set_callback(switchc6_controller_off_event, switchc6_controller.OFF)
    switchc6_controller.set_callback(switchc6_controller_on_event, switchc6_controller.ON)
    label3.set_text(str(switchc6_controller.get_firmware_version("E4B3-2386-18B8", timeout=5000)))
    label1.set_text(str(switchc6_controller.get_capacitor_voltage("E4B3-2386-18B8", timeout=5000)))
    label2.set_text(str(switchc6_controller.get_switch_status("E4B3-2386-18B8", timeout=5000)))


def loop():
    global \
        page0, \
        switch0, \
        label0, \
        label1, \
        label2, \
        label3, \
        switchc6_controller, \
        switchc6_target_mac, \
        switchc6_onoff, \
        switchc6_voltage
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
