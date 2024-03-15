# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import struct
import sys

if sys.platform != "esp32":
    from typing import Union

import time
import struct

ADS1115_ADDR = 0x49
EEPROM_ADDR = 0x53

RA_CONVERSION = 0x00
RA_CONFIG = 0x01

MODE_CONTINUOUS = 0x00
MODE_SINGLESHOT = 0x01

PGA_6144 = 0x00
PGA_4096 = 0x01
PGA_2048 = 0x02
PGA_1024 = 0x03
PGA_512 = 0x04
PGA_256 = 0x05

RATE_8 = 0x00
RATE_16 = 0x01
RATE_32 = 0x02
RATE_64 = 0x03
RATE_128 = 0x04
RATE_250 = 0x05
RATE_475 = 0x06
RATE_860 = 0x07

MV_6144 = 0.187500
MV_4096 = 0.125000
MV_2048 = 0.062500
MV_1024 = 0.031250
MV_512 = 0.015625
MV_256 = 0.007813

MEASURING_DIR = -1

VOLTAGE_DIVIDER_COEFFICIENT = 0.015918958

PAG_6144_CAL_ADDR = 208
PAG_4096_CAL_ADDR = 216
PAG_2048_CAL_ADDR = 224
PAG_1024_CAL_ADDR = 232
PAG_512_CAL_ADDR = 240
PAG_256_CAL_ADDR = 248

Resolution_list = {
    0: MV_6144 / VOLTAGE_DIVIDER_COEFFICIENT,
    1: MV_4096 / VOLTAGE_DIVIDER_COEFFICIENT,
    2: MV_2048 / VOLTAGE_DIVIDER_COEFFICIENT,
    3: MV_1024 / VOLTAGE_DIVIDER_COEFFICIENT,
    4: MV_512 / VOLTAGE_DIVIDER_COEFFICIENT,
    5: MV_256 / VOLTAGE_DIVIDER_COEFFICIENT,
}

PGA_EEPROM_Addr_list = {
    0: PAG_6144_CAL_ADDR,
    1: PAG_4096_CAL_ADDR,
    2: PAG_2048_CAL_ADDR,
    3: PAG_1024_CAL_ADDR,
    4: PAG_512_CAL_ADDR,
    5: PAG_256_CAL_ADDR,
}

Rate_list = {
    0: 1000 / 8,
    1: 1000 / 16,
    2: 1000 / 32,
    3: 1000 / 64,
    4: 1000 / 128,
    5: 1000 / 250,
    6: 1000 / 475,
    7: 1000 / 860,
}


