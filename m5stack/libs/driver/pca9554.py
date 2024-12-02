# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Melissa LeBlanc-Williams for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
import time
import micropython

try:
    from micropython import const
except ImportError:

    def const(expr):
        return expr


try:
    from typing_extensions import Literal
except ImportError:
    pass

_REGISTER_INPUT = const(0x00)
_REGISTER_OUTPUT = const(0x01)
_REGISTER_POLARITY_INVERSION = const(0x02)
_REGISTER_CONFIG = const(0x03)

_PCA9554_DEFAULT_ADDRESS = const(0x27)


class Pin:
    IN = 0x01
    OUT = 0x00

    def __init__(self, port, id, mode: int = IN, value=None) -> None:
        """! Initialize the Pin object with specified parameters.

        @param port: The port object controlling the pin.
        @param id: The pin identifier (e.g., GPIO number).
        @param mode: The mode of the pin, either `Pin.IN` (default) or `Pin.OUT`.
        @param value: Optional initial value for the pin, 0 or 1.
        """
        self._port = port
        self._id = id
        self._mode = mode
        self._value = value
        self._port.set_pin_mode(self._id, self._mode)
        if value is not None:
            self._port.digit_write(self._id, value)

    def init(self, mode: int = -1, value=None):
        """! Reinitialize the pin with a new mode or value.

        @param mode: New mode for the pin, `Pin.IN` or `Pin.OUT`.
        @param value: New value for the pin, 0 or 1.
        """
        self._port.set_pin_mode(self._id, mode)
        if value is not None:
            self._port.digit_write(self._id, value)

    def value(self, *args):
        """! Get or set the digital value of the pin.

        If no arguments are passed, the method returns the current value of the pin.
        If one argument is passed, it sets the pin to the specified value.

        @param args: Optional argument to set the pin value.
        @return: The current pin value when called without arguments; None when setting a value.
        """
        if len(args) == 0:
            return self._port.digit_read(self._id)
        elif len(args) == 1:
            self._port.digit_write(self._id, args[0])

    def __call__(self, *args):
        """! Shortcut to get or set the pin value.

        This method allows `Pin()` to behave like `Pin.value()`.

        @param args: Optional argument to set the pin value.
        @return: The current pin value when called without arguments; None when setting a value.
        """
        if len(args) == 0:
            return self._port.digit_read(self._id)
        elif len(args) == 1:
            self._port.digit_write(self._id, args[0])

    def on(self):
        """! Set the pin to a high state (1)."""
        self._port.digit_write(self._id, 1)

    def off(self):
        """! Set the pin to a low state (0)."""
        self._port.digit_write(self._id, 0)


class PCA9554:
    """! EXT.IO is a GPIO Expander. With simple I2C commands it's possible to extend the GPIO pins for up to 8 extra GPIOs.
    The EXT.IO Integrates the PCA9554PW chipset. This 8-bit I/O expander for the two-line bi-directional-bus (I2C) is designed for 2.3-V to 5.5-V VCC with Open-Drain Active-Low Interrupt Output operation.

    @en Unit EXT.IO 英文介绍
    @cn Unit EXT.IO 中文介绍

    @color #0FE6D7
    @link https://docs.m5stack.com/en/unit/extio
    @image https://static-cdn.m5stack.com/resource/docs/products/unit/extio/extio_01.webp
    @category unit

    @example

    """

    IN = 0x01
    OUT = 0x00

    def __init__(self, i2c: I2C, address: int = _PCA9554_DEFAULT_ADDRESS) -> None:
        """! Initialize the PCA9554 device.

        @param i2c: An instance of the I2C bus to communicate with the device.
        @param address: The I2C address of the PCA9554 device (default is _PCA9554_DEFAULT_ADDRESS).
        """
        self._i2c = i2c
        self._addr = address
        self._BUFFER = memoryview(bytearray(3))

    def set_port_mode(self, mode: Literal[0x00, 0x01]) -> None:
        """! Set the mode of the entire port.

        @param mode: The mode to set, either PCA9554.IN (input, 0x00) or PCA9554.OUT (output, 0x01).
        """
        self._write_u8(_REGISTER_CONFIG, 0xFF if mode == 0x01 else 0x00)

    def set_pin_mode(self, id: int, mode: Literal[0x00, 0x01]) -> None:
        """! Set the mode of a specific pin.

        @param id: The pin number (0-7).
        @param mode: The mode to set, either PCA9554.IN (input, 0x00) or PCA9554.OUT (output, 0x01).
        """
        config = self._read_u8(_REGISTER_CONFIG)
        config &= ~(1 << id)
        config |= mode << id
        self._write_u8(_REGISTER_CONFIG, config)

    def digit_write_port(self, value: int) -> None:
        """! Set a value to the entire port.

        @param value: An 8-bit value to set to the port.
        """
        self._write_u8(_REGISTER_OUTPUT, value)

    def digit_write(self, id: int, value: int) -> None:
        """! Set a value to a specific pin.

        @param id: The pin number (0-7).
        @param value: The value to set, either 0 (low) or 1 (high).
        """
        out = self._read_u8(_REGISTER_OUTPUT)
        out &= ~(1 << id)
        out |= value << id
        self._write_u8(_REGISTER_OUTPUT, out)

    def digit_read_port(self) -> int:
        """! Read the value from the entire port.

        @return: An 8-bit value representing the state of the port.
        """
        return self._read_u8(_REGISTER_INPUT)

    def digit_read(self, id: int) -> int:
        """! Read the value from a specific pin.

        @param id: The pin number (0-7).
        @return: The value of the pin, either 0 (low) or 1 (high).
        """
        input = self._read_u8(_REGISTER_INPUT)
        return 1 if (input & (1 << id)) else 0

    def _read_u8(self, reg: int) -> int:
        """! Read an 8-bit value from a specific register.

        @param reg: The register address to read from.
        @return: The 8-bit value read from the register.
        """
        buf = self._BUFFER[0:1]
        self._i2c.readfrom_mem_into(self._addr, reg & 0xFF, buf)
        return buf[0]

    def _write_u8(self, reg: int, val: int) -> None:
        """! Write an 8-bit value to a specific register.

        @param reg: The register address to write to.
        @param val: The 8-bit value to write to the register.
        """
        buf = self._BUFFER[0:1]
        buf[0] = val & 0xFF
        self._i2c.writeto_mem(self._addr, reg & 0xFF, buf)

    def pin(self, id: int, mode: int = IN, value=None) -> Pin:
        """! Provide a MicroPython-style interface for handling GPIO pins.

        @param id: The GPIO pin number to configure and control.
        @param mode: The pin mode, either `IN` (input) or `OUT` (output). Defaults to `IN`.
        @param value: The initial value to set for the pin if in `OUT` mode. Use `None` for no initial value.
        @return: A `Pin` object for further pin operations such as reading or writing values.
        """
        return Pin(self, id, mode, value)
