# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time

import M5
from stamp import StampLoRa1262


radio = None
sequence = None


def setup():
    global radio, sequence

    M5.begin()
    radio = StampLoRa1262()
    sequence = 0


def loop():
    global radio, sequence

    M5.update()
    message = "Stamp LoRa1262 %d" % sequence
    radio.send(message)
    print("sent:", message)
    sequence = (sequence + 1) & 0xFF
    time.sleep_ms(1000)


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
