# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import struct
import time
import sys

if sys.platform != "esp32":
    from typing import Union

SERVOS_8_ADDR = 0x25

DIGITAL_IN_MODE = 0x00
DIGITAL_OUT_MODE = 0x01
ADC_IN_MODE = 0x02
SERVO_CTRL_MODE = 0x03
RGB_LED_MODE = 0x04
PWM_DUTY_MODE = 0x05

MODE_REG = 0x00
DIGITAL_OUT_REG = 0x10
DIGITAL_IN_REG = 0x20
ADC_8IN_REG = 0x30
ADC_12IN_REG = 0x40
SERVO_ANGLE_REG = 0x50
SERVO_PULSE_REG = 0x60
RGB_LED_REG = 0x70
PWM_DUTY_REG = 0x90
SERVO_CURRENT_REG = 0xA0
FW_VER_REG = 0xFE
I2C_ADDR_REG = 0xFF


class Servos8Unit:
    """Create a servos 8 unit object.

    :param i2c: The I2C bus the servos 8 unit is connected to.
    :type i2c: machine.I2C | PAHUBUnit
    :param int address: The I2C address of the device. Default is 0x25.

    :raises UnitError: If the servos 8 unit is not connected.

    UiFlow2 Code Block:
        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from hardware import I2C
            from unit import Servos8Unit

            i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
            servos8_0 = Servos8Unit(i2c0, 0x25)
    """

    DIGITAL_INPUT_MODE = 0
    DIGITAL_OUTPUT_MODE = 1
    ADC_INPUT_MODE = 2
    SERVO_CTL_MODE = 3
    RGB_LED_MODE = 4
    PWM_DUTY_MODE = 5

    def __init__(
        self, i2c: Union[machine.I2C, PAHUBUnit], address: int | list | tuple = SERVOS_8_ADDR
    ):
        self._i2c = i2c
        self._address = address
        if self._address not in self._i2c.scan():
            raise UnitError("8 Servos unit maybe not connect")

    def get_mode(self, channel: int) -> int:
        """Get the current mode of a specific channel.

        :param int channel: The channel number (0 to 7) to get the mode for.
        :return: The mode of the specified channel.
        :rtype: int

        UiFlow2 Code Block:

            |get_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8_0.get_mode(0)
        """
        if channel >= 0 and channel <= 7:
            return self._i2c.readfrom_mem(self._address, MODE_REG + channel, 1)[0]

    def set_mode(self, mode: int, channel: int) -> None:
        """Set the mode of a specific channel.

        :param int mode: The mode to set for the channel.
        :param int channel: The channel number (0 to 7) to set the mode for.

        UiFlow2 Code Block:

            |set_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8_0.set_mode(0, 0)
        """
        if channel >= 0 and channel <= 7:
            self._i2c.writeto_mem(self._address, MODE_REG + channel, bytearray([mode]))

    def get_digital_input(self, channel: int) -> bool:
        """Get the digital input value of a specific channel.

        :param int channel: The channel number (0 to 7) to get the digital input for.
        :return: The digital input value (True or False) of the specified channel.
        :rtype: bool

        UiFlow2 Code Block:

            |get_digital_input.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8_0.get_digital_input(0)
        """
        if channel >= 0 and channel <= 7:
            if DIGITAL_IN_MODE == self.get_mode(channel):
                return bool(
                    self._i2c.readfrom_mem(self._address, (DIGITAL_IN_REG + channel), 1)[0]
                )

    def set_output_value(self, value: int, channel: int) -> None:
        """Set the digital output value of a specific channel.

        :param int value: The digital output value (0 or 1) to set for the channel.
        :param int channel: The channel number (0 to 7) to set the digital output for.

        UiFlow2 Code Block:

            |set_output_value.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8_0.set_output_value(1, 0)
        """
        if channel >= 0 and channel <= 7:
            if DIGITAL_OUT_MODE == self.get_mode(channel):
                self._i2c.writeto_mem(
                    self._address, (DIGITAL_OUT_REG + channel), bytearray([value])
                )

    def get_8bit_adc_raw(self, channel: int) -> int:
        """Get the 8-bit ADC value of a specific channel.

        :param int channel: The channel number (0 to 7) to get the 8-bit ADC value for.
        :return: The 8-bit ADC value (0 to 255) of the specified channel.
        :rtype: int

        UiFlow2 Code Block:

            |get_8bit_adc_raw.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8_0.get_8bit_adc_raw(0)
        """
        if channel >= 0 and channel <= 7:
            if ADC_IN_MODE == self.get_mode(channel):
                return self._i2c.readfrom_mem(self._address, (ADC_8IN_REG + channel), 1)[0]

    def get_12bit_adc_raw(self, channel: int) -> int:
        """Get the 12-bit ADC value of a specific channel.

        :param int channel: The channel number (0 to 7) to get the 12-bit ADC value for.
        :return: The 12-bit ADC value (0 to 4095) of the specified channel.
        :rtype: int

        UiFlow2 Code Block:

            |get_12bit_adc_raw.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8_0.get_12bit_adc_raw(0)
        """
        if channel >= 0 and channel <= 7:
            if ADC_IN_MODE == self.get_mode(channel):
                buf = self._i2c.readfrom_mem(self._address, (ADC_12IN_REG + (channel * 2)), 2)
                return struct.unpack("<h", buf)[0]

    def set_servo_angle(self, angle: int, channel: int) -> None:
        """Set the servo angle of a specific channel.

        :param int angle: The servo angle (0 to 180) to set for the channel.
        :param int channel: The channel number (0 to 7) to set the servo angle for.

        UiFlow2 Code Block:

            |set_servo_angle.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8_0.set_servo_angle(90, 0)
        """
        if channel >= 0 and channel <= 7:
            if SERVO_CTRL_MODE == self.get_mode(channel):
                self._i2c.writeto_mem(
                    self._address, (SERVO_ANGLE_REG + channel), bytearray([angle])
                )

    def get_servo_angle(self, channel: int) -> int:
        """Get the servo angle of a specific channel.

        :param int channel: The channel number (0 to 7) to get the servo angle for.
        :return: The servo angle (0 to 180) of the specified channel.
        :rtype: int

        UiFlow2 Code Block:

            |get_servo_angle.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8_0.get_servo_angle(0)
        """
        if channel >= 0 and channel <= 7:
            if SERVO_CTRL_MODE == self.get_mode(channel):
                return self._i2c.readfrom_mem(self._address, (SERVO_ANGLE_REG + channel), 1)[0]

    def set_servo_pulse(self, pulse: int, channel: int) -> None:
        """Set the servo pulse of a specific channel.

        :param int pulse: The servo pulse (500 to 2500) to set for the channel.
        :param int channel: The channel number (0 to 7) to set the servo pulse for.

        UiFlow2 Code Block:

            |set_servo_pulse.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8_0.set_servo_pulse(1500, 0)
        """
        if channel >= 0 and channel <= 7:
            if SERVO_CTRL_MODE == self.get_mode(channel):
                pulse = struct.pack("<h", pulse)
                self._i2c.writeto_mem(self._address, (SERVO_PULSE_REG + (channel * 2)), pulse)

    def get_servo_pulse(self, channel: int) -> int:
        """Get the servo pulse of a specific channel.

        :param int channel: The channel number (0 to 7) to get the servo pulse for.
        :return: The servo pulse (500 to 2500) of the specified channel.
        :rtype: int

        UiFlow2 Code Block:

            |get_servo_pulse.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8_0.get_servo_pulse(0)
        """
        if channel >= 0 and channel <= 7:
            if SERVO_CTRL_MODE == self.get_mode(channel):
                buf = self._i2c.readfrom_mem(self._address, (SERVO_PULSE_REG + (channel * 2)), 2)
                return struct.unpack("<h", buf)[0] // 10

    def set_rgb_led(self, rgb: int, channel: int) -> None:
        """Set the RGB LED color of a specific channel.

        :param int rgb: The RGB color value (0x000000 to 0xffffff) to set for the channel.
        :param int channel: The channel number (0 to 7) to set the RGB LED color for.

        UiFlow2 Code Block:

            |set_rgb_led.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8_0.set_rgb_led(0xFF0000, 0)
        """
        if channel >= 0 and channel <= 7:
            if RGB_LED_MODE == self.get_mode(channel):
                self._i2c.writeto_mem(
                    self._address, (RGB_LED_REG + (channel * 3)), rgb.to_bytes(3, "big")
                )

    def get_rgb_led(self, channel: int) -> int:
        """Get the RGB LED color of a specific channel.

        :param int channel: The channel number (0 to 7) to get the RGB LED color for.
        :return: The RGB color value (0x000000 to 0xffffff) of the specified channel.
        :rtype: int

        UiFlow2 Code Block:

            |get_rgb_led.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8_0.get_rgb_led(0)
        """
        if channel >= 0 and channel <= 7:
            if RGB_LED_MODE == self.get_mode(channel):
                buf = self._i2c.readfrom_mem(self._address, (RGB_LED_REG + (channel * 3)), 3)
                return int.from_bytes(buf, "big")

    def set_pwm_dutycycle(self, duty: int, channel: int) -> None:
        """Set the PWM duty cycle of a specific channel.

        :param int duty: The PWM duty cycle (0 to 100) to set for the channel.
        :param int channel: The channel number (0 to 7) to set the PWM duty cycle for.

        UiFlow2 Code Block:

            |set_pwm_dutycycle.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8_0.set_pwm_dutycycle(50, 0)
        """
        if channel >= 0 and channel <= 7:
            if PWM_DUTY_MODE == self.get_mode(channel):
                duty = max(min(duty, 100), 0)
                self._i2c.writeto_mem(self._address, (PWM_DUTY_REG + channel), bytearray([duty]))

    def get_input_current(self) -> float:
        """Get the input current of the servos 8 unit.

        :return: The input current in Amperes.
        :rtype: float

        UiFlow2 Code Block:

            |get_input_current.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8_0.get_input_current()
        """
        buf = self._i2c.readfrom_mem(self._address, SERVO_CURRENT_REG, 4)
        return round(struct.unpack("<f", buf)[0], 3)

    def get_device_spec(self, mode):
        """Get the device specification.
        :param int mode: The mode to get the specification for.
        :return: The device specification value.
        :rtype: int

        UiFlow2 Code Block:

            |get_device_spec.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8_0.get_device_spec(0xFE)
        """
        if mode >= FW_VER_REG and mode <= I2C_ADDR_REG:
            return self._i2c.readfrom_mem(self._address, mode, 1)[0]

    def set_i2c_address(self, addr):
        """Set the I2C address of the servos 8 unit.

        :param int addr: The new I2C address (1 to 127) to set for the servos 8 unit.

        UiFlow2 Code Block:

            |set_i2c_address.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8_0.set_i2c_address(0x25)
        """
        if addr >= 1 and addr <= 127:
            if addr != self._address:
                self._i2c.writeto_mem(self._address, I2C_ADDR_REG, bytearray([addr]))
                self._address = addr
                time.sleep_ms(150)
