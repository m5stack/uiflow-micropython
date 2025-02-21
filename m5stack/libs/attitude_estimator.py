# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import math
import time


class AttitudeEstimator:
    def __init__(self):
        self.gyro_x_offset = 0.0
        self.gyro_y_offset = 0.0
        self.gyro_z_offset = 0.0
        self.angle_gyro_x = 0.0
        self.angle_gyro_y = 0.0
        self.angle_gyro_z = 0.0
        self.angle_x = 0.0
        self.angle_y = 0.0
        self.angle_z = 0.0
        self.pre_interval = 0.0
        self.gyro_coef = 0.98
        self.acc_coef = 0.02

    def calibrate_gyro(self, read_gyro_func, sample_count=100, delay=0.01):
        sum_gx = 0.0
        sum_gy = 0.0
        sum_gz = 0.0

        print("Starting gyroscope calibration, please keep the sensor stationary...")
        for i in range(sample_count):
            gx, gy, gz = read_gyro_func()
            sum_gx += gx
            sum_gy += gy
            sum_gz += gz
            time.sleep(delay)

        self.gyro_x_offset = sum_gx / sample_count
        self.gyro_y_offset = sum_gy / sample_count
        self.gyro_z_offset = sum_gz / sample_count

        print("Gyroscope calibration completed:")
        print("gyro_x_offset = {:.2f} °/s".format(self.gyro_x_offset))
        print("gyro_y_offset = {:.2f} °/s".format(self.gyro_y_offset))
        print("gyro_z_offset = {:.2f} °/s".format(self.gyro_z_offset))

    def update_attitude(self, gx, gy, gz, ax, ay, az, dt):
        """
        Update attitude angles (fusing accelerometer and gyroscope data)

        :param gx: Gyroscope X-axis angular velocity (°/s)
        :param gy: Gyroscope Y-axis angular velocity (°/s)
        :param gz: Gyroscope Z-axis angular velocity (°/s)
        :param ax: Accelerometer X-axis acceleration (m/s²)
        :param ay: Accelerometer Y-axis acceleration (m/s²)
        :param az: Accelerometer Z-axis acceleration (m/s²)
        :param dt: Sampling time interval (seconds)
        """
        angle_acc_x = math.atan2(ay, az + abs(ax)) * 360 / (2 * math.pi)
        angle_acc_y = math.atan2(ax, az + abs(ay)) * 360 / (-2 * math.pi)

        gyro_x = gx - self.gyro_x_offset
        gyro_y = gy - self.gyro_y_offset
        gyro_z = gz - self.gyro_z_offset

        self.angle_gyro_x += gyro_x * dt
        self.angle_gyro_y += gyro_y * dt
        self.angle_gyro_z += gyro_z * dt

        self.angle_x = (self.gyro_coef * (self.angle_x + gyro_x * dt)) + (
            self.acc_coef * angle_acc_x
        )
        self.angle_y = (self.gyro_coef * (self.angle_y + gyro_y * dt)) + (
            self.acc_coef * angle_acc_y
        )
        self.angle_z = self.angle_gyro_z
        self.angle_z = (self.angle_z + 360) % 360

        self.pre_interval += dt

    def get_angles(self):
        return self.angle_x, self.angle_y, self.angle_z
