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
label_counts = None
label_rssi = None
label_lqi = None
label_payload = None
cap_cc1101 = None


cc1101_data = None
rx_count = None
crc_count = None
last_rx_ms = None
last_anim_ms = None


def setup():
    global \
        label_title, \
        label_status, \
        label_counts, \
        label_rssi, \
        label_lqi, \
        label_payload, \
        cap_cc1101, \
        cc1101_data, \
        rx_count, \
        crc_count, \
        last_rx_ms, \
        last_anim_ms

    M5.begin()
    Widgets.fillScreen(0x101418)
    label_title = Widgets.Label(
        "CC1101 RX", 75, 3, 1.0, 0x22D3A6, 0x101418, Widgets.FONTS.Montserrat18
    )
    label_status = Widgets.Label(
        "Listening...", 5, 28, 1.0, 0x22D3A6, 0x101418, Widgets.FONTS.Montserrat16
    )
    label_counts = Widgets.Label(
        "RX:0 CRC:0", 5, 50, 1.0, 0xEAF2F8, 0x101418, Widgets.FONTS.Montserrat16
    )
    label_rssi = Widgets.Label(
        "RSSI: -", 5, 72, 1.0, 0xEAF2F8, 0x101418, Widgets.FONTS.Montserrat16
    )
    label_lqi = Widgets.Label(
        "LQI: -", 136, 72, 1.0, 0xEAF2F8, 0x101418, Widgets.FONTS.Montserrat16
    )
    label_payload = Widgets.Label(
        "RX:", 5, 100, 1.0, 0x22D3A6, 0x101418, Widgets.FONTS.Montserrat18
    )

    cap_cc1101 = CC1101Cap(868000, 2.4, 25.4, 58, 10, 64, 0x12, 0xAD)
    cap_cc1101.start_recv()
    rx_count = 0
    crc_count = 0
    last_rx_ms = time.ticks_ms()
    last_anim_ms = time.ticks_ms()
    Speaker.begin()
    Speaker.setVolumePercentage(0.5)
    label_status.setText(str("Listening..."))
    label_counts.setText(str("RX:0 CRC:0"))
    label_rssi.setText(str("RSSI: -"))
    label_lqi.setText(str("LQI: -"))
    label_payload.setText(str("RX: "))
    Speaker.tone(3600, 40)
    time.sleep_ms(35)
    Speaker.tone(4800, 45)


def loop():
    global \
        label_title, \
        label_status, \
        label_counts, \
        label_rssi, \
        label_lqi, \
        label_payload, \
        cap_cc1101, \
        cc1101_data, \
        rx_count, \
        crc_count, \
        last_rx_ms, \
        last_anim_ms
    M5.update()
    cc1101_data = cap_cc1101.recv(timeout_ms=0)
    if cc1101_data:
        if cc1101_data.crc_ok:
            last_rx_ms = time.ticks_ms()
            rx_count = (rx_count if isinstance(rx_count, (int, float)) else 0) + 1
            label_status.setText(str("Packet received"))
            label_counts.setText(
                str((str((str("RX:") + str(rx_count))) + str((str(" CRC:") + str(crc_count)))))
            )
            label_rssi.setText(str((str((str("RSSI: ") + str((cc1101_data.rssi)))) + str(" dBm"))))
            label_lqi.setText(str((str("LQI: ") + str((cc1101_data.lqi)))))
            label_payload.setText(str((str("RX:") + str(((cc1101_data.data).decode())))))
            Speaker.tone(5200, 35)
            cap_cc1101.start_recv()
        else:
            crc_count = (crc_count if isinstance(crc_count, (int, float)) else 0) + 1
            label_status.setText(str("CRC error"))
            label_counts.setText(
                str((str((str("RX:") + str(rx_count))) + str((str(" CRC:") + str(crc_count)))))
            )
            Speaker.tone(900, 100)
            cap_cc1101.start_recv()
    else:
        if (time.ticks_diff((time.ticks_ms()), last_anim_ms)) >= 1000:
            last_anim_ms = time.ticks_ms()
            label_status.setText(str("Listening..."))


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
