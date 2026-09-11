# SPDX-FileCopyrightText: 2017 Peter Hinch
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

"""Allocation-conscious Madgwick 6DoF and 9DoF sensor fusion."""

import math


class Madgwick:
    def __init__(self, beta=0.1):
        self.beta = beta
        self.q = (1.0, 0.0, 0.0, 0.0)

    def reset(self):
        self.q = (1.0, 0.0, 0.0, 0.0)

    def set_beta(self, beta):
        if beta < 0:
            raise ValueError("beta must be non-negative")
        self.beta = beta

    @staticmethod
    def _normalise(values):
        norm_sq = sum(value * value for value in values)
        if norm_sq <= 0.0 or not math.isfinite(norm_sq):
            return None
        scale = 1.0 / math.sqrt(norm_sq)
        return tuple(value * scale for value in values)

    def _integrate(self, q1, q2, q3, q4, qdot, dt):
        q1 += qdot[0] * dt
        q2 += qdot[1] * dt
        q3 += qdot[2] * dt
        q4 += qdot[3] * dt
        normalised = self._normalise((q1, q2, q3, q4))
        if normalised is not None:
            self.q = normalised
        return self.q

    def update_imu(self, accel, gyro, dt):
        """Advance 6DoF fusion. Gyroscope input is degrees per second."""
        normalised = self._normalise(accel)
        if normalised is None:
            return self.q
        ax, ay, az = normalised
        gx, gy, gz = (math.radians(value) for value in gyro)
        q1, q2, q3, q4 = self.q

        qdot = [
            0.5 * (-q2 * gx - q3 * gy - q4 * gz),
            0.5 * (q1 * gx + q3 * gz - q4 * gy),
            0.5 * (q1 * gy - q2 * gz + q4 * gx),
            0.5 * (q1 * gz + q2 * gy - q3 * gx),
        ]

        q1q1, q2q2, q3q3, q4q4 = q1 * q1, q2 * q2, q3 * q3, q4 * q4
        step = (
            4 * q1 * q3q3 + 2 * q3 * ax + 4 * q1 * q2q2 - 2 * q2 * ay,
            4 * q2 * q4q4
            - 2 * q4 * ax
            + 4 * q1q1 * q2
            - 2 * q1 * ay
            - 4 * q2
            + 8 * q2 * q2q2
            + 8 * q2 * q3q3
            + 4 * q2 * az,
            4 * q1q1 * q3
            + 2 * q1 * ax
            + 4 * q3 * q4q4
            - 2 * q4 * ay
            - 4 * q3
            + 8 * q3 * q2q2
            + 8 * q3 * q3q3
            + 4 * q3 * az,
            4 * q2q2 * q4 - 2 * q2 * ax + 4 * q3q3 * q4 - 2 * q3 * ay,
        )
        step = self._normalise(step)
        if step is not None:
            for index in range(4):
                qdot[index] -= self.beta * step[index]
        return self._integrate(q1, q2, q3, q4, qdot, dt)

    def update(self, accel, gyro, magnetometer, dt):
        """Advance 9DoF fusion. Gyroscope input is degrees per second."""
        accel = self._normalise(accel)
        magnetometer = self._normalise(magnetometer)
        if accel is None:
            return self.q
        if magnetometer is None:
            return self.update_imu(accel, gyro, dt)

        ax, ay, az = accel
        mx, my, mz = magnetometer
        gx, gy, gz = (math.radians(value) for value in gyro)
        q1, q2, q3, q4 = self.q
        q1q1, q1q2, q1q3, q1q4 = q1 * q1, q1 * q2, q1 * q3, q1 * q4
        q2q2, q2q3, q2q4 = q2 * q2, q2 * q3, q2 * q4
        q3q3, q3q4, q4q4 = q3 * q3, q3 * q4, q4 * q4

        _2q1, _2q2, _2q3, _2q4 = 2 * q1, 2 * q2, 2 * q3, 2 * q4
        _2q1q3, _2q3q4 = 2 * q1q3, 2 * q3q4
        _2q1mx, _2q1my, _2q1mz = 2 * q1 * mx, 2 * q1 * my, 2 * q1 * mz
        _2q2mx = 2 * q2 * mx
        hx = (
            mx * q1q1
            - _2q1my * q4
            + _2q1mz * q3
            + mx * q2q2
            + _2q2 * my * q3
            + _2q2 * mz * q4
            - mx * q3q3
            - mx * q4q4
        )
        hy = (
            _2q1mx * q4
            + my * q1q1
            - _2q1mz * q2
            + _2q2mx * q3
            - my * q2q2
            + my * q3q3
            + _2q3 * mz * q4
            - my * q4q4
        )
        _2bx = math.sqrt(hx * hx + hy * hy)
        _2bz = (
            -_2q1mx * q3
            + _2q1my * q2
            + mz * q1q1
            + _2q2mx * q4
            - mz * q2q2
            + _2q3 * my * q4
            - mz * q3q3
            + mz * q4q4
        )
        _4bx, _4bz = 2 * _2bx, 2 * _2bz

        f1 = 2 * q2q4 - _2q1q3 - ax
        f2 = 2 * q1q2 + _2q3q4 - ay
        f3 = 1 - 2 * q2q2 - 2 * q3q3 - az
        f4 = _2bx * (0.5 - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx
        f5 = _2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my
        f6 = _2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz
        step = (
            -_2q3 * f1
            + _2q2 * f2
            - _2bz * q3 * f4
            + (-_2bx * q4 + _2bz * q2) * f5
            + _2bx * q3 * f6,
            _2q4 * f1
            + _2q1 * f2
            - 4 * q2 * f3
            + _2bz * q4 * f4
            + (_2bx * q3 + _2bz * q1) * f5
            + (_2bx * q4 - _4bz * q2) * f6,
            -_2q1 * f1
            + _2q4 * f2
            - 4 * q3 * f3
            + (-_4bx * q3 - _2bz * q1) * f4
            + (_2bx * q2 + _2bz * q4) * f5
            + (_2bx * q1 - _4bz * q3) * f6,
            _2q2 * f1
            + _2q3 * f2
            + (-_4bx * q4 + _2bz * q2) * f4
            + (-_2bx * q1 + _2bz * q3) * f5
            + _2bx * q2 * f6,
        )

        qdot = [
            0.5 * (-q2 * gx - q3 * gy - q4 * gz),
            0.5 * (q1 * gx + q3 * gz - q4 * gy),
            0.5 * (q1 * gy - q2 * gz + q4 * gx),
            0.5 * (q1 * gz + q2 * gy - q3 * gx),
        ]
        step = self._normalise(step)
        if step is not None:
            for index in range(4):
                qdot[index] -= self.beta * step[index]
        return self._integrate(q1, q2, q3, q4, qdot, dt)
