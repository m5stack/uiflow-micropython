# Copyright (c) 2022 Sebastian Wicki
# SPDX-FileCopyrightText: Copyright (c) 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
"""
I2C-based driver for the BH1750FVI ambient light sensor.
"""

from micropython import const
from time import sleep_ms

I2C_DEFAULT_ADDR = const(0x23)

_BH1750FVI_POWER_DOWN = const(0b0000_0000)

_BH1750FVI_MTREG_DEFAULT = const(69)
_BH1750FVI_MTREG_SET_HI = const(0b01000_000)
_BH1750FVI_MTREG_SET_HI_SHIFT = const(5)
_BH1750FVI_MTREG_SET_LO = const(0b011_00000)
_BH1750FVI_MTREG_SET_LO_MASK = const(0b11111)

_BH1750FVI_THR_MAX_MS = const(180.0)
_BH1750FVI_TLR_MAX_MS = const(24.0)
_BH1750FVI_LX_PER_COUNT = const(1.2)

MODE_CONTINUOUS = const(0b0001)
MODE_ONE_SHOT = const(0b0010)

RESOLUTION_HIGH = const(0b0000)
RESOLUTION_HIGH2 = const(0b0001)
RESOLUTION_LOW = const(0b0011)


class BH1750FVI:
    def __init__(
        self, i2c, addr=I2C_DEFAULT_ADDR, *, mode=MODE_CONTINUOUS, resolution=RESOLUTION_HIGH
    ):
        self.i2c = i2c
        self.addr = addr
        self.running = False
        if mode != MODE_CONTINUOUS and mode != MODE_ONE_SHOT:
            raise ValueError("invalid argument(s) value")
        self.mode = mode
        if (
            resolution != RESOLUTION_HIGH
            and resolution != RESOLUTION_HIGH2
            and resolution != RESOLUTION_LOW
        ):
            raise ValueError("invalid argument(s) value")
        self.resolution = resolution
        self.reset()
        self.sensitivity(1.0)

    def reset(self):
        cmd = bytearray(1)
        cmd[0] = _BH1750FVI_POWER_DOWN
        self.i2c.writeto(self.addr, cmd)

    def sensitivity(self, factor=None):
        """
        Sets or gets the sensitivity of the sensor. This is floating point value
        between 0.35 and 3.68 (inclusive). A higher sensitivity value increases
        the resolution, but also the measurement duration time.
        """
        if factor is None:
            return self.factor
        if factor < 0.35 or factor > 3.68:
            raise ValueError("invalid argument(s) value")

        cmd = bytearray(1)
        mtreg = round(factor * _BH1750FVI_MTREG_DEFAULT)
        cmd[0] = _BH1750FVI_MTREG_SET_HI | (mtreg >> _BH1750FVI_MTREG_SET_HI_SHIFT)
        self.i2c.writeto(self.addr, cmd)
        cmd[0] = _BH1750FVI_MTREG_SET_LO | (mtreg & _BH1750FVI_MTREG_SET_LO_MASK)
        self.i2c.writeto(self.addr, cmd)

        self.factor = factor

    def measure(self):
        """
        Returns the ambient light (in lx)
        """
        cmd = bytearray(1)
        cmd[0] = (self.mode << 4) | self.resolution
        self.i2c.writeto(self.addr, cmd)
        # wait for the measurement to be taken
        if self.mode == MODE_ONE_SHOT or not self.running:
            if self.resolution == RESOLUTION_LOW:
                sleep_ms(round(_BH1750FVI_TLR_MAX_MS * self.factor))
            else:
                sleep_ms(round(_BH1750FVI_THR_MAX_MS * self.factor))
            self.running = True
        b = self.i2c.readfrom(self.addr, 2)
        val = (b[0] << 8) | b[1]
        if self.resolution == RESOLUTION_HIGH2:
            val /= 2

        return val / (self.factor * _BH1750FVI_LX_PER_COUNT)
