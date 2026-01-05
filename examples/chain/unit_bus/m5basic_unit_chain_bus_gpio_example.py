# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from chain import ChainBus
from chain import BusChainUnit
import time


title = None
label_gpio1 = None
label_tip1 = None
label_tip2 = None
label_gpio2 = None
bus2 = None
unit_chain_bus_0 = None
last_time = None
gpio1_value = None
cnt = None
gpio2_value = None


def setup():
    global \
        title, \
        label_gpio1, \
        label_tip1, \
        label_tip2, \
        label_gpio2, \
        bus2, \
        unit_chain_bus_0, \
        last_time, \
        gpio1_value, \
        cnt, \
        gpio2_value

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title = Widgets.Title(
        "Unit Chain Bus Example: GPIO", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label_gpio1 = Widgets.Label(
        "GPIO1 Value: --", 10, 85, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_tip1 = Widgets.Label(
        "Unit Chain Bus GPIO1: Input", 10, 55, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_tip2 = Widgets.Label(
        "Unit Chain Bus GPIO2: Output", 10, 136, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_gpio2 = Widgets.Label(
        "GPIO2 Value: --", 10, 165, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    bus2 = ChainBus(2, tx=21, rx=22)
    unit_chain_bus_0 = BusChainUnit(bus2, 1)
    unit_chain_bus_0.set_gpio_input(1, BusChainUnit.GPIO_PULL_UP)
    unit_chain_bus_0.set_gpio_output(2, BusChainUnit.GPIO_MODE_PUSHPULL, BusChainUnit.GPIO_PULL_UP)
    if (unit_chain_bus_0.get_work_mode(1)) == (BusChainUnit.WORK_MODE_GPIO_INPUT):
        print("set gpio1 as gpio input success")
    else:
        print("set gpio1 as gpio input failed")
    if (unit_chain_bus_0.get_work_mode(2)) == (BusChainUnit.WORK_MODE_GPIO_OUTPUT):
        print("set gpio2 as gpio output success")
    else:
        print("set gpio2 as gpio output failed")
    unit_chain_bus_0.set_rgb_color(0x000099)


def loop():
    global \
        title, \
        label_gpio1, \
        label_tip1, \
        label_tip2, \
        label_gpio2, \
        bus2, \
        unit_chain_bus_0, \
        last_time, \
        gpio1_value, \
        cnt, \
        gpio2_value
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 200:
        last_time = time.ticks_ms()
        gpio1_value = unit_chain_bus_0.get_gpio_input_value(1)
        if gpio1_value:
            label_gpio1.setText(str("GPIO1 Value:  HIGH"))
        else:
            label_gpio1.setText(str("GPIO1 Value:  LOW"))
        cnt = (cnt if isinstance(cnt, (int, float)) else 0) + 1
        if cnt >= 5:
            cnt = 0
            gpio2_value = not gpio2_value
            if gpio2_value:
                unit_chain_bus_0.set_gpio_output_value(2, 1)
                label_gpio2.setText(str("GPIO2 Value:  HIGH"))
            else:
                unit_chain_bus_0.set_gpio_output_value(2, 0)
                label_gpio2.setText(str("GPIO2 Value:  LOW"))


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            bus2.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
