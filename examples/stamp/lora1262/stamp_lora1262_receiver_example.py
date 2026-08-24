# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import M5
from stamp import StampLoRa1262


radio = None


def receive_event(packet):
    print("received:", packet.decode())
    print("rssi:", packet.rssi, "snr:", packet.snr / 4)


def setup():
    global radio

    M5.begin()
    radio = StampLoRa1262()
    radio.set_irq_callback(receive_event)
    radio.start_recv()


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
