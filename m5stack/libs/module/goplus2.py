# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .mbus import i2c1
import struct


class GoPlus2Module:
    """! GoPlus2 is a stackable multi-functional motor and servo control module.

    @en Module GoPlus2 英文介绍
    @cn Module GoPlus2 中文介绍

    @color #0FE6D7
    @link https://docs.m5stack.com/en/module/goplus2
    @image https://static-cdn.m5stack.com/resource/docs/products/module/goplus2/goplus2_01.webp
    @category module

    """

    _GOPLUS2_ADDR = 0x38

    _GOPLUS2_SERVO_ANGLE_REG = 0x00
    _GOPLUS2_SERVO_PLUSEWIDTH_REG = 0x10

    _GOPLUS2_MOTOR_CTR_REG = 0x30

    _GOPLUS2_PBI_ANALOG_INPUT_REG = 0x40
    _GOPLUS2_PBI_DIGITAL_INPUT_REG = 0x50
    _GOPLUS2_PBO_DIGITAL_OUTPUT_REG = 0x60
    _GOPLUS2_PBO_DIGITAL_INPUT_REG = 0x70
    _GOPLUS2_PBO_CTR_REG = 0x80

    def __init__(self, address: int | list | tuple = _GOPLUS2_ADDR) -> None:
        """! Initialize the GoPlus2Module.

        @param address The I2C address of the GoPlus2 module (default is 0x38).
        """
        self._i2c = i2c1
        self._i2c_addr = address
        if self._i2c_addr not in self._i2c.scan():
            raise Exception("GoPlus2 Module not found in Base")

    def set_servo_angle(self, servo_num: int, angle: int) -> None:
        """! Set the angle of the specified servo.

        @param servo_num The number of the servo (1 to 4).
        @param angle The angle to set the servo to (0 to 180 degrees).
        """
        if not (1 <= servo_num <= 4):
            raise ValueError("Servo select error")
        reg = self._GOPLUS2_SERVO_ANGLE_REG + servo_num - 1
        self._i2c.writeto_mem(self._i2c_addr, reg, bytes([angle]))

    def set_servo_pulse_width(self, servo_num: int, pulse_width: int) -> None:
        """! Set the pulse width for the specified servo.

        @param servo_num The number of the servo (1 to 4).
        @param pulse_width The pulse width to set (in microseconds).
        """
        if not (1 <= servo_num <= 4):
            raise ValueError("LED select error")
        reg = self._GOPLUS2_SERVO_PLUSEWIDTH_REG + servo_num - 1
        self._i2c.writeto_mem(
            self._i2c_addr, reg, bytes([pulse_width & 0xFF, (pulse_width >> 8) & 0xFF])
        )

    def set_motor_speed(self, motor_num: int, speed: int) -> None:
        """! Set the speed of the specified motor.

        @param motor_num The number of the motor (1 or 2).
        @param speed The speed to set (negative for reverse).
        """
        if not (1 <= motor_num <= 2):
            raise ValueError("Motor select error")
        reg = self._GOPLUS2_MOTOR_CTR_REG + motor_num - 1
        if speed < 0:
            speed = 255 + speed + 1  # 将负数转换为补码表示
        self._i2c.writeto_mem(self._i2c_addr, reg, bytes([speed]))

    def set_digital_output(self, pin_num: int, value: int) -> None:
        """! Set the digital output for the specified pin.

        @param pin_num The number of the pin (1 to 3).
        @param value The value to set (0 or 1).
        """
        if not (1 <= pin_num <= 3):
            raise ValueError("Port select error")
        reg = self._GOPLUS2_PBO_DIGITAL_OUTPUT_REG + pin_num - 1
        self._i2c.writeto_mem(self._i2c_addr, self._GOPLUS2_PBO_CTR_REG + pin_num - 1, bytes([0]))
        self._i2c.writeto_mem(self._i2c_addr, reg, bytes([value]))

    def get_digital_input(self, pin_num: int) -> int:
        """! Get the digital input value of the specified pin.

        @param pin_num The number of the pin (1 to 3).
        @return The digital input value (0 or 1).
        """
        if not (1 <= pin_num <= 3):
            raise ValueError("Port select error")
        reg = self._GOPLUS2_PBI_DIGITAL_INPUT_REG + pin_num - 1
        self._i2c.writeto(self._i2c_addr, bytes([reg]))
        buf = self._i2c.readfrom(self._i2c_addr, 1)
        return struct.unpack("<B", buf)[0]

    def get_analog_input(self, pin_num: int) -> int:
        """! Get the analog input value of the specified pin.

        @param pin_num The number of the pin (1 to 3).
        @return The analog input value (0 to 1023).
        """
        if not (1 <= pin_num <= 3):
            raise ValueError("Port select error")
        reg = self._GOPLUS2_PBI_ANALOG_INPUT_REG + (pin_num - 1) * 2
        buf = self._i2c.readfrom_mem(self._i2c_addr, reg, 2)
        return struct.unpack(">H", buf)[0]
