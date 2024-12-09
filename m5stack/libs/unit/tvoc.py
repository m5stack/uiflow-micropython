# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
from driver.sgp30 import SGP30
from .pahub import PAHUBUnit
from .unit_helper import UnitError


SGP30_I2C_ADDR = 0x58


class TVOCUnit(SGP30):
    """
    note:
        en: TVOCUnit is a hardware module for measuring Total Volatile Organic Compounds (TVOC) and equivalent CO2 (eCO2). It is based on the SGP30 sensor and communicates via the I2C interface. The class supports configuration and measurement operations.

    details:
        link: https://docs.m5stack.com/en/unit/tvoc
        image: https://static-cdn.m5stack.com/resource/docs/products/unit/tvoc/tvoc_01.webp
        category: Unit

    example:
        - ../../../examples/unit/tvoc/tvoc_cores3_example.py

    m5f2:
        - unit/tvoc/tvoc_cores3_example.m5f2
    """

    def __init__(self, i2c: I2C | PAHUBUnit, address: int = SGP30_I2C_ADDR) -> None:
        """
        note:
            en: Initialize the TVOCUnit with the specified I2C interface and address.

        params:
            i2c:
                note: The I2C interface or PAHUBUnit object for communication with the sensor.
            address:
                note: The I2C address of the TVOC unit. Defaults to 0x58.
        """
        self._i2c = i2c
        self._i2c_addr = address
        self.available()
        super().__init__(i2c=i2c, addr=address)

    def available(self) -> None:
        """
        note:
            en: Check whether the TVOC/eCO2 unit is available.

        params:
            note:
        """
        if self._i2c_addr not in self._i2c.scan():
            raise UnitError("TVOC/eCO2 unit not found in Grove")

    def set_baseline_co2_tvoc(self, co2eq: int, tvoc: int) -> None:
        """
        note:
            en: Set the baseline values for CO2 and TVOC measurements.

        params:
            co2eq:
                note: The CO2 equivalent baseline value to be set.
            tvoc:
                note: The TVOC baseline value to be set.
        """
        self.set_iaq_baseline(co2eq, tvoc)

    def set_relative_humidity(self, humidity_per: float, temp_c: float) -> None:
        """
        note:
            en: Set the relative humidity and temperature for accurate air quality measurement.

        params:
            humidity_per:
                note: The relative humidity in percentage (%).
            temp_c:
                note: The ambient temperature in Celsius (°C).
        """
        abs_humi = self.convert_r_to_a_humidity(temp_c, humidity_per)
        self.set_absolute_humidity(abs_humi)
