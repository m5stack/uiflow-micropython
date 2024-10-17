# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from module import Module4In8Out
import time


title0 = None
label0 = None
label1 = None
label2 = None
label3 = None
module_4in8out_0 = None


load_num = None
switch_num = None
state = None


def setup():
    global title0, label0, label1, label2, label3, module_4in8out_0, load_num, switch_num, state

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("4In8OutModule Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label(
        "Switch i Status:", 1, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "Load i Status:", 1, 118, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label2 = Widgets.Label("I2C Addr:", 1, 178, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label(
        "FW Version:", 176, 178, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    module_4in8out_0 = Module4In8Out(address=0x45)
    label2.setText(str((str("I2C Addr:") + str((module_4in8out_0.get_i2c_address())))))
    label3.setText(str((str("FW Version:") + str((module_4in8out_0.get_firmware_version())))))
    load_num = 1
    switch_num = 1
    state = 1


def loop():
    global title0, label0, label1, label2, label3, module_4in8out_0, load_num, switch_num, state
    M5.update()
    load_num = load_num + 1
    switch_num = switch_num + 1
    if load_num > 8:
        load_num = 1
        state = not state
    if switch_num > 4:
        switch_num = 1
    module_4in8out_0.set_load_state(load_num, state)
    label0.setText(
        str(
            (
                str("Switch ")
                + str(
                    (
                        str(switch_num)
                        + str(
                            (
                                str(" Status:")
                                + str((module_4in8out_0.get_switch_value(switch_num)))
                            )
                        )
                    )
                )
            )
        )
    )
    label1.setText(
        str(
            (
                str("Load ")
                + str(
                    (
                        str(load_num)
                        + str(
                            (str(" Status:") + str((module_4in8out_0.get_load_state(switch_num))))
                        )
                    )
                )
            )
        )
    )
    time.sleep(1)


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
