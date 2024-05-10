# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
from micropython import const
import struct
import time

ADDRESS = const(0x48)

MODE_CONTIN = const(0x00)
MODE_SINGLE = const(0x10)

SPS_240 = const(0x00)
SPS_60 = const(0x04)
SPS_30 = const(0x08)
SPS_15 = const(0x0C)
SPS_MASK = const(0x0C)

GAIN_ONE = const(0x00)
GAIN_TWO = const(0x01)
GAIN_FOUR = const(0x02)
GAIN_EIGHT = const(0x03)
GAIN_MASK = const(0x03)

NO_EFFECT = const(0x00)
START = const(0x80)


class ADS1110:
    def __init__(self, i2c: I2C, address: int = ADDRESS) -> None:
        self._i2c = i2c
        self._i2c_addr = address
        self.start = NO_EFFECT
        self.mode = MODE_CONTIN
        self.rate = SPS_15
        self.gain = GAIN_ONE
        self.mini_code = {SPS_15: 16, SPS_30: 15, SPS_60: 14, SPS_240: 12}
        self.gain_code = {GAIN_ONE: 1, GAIN_TWO: 2, GAIN_FOUR: 4, GAIN_EIGHT: 8}

    def set_gain(self, gain):
        """
        GA1 GA0 GAIN
        0   0   1
        0   1   2
        1   0   4
        1   1   8
        """
        self.gain = gain
        self.set_config()

    def set_sample_rate(self, rate):
        """
        DR1 DR0 DATARATE
        0   0   240SPS
        0   1   60SPS
        1   0   30SPS
        1   1   15SPS
        """
        self.rate = rate
        self.set_config()

    def set_mode(self, mode):
        """
        SC  MODE
        0   CONTINUOUS
        1   SINGLE
        """
        self.mode = mode
        self.set_config()

    def start_single_conversion(self):
        """
        ST/DRDY
        0   NO EFFECT
        1   START CONVERSION
        """
        self.start = START
        self.set_config()
        self.start = NO_EFFECT

    def set_config(self):
        """
        7   6   5   4   3   2   1   0
        S/D 0   0   SC  DR1 DR0 GA1 GA0
        x   0   0   x   x   x   x   x
        """
        value = 0x00
        value |= self.gain | self.rate | self.mode | self.start
        self._i2c.writeto(self._i2c_addr, bytearray([value]))

    def get_adc_raw_value(self):
        buf = bytearray(2)
        self._i2c.readfrom_into(self._i2c_addr, buf)
        return struct.unpack(">h", buf)[0]
