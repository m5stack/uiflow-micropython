# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.bme68x import BME68X_I2C
from .pahub import PAHUBUnit
from .unit_helper import UnitError
from machine import I2C


class ENVPROUnit(BME68X_I2C):
    TEMPERATURE = 1
    PRESSURE = 2
    HUMIDITY = 3

    def __init__(self, i2c: I2C | PAHUBUnit, address: int | list | tuple = 0x77):
        if address not in i2c.scan():
            raise UnitError("ENV PRO unit maybe not connect")
        super().__init__(i2c, address)

    def get_over_sampling_rate(self, env):
        if env == self.TEMPERATURE:
            return self.temperature_oversample
        elif env == self.PRESSURE:
            return self.pressure_oversample
        elif env == self.HUMIDITY:
            return self.humidity_oversample

    def set_over_sampling_rate(self, env, rate):
        if env == self.TEMPERATURE:
            self.temperature_oversample = rate
        elif env == self.PRESSURE:
            self.pressure_oversample = rate
        elif env == self.HUMIDITY:
            self.humidity_oversample = rate

    def get_iir_filter_coefficient(self):
        return self.filter_size

    def set_iir_filter_coefficient(self, value):
        self.filter_size = value

    def get_temperature(self):
        return self.temperature

    def get_humidity(self):
        return self.humidity

    def get_pressure(self):
        return self.pressure

    def get_gas_resistance(self):
        return round(self.gas / 1000, 3)

    def get_altitude(self):
        return round(self.altitude, 2)
