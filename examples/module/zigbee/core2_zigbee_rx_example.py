# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import ZigbeeModule


label0 = None
com_zigbee_0 = None


zigbee_str_data = None
zigbee_dest_address = None
zigbee_src_address = None


def com_zigbee_0_receive_event(dest_address, src_address, received_data):
    global label0, com_zigbee_0, zigbee_str_data, zigbee_dest_address, zigbee_src_address
    zigbee_dest_address = dest_address
    zigbee_src_address = src_address
    try:
        zigbee_str_data = received_data.decode()
    except:
        zigbee_str_data = str(received_data)
    label0.setText(str(zigbee_str_data))


def setup():
    global label0, com_zigbee_0, zigbee_str_data, zigbee_dest_address, zigbee_src_address

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 50, 34, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    com_zigbee_0 = ZigbeeModule(2, 14, 13, verbose=True)
    com_zigbee_0.set_module_param(
        ZigbeeModule.DEVICE_TYPE_ROUTER,
        0x1620,
        11,
        ZigbeeModule.TRANSFER_MODE_PASS_THROUGH,
        0x0066,
    )
    while not (com_zigbee_0.isconnected()):
        pass
    label0.setText(str(com_zigbee_0.get_custom_address()))
    com_zigbee_0.receive_none_block(com_zigbee_0_receive_event)


def loop():
    global label0, com_zigbee_0, zigbee_str_data, zigbee_dest_address, zigbee_src_address
    M5.update()


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            com_zigbee_0.stop_receive()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
