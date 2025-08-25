# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
import M5
from collections import namedtuple

MBusIO = namedtuple(
    "MBusIO", ["sda0", "scl0", "sda1", "scl1", "spi_host", "spi_sck", "spi_mosi", "spi_miso"]
)

iomap = {
    M5.BOARD.M5Stack: MBusIO(
        sda0=21,
        scl0=22,
        sda1=21,
        scl1=22,
        spi_host=2,
        spi_sck=18,
        spi_mosi=23,
        spi_miso=19,  # SPI3_HOST
    ),
    M5.BOARD.M5StackCore2: MBusIO(
        sda0=32,
        scl0=33,
        sda1=21,
        scl1=22,
        spi_host=2,
        spi_sck=18,
        spi_mosi=23,
        spi_miso=38,  # SPI3_HOST
    ),
    M5.BOARD.M5StackCoreS3: MBusIO(
        sda0=2,
        scl0=1,
        sda1=12,
        scl1=11,
        spi_host=1,
        spi_sck=36,
        spi_mosi=37,
        spi_miso=35,  # SPI2_HOST
    ),
    M5.BOARD.M5Tough: MBusIO(
        sda0=32,
        scl0=33,
        sda1=21,
        scl1=22,
        spi_host=2,
        spi_sck=18,
        spi_mosi=23,
        spi_miso=38,  # SPI3_HOST
    ),
    M5.BOARD.M5Tab5: MBusIO(
        sda0=53,
        scl0=54,
        sda1=31,
        scl1=32,
        spi_host=1,
        spi_sck=5,
        spi_mosi=18,
        spi_miso=19,  # SPI2_HOST
    ),
}.get(M5.getBoard())


def _i2c0_init():
    return machine.I2C(0, scl=machine.Pin(iomap.scl0), sda=machine.Pin(iomap.sda0), freq=100000)


def _i2c1_init():
    if iomap.scl1 == iomap.scl0 and iomap.sda1 == iomap.sda0:
        return _i2c0_init()
    return machine.I2C(1, scl=machine.Pin(iomap.scl1), sda=machine.Pin(iomap.sda1), freq=100000)


def _spi_init():
    return machine.SPI(
        iomap.spi_host,
        sck=machine.Pin(iomap.spi_sck),
        mosi=machine.Pin(iomap.spi_mosi),
        miso=machine.Pin(iomap.spi_miso),
    )


_attrs = {
    "i2c0": _i2c0_init,
    "i2c1": _i2c1_init,
    "spi": _spi_init,
}


def __getattr__(attr):
    value = _attrs.get(attr, None)
    if value is None:
        raise AttributeError(attr)
    o = value()
    globals()[attr] = o
    return o
