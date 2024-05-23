# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
"""
@File    :   catch.py
@Time    :   2024/5/7
@Author  :   TONG YIHAN
@E-mail  :   icyqwq@gmail.com
@License :   (C)Copyright 2015-2024, M5STACK
"""

# Import necessary libraries
from machine import PWM
import math


class CatchUnit:
    """! Catch is a gripper that uses a SG92R servo as a power source.

    @en Catch is a gripper that uses a SG92R servo as a power source. The servo uses a PWM signal to drive the gripper gear to rotate and control the gripper for clamping and releasing operations. The structure adopts a design compatible with Lego 8mm round holes. You can combine it with other Lego components to build creative control structures, such as robotic arms, gripper carts, etc.
    @cn Catch是一个使用SG92R舵机作为动力源的夹爪。舵机使用PWM信号驱动夹爪齿轮旋转，控制夹爪进行夹持和释放操作。结构采用与乐高8mm圆孔兼容的设计。您可以将其与其他乐高组件组合在一起，构建创意控制结构，例如机械臂，夹持车等。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/unit/catch
    @image https://static-cdn.m5stack.com/resource/docs/products/unit/catch/catch_01.webp
    @category unit

    @example
        from hardware import *
        from unit import CatchUnit
        catch = CatchUnit((33, 32))
        catch.clamp()
        catch.release()
        catch.set_duty(30)
        catch.set_clamp_percent(50)

    """

    def __init__(self, port: tuple) -> None:
        """! Initialize the Servo.

        @param port The port to which the Servo is connected. port[1]: servo pin
        """
        self.max_duty = 54
        self.min_duty = 20
        self.port = port
        self.pwm = PWM(port[1], freq=50)

    def clamp(self) -> None:
        """! Clamp the gripper.

        @en %1 Clamp the gripper.
        @cn %1 夹住夹爪。
        """
        self.pwm.duty(self.max_duty)

    def release(self) -> None:
        """! Release the gripper.

        @en %1 Release the gripper.
        @cn %1 释放夹爪。
        """
        self.pwm.duty(self.min_duty)

    def set_duty(self, duty: int) -> None:
        """! Set the duty cycle.

        @en %1 Set the duty cycle to %2.
        @cn %1 将占空比设置为%2。

        @param duty The duty cycle. from 20 to 54.
        """
        duty = min(self.max_duty, max(self.min_duty, duty))
        self.pwm.duty(duty)

    def set_clamp_percent(self, percent: int) -> None:
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
