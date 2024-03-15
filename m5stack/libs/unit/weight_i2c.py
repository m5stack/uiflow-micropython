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

WEIGHT_I2C_ADDR = 0x26

ADC_REG = 0x00
WEIGHT_REG = 0x10
GAP_REG = 0x40
OFFSET_REG = 0x50
WEIGHT_X100_REG = 0x60
WEIGHT_STR_REG = 0x70
FILTER_IP_REG = 0x80
FILTER_AVG_REG = 0x81
FILTER_EMA_REG = 0x82
FW_VER_REG = 0xFE
I2C_ADDR_REG = 0xFF


class WEIGHT_I2CUnit:
    def __init__(self, i2c: Union[I2C, PAHUBUnit], addr=WEIGHT_I2C_ADDR) -> None:
        """Initialize the weight i2c sensor."""
        self.i2c = i2c
        if addr >= 1 and addr <= 127:
            self.unit_addr = addr
        self._available()

    def _available(self) -> None:
        """! Check if sensor is available on the I2C bus."""
        if not (self.unit_addr in self.i2c.scan()):
            raise UnitError("Weight Unit not found in Grove")

    @property
    def get_adc_raw(self) -> int:
        """! Get the ADC value."""
        data = self.i2c.readfrom_mem(self.unit_addr, ADC_REG, 4)
        return struct.unpack("<I", data)[0]

    @property
    def get_weight_float(self) -> float:
        """! Get the weight in grams(float)."""
        data = self.i2c.readfrom_mem(self.unit_addr, WEIGHT_REG, 4)
        return round(struct.unpack("<f", data)[0], 3)

    def set_calibration(
        self, weight1_g: float, weight1_adc: int, weight2_g: float, weight2_adc: int
    ) -> None:
        """! Calibration the Weight I2C sensor.

        (1) step 1:  Reset offset;
        (2) step 2: Get RawADC, this is RawADC_0g
        (3) step 3: Put 100g weight on it, and get RawADC, this is RawADC_100g
        (4) step 4: Calculate the value of GAP = (RawADC_100g-RawADC0g) / 100
        (5) step 5:  Write GAP value to the unit Via I2C

        weight1_g:   Weight1 in grams.
        weight1_adc: Weight1 in ADC.
        weight2_g:   Weight2 in grams.
        weight2_adc: Weight2 in ADC.
        """

        gap = abs(weight2_adc - weight1_adc) / abs(weight2_g - weight1_g)
        self.i2c.writeto_mem(self.unit_addr, GAP_REG, struct.pack("<f", gap))
        time.sleep_ms(200)

    def set_reset_offset(self) -> None:
        """! Reset offest weight value to zero."""
        self.i2c.writeto_mem(self.unit_addr, OFFSET_REG, b"\x01")

    @property
    def get_weight_int(self) -> int:
        """! Get the weight in grams(int)."""
        data = self.i2c.readfrom_mem(self.unit_addr, WEIGHT_X100_REG, 4)
        return struct.unpack("<i", data)[0]

    @property
    def get_weight_str(self) -> str:
        """! Get the weight in grams(str)."""
        data = self.i2c.readfrom_mem(self.unit_addr, WEIGHT_STR_REG, 16)
        return data.replace(b"\x00", b"").decode("utf8")

    def set_lowpass_filter(self, enabled: bool) -> None:
        """! Set low pass filter enabled or not
        enabled: Enable or Disable
        """
        self.i2c.writeto_mem(self.unit_addr, FILTER_IP_REG, bytes([enabled]))

    @property
    def get_lowpass_filter(self) -> bool:
        """! Get low pass filter enabled or not."""
        return bool(self.i2c.readfrom_mem(self.unit_addr, FILTER_IP_REG, 1)[0])

    def set_average_filter_level(self, level: int) -> None:
        """! Set average filter level
        level of average filter, larger value for smoother result but more latency
        level: 0~50
        """
        if level > 50 or level < 0:
            raise UnitError("Level for average filter must between 0 ~ 50")

        self.i2c.writeto_mem(self.unit_addr, FILTER_AVG_REG, struct.pack("b", level))

    @property
    def get_average_filter_level(self) -> int:
        """! Get average filter level."""
        return self.i2c.readfrom_mem(self.unit_addr, FILTER_AVG_REG, 1)[0]

    def set_ema_filter_alpha(self, alpha: int) -> None:
        """! Set ema filter alpha
        alpha of ema filter, smaller value for smoother result but more latency
        alpha: 0~99
        """
        if alpha > 99 or alpha < 0:
            raise Exception("Alpha for EMA filter must between 0 ~ 99")

        self.i2c.writeto_mem(self.unit_addr, FILTER_EMA_REG, struct.pack("b", alpha))

    @property
    def get_ema_filter_alpha(self) -> int:
        """! Get ema filter alpha."""
        return self.i2c.readfrom_mem(self.unit_addr, FILTER_EMA_REG, 1)[0]

    def get_device_spec(self, mode) -> int:
        """! Get device firmware version and i2c address.
        mode: 0xFE and 0xFF
        """
        if mode >= FW_VER_REG and mode <= I2C_ADDR_REG:
            return self.i2c.readfrom_mem(self.unit_addr, mode, 1)[0]

    def set_i2c_address(self, addr) -> None:
        """! Set i2c address.
        addr:  1 to 127
        """
        if addr >= 1 and addr <= 127:
            if addr != self.unit_addr:
                self.i2c.writeto_mem(self.unit_addr, I2C_ADDR_REG, struct.pack("b", addr))
                self.unit_addr = addr
                time.sleep_ms(200)
