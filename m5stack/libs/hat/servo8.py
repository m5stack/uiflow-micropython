# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
"""
@File    :   servo8.py
@Time    :   2024/4/28
@Author  :   TONG YIHAN
@E-mail  :   icyqwq@gmail.com
@License :   (C)Copyright 2015-2024, M5STACK
"""

# Import necessary libraries
from machine import I2C
import struct
import time


class Servos8Hat:
    """! 8Servos HAT v1.1 is an 8-channel servo driver module that works with the M5StickC/C Plus series.

    @en 8Servos HAT v1.1 is an 8-channel servo driver module that works with the M5StickC/C Plus series. Adopt STM32F030F4 as main controller to drive servos with PWM (Pulse Width Modulation) signal. I2C communication. Embedded power management circuit to control servo ON/OFF with programming. With the rechargeable 16340 lithium battery (with the capacity of 700mAh),It also supports 18350 lithium batteries, it can support Maximum 1.3A load. Applied for robotic and DIY projects.
    @cn 8Servos HAT v1.1 是一款8通道舵机驱动模块，适用于M5StickC/C Plus系列。采用STM32F030F4作为主控制器，通过PWM（脉宽调制）信号驱动舵机。I2C通信。内置电源管理电路，可通过编程控制舵机的开关。配备可充电的16340锂电池（容量为700mAh），也支持18350锂电池，最大支持1.3A负载。适用于机器人和DIY项目。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/hat/hat_8servos_1.1
    @image https://static-cdn.m5stack.com/resource/docs/products/hat/hat_8servos_1.1/hat_8servos_1.1_01.webp
    @category hat

    @example
        from hardware import *
        from hat import Servos8Hat
        i2c = I2C(0, scl=Pin(26), sda=Pin(0), freq=100000)
        servo = Servos8Hat(i2c, 0x36)
        servo.power_on()
        for i in range(1, 9):
            servo.write_servo_angle(i, 90)
        servo.power_off()
        servo.get_power_state()

    """

    SERVO_ANGLE_REG = 0x00
    SERVO_PULSE_REG = 0x10
    POWER_CTRL_REG = 0x30

    def __init__(self, i2c: I2C, address: int | list | tuple = 0x36) -> None:
        """! Initialize the Servo8.

        @param i2c I2C port to use.
        @param address I2C address of the servo8.
        """
        self.i2c = i2c
        self.addr = address
        self._available()

    def _available(self) -> None:
        """! Check if sensor is available on the I2C bus.

        Raises:
            Exception: If the sensor is not found.
        """
        if self.addr not in self.i2c.scan():
            raise Exception("Servo8 Hat not found, please check your connection.")

    def write_servo_angle(self, ch, angle) -> None:
        """! Set the angle of the servo.

        @en %1 Set the angle of channel %2 to %3.
        @cn %1 设置通道%2的角度为%3

        @param ch The channel (1 to 8) of the servo.
        @param angle The angle (0 to 180) of the servo.
        """
        ch = int(min(8, ch))
        ch = int(max(1, ch))
        angle = int(min(180, angle))
        angle = int(max(0, angle))
        ch -= 1
        self.write_reg_data(self.SERVO_ANGLE_REG + ch, [angle])

    def read_servo_angle(self, ch) -> int:
        """! Read the angle of the servo.

        @en %1 Read the angle of channel %2.
        @cn %1 读取通道%2的角度。

        @param ch The channel (1 to 8) of the servo.
        @return: The angle (0 to 180) of the servo.
        """
        ch = int(min(8, ch))
        ch = int(max(1, ch))
        ch -= 1
        return self.read_reg_data(self.SERVO_ANGLE_REG + ch, 1)[0]

    def write_servo_pulse(self, ch, pulse) -> None:
        """! Set the pulse of the servo.

        @en %1 Set the pulse width of channel %2 to %3.
        @cn %1 设置通道%2的脉宽为%3。

        @param ch The channel (1 to 8) of the servo.
        @param pulse The pulse (500 to 2500) of the servo.
        """
        ch = int(min(8, ch))
        ch = int(max(1, ch))
        pulse = int(min(2500, pulse))
        pulse = int(max(500, pulse))
        ch -= 1
        data = list(struct.pack(">h", pulse))
        self.write_reg_data((self.SERVO_PULSE_REG + ch * 2), data)

    def read_servo_pulse(self, ch) -> int:
        """! Read the pulse of the servo.

        @en %1 Read the pulse width of channel %2.
        @cn %1 读取通道%2的脉宽。

        @param ch The channel (1 to 8) of the servo.
        @return: The pulse (500 to 2500) of the servo.
        """
        ch = int(min(8, ch))
        ch = int(max(1, ch))
        ch -= 1
        buf = self.read_reg_data((self.SERVO_PULSE_REG + ch * 2), 2)
        return struct.unpack(">h", buf)[0]

    def power_ctrl(self, state) -> None:
        """! Control the power of the servo.

        @en %1 Set the power of the servo to %2.
        @cn %1 设置舵机的电源为%2。

        @param state [field_switch] The state of the power, 0 for OFF and 1 for ON.
        """
        if state:
            state = 1
        else:
            state = 0
        self.write_reg_data(self.POWER_CTRL_REG, [state])

    def power_on(self) -> None:
        """! Turn on the power of the servo.

        @en %1 Turn on the power of the servo.
        @cn %1 打开舵机的电源。
        """
        self.power_ctrl(1)

    def power_off(self) -> None:
        """! Turn off the power of the servo.

        @en %1 Turn off the power of the servo.
        @cn %1 关闭舵机的电源。
        """
        self.power_ctrl(0)

    def get_power_state(self) -> int:
        """! Get the state of the power of the servo.

        @en %1 Get the state of the power of the servo.
        @cn %1 获取舵机的电源状态。
        @return: The state of the power of the servo.
        """
        return self.read_reg_data(self.POWER_CTRL_REG, 1)[0]

    def read_reg_data(self, reg: int = 0, num: int = 0) -> bytearray:
        buf = bytearray(1)
        buf[0] = reg
        time.sleep_ms(1)
        self.i2c.writeto(self.addr, buf)
        buf = bytearray(num)
        self.i2c.readfrom_into(self.addr, buf)
        return buf

    def write_reg_data(self, reg, byte_lst):
        buf = bytearray(1 + len(byte_lst))
        buf[0] = reg
        buf[1:] = bytes(byte_lst)
        time.sleep_ms(1)
        self.i2c.writeto(self.addr, buf)
