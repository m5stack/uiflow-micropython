# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import LoRa868V12Module
import time


title0 = None
label_r = None
label_rx = None
label_t = None
label_time = None
label_rssi = None
label_snr = None
label_rssi_v = None
label_snr_v = None
lora868v12_0 = None
lora868v12_data = None
rssi = None
snr = None
last_time = None


def lora868v12_0_receive_event(received_data):
    global \
        title0, \
        label_r, \
        label_rx, \
        label_t, \
        label_time, \
        label_rssi, \
        label_snr, \
        label_rssi_v, \
        label_snr_v, \
        lora868v12_0, \
        lora868v12_data, \
        rssi, \
        snr, \
        last_time
    lora868v12_data = received_data
    label_rx.setText(str(lora868v12_data.decode()))
    rssi = lora868v12_data.rssi
    snr = (lora868v12_data.snr) / 4
    label_rssi_v.setText(str(rssi))
    label_snr_v.setText(str(snr))


def setup():
    global \
        title0, \
        label_r, \
        label_rx, \
        label_t, \
        label_time, \
        label_rssi, \
        label_snr, \
        label_rssi_v, \
        label_snr_v, \
        lora868v12_0, \
        lora868v12_data, \
        rssi, \
        snr, \
        last_time

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("LoRa Module Rx", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label_r = Widgets.Label("Recv:", 5, 50, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_rx = Widgets.Label(" ", 65, 50, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_t = Widgets.Label("timestamp:", 5, 150, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_time = Widgets.Label("1", 118, 150, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_rssi = Widgets.Label("RSSI: ", 5, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_snr = Widgets.Label("SNR: ", 5, 108, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_rssi_v = Widgets.Label(" ", 65, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_snr_v = Widgets.Label(" ", 65, 108, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    lora868v12_0 = LoRa868V12Module(
        pin_rst=5,
        pin_cs=1,
        pin_irq=10,
        pin_busy=2,
        freq_khz=868000,
        bw="250",
        sf=8,
        coding_rate=8,
        preamble_len=12,
        syncword=0x12,
        output_power=10,
    )
    lora868v12_0.set_irq_callback(lora868v12_0_receive_event)
    lora868v12_0.start_recv()
    last_time = time.ticks_ms()


def loop():
    global \
        title0, \
        label_r, \
        label_rx, \
        label_t, \
        label_time, \
        label_rssi, \
        label_snr, \
        label_rssi_v, \
        label_snr_v, \
        lora868v12_0, \
        lora868v12_data, \
        rssi, \
        snr, \
        last_time
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 1000:
        last_time = time.ticks_ms()
        label_time.setText(str(last_time))


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
