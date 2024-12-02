# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from machine import I2C
from micropython import const
from .pahub import PAHUBUnit
import sys

if sys.platform != "esp32":
    from typing import Literal


_REG_MODE_CH_1 = const(0x00)
_REG_OUTPUT_REG_CH_1 = const(0x10)
_REG_INPUT_REG_CH_1 = const(0x20)
_REG_ANALOG_INPUT_8B_REG_CH_1 = const(0x30)
_REG_ANALOG_INPUT_12B_REG_CH_1 = const(0x40)
_REG_SERVO_ANGLE_8B_REG_CH_1 = const(0x50)
_REG_SERVO_PULSE_16B_REG_CH_1 = const(0x60)
_REG_RGB_24B_REG_CH_1 = const(0x70)
_REG_FW_VERSION = const(0xFE)
_REG_ADDR_CONFIG = const(0xFF)

_DEFAULT_ADDRESS = const(0x45)


class Pin:
    IN = 0x01
    OUT = 0x00

    def __init__(self, port, id, mode: int = IN, value=None) -> None:
        """
        note:
            en: Initialize a Pin object with a port, pin ID, mode, and optional value.

        params:
            port:
                note: The port object associated with the pin.
            id:
                note: The pin ID to identify the pin on the port.
            mode:
                note: The mode to set for the pin, default is Pin.IN (input mode).
            value:
                note: The initial value to set for the pin, optional.
        """
        self._port = port
        self._id = id
        self._mode = mode
        self._value = value
        self._port.set_config_mode(self._id, self._mode)
        if value is not None:
            self._port.digit_write(self._id, value)

    def init(self, mode: int = -1, value=None):
        """
        note:
            en: Initialize or reconfigure the pin with a new mode and optional value.

        params:
            mode:
                note: The new mode to set for the pin. If -1, it retains the previous mode.
            value:
                note: The value to set for the pin, optional.
        """
        self._port.set_config_mode(self._id, mode)
        if value is not None:
            self._port.write_output_pin(self._id, value)

    def value(self, *args):
        """
        note:
            en: Set or get the value of the pin, depending on whether an argument is provided.

        params:
            args:
                note: If no arguments are provided, this method returns the current input value of the pin.
                      If an argument is provided, it sets the output value of the pin.

        returns:
            note: The current input value of the pin (0 or 1) if no argument is provided, otherwise None.
        """
        if len(args) == 0:
            return self._port.read_input_pin(self._id)
        elif len(args) == 1:
            self._port.write_output_pin(self._id, args[0])

    def __call__(self, *args):
        if len(args) == 0:
            return self._port.read_input_pin(self._id)
        elif len(args) == 1:
            self._port.write_output_pin(self._id, args[0])

    def on(self):
        """
        note:
            en: Set the pin to high (1) to turn it on.

        """
        self._port.write_output_pin(self._id, 1)

    def off(self):
        """
        note:
            en: Set the pin to low (0) to turn it off.

        """
        self._port.write_output_pin(self._id, 0)