class VMeterUnit:
    def __init__(self, i2c: Union[I2C, PAHUBUnit], ads_addr=ADS1115_ADDR):
        self.ads_i2c = i2c
        self.ads_i2c_addr = ads_addr
        if not (self.ads_i2c_addr in self.ads_i2c.scan()):
            raise UnitError("Vmeter unit maybe not connect")
        self.eeprom_i2c = i2c
        self.eeprom_i2c_addr = EEPROM_ADDR
        self._gain = PGA_2048
        self._rate = RATE_128
        self._mode = MODE_SINGLESHOT
        self._calibration_factor = 1
        self._resolution = Resolution_list[self._gain]
        self._cover_time = Rate_list[self._rate]
        self.calibration = True

    def set_gain(self, gain):
        buf = self.ads_i2c.readfrom_mem(self.ads_i2c_addr, RA_CONFIG, 2)
        config = struct.unpack(">h", buf)[0]
        config &= ~(0b0111 << 9)
        config |= gain << 9
        buf = struct.pack(">h", config)
        self.ads_i2c.writeto_mem(self.ads_i2c_addr, RA_CONFIG, buf)
        self._gain = gain
        self._resolution = Resolution_list[self._gain]
        expect, real = self.read_calibration(self._gain)
        self._calibration_factor = expect / real

    def get_gain(self):
        buf = self.ads_i2c.readfrom_mem(self.ads_i2c_addr, RA_CONFIG, 2)
        config = struct.unpack(">h", buf)[0]
        return (config & (0b0111 << 9)) >> 9

    def set_data_rate(self, rate):
        buf = self.ads_i2c.readfrom_mem(self.ads_i2c_addr, RA_CONFIG, 2)
        config = struct.unpack(">h", buf)[0]
        config &= ~(0b0111 << 5)
        config |= rate << 5
        buf = struct.pack(">h", config)
        self.ads_i2c.writeto_mem(self.ads_i2c_addr, RA_CONFIG, buf)
        self._rate = rate
        self._cover_time = Rate_list[self._rate]

    def get_data_rate(self):
        buf = self.ads_i2c.readfrom_mem(self.ads_i2c_addr, RA_CONFIG, 2)
        config = struct.unpack(">h", buf)[0]
        return (config & (0b0111 << 5)) >> 5

    def set_operation_mode(self, mode):
        buf = self.ads_i2c.readfrom_mem(self.ads_i2c_addr, RA_CONFIG, 2)
        config = struct.unpack(">h", buf)[0]
        config &= ~(0b0001 << 8)
        config |= mode << 8
        buf = struct.pack(">h", config)
        self.ads_i2c.writeto_mem(self.ads_i2c_addr, RA_CONFIG, buf)
        self._mode = mode

    def get_operation_mode(self):
        buf = self.ads_i2c.readfrom_mem(self.ads_i2c_addr, RA_CONFIG, 2)
        config = struct.unpack(">h", buf)[0]
        return (config & (0b0001 << 8)) >> 8

    def get_voltage(self):
        if self.calibration:
            return self._resolution * self._calibration_factor * self.conversion() * MEASURING_DIR
        else:
            return self._resolution * self.conversion() * MEASURING_DIR

    def get_adc_raw(self):
        return self.conversion()

    def conversion(self, timeout=125):
        if self._mode == MODE_SINGLESHOT:
            self.single_conversion()
            time.sleep_ms(int(self._cover_time))
            time_ms = time.ticks_ms() + timeout
            while time.ticks_ms() < time_ms and self.is_conversion():
                pass

        return self.adc_raw()

    def single_conversion(self):
        buf = self.ads_i2c.readfrom_mem(self.ads_i2c_addr, RA_CONFIG, 2)
        config = struct.unpack(">h", buf)[0]
        config &= ~(0b0001 << 15)
        config |= 0x01 << 15
        buf = struct.pack(">h", config)
        self.ads_i2c.writeto_mem(self.ads_i2c_addr, RA_CONFIG, buf)

    def is_conversion(self):
        buf = self.ads_i2c.readfrom_mem(self.ads_i2c_addr, RA_CONFIG, 2)
        result = struct.unpack(">h", buf)[0]
        if result & (1 << 15):
            return False
        else:
            return True

    def adc_raw(self):
        buf = self.ads_i2c.readfrom_mem(self.ads_i2c_addr, RA_CONVERSION, 2)
        return struct.unpack(">h", buf)[0]

    def eeprom_read(self, reg, num):
        return self.eeprom_i2c.readfrom_mem(self.eeprom_i2c_addr, reg, num)

    def eeprom_write(self, reg, data):
        buf = bytearray(data)
        self.eeprom_i2c.writeto_mem(self.eeprom_i2c_addr, reg, buf)

    def save_calibration(self, gain, expect, real):
        if expect == 0 and real == 0:
            return
        buf = [0] * 8
        buf[0] = gain
        buf[1] = expect >> 8
        buf[2] = expect & 0xFF
        buf[3] = real >> 8
        buf[4] = real & 0xFF

        for i in range(0, 5):
            buf[5] ^= buf[i]

        addr = PGA_EEPROM_Addr_list[gain]
        self.eeprom_write(addr, buf)

    def read_calibration(self, gain):
        expect = 1
        real = 1
        addr = PGA_EEPROM_Addr_list[gain]
        read_data = self.eeprom_read(addr, 8)
        crc = 0
        for i in range(0, 5):
            crc ^= read_data[i]

        if crc != read_data[5]:
            return expect, real

        expect = read_data[1] << 8 | read_data[2]
        real = read_data[3] << 8 | read_data[4]
        return expect, real
