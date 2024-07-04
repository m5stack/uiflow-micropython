# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-FileCopyrightText: Copyright (c) 2020 Mika Tuupola
#
# SPDX-License-Identifier: MIT


from machine import I2C
from .pahub import PAHUBUnit
from .unit_helper import UnitError
from driver.mpu6886 import MPU6886
import math
import time

MPU6886_ADDR = 0x68

# Constants for unit conversion
SF_G = 1
SF_M_S2 = 9.80665  # 1 g = 9.80665 m/s2 ie. standard gravity
SF_DEG_S = 1
SF_RAD_S = 0.017453292519943  # 1 deg/s is 0.017453292519943 rad/s

ACC_ODR = {2: 0x00, 4: 0x08, 8: 0x10, 16: 0x18}
GYRO_ODR = {250: 0x00, 500: 0x08, 1000: 0x10, 2000: 0x18}


class IMUUnit(MPU6886):
    def __init__(self, i2c: I2C | PAHUBUnit, address: int | list | tuple = MPU6886_ADDR) -> None:
        #! Initializes Gyro, Accelerometer using default values.
        self._i2c = i2c
        if address not in self._i2c.scan():
            raise UnitError("IMU unit maybe not found in Grove")

        super().__init__(self._i2c)

        # for attitude computing
        self.accCoef = 0.02
        self.gyroCoef = 0.98
        self.angleGyroX = 0
        self.angleGyroY = 0
        self.angleGyroZ = 0
        self.angleX = 0
        self.angleZ = 0
        self.angleY = 0
        self.gyroXoffset = 0
        self.gyroYoffset = 0
        self.gyroZoffset = 0
        self.preInterval = time.ticks_us()

    def set_accel_range(self, accel_scale) -> None:
        # Set accelerometer scale and range.
        self._accel_so = self._accel_fs(ACC_ODR.get(accel_scale))

    def set_gyro_range(self, gyro_scale) -> None:
        #! Set gyroscope scale and range.
        self._gyro_so = self._gyro_fs(GYRO_ODR.get(gyro_scale))

    def set_accel_unit(self, unit) -> None:
        #! Set accelerometer unit g or m/s^2
        self._accel_sf = SF_M_S2 if unit else SF_G

    def set_gyro_unit(self, unit) -> None:
        #! Set gyroscope unit rad/sec or degrees/sec
        self._gyro_sf = SF_RAD_S if unit else SF_DEG_S

    def set_gyro_calibrate(self, samples=256, delay=5) -> None:
        #! Set the gyro calibrations with samples.
        offset = self.calibrate(samples, delay)
        self.gyroXoffset = offset[0]
        self.gyroYoffset = offset[1]
        self.gyroZoffset = offset[2]

    def set_gyro_offsets(self, x, y, z) -> None:
        #! Set the gyro offsets for attitude computing.
        self.gyroXoffset = x
        self.gyroYoffset = y
        self.gyroZoffset = z

    def get_gyroscope(self) -> tuple:
        #! Returns gyroscope vector in rad/sec.
        return self.gyro()

    def get_accelerometer(self) -> tuple:
        #! Returns acceleration vector in gravity units (9.81m/s^2).
        return self.acceleration()

    def get_attitude(self) -> tuple:
        # !Attitude angles as yaw, pitch, and roll in degrees.
        (
            accX,  # noqa: N806
            accY,  # noqa: N806
            accZ,  # noqa: N806
        ) = self.get_accelerometer()  # Get processed acceleration data

        # Compute tilt angles from the accelerometer data
        angleAccX = math.atan2(accY, accZ + abs(accX)) * (SF_DEG_S / SF_RAD_S)  # noqa: N806
        angleAccY = math.atan2(accX, accZ + abs(accY)) * (-SF_DEG_S / SF_RAD_S)  # noqa: N806

        # Get processed gyro data and remove offsets
        gyroX, gyroY, gyroZ = self.get_gyroscope()  # noqa: N806
        gyroX -= self.gyroXoffset  # noqa: N806
        gyroY -= self.gyroYoffset  # noqa: N806
        gyroZ -= self.gyroZoffset  # noqa: N806

        # Calculate the time elapsed since the last measurement
        interval = (time.ticks_us() - self.preInterval) / 1000000
        self.preInterval = time.ticks_us()

        # Compute the change in angles from the gyro data
        self.angleGyroX += gyroX * interval
        self.angleGyroY += gyroY * interval
        self.angleGyroZ += gyroZ * interval

        # Combine accelerometer and gyro angles using complementary filter
        self.angleX = (self.gyroCoef * (self.angleX + gyroX * interval)) + (
            self.accCoef * angleAccX
        )
        self.angleY = (self.gyroCoef * (self.angleY + gyroY * interval)) + (
            self.accCoef * angleAccY
        )
        self.angleZ = self.angleGyroZ  # Z angle is taken from the gyro only

        return tuple([round(self.angleZ, 3), round(angleAccX, 3), round(angleAccY, 3)])