class EXTIO2Unit:
    """
    note:
        en: EXT.IO2 is an IO extended unit, based on STM32F030 main controller, using I2C communication interface and providing 8 IO expansion. Each IO supports independent configuration of digital I/O, ADC, SERVO control, RGB LED control modes. Supports configuration of device I2C address, which means that users can mount multiple EXT.IO2 UNITs on the same I2C BUS to extend more IO resources. Suitable for multiple digital/analog signal acquisition, with lighting/servo control applications.

    details:
        link: https://docs.m5stack.com/en/unit/extio2
        image: https://static-cdn.m5stack.com/resource/docs/products/unit/extio2/extio2_01.webp
        category: Unit

    example:
        - ../../../examples/unit/extio2/extio2_core2_example.py

    m5f2:
        - unit/extio2/extio2_core2_example.m5f2
    """

    IN = const(0)
    OUT = const(1)
    ANALOG = const(2)
    SERVO = const(3)
    NEOPIXEL = const(4)

    def __init__(self, i2c: I2C | PAHUBUnit, address: int = _DEFAULT_ADDRESS) -> None:
        """
        note:
            en: Initialize EXTIO2Unit with I2C or PAHUBUnit and address for communication.

        params:
            i2c:
                note: The I2C or PAHUBUnit interface for communication with the EXTIO2Unit.
            address:
                note: The I2C address for the unit, default is 0x45.
        """
        self._i2c = i2c
        self._addr = address
        self._BUFFER = memoryview(bytearray(3))

    def set_config_mode(self, id: int, mode: Literal[0, 1, 2, 3, 4]) -> None:
        """
        note:
            en: Set the configuration mode for a specific channel.

        params:
            id:
                note: The channel ID to set the mode for.
            mode:
                note: The mode to set, defined by the EXTIO2Unit. Can be 0, 1, 2, 3, or 4.
        """
        self._write_u8(_REG_MODE_CH_1 + id, mode)

    def write_output_pin(self, id: int, value: Literal[0, 1]) -> None:
        """
        note:
            en: Write a value to an output pin of the EXTIO2Unit.

        params:
            id:
                note: The pin ID to write the value to.
            value:
                note: The value to write, either 0 or 1.
        """
        self._write_u8(_REG_OUTPUT_REG_CH_1 + id, value)

    def write_servo_angle(self, id: int, angle: int) -> None:
        """
        note:
            en: Write an angle to a servo connected to the EXTIO2Unit.

        params:
            id:
                note: The servo ID to set the angle for.
            angle:
                note: The angle to set the servo to (0-255).
        """
        self._write_u8(_REG_SERVO_ANGLE_8B_REG_CH_1 + id, angle)

    def write_servo_pulse(self, id: int, pulse: int) -> None:
        """
        note:
            en: Write a pulse width to a servo connected to the EXTIO2Unit.

        params:
            id:
                note: The servo ID to set the pulse for.
            pulse:
                note: The pulse width to set the servo to, in microseconds.
        """
        self._write_u16(_REG_SERVO_PULSE_16B_REG_CH_1 + (id * 2), pulse & 0xFF, pulse >> 8)

    def write_rgb_led(self, id: int, value) -> None:
        """
        note:
            en: Write an RGB color value to a NeoPixel LED.

        params:
            id:
                note: The NeoPixel ID to set the color for.
            value:
                note: The RGB value to set, represented as a 24-bit integer.
        """
        r = (value >> 16) & 0xFF
        g = (value >> 8) & 0xFF
        b = value & 0xFF
        self._write_u24(_REG_RGB_24B_REG_CH_1 + (id * 3), r, g, b)

    def set_address(self, address: int) -> None:
        """
        note:
            en: Set the I2C address for the EXTIO2Unit.

        params:
            address:
                note: The new I2C address to set for the unit.
        """
        self._write_u8(_REG_ADDR_CONFIG, address & 0xFF)
        self._addr = address

    def get_config_mode(self, id: int) -> int:
        """
        note:
            en: Get the current configuration mode of a specific channel.

        params:
            id:
                note: The channel ID to get the mode for.

        returns:
            note: The current mode of the channel.
        """
        return self._read_u8(_REG_MODE_CH_1 + id)

    def read_input_pin(self, id: int) -> int:
        """
        note:
            en: Read the value of an input pin.

        params:
            id:
                note: The pin ID to read the value from.

        returns:
            note: The value of the input pin.
        """
        return self._read_u8(_REG_INPUT_REG_CH_1 + id)

    def read_adc8_pin(self, id: int) -> int:
        """
        note:
            en: Read the 8-bit ADC value of a pin.

        params:
            id:
                note: The pin ID to read the ADC value from.

        returns:
            note: The 8-bit ADC value of the pin.
        """
        return self._read_u8(_REG_ANALOG_INPUT_8B_REG_CH_1 + id)

    def read_adc12_pin(self, id: int) -> int:
        """
        note:
            en: Read the 12-bit ADC value of a pin.

        params:
            id:
                note: The pin ID to read the ADC value from.

        returns:
            note: The 12-bit ADC value of the pin.
        """
        return self._read_u16(_REG_ANALOG_INPUT_12B_REG_CH_1 + (id * 2))

    def read_servo_angle(self, id: int) -> int:
        """
        note:
            en: Read the angle of a servo.

        params:
            id:
                note: The servo ID to read the angle from.

        returns:
            note: The current angle of the servo.
        """
        return self._read_u8(_REG_SERVO_ANGLE_8B_REG_CH_1 + id)

    def read_servo_pulse(self, id: int) -> int:
        """
        note:
            en: Read the pulse width of a servo.

        params:
            id:
                note: The servo ID to read the pulse width from.

        returns:
            note: The current pulse width of the servo, in microseconds.
        """
        return self._read_u16(_REG_SERVO_PULSE_16B_REG_CH_1 + (id * 2))

    def read_rgb_led(self, id: int) -> int:
        """
        note:
            en: Read the RGB color value of a NeoPixel LED.

        params:
            id:
                note: The NeoPixel ID to read the color from.

        returns:
            note: The RGB color value of the NeoPixel.
        """
        return self._read_u24(_REG_RGB_24B_REG_CH_1 + (id * 3))

    def read_fw_version(self) -> int:
        """
        note:
            en: Read the firmware version of the EXTIO2Unit.

        returns:
            note: The firmware version of the EXTIO2Unit.
        """
        return self._read_u8(_REG_FW_VERSION)

    def get_address(self) -> int:
        """
        note:
            en: Get the current I2C address of the EXTIO2Unit.

        returns:
            note: The current I2C address of the unit.
        """
        return self._read_u8(_REG_ADDR_CONFIG)

    def pin(self, id, mode: int = IN, value=None):
        """
        note:
            en: Create and return a Pin object with the specified mode and value.

        params:
            id:
                note: The pin ID to create the Pin object for.
            mode:
                note: The mode to set for the pin (default is input).
            value:
                note: The value to set for the pin, if applicable.

        returns:
            note: A Pin object for the specified pin.
        """
        return Pin(self, id, mode, value)

    def _write_u8(self, reg: int, val: int) -> None:
        buf = self._BUFFER[0:1]
        buf[0] = val & 0xFF
        self._i2c.writeto_mem(self._addr, reg & 0xFF, buf)

    def _write_u16(self, reg: int, *vals) -> None:
        buf = self._BUFFER[0:2]
        buf[0] = vals[0] & 0xFF
        buf[1] = vals[1] & 0xFF
        self._i2c.writeto_mem(self._addr, reg & 0xFF, buf)

    def _write_u24(self, reg: int, *vals) -> None:
        buf = self._BUFFER[0:3]
        buf[0] = vals[0] & 0xFF
        buf[1] = vals[1] & 0xFF
        buf[2] = vals[2] & 0xFF
        self._i2c.writeto_mem(self._addr, reg & 0xFF, buf)

    def _read_u8(self, reg: int) -> int:
        buf = self._BUFFER[0:1]
        buf[0] = reg & 0xFF
        self._i2c.writeto(self._addr, buf)
        self._i2c.readfrom_into(self._addr, buf)
        return buf[0]

    def _read_u16(self, reg: int) -> int:
        buf = self._BUFFER[0:1]
        buf[0] = reg & 0xFF
        self._i2c.writeto(self._addr, buf)
        buf = self._BUFFER[0:2]
        self._i2c.readfrom_into(self._addr, buf)
        return buf[0] | (buf[1] << 8)

    def _read_u24(self, reg: int) -> int:
        buf = self._BUFFER[0:1]
        buf[0] = reg & 0xFF
        self._i2c.writeto(self._addr, buf)
        buf = self._BUFFER[0:3]
        self._i2c.readfrom_into(self._addr, buf)
        return buf[0] << 16 | (buf[1] << 8) | buf[2]
