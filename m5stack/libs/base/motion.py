# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
"""
@File    :   motion.py
@Time    :   2024/4/28
@Author  :   TONG YIHAN
@E-mail  :   icyqwq@gmail.com
@License :   (C)Copyright 2015-2024, M5STACK
"""

# Import necessary libraries
from machine import I2C
import struct
from driver.ina226 import INA226


class Motion:
    """! Atomic Motion Base is a servo and DC motor driver designed specifically for the ATOM series controllers.

    @en Atomic Motion Base is a servo and DC motor driver designed specifically for the ATOM series controllers. It integrates an STM32 control chip internally and uses I2C communication for control. Atomic Motion Base provides 4 servo channels and 2 DC motor interfaces, offering convenience for scenarios that require control of multiple servos or motor drivers, such as multi-axis servo robotic arms or small car motor control.
    @cn Atomic Motion Base是专为ATOM系列控制器设计的舵机和直流电机驱动器。它内部集成了STM32控制芯片，并使用I2C通信进行控制。Atomic Motion Base提供4个舵机通道和2个直流电机接口，为需要控制多个舵机或电机驱动器的场景提供了便利，如多轴舵机机械臂或小型车辆电机控制。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/atom/Atomic%20Motion%20Base
    @image https://static-cdn.m5stack.com/resource/docs/products/atom/Atomic%20Motion%20Base/img-40a0d2ba-04b3-4aa3-8417-0624762b3cc3.webp
    @category base

    @example
        from base import Motion
        from hardware import *
        i2c0 = I2C(0, scl=Pin(21), sda=Pin(25), freq=100000)
        motion = Motion(i2c0)
        motion.set_servo_angle(1, 90)

    """

    def __init__(self, i2c: I2C, address: int | list | tuple = 0x38) -> None:
        """! Initialize the Servo8.

        @param i2c I2C port to use.
        @param address I2C address of the servo8.
        """
        self.i2c = i2c
        self.addr = address
        self._available()
        self.ina = None
        self.addr_ina266 = 0x40
        if self.addr_ina266 in self.i2c.scan():
            self.ina = INA226(
                self.i2c, addr=self.addr_ina266, shunt_resistor=0.02
            )  # shunt resistor 20mΩ
            self.ina.configure(
                avg=self.ina.CFG_AVGMODE_16SAMPLES,
                vbus_conv_time=self.ina.CFG_VBUSCT_1100us,
                vshunt_conv_time=self.ina.CFG_VSHUNTCT_1100us,
                mode=self.ina.CFG_MODE_SANDBVOLT_CONTINUOUS,
            )
            self.ina.calibrate(max_expected_current=3.6)  # max expected current 3.6A

    def _available(self) -> None:
        """! Check if sensor is available on the I2C bus.

        Raises:
            Exception: If the sensor is not found.
        """
        if self.addr not in self.i2c.scan():
            raise Exception("Motion Base not found, please check your connection.")

    def get_servo_angle(self, ch) -> int:
        """! Get the angle of the servo.

        @en %1 Get the angle of channel %2.
        @cn %1 获取通道%2的角度。

        @param ch Servo channel (1 to 4).
        @return Angle of the servo (0 to 180).
        """
        ch = int(min(4, ch))
        ch = int(max(1, ch))
        ch -= 1
        return self.i2c.readfrom_mem(self.addr, ch, 1)[0]

    def set_servo_angle(self, ch, angle) -> None:
        """! Set the angle of the servo.

        @en %1 Set the angle of channel %2 to %3.
        @cn %1 设置通道%2的角度为3%。

        @param ch Servo channel (1 to 4).
        @param angle Angle of the servo (0 to 180).
        """
        ch = int(min(4, ch))
        ch = int(max(1, ch))
        ch -= 1
        angle = int(min(180, angle))
        angle = int(max(0, angle))
        self.i2c.writeto_mem(self.addr, ch, struct.pack("b", angle))

    def get_servo_pulse(self, ch) -> int:
        """! Get the pulse width of the servo.

        @en %1 Get the pulse width of channel %2.
        @cn %1 获取通道%2的脉冲宽度。

        @param ch Servo channel (1 to 4).
        @return Pulse width of the servo (500 to 2500).
        """
        ch = int(min(4, ch))
        ch = int(max(1, ch))
        ch -= 1
        return struct.unpack(">h", self.i2c.readfrom_mem(self.addr, ch * 2 + 0x10, 2))[0]

    def write_servo_pulse(self, ch, pulse) -> None:
        """! Set the pulse width of the servo.

        @en %1 Set the pulse width of channel %2 to %3.
        @cn %1 设置通道%2的脉宽为%3。

        @param ch Servo channel (1 to 4).
        @param pulse Pulse width of the servo (500 to 2500).
        """
        ch = int(min(4, ch))
        ch = int(max(1, ch))
        ch -= 1
        pulse = int(min(2500, pulse))
        pulse = int(max(500, pulse))
        self.i2c.writeto_mem(self.addr, ch * 2 + 0x10, struct.pack(">h", pulse))

    def get_motor_speed(self, ch) -> int:
        """! Get the speed of the motor.

        @en %1 Get the speed of motor %2.
        @cn %1 获取电机%2的速度。

        @param ch Motor channel (1 or 2).
        @return Speed of the motor (0 to 255).
        """
        ch = int(min(2, ch))
        ch = int(max(1, ch))
        ch -= 1
        speed = self.i2c.readfrom_mem(self.addr, ch + 0x20, 1)[0]
        if speed > 128:
            return speed - 256
        return speed

    def set_motor_speed(self, ch, speed) -> None:
        """! Set the speed of the motor.

        @en %1 Set the speed of motor %2 to %3.
        @cn %1 设置电机%2的速度为%3。

        @param ch Motor channel (1 or 2).
        @param speed Speed of the motor (-127 to 127).
        """
        ch = int(min(2, ch))
        ch = int(max(1, ch))
        ch -= 1
        speed = int(min(127, speed))
        speed = int(max(-127, speed))
        self.i2c.writeto_mem(self.addr, ch + 0x20, struct.pack("b", speed))

    def read_voltage(self):
        """
        read bus voltage (unit: V)
        """
        return self.ina.read_bus_voltage()

    def read_current(self):
        """
        read current (unit: A)
        """
        return self.ina.read_current()

    def read_power(self):
        """
        read power (unit: W)
        """
        return self.ina.read_power()
