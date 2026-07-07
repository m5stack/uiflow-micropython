# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from chain import PIRChain
from chain import ChainBus
import time


title0 = None
label_status = None
label_count = None
bus2 = None
chain_pir_0 = None
detected = None
count = None
last_time = None
trigger_hold_time = None


def chain_pir_0_motion_detected_event(args):
    global \
        title0, \
        label_status, \
        label_count, \
        bus2, \
        chain_pir_0, \
        detected, \
        count, \
        last_time, \
        trigger_hold_time
    print("detect motion")
    detected = True
    count = 0
    label_status.setText(str("Status: detected"))
    label_status.setColor(0x009900, 0x000000)
    label_count.setVisible(True)


def chain_pir_0_motion_ended_event(args):
    global \
        title0, \
        label_status, \
        label_count, \
        bus2, \
        chain_pir_0, \
        detected, \
        count, \
        last_time, \
        trigger_hold_time
    print("not detect")
    detected = False
    label_status.setText(str("Status: no detect"))
    label_status.setColor(0xCCCCCC, 0x000000)
    label_count.setVisible(False)


def setup():
    global \
        title0, \
        label_status, \
        label_count, \
        bus2, \
        chain_pir_0, \
        detected, \
        count, \
        last_time, \
        trigger_hold_time

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    title0 = Widgets.Title("Chain PIR Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_status = Widgets.Label(
        "Status: --", 20, 70, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu24
    )
    label_count = Widgets.Label(
        "Count: --", 20, 165, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu24
    )

    bus2 = ChainBus(2, tx=21, rx=22)
    chain_pir_0 = PIRChain(bus2, 1)
    chain_pir_0.set_trigger_callback(
        PIRChain.TRIGGER_MOTION_DETECTED, chain_pir_0_motion_detected_event
    )
    chain_pir_0.set_trigger_callback(PIRChain.TRIGGER_MOTION_ENDED, chain_pir_0_motion_ended_event)
    chain_pir_0.set_trigger(True)
    chain_pir_0.set_trigger_hold_time(5, save=False)
    trigger_hold_time = chain_pir_0.get_trigger_hold_time()
    print((str("trigger hold time: ") + str(trigger_hold_time)))
    detected = chain_pir_0.get_detect_status()
    if detected:
        label_status.setText(str("Status: detected"))
        label_status.setColor(0x009900, 0x000000)


def loop():
    global \
        title0, \
        label_status, \
        label_count, \
        bus2, \
        chain_pir_0, \
        detected, \
        count, \
        last_time, \
        trigger_hold_time
    M5.update()
    if detected:
        if (time.ticks_diff((time.ticks_ms()), last_time)) >= 1000:
            last_time = time.ticks_ms()
            count = (count if isinstance(count, (int, float)) else 0) + 1
            label_count.setText(str((str("Count: ") + str(count))))
    else:
        pass


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
