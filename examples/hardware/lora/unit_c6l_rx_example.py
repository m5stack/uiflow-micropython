# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import LoRa


title0 = None
label_rx = None
lora = None
lora_data = None
snr = None
rssi = None


def lora_receive_event(received_data):
    global title0, label_rx, lora, lora_data, snr, rssi
    lora_data = received_data
    label_rx.setText(str(lora_data.decode()))
    snr = (lora_data.snr) / 4
    rssi = lora_data.rssi
    print((str((str("SNR: ") + str(snr))) + str((str(" RSSI： ") + str(rssi)))))


def setup():
    global title0, label_rx, lora, lora_data, snr, rssi
    M5.begin()
    Widgets.fillScreen(0x000000)
    title0 = Widgets.Title("Rx", 3, 0x000000, 0xFFFFFF, Widgets.FONTS.DejaVu12)
    label_rx = Widgets.Label("label0", 2, 23, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu12)
    lora = LoRa(
        freq_khz=868000,
        bw="250",
        sf=8,
        coding_rate=8,
        preamble_len=12,
        syncword=0x12,
        output_power=10,
    )
    lora.set_irq_callback(lora_receive_event)
    lora.start_recv()


def loop():
    global title0, label_rx, lora, lora_data, snr, rssi
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
