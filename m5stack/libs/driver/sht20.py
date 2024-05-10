# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
# SPDX-FileCopyrightText: Copyright (c) 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
"""
`sht20`
================================================================================

MicroPython Driver for the Sensirion SHT20 Temperature Sensor


* Author(s): Jose D. Montoya


"""

import time
import struct
from micropython import const


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/MicroPython_SHT20.git"

_SOFTRESET = const(0xFE)
_TEMPERATURE = const(0xF3)
_HUMIDITY = const(0xF5)
_READ_USER1 = const(0xE7)
_WRITE_USER1 = const(0xE6)
_TEMP_RH_RES = (0, 1, 128, 129)


class SHT20:
    """Driver for the SHT20 Sensor connected over I2C.

    :param ~machine.I2C i2c: The I2C bus the SHT20 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x40`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`SHT20` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        from machine import Pin, I2C
        from micropython_sht20 import sht20

    Once this is done you can define your `machine.I2C` object and define your sensor object

    .. code-block:: python

        i2c = I2C(1, sda=Pin(2), scl=Pin(3))
        sht20 = sht20.SHT20(i2c)

    Now you have access to the attributes

    .. code-block:: python

        temperature = sht20.temperature
        humidity = sht20.humidity

    """

    def __init__(self, i2c, address: int = 0x40) -> None:
        self._i2c = i2c
        self._address = address

    def reset(self) -> None:
        """Perform a soft reset of the sensor, resetting all settings to their power-on defaults"""
        self._i2c.writeto(self._address, bytes([_SOFTRESET]))
        time.sleep(0.015)

    @property
    def temperature(self) -> float:
        """The measured temperature in Celsius."""
        self._i2c.writeto(self._address, bytes([_TEMPERATURE]))
        data = bytearray(3)
        while True:
            # While busy, the sensor doesn't respond to reads.
            try:
                self._i2c.readfrom_into(self._address, data)
                if data[0] != 0xFF:  # Check if read succeeded.
                    break
            except OSError:
                pass
        value, checksum = struct.unpack(">HB", data)

        if checksum != self._crc(data[:2]):
            raise ValueError("CRC mismatch")

        time.sleep(0.050)

        return value * 175.72 / 65536.0 - 46.85

    @property
    def humidity(self) -> float:
        """The measured relative humidity in percent."""
        self._i2c.writeto(self._address, bytes([_HUMIDITY]))
        data = bytearray(3)
        while True:
            try:
                self._i2c.readfrom_into(self._address, data)
                if data[0] != 0xFF:
                    break
            except OSError:
                pass
        value, checksum = struct.unpack(">HB", data)

        if checksum != self._crc(data[:2]):
            raise ValueError("CRC mismatch")

        time.sleep(0.016)

        return value * 125.0 / 65536.0 - 6.0

    @property
    def temp_rh_resolution(self) -> str:
        """The temperature and relative humidity resolution

        Have one of the following values: [#f1]_

            =======  ==============  ==============
             value       RH res %        T res C
            =======  ==============  ==============
               0      0.04 (12bit)    0.01 (14bit)
               1      0.7  (8bit)     0.04 (12bit)
               2      0.17 (10bit)    0.02 (13bit)
               3      0.08 (11bit)    0.08 (11bit)
            =======  ==============  ==============


        .. [#f1] HTU21D(F) RH/T Sensor IC Datasheet. TE connectivity. 2017. p13

        """
        data = bytearray(1)
        values = {
            0x00: "RH=0.04, T=0.01",
            0x01: "RH=0.7, T=0.04",
            0x80: "RH=0.17, T=0.02",
            0x81: "RH=0.08, T=0.08",
        }

        self._i2c.writeto(self._address, bytes([_READ_USER1]))
        self._i2c.readfrom_into(self._address, data)
        res = data[0] & 0x81

        return values[res]

    @temp_rh_resolution.setter
    def temp_rh_resolution(self, val: int) -> None:
        if val not in _TEMP_RH_RES:
            raise ValueError("Temp/Humidity Resolution must be a valid option")
        data = bytearray(1)
        self._i2c.writeto(self._address, bytes([_READ_USER1]))
        self._i2c.readfrom_into(self._address, data)
        reg = data[0] & ~0x81
        reg |= val
        self._i2c.writeto(self._address, bytes([_WRITE_USER1, reg]))

    @staticmethod
    def _crc(data: bytearray) -> int:
        crc = 0
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc <<= 1
                    crc ^= 0x131
                else:
                    crc <<= 1
        return crc
