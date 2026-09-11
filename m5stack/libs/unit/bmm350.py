# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

"""Unit BMM350 direct-I2C magnetometer support."""

import math

from machine import I2C
from driver.bmm350 import BMM350, BMM350_ADDR
from .pahub import PAHUBUnit


class BMM350Unit:
    """Direct-I2C BMM350 with cached, mapped, and calibrated measurements.

    Args:
        i2c (I2C | PAHUBUnit): I2C interface connected directly to the BMM350.
        addr (int): I2C address. Defaults to ``0x14``.
        output_data_rate_hz (int): Output data rate in Hz. Valid values are
            25, 50, 100, 200, and 400. Defaults to 100.

    Raises:
        OSError: The BMM350 is missing or communication fails.
        ValueError: ``output_data_rate_hz`` is unsupported.
    """

    _MIN_CALIBRATION_SAMPLES = 32
    _MIN_CALIBRATION_RANGE_UT = 10.0

    def __init__(
        self,
        i2c: I2C | PAHUBUnit,
        addr: int = BMM350_ADDR,
        output_data_rate_hz: int = 100,
    ) -> None:
        self._sensor = BMM350(i2c, address=addr, output_data_rate_hz=output_data_rate_hz)
        self._axis_mapping = (-2, -1, -3)
        self._offsets = (0.0, 0.0, 0.0)
        self._scales = (1.0, 1.0, 1.0)
        self._raw_magnetic = None
        self._magnetic = (0.0, 0.0, 0.0)
        self._temperature = 0.0
        self._heading = 0.0
        self._magnetic_declination = 0.0
        self._calibrating = False
        self._calibration_samples = 0
        self._calibration_minimums = None
        self._calibration_maximums = None

    @staticmethod
    def _validate_vector(values, name, positive=False):
        try:
            if isinstance(values, (str, bytes)) or len(values) != 3:
                raise ValueError
            if any(isinstance(value, (str, bytes, bool)) for value in values):
                raise ValueError
            result = tuple(float(value) for value in values)
        except (TypeError, ValueError):
            raise ValueError("%s must contain three finite numeric values" % name)
        if any(not math.isfinite(value) for value in result):
            raise ValueError("%s must contain three finite numeric values" % name)
        if positive and any(value <= 0.0 for value in result):
            raise ValueError("scales must be greater than zero")
        return result

    @staticmethod
    def _validate_mapping(x_axis, y_axis, z_axis):
        mapping = (x_axis, y_axis, z_axis)
        if any(
            not isinstance(axis, int) or isinstance(axis, bool) or axis == 0 or abs(axis) > 3
            for axis in mapping
        ):
            raise ValueError("axis values must be 1/-1, 2/-2, or 3/-3")
        if len({abs(axis) for axis in mapping}) != 3:
            raise ValueError("axis mapping cannot reuse a source axis")
        return mapping

    @staticmethod
    def _map_vector(vector, mapping):
        return tuple(vector[abs(axis) - 1] * (1 if axis > 0 else -1) for axis in mapping)

    def _refresh_cache(self):
        if self._raw_magnetic is None:
            return
        mapped = self._map_vector(self._raw_magnetic, self._axis_mapping)
        self._magnetic = tuple(
            (mapped[axis] - self._offsets[axis]) * self._scales[axis] for axis in range(3)
        )
        self._heading = (
            math.degrees(math.atan2(self._magnetic[1], self._magnetic[0]))
            + self._magnetic_declination
        ) % 360.0

    def _accumulate_calibration_sample(self):
        mapped = self._map_vector(self._raw_magnetic, self._axis_mapping)
        for axis in range(3):
            self._calibration_minimums[axis] = min(self._calibration_minimums[axis], mapped[axis])
            self._calibration_maximums[axis] = max(self._calibration_maximums[axis], mapped[axis])
        self._calibration_samples += 1

    def _apply_calibration(self, offsets, scales):
        self._offsets = tuple(offsets)
        self._scales = tuple(scales)
        self._refresh_cache()

    def _sample(self):
        self._raw_magnetic, self._temperature = self._sensor.read()
        if self._calibrating:
            self._accumulate_calibration_sample()
        self._refresh_cache()

    def get_mag(self) -> tuple:
        """Sample and return the mapped and calibrated magnetic field.

        Returns:
            tuple: Magnetic field as ``(x, y, z)`` in uT.

        Raises:
            OSError: I2C communication fails.
        """
        self._sample()
        return self._magnetic

    def get_mag_raw(self) -> tuple:
        """Sample and return signed raw BMM350 register counts."""
        field, _ = self._sensor.read(raw=True)
        return field

    def get_temperature(self) -> float:
        """Sample and return the sensor temperature.

        Returns:
            float: Sensor temperature in degrees Celsius.

        Raises:
            OSError: I2C communication fails.
        """
        self._sample()
        return self._temperature

    def get_heading(self) -> float:
        """Sample and return the horizontal heading.

        Returns:
            float: Horizontal heading in the range [0, 360) degrees.

        Raises:
            OSError: I2C communication fails.
        """
        self._sample()
        return self._heading

    def set_output_data_rate(self, rate_hz: int) -> None:
        """Set the output data rate.

        Args:
            rate_hz (int): One of 25, 50, 100, 200, or 400 Hz.

        Raises:
            ValueError: ``rate_hz`` is unsupported.
            OSError: I2C communication fails.
        """
        self._sensor.set_output_data_rate(rate_hz)

    def get_output_data_rate(self) -> int:
        """Return the configured output data rate without accessing I2C.

        Returns:
            int: Output data rate in Hz.
        """
        return self._sensor.output_data_rate_hz

    def set_axis_mapping(self, x_axis: int, y_axis: int, z_axis: int) -> None:
        """Set source axes and signs for output X, Y, and Z.

        Args:
            x_axis (int): Source axis for X, from ``+/-1``, ``+/-2``, ``+/-3``.
            y_axis (int): Source axis for Y, from ``+/-1``, ``+/-2``, ``+/-3``.
            z_axis (int): Source axis for Z, from ``+/-1``, ``+/-2``, ``+/-3``.

        Raises:
            ValueError: An axis is invalid or a source axis is reused.
        """
        self._axis_mapping = self._validate_mapping(x_axis, y_axis, z_axis)
        self._refresh_cache()

    def get_axis_mapping(self) -> tuple:
        """Return the output axis mapping without accessing I2C.

        Returns:
            tuple: Source and sign for output X, Y, and Z.
        """
        return self._axis_mapping

    def set_calibration(self, offsets: tuple, scales: tuple) -> None:
        """Set hard-iron offsets and soft-iron scale factors.

        Args:
            offsets (tuple): Three finite hard-iron offsets in uT.
            scales (tuple): Three finite, positive, unitless scale factors.

        Raises:
            ValueError: A parameter is not a finite length-three vector or a
                scale is not greater than zero.
        """
        new_offsets = self._validate_vector(offsets, "offsets")
        new_scales = self._validate_vector(scales, "scales", positive=True)
        self._apply_calibration(new_offsets, new_scales)

    def get_calibration(self) -> tuple:
        """Return calibration parameters without accessing I2C.

        Returns:
            tuple: ``(offsets, scales)`` currently applied in memory.
        """
        return self._offsets, self._scales

    def clear_calibration(self) -> None:
        """Restore zero offsets and unit scales, then refresh the cache."""
        self._offsets = (0.0, 0.0, 0.0)
        self._scales = (1.0, 1.0, 1.0)
        self._refresh_cache()

    def start_calibration(self) -> None:
        """Start non-blocking min/max calibration.

        Raises:
            RuntimeError: Calibration is already active.
        """
        if self._calibrating:
            raise RuntimeError("BMM350 calibration is already active")
        self._calibration_samples = 0
        self._calibration_minimums = [float("inf"), float("inf"), float("inf")]
        self._calibration_maximums = [float("-inf"), float("-inf"), float("-inf")]
        self._calibrating = True

    def stop_calibration(self) -> tuple:
        """Finish calibration and apply the computed parameters.

        Returns:
            tuple: ``(offsets, scales)`` calculated from collected samples.

        Raises:
            RuntimeError: Calibration is inactive, has fewer than 32 samples,
                or any axis covers less than 10 uT.
        """
        if not self._calibrating:
            raise RuntimeError("BMM350 calibration is not active")
        minimums = self._calibration_minimums
        maximums = self._calibration_maximums
        sample_count = self._calibration_samples
        self._calibrating = False
        if sample_count < self._MIN_CALIBRATION_SAMPLES:
            raise RuntimeError("BMM350 calibration requires at least 32 samples")
        ranges = tuple(maximums[axis] - minimums[axis] for axis in range(3))
        if any(value < self._MIN_CALIBRATION_RANGE_UT for value in ranges):
            raise RuntimeError("BMM350 calibration requires at least 10 uT range on every axis")
        radii = tuple(value / 2.0 for value in ranges)
        average_radius = sum(radii) / 3.0
        offsets = tuple((minimums[axis] + maximums[axis]) / 2.0 for axis in range(3))
        scales = tuple(average_radius / radius for radius in radii)
        self._apply_calibration(offsets, scales)
        return offsets, scales

    def cancel_calibration(self) -> None:
        """Cancel active sample collection while preserving calibration."""
        self._calibrating = False

    def is_calibrating(self) -> bool:
        """Return whether non-blocking calibration is active.

        Returns:
            bool: ``True`` while samples are being collected.
        """
        return self._calibrating

    def set_magnetic_declination(self, angle: float) -> None:
        """Set magnetic declination in degrees.

        Args:
            angle (float): Finite declination angle in degrees.

        Raises:
            ValueError: ``angle`` is not finite numeric data.
        """
        try:
            if isinstance(angle, (str, bytes, bool)):
                raise ValueError
            angle = float(angle)
        except (TypeError, ValueError):
            raise ValueError("magnetic declination must be a finite numeric value")
        if not math.isfinite(angle):
            raise ValueError("magnetic declination must be a finite numeric value")
        self._magnetic_declination = angle
        self._refresh_cache()

    def get_magnetic_declination(self) -> float:
        """Return magnetic declination without accessing I2C.

        Returns:
            float: Magnetic declination in degrees.
        """
        return self._magnetic_declination
