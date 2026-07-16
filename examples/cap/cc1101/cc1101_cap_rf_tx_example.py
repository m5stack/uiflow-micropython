# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from cap import CC1101Cap
import time


label_title = None
label_status = None
label_seq = None
label_ok = None
label_fail = None
label_payload = None
cap_cc1101 = None


seq = None
last_tx_ms = None
ok_count = None
payload = None
fail_count = None
tx_ok = None


def setup():
    global \
        label_title, \
        label_status, \
        label_seq, \
        label_ok, \
        label_fail, \
        label_payload, \
        cap_cc1101, \
        seq, \
        last_tx_ms, \
        ok_count, \
        payload, \
        fail_count, \
        tx_ok

    M5.begin()
    Widgets.fillScreen(0x101418)
    label_title = Widgets.Label(
        "CC1101 TX", 76, 3, 1.0, 0x22D3A6, 0x101418, Widgets.FONTS.Montserrat18
    )
    label_status = Widgets.Label(
        "Auto TX every 1s", 5, 28, 1.0, 0x22D3A6, 0x101418, Widgets.FONTS.Montserrat16
    )
    label_seq = Widgets.Label("SEQ: 0", 5, 50, 1.0, 0xEAF2F8, 0x101418, Widgets.FONTS.Montserrat16)
    label_ok = Widgets.Label("OK: 0", 5, 72, 1.0, 0x22D3A6, 0x101418, Widgets.FONTS.Montserrat16)
    label_fail = Widgets.Label(
        "FAIL: 0", 120, 72, 1.0, 0xFF5C5C, 0x101418, Widgets.FONTS.Montserrat16
    )
    label_payload = Widgets.Label(
        "TX:", 5, 100, 1.0, 0xEAF2F8, 0x101418, Widgets.FONTS.Montserrat18
    )

    cap_cc1101 = CC1101Cap(868000, 2.4, 25.4, 58, 10, 64, 0x12, 0xAD)
    seq = 0
    ok_count = 0
    fail_count = 0
    last_tx_ms = 0
    Speaker.begin()
    Speaker.setVolumePercentage(0.5)
    label_status.setText(str("Auto TX every 1s"))
    label_seq.setText(str("SEQ: 0"))
    label_ok.setText(str("OK: 0"))
    label_fail.setText(str("FAIL: 0"))
    label_payload.setText(str("TX: "))
    Speaker.tone(3600, 40)
    time.sleep_ms(35)
    Speaker.tone(4800, 45)


def loop():
    global \
        label_title, \
        label_status, \
        label_seq, \
        label_ok, \
        label_fail, \
        label_payload, \
        cap_cc1101, \
        seq, \
        last_tx_ms, \
        ok_count, \
        payload, \
        fail_count, \
        tx_ok
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_tx_ms)) >= 1000:
        last_tx_ms = time.ticks_ms()
        payload = str((str("CC1101, SEQ=") + str(seq))) + str(", Hello")
        tx_ok = cap_cc1101.send(payload)
        if tx_ok:
            ok_count = (ok_count if isinstance(ok_count, (int, float)) else 0) + 1
            label_status.setText(str("TX OK"))
            Speaker.tone(3600, 25)
        else:
            fail_count = (fail_count if isinstance(fail_count, (int, float)) else 0) + 1
            label_status.setText(str("TX failed"))
            Speaker.tone(900, 100)
        label_payload.setText(str((str("TX: ") + str(payload))))
        seq = (seq if isinstance(seq, (int, float)) else 0) + 1
        label_seq.setText(str((str("SEQ: ") + str(seq))))
        label_ok.setText(str((str("OK: ") + str(ok_count))))
        label_fail.setText(str((str("FAIL: ") + str(fail_count))))


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
