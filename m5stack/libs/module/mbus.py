# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C, Pin, SPI
import M5
from collections import namedtuple

MBusIO = namedtuple(
    "MBusIO", ["sda0", "scl0", "sda1", "scl1", "spi2_sck", "spi2_mosi", "spi2_miso"]
)

iomap = {
    M5.BOARD.M5Stack: MBusIO(2, 5, 21, 22, 18, 23, 19),
    M5.BOARD.M5StackCore2: MBusIO(32, 33, 21, 22, 18, 23, 38),
    M5.BOARD.M5StackCoreS3: MBusIO(2, 1, 12, 11, 36, 37, 35),
    M5.BOARD.M5Tough: MBusIO(32, 33, 21, 22, 18, 23, 38),
}.get(M5.getBoard())


def _i2c0_init():
    return I2C(0, scl=Pin(iomap.scl0), sda=Pin(iomap.sda0), freq=100000)


def _i2c1_init():
    return I2C(1, scl=Pin(iomap.scl1), sda=Pin(iomap.sda1), freq=100000)


def _spi2_init():
    return SPI(1, sck=Pin(iomap.spi2_sck), mosi=Pin(iomap.spi2_mosi), miso=Pin(iomap.spi2_miso))


_attrs = {
    "i2c0": _i2c0_init,
    "i2c1": _i2c1_init,
    "spi2": _spi2_init,
}


def __getattr__(attr):
    value = _attrs.get(attr, None)
    if value is None:
        raise AttributeError(attr)
    o = value()
    globals()[attr] = o
    return o
