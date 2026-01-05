# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from chain import ChainBus
from chain import BusChainUnit
import time
import m5utils


title = None
label_adc = None
label_tip = None
bus2 = None
unit_chain_bus_0 = None
last_time = None
adc_value = None


def setup():
    global title, label_adc, label_tip, bus2, unit_chain_bus_0, last_time, adc_value

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title = Widgets.Title(
        "Unit Chain Bus Example: ADC", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label_adc = Widgets.Label(
        "ADC Value: --", 10, 85, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_tip = Widgets.Label(
        "Unit Chain Bus GPIO1: ADC", 10, 55, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    bus2 = ChainBus(2, tx=21, rx=22)
    unit_chain_bus_0 = BusChainUnit(bus2, 1)
    unit_chain_bus_0.set_adc(1)
    if (unit_chain_bus_0.get_work_mode(1)) == (BusChainUnit.WORK_MODE_ADC):
        print("set gpio1 as adc input success")
    else:
        print("set gpio1 as adc input failed")
    unit_chain_bus_0.set_rgb_color(0x000099)


def loop():
    global title, label_adc, label_tip, bus2, unit_chain_bus_0, last_time, adc_value
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 200:
        last_time = time.ticks_ms()
        adc_value = unit_chain_bus_0.get_adc_input(1)
        label_adc.setText(str((str("ADC Value: ") + str(adc_value))))
        print((str("ADC Value: ") + str(adc_value)))
        unit_chain_bus_0.set_rgb_brightness(
            int(m5utils.remap(adc_value, 0, 4096, 0, 100)), save=False
        )


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
