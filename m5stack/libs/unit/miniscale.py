# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import struct


class MiniScaleUnit:
    """! MiniScale is a weight sensor module with an internal HX711 22-bit ADC chip."""

    def __init__(self, i2c: I2C | PAHUBUnit, address: int = 0x26):
        """! Initialize MiniScale module

        @param i2c I2C or PAHUB object
        @param address Module I2C address, default is 0x26
        """
        self.i2c = i2c
        self.addr = address
        self._tare = 0.0  # Tare offset value
        self._available()  # Check if device is online

    def _available(self):
        """! Check if MiniScale module exists on I2C bus

        @raises UnitError: If module is not detected
        """
        if self.addr not in self.i2c.scan():
            raise UnitError("MiniScale Unit not found.")

    # ------------------------------------------------------------------------
    # Basic data reading
    # ------------------------------------------------------------------------

    @property
    def adc(self) -> int:
        """! Read raw ADC value (unprocessed)

        @return Raw ADC value (integer)
        """
        data = self.i2c.readfrom_mem(self.addr, 0x00, 4)
        return struct.unpack("<I", data)[0]

    @property
    def weight(self) -> float:
        """! Read current weight (grams)

        @return Actual weight (float after subtracting tare value)
        """
        data = self.i2c.readfrom_mem(self.addr, 0x10, 4)
        result = struct.unpack("<f", data)[0]
        return result - self._tare

    @property
    def button(self) -> bool:
        """! Read button state

        @return True if pressed, False if not pressed
        """
        data = self.i2c.readfrom_mem(self.addr, 0x20, 1)
        return struct.unpack("B", data)[0] == 0

    # ------------------------------------------------------------------------
    # Control functions
    # ------------------------------------------------------------------------

    def tare(self):
        """! Tare operation
        Record current weight as offset value, so subsequent weight readings use current as zero point."""
        self._tare = self.weight

    def set_led(self, r: int, g: int, b: int):
        """! Set RGB indicator color

        @param r Red component (0~255)
        @param g Green component (0~255)
        @param b Blue component (0~255)
        """
        self.i2c.writeto_mem(self.addr, 0x30, bytes([r, g, b]))

    def reset(self):
        """! Reset module internal weight register (clear to zero)"""
        self.i2c.writeto_mem(self.addr, 0x50, b"\x01")

    # ------------------------------------------------------------------------
    # Calibration functions
    # ------------------------------------------------------------------------

    def calibration(self, weight1_g: float, weight1_adc: int, weight2_g: float, weight2_adc: int):
        """! Calibrate module gain (GAP value)

        Calibration process example:
        1. Reset offset
        2. Read no-load ADC (RawADC_0g)
        3. Place known weight (e.g., 100g) and read ADC (RawADC_100g)
        4. Calculate GAP = (RawADC_100g - RawADC_0g) / 100
        5. Write to module to save calibration coefficient

        @param weight1_g Weight at first point (unit: g)
        @param weight1_adc ADC value at first point
        @param weight2_g Weight at second point (unit: g)
        @param weight2_adc ADC value at second point
        @raises ValueError If two weights are equal
        """
        if weight2_g == weight1_g:
            raise ValueError("Invalid calibration points: weight1_g and weight2_g cannot be equal")

        gap = (weight2_adc - weight1_adc) / (weight2_g - weight1_g)
        self.i2c.writeto_mem(self.addr, 0x40, struct.pack("<f", gap))

    # ------------------------------------------------------------------------
    # Filter control
    # ------------------------------------------------------------------------

    def set_low_pass_filter(self, enabled: bool):
        """! Enable or disable low-pass filter

        @param enabled True to enable filter / False to disable filter
        """
        self.i2c.writeto_mem(self.addr, 0x80, b"\x01" if enabled else b"\x00")

    def get_low_pass_filter(self) -> bool:
        """! Get low-pass filter status

        @return True if filter is enabled
        """
        data = self.i2c.readfrom_mem(self.addr, 0x80, 1)
        return struct.unpack("B", data)[0] == 1

    def set_average_filter_level(self, level: int):
        """! Set average filter level

        @param level Average count level (0~50), higher value means smoother but more delay
        @raises ValueError If out of range
        """
        if not (0 <= level <= 50):
            raise ValueError("Level for average filter must be between 0 and 50")
        self.i2c.writeto_mem(self.addr, 0x81, struct.pack("b", level))

    def get_average_filter_level(self) -> int:
        """! Get average filter level

        @return Current average filter level (integer)
        """
        data = self.i2c.readfrom_mem(self.addr, 0x81, 1)
        return struct.unpack("b", data)[0]

    def set_ema_filter_alpha(self, alpha: int):
        """! Set exponential moving average (EMA) filter parameter

        @param alpha EMA filter coefficient (0~99), smaller value means smoother but more response delay
        @raises ValueError If out of range
        """
        if not (0 <= alpha <= 99):
            raise ValueError("Alpha for EMA filter must be between 0 and 99")
        self.i2c.writeto_mem(self.addr, 0x82, struct.pack("b", alpha))

    def get_ema_filter_alpha(self) -> int:
        """! Get EMA filter coefficient

        @return Current EMA alpha value (integer)
        """
        data = self.i2c.readfrom_mem(self.addr, 0x82, 1)
        return struct.unpack("b", data)[0]
