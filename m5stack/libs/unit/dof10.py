# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
from driver.spl06 import SPL06, SPL06_ADDR
from .dof9 import DoF9Unit
from .pahub import PAHUBUnit


class DoF10Unit(DoF9Unit):
    """
    note:
        en: Unit DoF10 adds an SPL06-001 pressure sensor to the BMI270 and direct-I2C BMM350 used by Unit DoF9.

    details:
        category: Unit

    example:
        - ../../../examples/unit/dof10/cores3_unit_dof10_accel_example.py
        - ../../../examples/unit/dof10/cores3_unit_dof10_barometer_example.py

    m5f2:
        - unit/dof10/cores3_unit_dof10_accel_example.m5f2
        - unit/dof10/cores3_unit_dof10_barometer_example.m5f2
    """

    def __init__(self, i2c: I2C | PAHUBUnit, addr: int = 0x68) -> None:
        """
        note:
            en: Initialize Unit DoF10 on an I2C bus. The BMM350 and SPL06-001 addresses remain 0x14 and 0x76.
        params:
            i2c:
                note: Initialized I2C or PAHUBUnit interface used to configure the sensors.
            addr:
                note: Integer BMI270 I2C address, 0x68 or 0x69. Defaults to 0x68.
        returns:
            note: None.
        raises:
            TypeError: addr is not an integer.
            ValueError: addr is not 0x68 or 0x69.
            UnitError: No BMI270 responds at the selected address.
            OSError: Sensor initialization or I2C communication fails.
        """
        super().__init__(i2c, addr=addr)
        self._pressure_sensor = SPL06(i2c, SPL06_ADDR)
        self._sea_level_pressure = 1013.25
        self._pressure_temperature = 0.0
        self._pressure = 0.0
        self._altitude = 0.0

    def get_temperature(self, sensor: str = "pressure") -> float:
        """
        note:
            en: Read the selected BMI270, BMM350, or SPL06-001 temperature in degrees Celsius.
        params:
            sensor:
                note: Sensor name, imu, magnetometer, or pressure. The default is pressure.
        returns:
            note: Selected sensor temperature in degrees Celsius.
        """
        if sensor in ("imu", "magnetometer", "mag"):
            return DoF9Unit.get_temperature(self, sensor)
        if sensor == "pressure":
            self._pressure_temperature = self._pressure_sensor.read_temperature()
            return self._pressure_temperature
        raise ValueError("sensor must be imu, magnetometer, or pressure")

    def get_pressure(self) -> float:
        """
        note:
            en: Read and return the current compensated pressure in hPa.
        returns:
            note: Atmospheric pressure in hPa.
        """
        self._pressure = self._pressure_sensor.read_pressure()
        return self._pressure

    def get_altitude(self) -> float:
        """
        note:
            en: Read current pressure and calculate altitude from the configured sea-level pressure.
        returns:
            note: Barometric altitude in meters.
        """
        self._altitude = SPL06.altitude(self.get_pressure(), self._sea_level_pressure)
        return self._altitude

    def set_sea_level_pressure(self, pressure: float) -> None:
        """
        note:
            en: Set the reference sea-level pressure used for altitude calculation.
        params:
            pressure:
                note: Positive sea-level pressure in hPa.
        """
        if pressure <= 0:
            raise ValueError("sea-level pressure must be positive")
        self._sea_level_pressure = pressure
