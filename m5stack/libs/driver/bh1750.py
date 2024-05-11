# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from micropython import const
from struct import unpack_from
import time

# I2C addresses (without R/W bit)
_BH1750_DEFAULT_ADDRESS = const(0x23)  # I2C address with ADDR pin low


class Power:
    POWER_DOWN = const(0b00000000)
    POWER_ON = const(0b00000001)
    RESET = const(0b00000111)


class BH1750:
    CONTINUOUSLY = 0b00010000
    ONE_TIME = 0b00100000

    H_RESOLUTION_MODE = 0b00000000
    H_RESOLUTION_MODE2 = 0b00000001
    L_RESOLUTION_MODE = 0b00000011

    _CONV_FACTOR = 1.2

    def __init__(self, i2c, address: int = _BH1750_DEFAULT_ADDRESS) -> None:
        self._i2c = i2c
        self._addr = address

        self._mode = self.CONTINUOUSLY
        self._resolution = self.H_RESOLUTION_MODE
        self._sensitivity = 1.0  # default
        self._interval = 0
        self._BUFFER = memoryview(bytearray(2))

        self._configure()
        self._last_time = time.ticks_ms()

    def get_lux(self) -> float:
        self._ready()
        raw_lux = self._read_u16()
        return self._convert_to_lux(raw_lux)

    def configure(self, mode, resolution):
        self._mode = mode
        self._resolution = resolution
        self._configure()

    def get_sensitivity(self) -> float:
        return self._sensitivity

    def set_sensitivity(self, sensitivity) -> None:
        self._sensitivity = sensitivity
        mt_reg = int(69 * sensitivity)
        self._write_byte((0b01000 << 3) | (mt_reg >> 5))
        self._write_byte((0b011 << 5) | (mt_reg & 0b11111))
        self._configure()

    def _configure(self) -> None:
        self._write_byte(self._mode | self._resolution)
        self._cal_interval()
        time.sleep_ms(self._interval)

    def _write_byte(self, byte) -> None:
        self._BUFFER[0] = byte & 0xFF
        self._i2c.writeto(self._addr, self._BUFFER[0:1])

    def _read_u16(self) -> int:
        self._i2c.readfrom_into(self._addr, self._BUFFER)
        return unpack_from(">H", self._BUFFER)[0]

    def _convert_to_lux(self, raw_lux: int) -> float:
        measured_lux = raw_lux / self._CONV_FACTOR
        measured_lux *= 1 / self._sensitivity
        if self._resolution == self.H_RESOLUTION_MODE2:
            measured_lux = measured_lux / 2
        return measured_lux

    def _ready(self):
        if time.ticks_ms() - self._last_time > self._interval:
            return
        time.sleep_ms(self._interval - time.ticks_ms() - self._last_time)

    def _cal_interval(self):
        if self._resolution == self.L_RESOLUTION_MODE:
            self._interval = int(24 * 1 / self._sensitivity)
        else:
            self._interval = int(180 * 1 / self._sensitivity)
