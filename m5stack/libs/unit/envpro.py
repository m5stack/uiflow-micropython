# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.bme68x import BME68X_I2C
from .pahub import PAHUBUnit
from .unit_helper import UnitError
from machine import I2C


class ENVPROUnit(BME68X_I2C):
    """
    note:
        en: ENV Pro Unit is an environmental sensor that utilizes the BME688 sensor solution, supporting the measurement of various environmental parameters such as volatile organic compounds (VOCs), indoor air quality (IAQ), temperature, humidity, and atmospheric pressure. It features a compact size, wide operating range, simple communication interface (I2C), excellent performance, and low power consumption, making it suitable for weather stations, indoor environmental monitoring, and air quality detection applications.

    details:
        link: https://docs.m5stack.com/en/unit/ENV%20Pro%20Unit
        image: https://static-cdn.m5stack.com/resource/docs/products/unit/ENV%20Pro%20Unit/img-2ba12134-9756-471a-b1a5-ba803a875e8f.webp
        category: Unit

    example:
        - ../../../examples/unit/envpro/envpro_cores3_example.py

    m5f2:
        - unit/envpro/envpro_cores3_example.m5f2
    """

    TEMPERATURE = 1
    PRESSURE = 2
    HUMIDITY = 3

    def __init__(self, i2c: I2C | PAHUBUnit, address: int | list | tuple = 0x77):
        """
        note:
            en: Initialize the ENVPROUnit with an I2C object and an optional address.

        params:
            i2c:
                note: The I2C interface or PAHUBUnit instance to communicate with the ENV PRO sensor.
            address:
                note: The I2C address of the ENV PRO sensor. Defaults to 0x77.
        """
        if address not in i2c.scan():
            raise UnitError("ENV PRO unit maybe not connect")
        super().__init__(i2c, address)

    def get_over_sampling_rate(self, env):
        """
        note:
            en: Retrieve the oversampling rate for the specified environment parameter.

        params:
            env:
                note: The environment parameter (TEMPERATURE, PRESSURE, HUMIDITY).

        returns:
            note: The oversampling rate for the specified parameter.
        """
        if env == self.TEMPERATURE:
            return self.temperature_oversample
        elif env == self.PRESSURE:
            return self.pressure_oversample
        elif env == self.HUMIDITY:
            return self.humidity_oversample

    def set_over_sampling_rate(self, env, rate):
        """
        note:
            en: Set the oversampling rate for the specified environment parameter.

        params:
            env:
                note: The environment parameter (TEMPERATURE, PRESSURE, HUMIDITY).
            rate:
                note: The oversampling rate to be set.
        """
        if env == self.TEMPERATURE:
            self.temperature_oversample = rate
        elif env == self.PRESSURE:
            self.pressure_oversample = rate
        elif env == self.HUMIDITY:
            self.humidity_oversample = rate

    def get_iir_filter_coefficient(self):
        """
        note:
            en: Retrieve the IIR filter coefficient.

        params:
            note:

        returns:
            note: The current IIR filter coefficient.
        """
        return self.filter_size

    def set_iir_filter_coefficient(self, value):
        """
        note:
            en: Set the IIR filter coefficient.

        params:
            value:
                note: The IIR filter coefficient to be set.
        """
        self.filter_size = value

    def get_temperature(self):
        """
        note:
            en: Retrieve the measured temperature.

        params:
            note:

        returns:
            note: The temperature value in degrees Celsius.
        """
        return self.temperature

    def get_humidity(self):
        """
        note:
            en: Retrieve the measured humidity.

        params:
            note:

        returns:
            note: The humidity value as a percentage.
        """
        return self.humidity

    def get_pressure(self):
        """
        note:
            en: Retrieve the measured pressure.

        params:
            note:

        returns:
            note: The pressure value in hPa.
        """
        return self.pressure

    def get_gas_resistance(self):
        """
        note:
            en: Retrieve the measured gas resistance.

        params:
            note:

        returns:
            note: The gas resistance value in kOhms.
        """
        return round(self.gas / 1000, 3)

    def get_altitude(self):
        """
        note:
            en: Retrieve the calculated altitude based on pressure readings.

        params:
            note:

        returns:
            note: The altitude value in meters.
        """
        return round(self.altitude, 2)
