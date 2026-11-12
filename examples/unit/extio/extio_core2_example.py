# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
# SPDX-License-Identifier: MIT
"""Read IO0 on a first-generation EXT.IO Unit connected to Core2 PORT.A."""

import time

import M5
from hardware import I2C, Pin
from unit import EXTIOUnit


extio = None


def setup():
    global extio
    M5.begin()
    i2c = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    if 0x27 not in i2c.scan():
        raise RuntimeError("EXT.IO not found at 0x27; check PORT.A and the Unit address")
    extio = EXTIOUnit(i2c, address=0x27)
    extio.set_port_mode(EXTIOUnit.IN)


def loop():
    M5.update()
    print("IO0:", extio.digit_read(0))
    time.sleep_ms(200)


if __name__ == "__main__":
    setup()
    while True:
        loop()
