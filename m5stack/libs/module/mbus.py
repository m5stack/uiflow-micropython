from machine import I2C, Pin
from M5 import getBoard, BOARD
from collections import namedtuple

MBusIO = namedtuple("MBusIO", ["sda0", "scl0", "sda1", "scl1"])

iomap = {
    BOARD.M5StackCore2: MBusIO(32, 33, 21, 22),
    BOARD.M5StackCoreS3: MBusIO(2, 1, 12, 11),
}.get(getBoard())


def _i2c0_init():
    return I2C(1, scl=Pin(iomap.scl0), sda=Pin(iomap.sda0), freq=100000)


def _i2c1_init():
    return I2C(1, scl=Pin(iomap.scl1), sda=Pin(iomap.sda1), freq=100000)


_attrs = {
    "i2c0": _i2c0_init,
    "i2c1": _i2c1_init,
}


def __getattr__(attr):
    value = _attrs.get(attr, None)
    if value is None:
        raise AttributeError(attr)
    o = value()
    globals()[attr] = o
    return o
