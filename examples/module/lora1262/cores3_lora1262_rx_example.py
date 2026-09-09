# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time

import M5
from M5 import Widgets
from module import LoRa1262Module


title0 = None
label_r = None
label_rx = None
label_t = None
label_time = None
label_rssi = None
label_snr = None
label_rssi_v = None
label_snr_v = None
lora1262_0 = None
lora1262_data = None
rssi = None
snr = None


def lora1262_0_receive_event(received_data):
    global label_rx, label_time, label_rssi_v, label_snr_v
    global lora1262_data, rssi, snr

    lora1262_data = received_data
    label_rx.setText(str(lora1262_data.decode()))
    rssi = lora1262_data.rssi
    snr = lora1262_data.snr / 4
    label_rssi_v.setText(str(rssi))
    label_snr_v.setText(str(snr))
    label_time.setText(str(time.ticks_ms()))


def setup():
    global title0, label_r, label_rx, label_t, label_time
    global label_rssi, label_snr, label_rssi_v, label_snr_v, lora1262_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("LoRa1262 Module Rx", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label_r = Widgets.Label("Recv:", 5, 50, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_rx = Widgets.Label(" ", 65, 50, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_rssi = Widgets.Label("RSSI:", 5, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_rssi_v = Widgets.Label(" ", 65, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_snr = Widgets.Label("SNR:", 5, 108, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_snr_v = Widgets.Label(" ", 65, 108, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_t = Widgets.Label("timestamp:", 5, 150, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_time = Widgets.Label("1", 118, 150, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    lora1262_0 = LoRa1262Module()
    lora1262_0.set_rx_callback(lora1262_0_receive_event)
    lora1262_0.start_recv()


def loop():
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
