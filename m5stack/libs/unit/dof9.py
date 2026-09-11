# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
from driver.bmm350 import BMM350_ADDR
from .bmm350 import BMM350Unit
from .dof6 import DoF6Unit
from .pahub import PAHUBUnit


class DoF9Unit(DoF6Unit):
    """
    note:
        en: Unit DoF9 combines a BMI270 with a direct-I2C BMM350 for nine-axis orientation sensing.

    details:
        category: Unit

    example:
        - ../../../examples/unit/dof9/cores3_unit_dof9_example.py

    m5f2:
        - unit/dof9/cores3_unit_dof9_example.m5f2
    """

    def __init__(self, i2c: I2C | PAHUBUnit, addr: int = 0x68) -> None:
        """
        note:
            en: Initialize Unit DoF9 on an I2C bus. The BMM350 address remains 0x14.
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
        self._magnetometer_sensor = BMM350Unit(i2c, addr=BMM350_ADDR)
        self._magnetometer = (0.0, 0.0, 0.0)
        self._heading = 0.0
        self.reset_fusion()

    def _advance_fusion(self) -> None:
        self._sample_imu()
        self._magnetometer = self._magnetometer_sensor.get_mag()
        self._fusion.update(
            self._accelerometer,
            self._gyroscope,
            self._magnetometer,
            self._sample_interval(),
        )
        self._cache_attitude()
        self._heading = self._fusion.get_heading()

    def get_mag(self) -> tuple:
        """
        note:
            en: Read mapped and calibrated magnetic field in uT.
        returns:
            note: Magnetic field as (x, y, z) in uT.
        """
        self._magnetometer = self._magnetometer_sensor.get_mag()
        return self._magnetometer

    def get_mag_raw(self) -> tuple:
        """
        note:
            en: Read signed raw BMM350 magnetometer register counts.
        returns:
            note: Raw magnetic counts as (x, y, z), from -8388608 to 8388607.
        """
        return self._magnetometer_sensor.get_mag_raw()

    def get_temperature(self, sensor: str = "imu") -> float:
        """
        note:
            en: Read the selected BMI270 or BMM350 temperature in degrees Celsius.
        params:
            sensor:
                note: Sensor name, imu or magnetometer.
        returns:
            note: Selected sensor temperature in degrees Celsius.
        """
        if sensor == "imu":
            return self._read_imu_temperature()
        if sensor in ("magnetometer", "mag"):
            return self._magnetometer_sensor.get_temperature()
        raise ValueError("sensor must be imu or magnetometer")

    def get_heading(self) -> float:
        """
        note:
            en: Sample the sensors and return the current tilt-compensated magnetic heading in degrees.
        returns:
            note: Heading from 0 to less than 360 degrees.
        """
        self._advance_fusion()
        return self._heading

    def get_attitude(self) -> tuple:
        """
        note:
            en: Sample the sensors and return fused yaw, pitch, and roll in degrees.
        returns:
            note: Attitude as (yaw, pitch, roll) in degrees.
        """
        self._advance_fusion()
        return self._attitude

    def set_magnetometer_calibration(self, offsets: tuple, scales: tuple) -> None:
        """
        note:
            en: Set hard-iron offsets and soft-iron scale factors for mapped magnetometer axes.
        params:
            offsets:
                note: Three offsets in uT.
            scales:
                note: Three unitless scale factors.
        """
        if len(offsets) != 3 or len(scales) != 3:
            raise ValueError("offsets and scales must contain three values")
        if any(scale == 0 for scale in scales):
            raise ValueError("magnetometer scales cannot be zero")
        self._magnetometer_sensor._apply_calibration(offsets, scales)
        self._magnetometer = self._magnetometer_sensor._magnetic

    def set_axis_mapping(self, sensor: str, x_axis: int, y_axis: int, z_axis: int) -> None:
        aliases = {"mag": "magnetometer"}
        sensor = aliases.get(sensor, sensor)
        if sensor == "magnetometer":
            self._magnetometer_sensor.set_axis_mapping(x_axis, y_axis, z_axis)
            self._magnetometer = self._magnetometer_sensor._magnetic
            return
        super().set_axis_mapping(sensor, x_axis, y_axis, z_axis)
