# Copyright (c) 2022 Sebastian Wicki
# SPDX-License-Identifier: MIT
"""
I2C-based driver for the SGP30 air quality sensor.
"""
from math import exp
from micropython import const
from ustruct import pack, pack_into, unpack_from
from time import ticks_diff, ticks_ms
from uasyncio import create_task, sleep_ms

from checksum import crc8

I2C_DEFAULT_ADDR = const(0x58)

_SGP30_CMD_INIT = const(0x2003)
_SGP30_CMD_MEASURE = const(0x2008)
_SGP30_CMD_FEATURE_SET = const(0x202F)
_SGP30_CMD_READ_BASELINE = const(0x2015)
_SGP30_CMD_WRITE_BASELINE = const(0x201E)
_SGP30_CMD_WRITE_ABS_HUMIDITY = const(0x2061)

_SGP30_FEATURE_SET = const(0x0022)

_SGP30_FRAME_LEN = const(3)
_SGP30_DATA_LEN = const(2)
_SGP30_CMD_LEN = const(2)


def absolute_humidity(t, rh):
    """
    Returns the absolute humidity from the relative humidity and temperature.
    This value may be passed to SGP30.set_absolute_humidity for the on-chip
    humidity compensation.

    t is the temperature in °C
    rh is the relative humidity in percent (0-100)
    """
    return 216.7 * ((rh / 100.0) * 6.112 * exp((17.62 * t) / (243.12 + t)) / (273.15 + t))


class SGP30:
    def __init__(self, i2c, *, addr=I2C_DEFAULT_ADDR):
        self.i2c = i2c
        self.addr = addr
        self.eco2 = 400
        self.tvoc = 0

    async def start(self, baseline=None):
        feature_set = await self._read_values(_SGP30_CMD_FEATURE_SET, 1, delay_ms=10)
        if feature_set[0] != _SGP30_FEATURE_SET:
            raise ValueError("device not found")
        self._write_values(_SGP30_CMD_INIT)
        if baseline is not None:
            if isinstance(baseline, tuple) and len(baseline) == 2:
                self._write_values(_SGP30_CMD_WRITE_BASELINE, baseline)
            else:
                raise ValueError("invalid argument(s) value")
        self.loop = create_task(self._loop())

    async def baseline(self):
        """
        Gets the baseline as a 2-tuple. This can be passed to the constructor
        as the baseline value.
        """
        v = await self._read_values(_SGP30_CMD_READ_BASELINE, 2, delay_ms=10)
        return tuple(v)

    async def _loop(self):
        # A sgp30_measure_iaq command has to be sent in regular intervals
        # of 1s to ensure proper operation of the dynamic baseline compensation
        # algorithm
        while True:
            start = ticks_ms()
            self.eco2, self.tvoc = await self._read_values(_SGP30_CMD_MEASURE, 2, delay_ms=12)
            end = ticks_ms()
            await sleep_ms(1000 - ticks_diff(end, start))

    def set_absolute_humidity(self, ah):
        """
        Sets the absolute humidity for the on-chip compensation. The ah value
        must represent the absolute humidity in g/m³
        """
        val = int(ah * 256)
        if not 0x0001 <= val <= 0xFFFF:
            raise ValueError("value out of range")
        self._write_values(_SGP30_CMD_WRITE_ABS_HUMIDITY, (val,))

    def measure(self):
        """
        Returns the measured CO2-equivalent (in ppm) and TVOC (in ppb) in the
        form of

        (eco2, tvoc)
        """
        if self.loop is None:
            raise RuntimeError("device not ready")
        return self.eco2, self.tvoc

    def stop(self):
        if self.loop is not None:
            self.loop.cancel()
            self.loop = None

    async def _read_values(self, cmd, nvalues, delay_ms=1):
        self.i2c.writeto(self.addr, pack(">H", cmd), False)
        await sleep_ms(delay_ms)

        buf = memoryview(bytearray(nvalues * _SGP30_FRAME_LEN))
        self.i2c.readfrom_into(self.addr, buf, True)

        offset = 0
        values = []
        for _ in range(nvalues):
            value, crc = unpack_from(">HB", buf, offset)
            if crc != crc8(buf[offset : offset + _SGP30_DATA_LEN]):
                raise Exception("checksum error")
            values.append(value)
            offset += _SGP30_FRAME_LEN

        return values

    def _write_values(self, cmd, values=()):
        nvalues = len(values)
        buf = memoryview(bytearray(_SGP30_CMD_LEN + nvalues * _SGP30_FRAME_LEN))

        pack_into(">H", buf, 0, cmd)
        offset = _SGP30_CMD_LEN

        for value in values:
            pack_into(">H", buf, offset, value)

            offset_crc = offset + _SGP30_DATA_LEN
            crc = crc8(buf[offset:offset_crc])
            pack_into("b", buf, offset_crc, crc)

            offset += _SGP30_FRAME_LEN

        self.i2c.writeto(self.addr, buf, True)
