# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# Import necessary libraries
from machine import I2C
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import struct
import sys

if sys.platform != "esp32":
    from typing import Union


class MiniScaleUnit:
    """! MiniScale is a weight sensor, includes a hx711 22bit ADC."""

    def __init__(self, i2c: Union[I2C, PAHUBUnit], addr=0x26):
        self.i2c = i2c
        self.addr = addr
        self._available()

    def _available(self):
        """! Check if sensor is available on the I2C bus.

        Raises:
            UnitError: If the sensor is not found.
        """
        if self.addr not in self.i2c.scan():
            raise UnitError("MiniScale Unit not found.")

    @property
    def adc(self) -> int:
        """! Get the ADC value."""
        data = self.i2c.readfrom_mem(self.addr, 0x00, 4)
        return struct.unpack("<I", data)[0]

    @property
    def weight(self) -> float:
        """! Get the weight in grams."""
        data = self.i2c.readfrom_mem(self.addr, 0x10, 4)
        return struct.unpack("<f", data)[0]

    @property
    def button(self) -> bool:
        """! Get the button state."""
        data = self.i2c.readfrom_mem(self.addr, 0x20, 1)
        return struct.unpack("b", data)[0] == 0

    def set_led(self, r: int, g: int, b: int):
        # 2.0.3 添加
        self.setLed(r, g, b)

    def setLed(self, r: int, g: int, b: int):  # noqa: N802
        # TODO: 2.0.6移除
        """! Set the RGB LED color.

        @param r Red value. 0 - 255
        @param g Green value. 0 - 255
        @param b Blue value. 0 - 255
        """
        self.i2c.writeto_mem(self.addr, 0x30, bytes([r, g, b]))

    def reset(self):
        """! Reset weight value to zero"""
        self.i2c.writeto_mem(self.addr, 0x50, b"\x01")

    def calibration(self, weight1_g: float, weight1_adc: int, weight2_g: float, weight2_adc: int):
        """! Calibration the MiniScale sensor.

        (1) step 1:  Reset offset;
        (2) step 2: Get RawADC, this is RawADC_0g
        (3) step 3: Put 100g weight on it, and get RawADC, this is RawADC_100g
        (4) step 4: Calculate the value of GAP = (RawADC_100g-RawADC0g) / 100
        (5) step 5:  Write GAP value to the unit Via I2C

        @param weight1_g Weight1 in grams.
        @param weight1_adc Weight1 in ADC.
        @param weight2_g Weight2 in grams.
        @param weight2_adc Weight2 in ADC.
        """

        gap = (weight2_adc - weight1_adc) / (weight2_g - weight1_g)
        self.i2c.writeto_mem(self.addr, 0x40, struct.pack("<f", gap))

    def set_low_pass_filter(self, enabled: bool):
        # 2.0.3 添加
        self.setLowPassFilter(enabled)

    def setLowPassFilter(self, enabled: bool):  # noqa: N802
        # TODO: 2.0.6 移除
        """! Set low pass filter enabled or not

        @param enabled Enable filter or not
        """
        if enabled:
            self.i2c.writeto_mem(self.addr, 0x80, b"\x01")
        else:
            self.i2c.writeto_mem(self.addr, 0x80, b"\x00")

    def get_low_pass_filter(self) -> bool:
        # 2.0.3 添加
        return self.getLowPassFilter()

    def getLowPassFilter(self) -> bool:  # noqa: N802
        # TODO: 2.0.6 移除
        """! Get low pass filter enabled or not"""
        data = self.i2c.readfrom_mem(self.addr, 0x80, 1)
        return data == b"\x01"

    def set_average_filter_level(self, level: int):
        # 2.0.3 添加
        self.setAverageFilterLevel(level)

    def setAverageFilterLevel(self, level: int):  # noqa: N802
        # TODO: 2.0.6 移除
        """! Set average filter level

        @param level level of average filter, larger value for smoother result but more latency
        """
        if level > 50 or level < 0:
            raise Exception("Level for average filter must between 0 ~ 50")

        self.i2c.writeto_mem(self.addr, 0x81, struct.pack("b", level))

    def get_average_filter_level(self) -> int:
        # 2.0.3 添加
        return self.getAverageFilterLevel()

    def getAverageFilterLevel(self) -> int:  # noqa: N802
        # TODO: 2.0.6 移除
        """! Get average filter level"""
        data = self.i2c.readfrom_mem(self.addr, 0x81, 1)
        return struct.unpack("b", data)[0]

    def set_ema_filter_alpha(self, alpha: int):
        # 2.0.3 添加
        self.setEMAFilterAlpha(alpha)

    def setEMAFilterAlpha(self, alpha: int):  # noqa: N802
        # TODO: 2.0.6 移除
        """! Set ema filter alpha

        @param alpha alpha of ema filter, smaller value for smoother result but more latency
        """
        if alpha > 99 or alpha < 0:
            raise Exception("Alpha for EMA filter must between 0 ~ 99")

        self.i2c.writeto_mem(self.addr, 0x82, struct.pack("b", alpha))

    def get_ema_filter_alpha(self) -> int:
        return self.getEMAFilterAlpha()

    def getEMAFilterAlpha(self) -> int:  # noqa: N802
        # TODO: 2.0.6 移除
        """! Get ema filter alpha"""
        data = self.i2c.readfrom_mem(self.addr, 0x82, 1)
        return struct.unpack("b", data)[0]
