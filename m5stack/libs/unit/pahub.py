# -*- encoding: utf-8 -*-
from machine import I2C
from micropython import const

try:
    from typing import overload, Sequence
    from typing_extensions import Literal
    from uio import AnyReadableBuf, AnyWritableBuf
except ImportError:
    pass

PAHUB_CHN0 = const(0)
PAHUB_CHN1 = const(1)
PAHUB_CHN2 = const(2)
PAHUB_CHN3 = const(3)
PAHUB_CHN4 = const(4)
PAHUB_CHN5 = const(5)

PAHUB_DEFAULT_ADDR = const(0x70)


class PAHUB:
    _i2c = None
    _chn = -1
    _addr = PAHUB_DEFAULT_ADDR

    def __init__(
        self, i2c: I2C, channel: Literal[0, 1, 2, 3, 4, 5] = 0, address=PAHUB_DEFAULT_ADDR
    ) -> None:
        self._i2c = i2c
        self._chn = channel
        self._addr = address

    def select_channel(self, channel: int) -> None:
        buf = bytearray(1)
        buf[0] = self._i2c.readfrom(self._addr, 1)[0] | (1 << channel)
        self._i2c.writeto(self._addr, buf)

    def release_channel(self, channel: int) -> None:
        buf = bytearray(1)
        buf[0] = self._i2c.readfrom(self._addr, 1)[0] & (~(1 << channel))
        self._i2c.writeto(self._addr, buf)

    def deinit(self) -> None:
        self.release_channel(self._chn)

    def scan(self) -> list[int]:
        self.select_channel(self._chn)
        result = self._i2c.scan()
        self.release_channel(self._chn)
        return result

    def start(self) -> None:
        self.select_channel(self._chn)
        self._i2c.start()
        self.release_channel(self._chn)

    def stop(self) -> None:
        self.select_channel(self._chn)
        self._i2c.stop()
        self.release_channel(self._chn)

    def readinto(self, buf: AnyWritableBuf, nack: bool = True) -> None:
        self.select_channel(self._chn)
        self._i2c.readinto(buf, nack)
        self.release_channel(self._chn)

    def write(self, buf: AnyReadableBuf) -> int:
        self.select_channel(self._chn)
        result = self._i2c.write(buf)
        self.release_channel(self._chn)
        return result

    def readfrom(self, addr: int, nbytes: int, stop: bool = True) -> bytes:
        self.select_channel(self._chn)
        result = self._i2c.readfrom(addr, nbytes, stop)
        self.release_channel(self._chn)
        return result

    def readfrom_into(self, addr: int, buf: AnyWritableBuf, stop: bool = True) -> None:
        self.select_channel(self._chn)
        self._i2c.readfrom_into(addr, buf, stop)
        self.release_channel(self._chn)

    def writeto(self, addr: int, buf: AnyReadableBuf, stop: bool = True) -> int:
        self.select_channel(self._chn)
        result = self._i2c.writeto(addr, buf, stop)
        self.release_channel(self._chn)
        return result

    def writevto(self, addr: int, vector: Sequence[AnyReadableBuf], stop: bool = True) -> int:
        self.select_channel(self._chn)
        result = self._i2c.writevto(addr, vector, stop)
        self.release_channel(self._chn)
        return result

    def readfrom_mem(self, addr: int, memaddr: int, nbytes: int) -> bytes:
        self.select_channel(self._chn)
        result = self._i2c.readfrom_mem(addr, memaddr, nbytes)
        self.release_channel(self._chn)
        return result

    def readfrom_mem_into(self, addr: int, memaddr: int, buf: AnyWritableBuf) -> None:
        self.select_channel(self._chn)
        self._i2c.readfrom_mem_into(addr, memaddr, buf)
        self.release_channel(self._chn)

    def writeto_mem(self, addr: int, memaddr: int, buf: AnyReadableBuf) -> None:
        self.select_channel(self._chn)
        self._i2c.writeto_mem(addr, memaddr, buf)
        self.release_channel(self._chn)
