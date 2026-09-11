# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

"""Lightweight complementary attitude filter for BMI270-based units."""

import math


_PI = math.pi
_HALF_PI = math.pi / 2.0
_TWO_PI = math.pi * 2.0


def _wrap(angle):
    return (angle + _PI) % _TWO_PI - _PI


class Complementary:
    """Fuse gyroscope data with gravity and an optional magnetic field."""

    def __init__(self, time_constant=0.5):
        self.set_time_constant(time_constant)
        self.reset()

    def reset(self):
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        self.heading = 0.0
        self.q = (1.0, 0.0, 0.0, 0.0)
        self._initialized = False

    def set_time_constant(self, time_constant):
        if time_constant < 0 or not math.isfinite(time_constant):
            raise ValueError("time constant must be non-negative")
        self.time_constant = time_constant

    @staticmethod
    def _accel_angles(accel):
        ax, ay, az = accel
        norm_sq = ax * ax + ay * ay + az * az
        if not math.isfinite(norm_sq) or norm_sq < 0.5625 or norm_sq > 1.5625:
            return None
        roll = math.atan2(-ay, -az)
        pitch = math.atan2(ax, math.sqrt(ay * ay + az * az))
        return roll, pitch

    @staticmethod
    def _magnetic_heading(magnetometer, roll, pitch):
        mx, my, mz = magnetometer
        sin_roll, cos_roll = math.sin(roll), math.cos(roll)
        sin_pitch, cos_pitch = math.sin(pitch), math.cos(pitch)
        horizontal_x = mx * cos_pitch + my * sin_roll * sin_pitch + mz * cos_roll * sin_pitch
        horizontal_y = my * cos_roll - mz * sin_roll
        horizontal_norm_sq = horizontal_x * horizontal_x + horizontal_y * horizontal_y
        if not math.isfinite(horizontal_norm_sq) or horizontal_norm_sq <= 1e-12:
            return None
        return math.atan2(horizontal_y, horizontal_x)

    def _integrate_gyro(self, gyro, dt):
        gx, gy, gz = (math.radians(value) for value in gyro)
        sin_roll, cos_roll = math.sin(self.roll), math.cos(self.roll)
        cos_pitch = math.cos(self.pitch)
        if abs(cos_pitch) < 0.01:
            cos_pitch = 0.01 if cos_pitch >= 0 else -0.01
        tan_pitch = math.sin(self.pitch) / cos_pitch
        self.roll += (gx + sin_roll * tan_pitch * gy + cos_roll * tan_pitch * gz) * dt
        self.pitch += (cos_roll * gy - sin_roll * gz) * dt
        self.yaw += (sin_roll / cos_pitch * gy + cos_roll / cos_pitch * gz) * dt
        self.roll = _wrap(self.roll)
        self.pitch = max(-_HALF_PI + 0.01, min(_HALF_PI - 0.01, self.pitch))
        self.yaw = _wrap(self.yaw)

    def _correction(self, dt):
        if self.time_constant == 0:
            return 1.0
        return dt / (self.time_constant + dt)

    def _update_quaternion(self):
        half_roll = self.roll * 0.5
        half_pitch = self.pitch * 0.5
        half_yaw = self.yaw * 0.5
        cr, sr = math.cos(half_roll), math.sin(half_roll)
        cp, sp = math.cos(half_pitch), math.sin(half_pitch)
        cy, sy = math.cos(half_yaw), math.sin(half_yaw)
        self.q = (
            cr * cp * cy + sr * sp * sy,
            sr * cp * cy - cr * sp * sy,
            cr * sp * cy + sr * cp * sy,
            cr * cp * sy - sr * sp * cy,
        )

    def _initialize(self, accel, magnetometer=None):
        angles = self._accel_angles(accel)
        if angles is None:
            return False
        self.roll, self.pitch = angles
        if magnetometer is not None:
            heading = self._magnetic_heading(magnetometer, self.roll, self.pitch)
            if heading is not None:
                self.heading = heading
                self.yaw = heading
        self._initialized = True
        self._update_quaternion()
        return True

    def update_imu(self, accel, gyro, dt):
        """Advance 6DoF fusion. Gyroscope input is degrees per second."""
        if not self._initialized:
            self._initialize(accel)
            return self.q
        if dt <= 0 or not math.isfinite(dt):
            return self.q

        self._integrate_gyro(gyro, dt)
        angles = self._accel_angles(accel)
        if angles is not None:
            correction = self._correction(dt)
            self.roll += correction * _wrap(angles[0] - self.roll)
            self.pitch += correction * _wrap(angles[1] - self.pitch)
            self.roll = _wrap(self.roll)
            self.pitch = max(-_HALF_PI + 0.01, min(_HALF_PI - 0.01, self.pitch))
        self._update_quaternion()
        return self.q

    def update(self, accel, gyro, magnetometer, dt):
        """Advance 9DoF fusion with tilt-compensated magnetic heading."""
        if not self._initialized:
            self._initialize(accel, magnetometer)
            return self.q
        if dt <= 0 or not math.isfinite(dt):
            return self.q

        self._integrate_gyro(gyro, dt)
        correction = self._correction(dt)
        angles = self._accel_angles(accel)
        if angles is not None:
            self.roll += correction * _wrap(angles[0] - self.roll)
            self.pitch += correction * _wrap(angles[1] - self.pitch)
            self.roll = _wrap(self.roll)
            self.pitch = max(-_HALF_PI + 0.01, min(_HALF_PI - 0.01, self.pitch))

        heading = self._magnetic_heading(magnetometer, self.roll, self.pitch)
        if heading is not None:
            self.heading = heading
            self.yaw += correction * _wrap(heading - self.yaw)
            self.yaw = _wrap(self.yaw)
        self._update_quaternion()
        return self.q

    def get_attitude(self):
        """Return yaw, pitch, and roll in degrees."""
        return (
            math.degrees(self.yaw) % 360.0,
            math.degrees(self.pitch),
            math.degrees(self.roll),
        )

    def get_heading(self):
        """Return the latest tilt-compensated magnetic heading in degrees."""
        return math.degrees(self.heading) % 360.0
