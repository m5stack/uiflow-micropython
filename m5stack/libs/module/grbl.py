# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .mbus import i2c1
from .module_helper import ModuleError
from micropython import const
import re
import math
import time


class GRBLModule:
    """

    note:
        cn: GRBL 13.2 是 M5Stack 堆叠模块系列中的三轴步进电机驱动器模块。它采用 ATmega328P-AU 控制器，带有三组 DRV8825PWPR 步进电机驱动芯片控制方式，可以同时驱动三个双极步进电机。
        en: GRBL 13.2 is a three-axis stepper motor driver module in the M5Stack stacking module series. It uses an ATmega328P-AU controller with three sets of DRV8825PWPR stepper motor driver chip control ways, which can drive three bipolar steppers at the same time.

    details:
        color: "#0FE6D7"
        link: https://docs.m5stack.com/en/module/grbl13.2
        image: https://static-cdn.m5stack.com/resource/docs/products/module/grbl13.2/grbl13.2_01.webp
        category: Module

    example:
        - ../../../examples/module/grbl_example.py

    m5f2:
        - module/grbl_example.m5f2


    """

    """
    constant: Motor mode
    """
    MODE_ABSOLUTE = const(0)
    MODE_RELATIVE = const(1)

    def __init__(
        self,
        address: int = 0x70,
    ):
        """
        note:
            en: Initialize the GRBLModule.
            cn: 初始化GRBL模块。

        params:
            address:
                note: The I2C address of the device.
        """

        self.i2c = i2c1
        self.addr = address

        # Check if the devices are connected and accessible
        if self.addr not in self.i2c.scan():
            raise ModuleError("GRBLModule not found at I2C address 0x%02X" % self.addr)

        self.mode = self.MODE_ABSOLUTE
        self.last_speed = 300

    def g_code(self, command):
        """
        note:
            en: Send the G-code command.
            cn: 发送G代码命令。

        params:
            command:
                note: The G-code command.
        """
        self.i2c.writeto(self.addr, command + "\n")
        return self.get_code_time(command)

    def get_code_time(self, code) -> int:
        """
        note:
            en: Get the time of the code.
            cn: 获取代码的时间。

        params:
            code:
                note: The G-code command

        return:
            note: The estimated time of the command.

        """
        x_value = re.search(r"X-*\d+", code)
        y_value = re.search(r"Y-*\d+", code)
        z_value = re.search(r"Z-*\d+", code)
        speed = re.search(r"F\d+", code)
        hold = re.search(r"P\d+", code)
        hold = float(hold.group(0)[1:]) * 1000 if hold else 0
        x_value = int(x_value.group(0)[1:]) if x_value else 0
        y_value = int(y_value.group(0)[1:]) if y_value else 0
        z_value = int(z_value.group(0)[1:]) if z_value else 0
        self.last_speed = int(speed.group(0)[1:]) if speed else self.last_speed
        time = (
            math.sqrt(x_value * x_value + y_value * y_value + z_value * z_value)
            * 60
            * 1000
            / self.last_speed
        )
        time += hold
        return int(time)

    def turn(self, x=None, y=None, z=None, speed=None) -> int:
        """
        note:
            en: Turn the motor to a specific position.
            cn: 将电机转到特定位置。

        params:
            x:
                note: The position of the X motor, 1.6=360°.
            y:
                note: The position of the Y motor, 1.6=360°.
            z:
                note: The position of the Z motor, 1.6=360°.
            speed:
                note: The speed of the motor.
        """
        command = "G1"
        command += " X{}".format(x) if x is not None else ""
        command += " Y{}".format(y) if y is not None else ""
        command += " Z{}".format(z) if z is not None else ""
        command += " F{}".format(speed) if speed else ""
        self.last_speed = speed if speed else self.last_speed
        return self.g_code(command)

    def set_mode(self, mode):
        """
        note:
            en: Set the mode of the motor.
            cn: 设置电机的模式。

        params:
            mode:
                note: The mode of the motor.
                field: dropdown
                options:
                    Absolute: GRBLModule.MODE_ABSOLUTE
                    Relative: GRBLModule.MODE_RELATIVE
        """
        self.mode = mode
        if mode == self.MODE_ABSOLUTE:
            return self.g_code("G90")
        else:
            return self.g_code("G91")

    def init(self, x_step=None, y_step=None, z_step=None, acc=None):
        """
        note:
            en: Initialize the motor.
            cn: 初始化电机。

        params:
            x_step:
                note: The step of the X motor.
            y_step:
                note: The step of the Y motor.
            z_step:
                note: The step of the Z motor.
            acc:
                note: The acceleration of the motor.
        """
        if x_step:
            self.i2c.writeto(self.addr, "$0={}\n".format(x_step))
            time.sleep(0.01)
        if y_step:
            self.i2c.writeto(self.addr, "$1={}\n".format(y_step))
            time.sleep(0.01)
        if z_step:
            self.i2c.writeto(self.addr, "$2={}\n".format(z_step))
            time.sleep(0.01)
        if acc:
            self.i2c.writeto(self.addr, "$8={}\n".format(acc))

    def flush(self):
        """
        note:
            en: Flush the buffer.
            cn: 清空缓冲区。
        """
        while True:
            data = self.i2c.readfrom(self.addr, 10)
            if data[-1] == 255:
                break

    def get_message(self) -> str:
        """
        note:
            en: Get the message.
            cn: 获取消息。
        return:
            note: The message string.
        """
        i2c_data = ""
        while True:
            data = self.i2c.readfrom(self.addr, 10)
            if data[-1] == 255:
                i2c_data += data[: data.find(b"\x00")].decode()
                break
            i2c_data += data.decode()
        return i2c_data

    def get_status(self) -> str:
        """
        note:
            en: Get the status.
            cn: 获取状态。
        return:
            note: The status string.
        """
        self.flush()
        self.i2c.writeto(self.addr, "@")
        return self.get_message()

    def get_idle_state(self) -> bool:
        """
        note:
            en: Get the idle state.
            cn: 获取空闲状态。
        return:
            note: The idle state.
        """
        return self.get_status()[0] == "I"

    def get_lock_state(self) -> bool:
        """
        note:
            en: Get the lock state.
            cn: 获取锁定状态。
        return:
            note: The lock state.
        """
        return self.get_status()[0] == "A"

    def wait_idle(self):
        """
        note:
            en: Wait until the motor is idle.
            cn: 等待电机空闲。
        """
        self.flush()
        while not self.get_idle_state():
            time.sleep(0.1)

    def unlock_alarm_state(self):
        """
        note:
            en: Unlock the alarm state.
            cn: 解锁报警状态。
        """
        self.i2c.writeto(self.addr, b"\x18")
        time.sleep(0.01)
        self.i2c.writeto(self.addr, "$X\r\n")

    def lock(self):
        """
        note:
            en: Lock the motor.
            cn: 锁定电机。
        """
        self.g_code("$7=255")

    def unlock(self):
        """
        note:
            en: Unlock the motor.
            cn: 解锁电机。
        """
        self.g_code("$7=25")
