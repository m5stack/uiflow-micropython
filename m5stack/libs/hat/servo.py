# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
"""
@File    :   servo.py
@Time    :   2024/5/7
@Author  :   TONG YIHAN
@E-mail  :   icyqwq@gmail.com
@License :   (C)Copyright 2015-2024, M5STACK
"""

# Import necessary libraries
from machine import PWM
import math


class ServoHat:
    """! SERVO HAT as the name suggests, is a servo motor module with the new and upgraded "ES9251II" digital servo

    @en SERVO HAT as the name suggests, is a servo motor module with the new and upgraded "ES9251II" digital servo,This comes with 145°±10° range of motion and can be controlled by PWM signals. The signal pin of the hat is connected to G26 on M5StickC.
    @cn SERVO HAT正如其名，是一个带有新升级的“ES9251II”数字舵机的舵机模块，具有145°±10°的运动范围，可以通过PWM信号控制。帽子的信号引脚连接到M5StickC上的G26。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/hat/hat-servo
    @image https://static-cdn.m5stack.com/resource/docs/products/hat/hat-servo/hat-servo_01.webp
    @category hat

    @example
        from hardware import *
        from hat import ServoHat
        servo = ServoHat((26, 0))
        servo.set_duty(100)
        servo.set_percent(50)

    """

    def __init__(self, port: tuple) -> None:
        """! Initialize the Servo.

        @param port The port to which the Servo is connected. port[0]: servo pin
        """
        self.min_duty = 26
        self.max_duty = 127
        self.port = port
        self.pwm = PWM(port[0], freq=50)

    def set_duty(self, duty: int) -> None:
        """! Set the duty cycle.

        @en %1 Set the duty cycle to %2.
        @cn %1 将占空比设置为%2。

        @param duty The duty cycle. from 26 to 127.
        """
        duty = min(self.max_duty, max(self.min_duty, duty))
        self.pwm.duty(duty)

    def set_percent(self, percent: int) -> None:
        """! Set the clamping percentage.

        @en %1 Set the clamping percentage to %2.
        @cn %1 将夹持百分比设置为%2。

        @param percent The clamping percentage. from 0 to 100.
        """
        percent = min(100, max(0, percent))
        duty = self.min_duty + (self.max_duty - self.min_duty) * percent / 100
        self.pwm.duty(int(duty))

    def deinit(self):
        """! Deinitialize the Servo.

        @en %1 Deinitialize the Servo.
        @cn %1 取消初始化舵机。

        """
        self.pwm.deinit()
