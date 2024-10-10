# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .mbus import i2c1
from .module_helper import ModuleError
import struct
from micropython import const
from machine import Pin, PWM


class StepMotorDriverModule:
    """

    note:
        cn: 步进电机驱动模块 13.2 V1.1 是一款适配于 M5 主控的步进电机驱动器，采用 STM32+HR8825 步进电机驱动方案，提供 3 路双极步进电机控制接口。
        en: StepMotor Driver Module 13.2 V1.1 is a stepper motor driver adapted to M5 main control, using STM32+HR8825 stepper motor drive scheme, providing 3-way bipolar stepper motor control interface.

    details:
        color: "#0FE6D7"
        link: https://docs.m5stack.com/en/module/Stepmotor%20Driver%20Module13.2%20v1.1
        image: https://static-cdn.m5stack.com/resource/docs/products/module/Stepmotor%20Driver%20Module13.2%20v1.1/img-c2b8ceac-b6be-4cec-9a15-228fcf8623e7.webp
        category: Module

    example: |
        from module import StepMotorDriverModule
        motor = StepMotorDriverModule(step_pin=(16, 12, 15), dir_pin=(17, 13, 0)) # Core


    """

    """
    constant: Motor IDs
    """
    MOTOR_X = const(0)
    MOTOR_Y = const(1)
    MOTOR_Z = const(2)

    """
    constant: Motor states
    """
    MOTOR_STATE_ENABLE = const(1)
    MOTOR_STATE_DISABLE = const(0)

    """
    constant: Register addresses
    """
    INPUT_REG = const(0x00)
    OUTPUT_REG = const(0x01)
    POLINV_REG = const(0x02)
    CONFIG_REG = const(0x03)
    FAULT_REG = const(0x04)
    RESET_REG = const(0x05)
    FIRM_REG = const(0xFE)
    I2C_REG = const(0xFF)

    """
    constant: Microstep values
    """
    STEP_FULL = const(0x00)
    STEP1_2 = const(0x04)
    STEP1_4 = const(0x02)
    STEP1_8 = const(0x06)
    STEP1_16 = const(0x01)
    STEP1_32 = const(0x07)

    def __init__(
        self,
        address: int = 0x27,
        step_pin: tuple | list = (16, 12, 15),
        dir_pin: tuple | list = (17, 13, 0),
    ):
        """
        note:
            en: Initialize the StepMotorDriverModule.
            cn: 初始化步进电机驱动模块。

        params:
            address:
              note: The I2C address of the device.
            step_pin:
              note: The step pin (X, Y, Z) of the motor.
            dir_pin:
              note: The dir pin (X, Y, Z) of the motor.
        """

        self.i2c = i2c1
        self.addr = address

        # Check if the devices are connected and accessible
        if self.addr not in self.i2c.scan():
            raise ModuleError("StepMotorDriverModule not found at I2C address 0x%02X" % self.addr)

        self.set_motor_state(self.MOTOR_STATE_DISABLE)
        self.reset_motor(self.MOTOR_X, 0)
        self.reset_motor(self.MOTOR_Y, 0)
        self.reset_motor(self.MOTOR_Z, 0)
        self.set_microstep(self.STEP_FULL)
        self.pwm_x = PWM(step_pin[0], freq=500, duty=50)
        self.pwm_y = PWM(step_pin[1], freq=500, duty=50)
        self.pwm_z = PWM(step_pin[2], freq=500, duty=50)
        self.dir_x = Pin(dir_pin[0], Pin.OUT, value=1)
        self.dir_y = Pin(dir_pin[1], Pin.OUT, value=1)
        self.dir_z = Pin(dir_pin[2], Pin.OUT, value=1)

    def reset_motor(self, motor_id, state: bool = False):
        """
        note:
            en: Reset the motor.
            cn: 重置电机。

        params:
            motor_id:
              note: The motor to reset.
              field: dropdown
              options:
                X: StepMotorDriverModule.MOTOR_X
                Y: StepMotorDriverModule.MOTOR_Y
                Z: StepMotorDriverModule.MOTOR_Z
            state:
              note: The state of the motor.
              field: switch
        """
        rdata = self.i2c.readfrom_mem(self.addr, self.RESET_REG, 1)
        rdata = struct.unpack("B", rdata)[0]
        if state:
            rdata &= ~(0x01 << motor_id)
        else:
            rdata |= 0x01 << motor_id
        self.i2c.writeto_mem(self.addr, self.RESET_REG, struct.pack("B", rdata))

    def set_motor_state(self, state: bool = False):
        """
        note:
            en: Enable or disable the motor.
            cn: 启用或禁用电机。

        params:
            state:
              note: The state of the motor.
              field: switch
        """
        rdata = self.i2c.readfrom_mem(self.addr, self.OUTPUT_REG, 1)
        rdata = struct.unpack("B", rdata)[0]
        rdata &= 0xEF
        if state == 0:
            rdata |= 0x10
        self.i2c.writeto_mem(self.addr, self.OUTPUT_REG, struct.pack("B", rdata))

    def set_microstep(self, step):
        """
        note:
            en: Set the microstep.
            cn: 设置微步。

        params:
            step:
              note: The microstep value.
              field: dropdown
              options:
                FULL: StepMotorDriverModule.STEP_FULL
                1/2: StepMotorDriverModule.STEP1_2
                1/4: StepMotorDriverModule.STEP1_4
                1/8: StepMotorDriverModule.STEP1_8
                1/16: StepMotorDriverModule.STEP1_16
                1/32: StepMotorDriverModule.STEP1_32
        """
        rdata = self.i2c.readfrom_mem(self.addr, self.OUTPUT_REG, 1)
        rdata = struct.unpack("B", rdata)[0]
        rdata &= 0x1F
        rdata |= step << 5
        self.i2c.writeto_mem(self.addr, self.CONFIG_REG, struct.pack("B", rdata))

    def set_motor_pwm_freq(self, motor_id, freq: int):
        """
        note:
            en: Set the motor pwm freq.
            cn: 设置电机PWM频率。

        params:
            motor_id:
              note: The motor to set the freq.
              field: dropdown
              options:
                X: StepMotorDriverModule.MOTOR_X
                Y: StepMotorDriverModule.MOTOR_Y
                Z: StepMotorDriverModule.MOTOR_Z
            freq:
              note: The freq value.
        """
        if motor_id == self.MOTOR_X:
            self.pwm_x.freq(freq)
        elif motor_id == self.MOTOR_Y:
            self.pwm_y.freq(freq)
        elif motor_id == self.MOTOR_Z:
            self.pwm_z.freq(freq)

    def set_motor_direction(self, motor_id, direction: bool):
        """
        note:
            en: Set the motor direction.
            cn: 设置电机方向。

        params:
            motor_id:
              note: The motor to set the direction.
              field: dropdown
              options:
                X: StepMotorDriverModule.MOTOR_X
                Y: StepMotorDriverModule.MOTOR_Y
                Z: StepMotorDriverModule.MOTOR_Z
            direction:
              note: The direction value.
              field: dropdown
              options:
                Positive: 1
                Negative: 0
        """
        if motor_id == self.MOTOR_X:
            self.dir_x.value(direction)
        elif motor_id == self.MOTOR_Y:
            self.dir_y.value(direction)
        elif motor_id == self.MOTOR_Z:
            self.dir_z.value(direction)

    def get_all_limit_switch_state(self):
        """
        note:
            en: Get all io state.
            cn: 获取所有IO状态。
        """
        rdata = self.i2c.readfrom_mem(self.addr, self.INPUT_REG, 1)
        return struct.unpack("B", rdata)[0] & 0x0F

    def get_limit_switch_state(self, switch_id: int):
        """
        note:
            en: Get the io state.
            cn: 获取IO状态。

        params:
            switch_id:
              note: The io id.
        """
        rdata = self.i2c.readfrom_mem(self.addr, self.INPUT_REG, 1)
        return (struct.unpack("B", rdata)[0] >> switch_id) & 0x01

    def get_fault_io_state(self, motor_id: int):
        """
        note:
            en: Get the fault io state.
            cn: 获取故障IO状态。

        params:
            motor_id:
              note: The motor id.
              field: dropdown
              options:
                X: StepMotorDriverModule.MOTOR_X
                Y: StepMotorDriverModule.MOTOR_Y
                Z: StepMotorDriverModule.MOTOR_Z
        """
        rdata = self.i2c.readfrom_mem(self.addr, self.FAULT_REG, 1)
        return (struct.unpack("B", rdata)[0] >> motor_id) & 0x01

    def motor_control(self, motor_id, state: bool):
        """
        note:
            en: Control the motor to rotate/stop.
            cn: 控制电机旋转/停止。

        params:
            motor_id:
              note: The motor id.
              field: dropdown
              options:
                X: StepMotorDriverModule.MOTOR_X
                Y: StepMotorDriverModule.MOTOR_Y
                Z: StepMotorDriverModule.MOTOR_Z
            state:
              note: The state value.
              field: dropdown
              options:
                Rotate: 1
                Stop: 0
        """
        target = [self.pwm_x, self.pwm_y, self.pwm_z][motor_id]
        if state:
            target.duty(50)
        else:
            target.duty(0)

    def get_firmware_version(self):
        """
        note:
            en: Get the firmware version.
            cn: 获取固件版本。
        """
        rdata = self.i2c.readfrom_mem(self.addr, self.FIRM_REG, 1)
        return struct.unpack("B", rdata)[0]

    def set_i2c_address(self, new_address: int):
        """
        note:
            en: Set the i2c address.
            cn: 设置I2C地址。

        params:
            new_address:
              note: The new address.
        """
        self.i2c.writeto_mem(self.addr, self.I2C_REG, struct.pack("B", new_address))
        self.addr = new_address
