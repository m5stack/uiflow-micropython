# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import GatewayH2Module


title0 = None
label0 = None
label1 = None
label2 = None
label_addr = None
module_h2_0 = None
module_h2_0_ep = None
device_addr = None
device_count = None
device_list = None


def first_index(my_list, elem):
    try:
        index = my_list.index(elem) + 1
    except:
        index = 0
    return index


def module_h2_0_ep_bind_event(addr):
    global \
        title0, \
        label0, \
        label1, \
        label2, \
        label_addr, \
        module_h2_0, \
        module_h2_0_ep, \
        device_addr, \
        device_count, \
        device_list
    device_addr = addr
    print(device_addr)
    if first_index(device_list, device_addr) == 0:
        device_list.append(device_addr)
        device_count = device_count + 1
        label_addr.setText(str((str("new device addr: ") + str(device_addr))))


def btn_pwr_was_clicked_event(state):
    global \
        title0, \
        label0, \
        label1, \
        label2, \
        label_addr, \
        module_h2_0, \
        module_h2_0_ep, \
        device_addr, \
        device_count, \
        device_list
    if not not len(device_list):
        module_h2_0_ep.toggle()


def setup():
    global \
        title0, \
        label0, \
        label1, \
        label2, \
        label_addr, \
        module_h2_0, \
        module_h2_0_ep, \
        device_addr, \
        device_count, \
        device_list

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "Switch Endpoint Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label(
        "press the power button toggle", 2, 50, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "if has device connect", 2, 26, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label2 = Widgets.Label(
        "connect device: ", 2, 90, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_addr = Widgets.Label("None", 5, 115, 1.0, 0x00FF00, 0x222222, Widgets.FONTS.DejaVu18)
    BtnPWR.setCallback(type=BtnPWR.CB_TYPE.WAS_CLICKED, cb=btn_pwr_was_clicked_event)
    module_h2_0 = GatewayH2Module(2, 17, 10)
    module_h2_0_ep = module_h2_0.create_switch_ep()
    module_h2_0_ep.set_bind_callback(module_h2_0_ep_bind_event)
    device_count = 0
    device_list = []


def loop():
    global \
        title0, \
        label0, \
        label1, \
        label2, \
        label_addr, \
        module_h2_0, \
        module_h2_0_ep, \
        device_addr, \
        device_count, \
        device_list
    M5.update()


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
