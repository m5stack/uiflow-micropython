# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import GatewayH2Unit


title0 = None
label0 = None
label1 = None
label2 = None
label_addr = None
gateway_h2_0 = None
gateway_h2_0_ep = None
device_addr = None
device_count = None
device_list = None


def first_index(my_list, elem):
    try:
        index = my_list.index(elem) + 1
    except:
        index = 0
    return index


def gateway_h2_0_ep_bind_event(addr):
    global \
        title0, \
        label0, \
        label1, \
        label2, \
        label_addr, \
        gateway_h2_0, \
        gateway_h2_0_ep, \
        device_addr, \
        device_count, \
        device_list
    device_addr = addr
    print(device_addr)
    if first_index(device_list, device_addr) == 0:
        device_list.append(device_addr)
        device_count = device_count + 1
        label_addr.setText(str((str("new device addr: ") + str(device_addr))))
        gateway_h2_0_ep.off(device_addr)


def btnPWR_wasClicked_event(state):
    global \
        title0, \
        label0, \
        label1, \
        label2, \
        label_addr, \
        gateway_h2_0, \
        gateway_h2_0_ep, \
        device_addr, \
        device_count, \
        device_list
    if not not len(device_list):
        gateway_h2_0_ep.toggle()


def setup():
    global \
        title0, \
        label0, \
        label1, \
        label2, \
        label_addr, \
        gateway_h2_0, \
        gateway_h2_0_ep, \
        device_addr, \
        device_count, \
        device_list

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("GatewayH2Unit Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label(
        "if has device connect", 2, 26, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "press the power button toggle", 2, 50, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label2 = Widgets.Label(
        "connect device: ", 2, 90, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_addr = Widgets.Label("None", 5, 115, 1.0, 0x00FF00, 0x222222, Widgets.FONTS.DejaVu18)

    BtnPWR.setCallback(type=BtnPWR.CB_TYPE.WAS_CLICKED, cb=btnPWR_wasClicked_event)

    gateway_h2_0 = GatewayH2Unit(1, port=(1, 2))
    gateway_h2_0_ep = gateway_h2_0.create_switch_ep()
    gateway_h2_0_ep.set_bind_callback(gateway_h2_0_ep_bind_event)
    device_count = 0
    device_list = []


def loop():
    global \
        title0, \
        label0, \
        label1, \
        label2, \
        label_addr, \
        gateway_h2_0, \
        gateway_h2_0_ep, \
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
