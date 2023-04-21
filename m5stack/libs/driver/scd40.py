# Copyright (c) 2023 Sebastian Wicki
# SPDX-License-Identifier: MIT
"""
I2C-based driver for the SCD40 CO2 sensor.
"""
from micropython import const
from ustruct import pack, pack_into, unpack_from
from uasyncio import Event, create_task, sleep_ms

from checksum import crc8

I2C_DEFAULT_ADDR = const(0x62)


_SCD40_CMD_START_MEASUREMENT = const(0x21B1)
_SCD40_CMD_READ_MEASUREMENT = const(0xEC05)
_SCD40_CMD_STOP_MEASUREMENT = const(0x3F86)
_SCD40_CMD_DATA_READY_STATUS = const(0xE4B8)
_SCD40_CMD_DATA_READY_STATUS_MASK = const(0x07FF)

_SCD40_CMD_SET_TEMPERATURE_OFFSET = const(0x241D)
_SCD40_CMD_SET_AMBIENT_PRESSURE = const(0xE000)

_SCD40_CMD_REINIT = const(0x3646)

_SCD40_FRAME_LEN = const(3)
_SCD40_DATA_LEN = const(2)
_SCD40_CMD_LEN = const(2)


class SCD40:
    def __init__(self, i2c, *, addr=I2C_DEFAULT_ADDR, temp_offset=None):
        self.i2c = i2c
        self.addr = addr

        self.init_done = Event()
        self.loop = None

        self.temp_offset = temp_offset
        self.pressure = None
        self.co2 = 0
        self.t = 0.0
        self.rh = 0.0

    async def start(self):
        # this re-initializes the sensor from eeprom to ensure idle mode
        await self._write_values(_SCD40_CMD_STOP_MEASUREMENT, delay_ms=500)
        await self._write_values(_SCD40_CMD_REINIT, delay_ms=1000)
        # temperature offset can only be configured in idle mode
        if self.temp_offset is not None:
            t = int((self.temp_offset * 2 ** 16) / 175)
            await self._write_values(_SCD40_CMD_SET_TEMPERATURE_OFFSET, (t,))

        # create background task and wait for measurements to arrive
        self.loop = create_task(self._loop())
        await self.init_done.wait()

    async def _ready(self):
        (ready,) = await self._read_values(_SCD40_CMD_DATA_READY_STATUS, 1)
        return (ready & _SCD40_CMD_DATA_READY_STATUS_MASK) != 0

    async def _loop(self):
        await self._write_values(_SCD40_CMD_START_MEASUREMENT)
        while True:
            ready = False
            while not ready:
                # adjust pressure if it was updated via set_ambient_pressure
                if self.pressure is not None:
                    await self._write_values(
                        _SCD40_CMD_SET_AMBIENT_PRESSURE, (int(self.pressure / 100),)
                    )
                    self.pressure = None

                await sleep_ms(625)
                ready = await self._ready()

            co2, t_raw, rh_raw = await self._read_values(_SCD40_CMD_READ_MEASUREMENT, 3)
            self.co2 = co2
            self.t = -45 + ((t_raw * 175) / 0xFFFF)
            self.rh = (rh_raw * 100) / 0xFFFF

            self.init_done.set()

    def stop(self):
        if self.loop is not None:
            self.loop.cancel()
            self.loop = None

    def set_ambient_pressure(self, pressure):
        """
        Sets the ambient pressure (in Pa) and enables pressure compensation
        """
        self.pressure = pressure

    def measure(self):
        """
        Returns the measured CO2 (in ppm), temperature (in °C), and relative
        humidity (in %) as a 3-tuple in the form of

        (co2, temperature, humidity)
        """
        if self.loop is None:
            raise RuntimeError("device not ready")
        return self.co2, self.t, self.rh

    async def _read_values(self, cmd, nvalues, delay_ms=1):
        self.i2c.writeto(self.addr, pack(">H", cmd), False)
        await sleep_ms(delay_ms)

        buf = memoryview(bytearray(nvalues * _SCD40_FRAME_LEN))
        self.i2c.readfrom_into(self.addr, buf, True)

        offset = 0
        values = []
        for _ in range(nvalues):
            value, crc = unpack_from(">HB", buf, offset)
            if crc != crc8(buf[offset : offset + _SCD40_DATA_LEN]):
                raise Exception("checksum error")
            values.append(value)
            offset += _SCD40_FRAME_LEN

        return values

    async def _write_values(self, cmd, values=(), *, delay_ms=1):
        nvalues = len(values)
        buf = memoryview(bytearray(_SCD40_CMD_LEN + nvalues * _SCD40_FRAME_LEN))

        pack_into(">H", buf, 0, cmd)
        offset = _SCD40_CMD_LEN

        for value in values:
            pack_into(">H", buf, offset, value)

            offset_crc = offset + _SCD40_DATA_LEN
            crc = crc8(buf[offset:offset_crc])
            pack_into("b", buf, offset_crc, crc)

            offset += _SCD40_FRAME_LEN

        self.i2c.writeto(self.addr, buf, True)
        await sleep_ms(delay_ms)
