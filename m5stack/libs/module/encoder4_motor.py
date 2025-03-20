# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from module.mbus import i2c1
from module.module_helper import ModuleError
import struct
import time


class Encoder4MotorModule:
    """Create an Encoder4MotorModule object

    :param int address: The I2C address of the device. Default is 0x24.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from module import Encoder4MotorModule

            encoder4_motor = Encoder4MotorModule(0x24)
    """

    DEVADDR = 0x24

    MTR_PWM_DUTY = 0x20
    MTR_ENCODER = 0x30
    MTR_SPEED = 0x40
    MTR1_MODE = 0x50
    MTR2_MODE = 0x60
    MTR3_MODE = 0x70
    MTR4_MODE = 0x80
    VIN_AMPS_FLT = 0x90
    VIN_ADC8 = 0xA0
    VIN_ADC12 = 0xB0
    VIN_AMPS_INT = 0xC0
    ENCODER_AB = 0xD0
    SOFT_START = 0xD1
    FIRM_VER = 0xFE
    I2C_ADDR = 0xFF

    NORMAL_MODE = 0x00
    POSITION_MODE = 0x01
    SPEED_MODE = 0x02

    def __init__(self, address: int = DEVADDR):
        self._i2c = i2c1
        self._address = address
        if address >= 1 and address <= 127:
            self._address = address
        self.available()
        self.mode = self.NORMAL_MODE

    def available(self):
        check = False
        for _ in range(3):
            if self._address in self._i2c.scan():
                check = True
                break
            time.sleep(0.2)
        if not check:
            raise ModuleError("4Encoder motor module maybe not connect")

    def set_motor_mode(self, motor, mode):
        """Set the motor mode.

        :param int motor: The motor to set the mode.
        :param int mode: The mode of the motor.

            Options:
                - ``NORMAL_MODE``: 0
                - ``POSITION_MODE``: 1
                - ``SPEED_MODE``: 2

        UiFlow2 Code Block:

            |set_motor_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.set_motor_mode(0, encoder4_motor.NORMAL_MODE)
        """
        self.mode = mode
        self._i2c.writeto_mem(self._address, self.MTR1_MODE + (0x10 * motor), bytearray([mode]))

    def set_all_motors_mode(self, mode):
        """Set the mode of all motors.

        :param int mode: The mode of the motors.

            Options:
                - ``NORMAL_MODE``: 0
                - ``POSITION_MODE``: 1
                - ``SPEED_MODE``: 2

        UiFlow2 Code Block:

            |set_all_motors_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.set_all_motors_mode(encoder4_motor.NORMAL_MODE)
        """
        for i in range(0, 4):
            self.set_motor_mode(i, mode)

    def set_motor_pwm_dutycycle(self, motor, duty):
        """Set the PWM duty cycle of a motor.

        :param int motor: The motor to set the PWM duty cycle.
        :param int duty: The PWM duty cycle.

        UiFlow2 Code Block:

            |set_motor_pwm_dutycycle.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.set_motor_pwm_dutycycle(0, 127)
        """
        duty = min(max(duty, -128), 127)
        duty = struct.pack(">b", duty)
        self._i2c.writeto_mem(self._address, self.MTR_PWM_DUTY + motor, duty)

    def get_motor_encoder_value(self, pos):
        """Get the encoder value of a motor.

        :param int pos: The motor to get the encoder value.

        :returns: The encoder value.
        :rtype: int

        UiFlow2 Code Block:

            |get_motor_encoder_value.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.get_motor_encoder_value(0)
        """
        buf = self._i2c.readfrom_mem(self._address, self.MTR_ENCODER + (0x04 * pos), 4)
        return struct.unpack(">i", buf)[0]

    def set_motor_encoder_value(self, pos, value):
        """Set the encoder value of a motor.

        :param int pos: The motor to set the encoder value.
        :param int value: The encoder value.

        UiFlow2 Code Block:

            |set_motor_encoder_value.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.set_motor_encoder_value(0, 100)
        """
        value = struct.pack(">i", value)
        self._i2c.writeto_mem(self._address, self.MTR_ENCODER + (0x04 * pos), value)

    def get_encoder_mode(self):
        """Get the encoder mode.

        :return: The encoder mode.
        :rtype: int

        UiFlow2 Code Block:

            |get_encoder_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.get_encoder_mode()
        """
        return self._i2c.readfrom_mem(self._address, self.ENCODER_AB, 1)[0]

    def set_encoder_mode(self, mode):
        """Set the encoder mode.

        :param int mode: The mode of the encoder.

            Options:
                - ``AB``: 0
                - ``BA``: 1

        UiFlow2 Code Block:

            |set_encoder_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.set_encoder_mode(0x00)
        """
        self._i2c.writeto_mem(self._address, self.ENCODER_AB, bytearray([mode]))
        time.sleep_ms(150)

    def get_motor_speed_value(self, pos):
        """Get the speed value of a motor.

        :param int pos: The motor to get the speed value.

        :returns: The speed value.
        :rtype: int

        UiFlow2 Code Block:

            |get_motor_speed_value.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.get_motor_speed_value(0)
        """
        return self._i2c.readfrom_mem(self._address, self.MTR_SPEED + pos, 1)[0]

    def set_position_encoder_value(self, pos, value):
        """Set the position encoder value of a motor.

        :param int pos: The motor to set the position encoder value.
        :param int value: The position encoder value.

        UiFlow2 Code Block:

            |set_position_encoder_value.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.set_position_encoder_value(0, 100)
        """
        value = struct.pack("<i", value)
        self._i2c.writeto_mem(self._address, self.MTR1_MODE + (0x10 * pos) + 0x04, value)

    def set_position_max_speed_value(self, pos, value):
        """Set the maximum speed value of a motor.

        :param int pos: The motor to set the maximum speed value.
        :param int value: The maximum speed value.

        UiFlow2 Code Block:

            |set_position_max_speed_value.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.set_position_max_speed_value(0, 127)
        """
        value = min(max(value, -128), 127)
        value = struct.pack("<b", value)
        self._i2c.writeto_mem(self._address, self.MTR1_MODE + (0x10 * pos) + 0x08, value)

    def get_position_pid_value(self, pos):
        """Get the position PID value of a motor.

        :param int pos: The motor to get the position P,I,D value.

        :returns: The position PID value.
        :rtype: list[int, int, int]

        UiFlow2 Code Block:

            |get_position_PID_value.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.get_position_pid_value(0)
        """
        return list(self._i2c.readfrom_mem(self._address, self.MTR1_MODE + (0x10 * pos) + 0x01, 3))

    def set_position_pid_value(self, pos, p, i, d):
        """Set the position P,I,D value of a motor.

        :param int pos: The motor to set the position P,I,D value.
        :param int p: The P value.
        :param int i: The I value.
        :param int d: The D value.

        UiFlow2 Code Block:

            |set_position_PID_value.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.set_position_pid_value(0, 100, 100, 100)
        """
        self._i2c.writeto_mem(
            self._address, self.MTR1_MODE + (0x10 * pos) + 0x01, bytearray([p, i, d])
        )

    def get_speed_pid_value(self, pos):
        """Get the speed PID value of a motor.

        :param int pos: The motor to get the speed P,I,D value.

        :returns: The speed P,I,D value.
        :rtype: list[int, int, int]

        UiFlow2 Code Block:

            |get_speed_PID_value.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.get_speed_PID_value(0)
        """
        return list(self._i2c.readfrom_mem(self._address, self.MTR1_MODE + (0x10 * pos) + 0x09, 3))

    def set_speed_pid_value(self, pos, p, i, d):
        """Set the speed PID value of a motor.

        :param int pos: The motor to set the speed PID value.
        :param int p: The P value.
        :param int i: The I value.
        :param int d: The D value.

        UiFlow2 Code Block:

            |set_speed_PID_value.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.set_speed_PID_value(0, 100, 100, 100)
        """
        self._i2c.writeto_mem(
            self._address, self.MTR1_MODE + (0x10 * pos) + 0x09, bytearray([p, i, d])
        )

    def set_speed_point_value(self, pos, point):
        """Set the speed point value of a motor.

        :param int pos: The motor to set the speed point value.
        :param int point: The speed point value.

        UiFlow2 Code Block:

            |set_speed_point_value.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.set_speed_point_value(0, 127)
        """
        point = min(max(point, -128), 127)
        point = struct.pack("<b", point)
        self._i2c.writeto_mem(self._address, self.MTR1_MODE + (0x10 * pos) + 0x0C, point)

    def get_vin_current_float_value(self):
        """Get the input current value in float.

        :return: The input current value.
        :rtype: float

        UiFlow2 Code Block:

            |get_vin_current_float_value.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.get_vin_current_float_value()
        """
        buf = self._i2c.readfrom_mem(self._address, self.VIN_AMPS_FLT, 4)
        return round(struct.unpack("<f", buf)[0], 3)

    def get_vin_current_int_value(self):
        """Get the input current value in int.

        :return: The input current value.
        :rtype: int

        UiFlow2 Code Block:

            |get_vin_current_int_value.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.get_vin_current_int_value()
        """
        buf = self._i2c.readfrom_mem(self._address, self.VIN_AMPS_INT, 4)
        return struct.unpack("<i", buf)[0] * 10

    def get_vin_adc_raw8_value(self):
        """Get the input voltage ADC raw value in 8-bit.

        :return: The input voltage ADC raw value.
        :rtype: int

        UiFlow2 Code Block:

            |get_vin_adc_raw8_value.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.get_vin_adc_raw8_value()
        """
        return self._i2c.readfrom_mem(self._address, self.VIN_ADC8, 1)[0]

    def get_vin_adc_raw12_value(self):
        """Get the input voltage ADC raw value in 12-bit.

        :return: The input voltage ADC raw value.
        :rtype: int

        UiFlow2 Code Block:

            |get_vin_adc_raw12_value.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.get_vin_adc_raw12_value()
        """
        buf = self._i2c.readfrom_mem(self._address, self.VIN_ADC12, 2)
        return struct.unpack("<h", buf)[0]

    def get_vin_voltage(self):
        """Get the input voltage value.

        :return: The input voltage value.
        :rtype: float

        UiFlow2 Code Block:

            |get_vin_voltage.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.get_vin_voltage()
        """
        value = self.get_vin_adc_raw12_value()
        return round(value / 4095 * 3.3 / (20 / 120), 2)  # 20k/(20k+100k)

    def get_device_spec(self, info):
        """Get the device specification.

        :param int info: The information to get.

        :returns: The device specification(firmware version/I2C address).
        :rtype: int

        UiFlow2 Code Block:

            |get_device_spec.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.get_device_spec(0xFE)
        """
        return self._i2c.readfrom_mem(self._address, info, 1)[0]

    def get_soft_start_state(self, motor):
        """Get the soft start state of a motor.

        :param int motor: The motor to get the soft start state.

        :returns: The soft start state.
        :rtype: bool

        UiFlow2 Code Block:

            |get_soft_start_state.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.get_soft_start_state(0)
        """
        return not (
            self._i2c.readfrom_mem(self._address, self.SOFT_START, 1)[0] & (1 << motor) == 0
        )

    def set_soft_start_state(self, motor, state):
        """Set the soft start state of a motor.

        :param int motor: The motor to set the soft start state.
        :param int state: The soft start state.

            Options:
                - ``True``: 1
                - ``False``: 0

        UiFlow2 Code Block:

            |set_soft_start_state.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.set_soft_start_state(0, True)
        """
        buf = self._i2c.readfrom_mem(self._address, self.SOFT_START, 1)[0]
        buf = buf & ~(1 << motor) | (state << motor)
        self._i2c.writeto_mem(self._address, self.SOFT_START, bytearray([buf]))

    def set_i2c_address(self, addr):
        """Set the I2C address of the device.

        :param int addr: The I2C address to set.

        UiFlow2 Code Block:

            |set_i2c_address.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder4_motor.set_i2c_address(0x24)
        """
        addr = min(max(addr, 1), 127)
        if addr != self._address:
            self._i2c.writeto_mem(self._address, self.I2C_ADDR, bytearray([addr]))
            self._address = addr
            time.sleep_ms(150)
