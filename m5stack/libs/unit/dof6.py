# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import math
import time

from machine import I2C
from driver.bmi270_bmm150 import BMI270
from driver.complementary import Complementary
from .pahub import PAHUBUnit
from .unit_helper import UnitError


BMI270_ADDR = 0x68
GRAVITY_MPS2 = 9.80665
DEG_TO_RAD = math.pi / 180.0


class DoF6Unit:
    ACCEL_RANGE_2G = 2
    ACCEL_RANGE_4G = 4
    ACCEL_RANGE_8G = 8
    ACCEL_RANGE_16G = 16
    GYRO_RANGE_125DPS = 125
    GYRO_RANGE_250DPS = 250
    GYRO_RANGE_500DPS = 500
    GYRO_RANGE_1000DPS = 1000
    GYRO_RANGE_2000DPS = 2000
    ACCEL_RANGES = (ACCEL_RANGE_2G, ACCEL_RANGE_4G, ACCEL_RANGE_8G, ACCEL_RANGE_16G)
    GYRO_RANGES = (
        GYRO_RANGE_125DPS,
        GYRO_RANGE_250DPS,
        GYRO_RANGE_500DPS,
        GYRO_RANGE_1000DPS,
        GYRO_RANGE_2000DPS,
    )
    ACCEL_ODR_VALUES = (0.78, 1.5, 3.1, 6.25, 12.5, 25, 50, 100, 200, 400, 800, 1600)
    GYRO_ODR_VALUES = (25, 50, 100, 200, 400, 800, 1600, 3200)

    """
    note:
        en: Unit DoF6 is a six-axis motion sensor based on BMI270. Raw sensor getters read the current value and attitude getters sample before returning.

    details:
        category: Unit

    example:
        - ../../../examples/unit/dof6/cores3_unit_dof6_example.py

    m5f2:
        - unit/dof6/cores3_unit_dof6_example.m5f2
    """

    def __init__(self, i2c: I2C | PAHUBUnit, addr: int = 0x68) -> None:
        """
        note:
            en: Initialize Unit DoF6 on an I2C bus.
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
        if not isinstance(addr, int) or isinstance(addr, bool):
            raise TypeError("addr must be an integer")
        if addr not in (0x68, 0x69):
            raise ValueError("addr must be 0x68 or 0x69")
        if addr not in i2c.scan():
            raise UnitError("BMI270 was not found at address 0x%02x" % addr)
        self._imu = BMI270(i2c, address=addr)
        self._fusion = Complementary()
        self._axis_mapping = {
            "accelerometer": (1, 2, 3),
            "gyroscope": (1, 2, 3),
        }
        self._gyro_offsets = (0.0, 0.0, 0.0)
        # Calibration is an explicit operation so construction does not block on samples.
        self._gyro_calibrated = False
        self._accelerometer = (0.0, 0.0, 0.0)
        self._gyroscope = (0.0, 0.0, 0.0)
        self._imu_temperature = 0.0
        self._attitude = (0.0, 0.0, 0.0)
        self._last_update = time.ticks_us()
        self._first_update = True

    @staticmethod
    def _map_vector(vector, mapping):
        return tuple(vector[abs(axis) - 1] * (1 if axis > 0 else -1) for axis in mapping)

    @staticmethod
    def _validate_mapping(x_axis, y_axis, z_axis):
        mapping = (x_axis, y_axis, z_axis)
        if any(axis == 0 or abs(axis) > 3 for axis in mapping):
            raise ValueError("axis values must be in 1/-1, 2/-2, or 3/-3")
        if len({abs(axis) for axis in mapping}) != 3:
            raise ValueError("axis mapping cannot reuse a source axis")
        return mapping

    def _sample_imu(self):
        self._read_accelerometer_native()
        self._read_gyroscope_native()
        self._read_imu_temperature()

    def _read_accelerometer_native(self):
        self._accelerometer = self._map_vector(
            self._imu.accel(), self._axis_mapping["accelerometer"]
        )
        return self._accelerometer

    def _read_gyroscope_native(self):
        gyro = self._map_vector(self._imu.gyro(), self._axis_mapping["gyroscope"])
        self._gyroscope = tuple(gyro[i] - self._gyro_offsets[i] for i in range(3))
        return self._gyroscope

    def _read_accelerometer(self, raw=False):
        if raw:
            return self._imu.accel(raw=True)
        return tuple(value * GRAVITY_MPS2 for value in self._read_accelerometer_native())

    def _read_gyroscope(self, raw=False):
        if raw:
            return self._imu.gyro(raw=True)
        return tuple(value * DEG_TO_RAD for value in self._read_gyroscope_native())

    def _read_imu_temperature(self):
        self._imu_temperature = self._imu.temperature()
        return self._imu_temperature

    def _sample_interval(self):
        now = time.ticks_us()
        if self._first_update:
            interval = 0.01
            self._first_update = False
        else:
            interval = time.ticks_diff(now, self._last_update) / 1000000.0
            interval = min(0.2, max(0.001, interval))
        self._last_update = now
        return interval

    def _cache_attitude(self):
        self._attitude = self._fusion.get_attitude()

    def _advance_fusion(self) -> None:
        self._sample_imu()
        self._fusion.update_imu(self._accelerometer, self._gyroscope, self._sample_interval())
        self._cache_attitude()

    def get_accel(self) -> tuple:
        """
        note:
            en: Read mapped acceleration in m/s2.
        returns:
            note: Acceleration as (x, y, z) in m/s2.
        """
        return self._read_accelerometer()

    def get_accel_raw(self) -> tuple:
        """
        note:
            en: Read signed raw BMI270 accelerometer register counts.
        returns:
            note: Raw acceleration counts as (x, y, z), from -32768 to 32767.
        """
        return self._read_accelerometer(raw=True)

    def get_gyro(self) -> tuple:
        """
        note:
            en: Read mapped and offset-corrected angular velocity in rad/s.
        returns:
            note: Angular velocity as (x, y, z) in rad/s.
        """
        return self._read_gyroscope()

    def get_gyro_raw(self) -> tuple:
        """
        note:
            en: Read signed raw BMI270 gyroscope register counts.
        returns:
            note: Raw angular velocity counts as (x, y, z), from -32768 to 32767.
        """
        return self._read_gyroscope(raw=True)

    def get_temperature(self) -> float:
        """
        note:
            en: Read and return the current BMI270 temperature in degrees Celsius.
        returns:
            note: BMI270 temperature in degrees Celsius.
        """
        return self._read_imu_temperature()

    def get_attitude(self) -> tuple:
        """
        note:
            en: Return the latest fused yaw, pitch, and roll in degrees.
        returns:
            note: Attitude as (yaw, pitch, roll) in degrees.
        """
        self._advance_fusion()
        return self._attitude

    def set_accel_range(self, accel_scale: int) -> None:
        """
        note:
            en: Set the BMI270 accelerometer range.
        params:
            accel_scale:
                note: Full scale in g. Valid values are 2, 4, 8, and 16.
        """
        if accel_scale not in self.ACCEL_RANGES:
            raise ValueError("accel_scale must be one of 2, 4, 8, or 16")
        self._imu.accel_range(accel_scale)

    def set_gyro_range(self, gyro_scale: int) -> None:
        """
        note:
            en: Set the BMI270 gyroscope range.
        params:
            gyro_scale:
                note: Full scale in deg/s. Valid values are 125, 250, 500, 1000, and 2000.
        """
        if gyro_scale not in self.GYRO_RANGES:
            raise ValueError("gyro_scale must be one of 125, 250, 500, 1000, or 2000")
        self._imu.gyro_range(gyro_scale)

    def set_accel_gyro_odr(self, accel_odr: float, gyro_odr: float) -> None:
        """
        note:
            en: Set the BMI270 accelerometer and gyroscope output data rates.
        params:
            accel_odr:
                note: Accelerometer output data rate in Hz.
            gyro_odr:
                note: Gyroscope output data rate in Hz.
        """
        if accel_odr not in self.ACCEL_ODR_VALUES:
            raise ValueError(
                "accel_odr must be one of 0.78, 1.5, 3.1, 6.25, 12.5, 25, 50, 100, 200, 400, 800, or 1600 Hz"
            )
        if gyro_odr not in self.GYRO_ODR_VALUES:
            raise ValueError(
                "gyro_odr must be one of 25, 50, 100, 200, 400, 800, 1600, or 3200 Hz"
            )
        self._imu.accel_gyro_odr(accel_odr, gyro_odr)

    def set_gyro_offsets(self, x: float, y: float, z: float) -> None:
        """
        note:
            en: Set angular velocity offsets in mapped axes and rad/s.
        params:
            x:
                note: X-axis offset in rad/s.
            y:
                note: Y-axis offset in rad/s.
            z:
                note: Z-axis offset in rad/s.
        """
        self._gyro_offsets = tuple(value / DEG_TO_RAD for value in (x, y, z))

    def calibrate_gyro(self, samples: int = 32) -> bool:
        """
        note:
            en: Estimate gyroscope offsets while the unit is stationary.
        params:
            samples:
                note: Number of samples. The default is 32.
        returns:
            note: True when the unit was stationary and offsets were updated.
        """
        if samples <= 0:
            raise ValueError("samples must be positive")
        totals = [0.0, 0.0, 0.0]
        minimums = [float("inf"), float("inf"), float("inf")]
        maximums = [float("-inf"), float("-inf"), float("-inf")]
        stationary = True
        for _ in range(8):
            self._imu.gyro()
            time.sleep_ms(10)
        for _ in range(samples):
            accel = self._map_vector(self._imu.accel(), self._axis_mapping["accelerometer"])
            gyro = self._map_vector(self._imu.gyro(), self._axis_mapping["gyroscope"])
            accel_norm_sq = sum(value * value for value in accel)
            if accel_norm_sq < 0.64 or accel_norm_sq > 1.44:
                stationary = False
            for axis in range(3):
                totals[axis] += gyro[axis]
                minimums[axis] = min(minimums[axis], gyro[axis])
                maximums[axis] = max(maximums[axis], gyro[axis])
            time.sleep_ms(10)
        if any(maximums[axis] - minimums[axis] > 5.0 for axis in range(3)):
            stationary = False
        if stationary:
            self._gyro_offsets = tuple(value / samples for value in totals)
        self._gyro_calibrated = stationary
        return stationary

    def set_fusion_time_constant(self, seconds: float) -> None:
        """
        note:
            en: Set the complementary filter time constant in seconds.
        params:
            seconds:
                note: Non-negative time constant. Smaller values correct drift
                    faster.
        """
        self._fusion.set_time_constant(seconds)

    def reset_fusion(self) -> None:
        """
        note:
            en: Reset fusion so the next sample initializes orientation from the sensors.
        """
        self._fusion.reset()
        self._attitude = (0.0, 0.0, 0.0)
        self._first_update = True

    def set_axis_mapping(self, sensor: str, x_axis: int, y_axis: int, z_axis: int) -> None:
        """
        note:
            en: Map a sensor to product axes. Values 1/-1, 2/-2, and 3/-3 represent X/-X, Y/-Y, and Z/-Z.
        params:
            sensor:
                note: Sensor name, accelerometer or gyroscope.
            x_axis:
                note: Source and sign for product X.
            y_axis:
                note: Source and sign for product Y.
            z_axis:
                note: Source and sign for product Z.
        """
        aliases = {"accel": "accelerometer", "gyro": "gyroscope"}
        sensor = aliases.get(sensor, sensor)
        if sensor not in self._axis_mapping:
            raise ValueError("sensor must be accelerometer or gyroscope")
        self._axis_mapping[sensor] = self._validate_mapping(x_axis, y_axis, z_axis)
