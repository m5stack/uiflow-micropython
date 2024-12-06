# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
from micropython import const
import time

# Register and command constants:
_REGISTER_ENABLE = const(0x00)
_REGISTER_ATIME = const(0x01)
_REGISTER_WTIME = const(0x03)
_REGISTER_AILT = const(0x04)
_REGISTER_AILTH = const(0x05)
_REGISTER_AIHT = const(0x06)
_REGISTER_AIHTH = const(0x07)
_REGISTER_APERS = const(0x0C)
_REGISTER_CONFIG = const(0x0D)
_REGISTER_CONTROL = const(0x0F)
_REGISTER_SENSORID = const(0x12)
_REGISTER_STATUS = const(0x13)
_REGISTER_CDATA = const(0x14)
_REGISTER_CDATAH = const(0x15)
_REGISTER_RDATA = const(0x16)
_REGISTER_RDATAH = const(0x17)
_REGISTER_GDATA = const(0x18)
_REGISTER_GDATAH = const(0x19)
_REGISTER_BDATA = const(0x1A)
_REGISTER_BDATAH = const(0x1B)

# Select Command Register. Must write as 1 when addressing COMMAND register.
_COMMAND_BIT = const(0x80)

# Enable Register Fields
_ENABLE_AIEN = const(0x10)
_ENABLE_WEN = const(0x08)
_ENABLE_AEN = const(0x02)
_ENABLE_PON = const(0x01)

_GAINS = (1, 4, 16, 60)
_CYCLES = (0, 1, 2, 3, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60)
_INTEGRATION_TIME_THRESHOLD_LOW = 2.4
_INTEGRATION_TIME_THRESHOLD_HIGH = 614.4

_TCS3472_DEFAULT_ADDR = const(0x29)


class TCS3472:
    """! COLOR is color recognition unit integrated with TCS3472 chipset. As the name says, COLOR is able to detect color value and return RGB data as response.

    @en Unit Color 英文介绍
    @cn Unit Color 中文介绍

    @color #0FE6D7
    @link https://docs.m5stack.com/en/unit/COLOR
    @image https://static-cdn.m5stack.com/resource/docs/products/unit/COLOR/img-5e8f77b1-0a2d-4810-8b8d-c2374bd738fb.webp
    @category unit

    @example

    """

    def __init__(self, i2c: I2C, address: int = _TCS3472_DEFAULT_ADDR) -> None:
        """! Initialize TCS3472 sensor with the given I2C interface and address.

        @param i2c: The I2C bus instance for communication.
        @param address: The I2C address of the sensor, default is _TCS3472_DEFAULT_ADDR.
        """
        self._i2c = i2c
        self._addr = address
        self._active = False
        self._BUFFER = bytearray(2)
        self.set_integration_time(2.4)
        self._glass_attenuation = None
        self.set_glass_attenuation(1.0)
        # Check sensor ID is expected value.
        sensor_id = self._read_u8(_REGISTER_SENSORID)
        if sensor_id not in (0x4D, 0x44, 0x10):
            raise RuntimeError("Incorrect sensor ID ({0:#0X})".format(sensor_id))

    def get_lux(self) -> float:
        """! Get the lux value computed from the color channels.

        @return: The computed lux value as a float.
        """
        return self._temperature_and_lux_dn40()[0]

    def get_color_temperature(self) -> float:
        """! Get the color temperature in degrees Kelvin.

        @return: The color temperature as a float in Kelvin.
        """
        return self._temperature_and_lux_dn40()[1]

    def get_color_rgb_bytes(self) -> tuple[int, int, int]:
        """! Get the RGB color detected by the sensor.

        @return: A tuple of red, green, and blue component values as bytes (0-255).
        """
        r, g, b, clear = self.get_color_raw()

        # Avoid divide by zero errors ... if clear = 0 return black
        if clear == 0:
            return (0, 0, 0)

        # Each color value is normalized to clear, to obtain int values between 0 and 255.
        # A gamma correction of 2.5 is applied to each value as well, first dividing by 255,
        # since gamma is applied to values between 0 and 1
        red = int(pow((int((r / clear) * 256) / 255), 2.5) * 255)
        green = int(pow((int((g / clear) * 256) / 255), 2.5) * 255)
        blue = int(pow((int((b / clear) * 256) / 255), 2.5) * 255)

        # Handle possible 8-bit overflow
        red = min(red, 255)
        green = min(green, 255)
        blue = min(blue, 255)
        return (red, green, blue)

    def get_color_r(self) -> int:
        """! Get the red component of the RGB color.

        @return: The red component value (0-255).
        """
        r, _, _, clear = self.get_color_raw()
        # Avoid divide by zero errors ... if clear = 0 return black
        if clear == 0:
            return 0
        red = int(pow((int((r / clear) * 256) / 255), 2.5) * 255)
        return min(red, 255)

    def get_color_g(self) -> int:
        """! Get the green component of the RGB color.

        @return: The green component value (0-255).
        """
        _, g, _, clear = self.get_color_raw()
        # Avoid divide by zero errors ... if clear = 0 return black
        if clear == 0:
            return 0
        green = int(pow((int((g / clear) * 256) / 255), 2.5) * 255)
        return min(green, 255)

    def get_color_b(self) -> int:
        """! Get the blue component of the RGB color.

        @return: The blue component value (0-255).
        """
        _, _, b, clear = self.get_color_raw()
        # Avoid divide by zero errors ... if clear = 0 return black
        if clear == 0:
            return 0
        blue = int(pow((int((b / clear) * 256) / 255), 2.5) * 255)
        return min(blue, 255)

    def get_color_h(self) -> int:
        """! Get the hue (H) value of the color in degrees.

        @return: The hue value as an integer in the range [0, 360].
        """
        rgb = self.get_color_rgb_bytes()
        c_max = max(rgb[0], rgb[1], rgb[2])
        c_min = min(rgb[0], rgb[1], rgb[2])
        if c_max == c_min:
            return 0
        elif c_max == rgb[0] and rgb[1] >= rgb[2]:
            return int(60 * ((rgb[1] - rgb[2]) / (c_max) - (c_min)))
        elif c_max == rgb[0] and rgb[1] < rgb[2]:
            return int(60 * ((rgb[1] - rgb[2]) / (c_max - c_min))) + 360
        elif c_max == rgb[1]:
            return int(60 * ((rgb[2] - rgb[0]) / (c_max - c_min))) + 120
        elif c_max == rgb[2]:
            return int(60 * ((rgb[0] - rgb[1]) / (c_max - c_min))) + 240

    def get_color_s(self) -> float:
        """! Get the saturation (S) value of the color.

        @return: The saturation value as a float in the range [0, 1].
        """
        rgb = self.get_color_rgb_bytes()
        c_max = max(rgb[0], rgb[1], rgb[2])
        c_min = min(rgb[0], rgb[1], rgb[2])
        if c_max == 0:
            return 0
        else:
            return 1.0 - c_min / c_max

    def get_color_v(self) -> float:
        """! Get the value (V) of the color (brightness).

        @return: The value as a float in the range [0, 1].
        """
        rgb = self.get_color_rgb_bytes()
        c_max = max(rgb[0], rgb[1], rgb[2])
        return c_max / 255

    def get_color(self) -> int:
        """! Get the RGB color as an integer value.
        Examples: Red = 16711680 (0xff0000), Green = 65280 (0x00ff00),
        Blue = 255 (0x0000ff), SlateGray = 7372944 (0x708090)
        @return: An integer representing the RGB color, with 8 bits per channel.
        """
        r, g, b = self.get_color_rgb_bytes()
        return (r << 16) | (g << 8) | b

    def get_color565(self) -> int:
        """! Get the RGB color in 5-6-5 format as an integer.

        @return: An integer representing the RGB color in 5-6-5 format.
        """
        r, g, b = self.get_color_rgb_bytes()
        return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | ((b & 0xF8) >> 3)

    def get_active(self) -> bool:
        """! Get the active state of the sensor.

        @return: True if the sensor is active, False if it is inactive.
        """
        return self._active

    def set_active(self, val: bool) -> None:
        """! Set the active state of the sensor.

        @param val: True to activate the sensor, False to deactivate it.
        """
        val = bool(val)
        if self._active == val:
            return
        self._active = val
        enable = self._read_u8(_REGISTER_ENABLE)
        if val:
            self._write_u8(_REGISTER_ENABLE, enable | _ENABLE_PON)
            time.sleep(0.003)
            self._write_u8(_REGISTER_ENABLE, enable | _ENABLE_PON | _ENABLE_AEN)
        else:
            self._write_u8(_REGISTER_ENABLE, enable & ~(_ENABLE_PON | _ENABLE_AEN))

    def get_integration_time(self) -> float:
        """! Get the integration time of the sensor in milliseconds.

        @return: The integration time as a float.
        """
        return self._integration_time

    def set_integration_time(self, val: float) -> None:
        """! Set the integration time of the sensor.

        @param val: The desired integration time in milliseconds.
        @raise ValueError: If the integration time is out of the allowed range.
        """
        if not _INTEGRATION_TIME_THRESHOLD_LOW <= val <= _INTEGRATION_TIME_THRESHOLD_HIGH:
            raise ValueError(
                "Integration Time must be between '{0}' and '{1}'".format(
                    _INTEGRATION_TIME_THRESHOLD_LOW, _INTEGRATION_TIME_THRESHOLD_HIGH
                )
            )
        cycles = int(val / 2.4)
        self._integration_time = cycles * 2.4
        self._write_u8(_REGISTER_ATIME, 256 - cycles)

    def get_gain(self) -> int:
        """! Get the gain of the sensor.

        @return: The gain value, which should be one of 1, 4, 16, or 60.
        """
        return _GAINS[self._read_u8(_REGISTER_CONTROL) & 0x11]

    def set_gain(self, val: int) -> None:
        """! Set the gain of the sensor.

        @param val: The desired gain value (1, 4, 16, or 60).
        @raise ValueError: If the gain is not one of the allowed values.
        """
        if val not in _GAINS:
            raise ValueError("Gain should be one of the following values: {0}".format(_GAINS))
        self._write_u8(_REGISTER_CONTROL, _GAINS.index(val))

    def read_interrupt(self) -> bool:
        """! Read the interrupt status.

        @return: True if the interrupt is set, False otherwise.
        """
        return bool(self._read_u8(_REGISTER_STATUS) & _ENABLE_AIEN)

    def clear_interrupt(self) -> None:
        """! Clear the interrupt status of the sensor by writing to the interrupt register."""
        self._i2c.write(b"\xe6")

    def get_color_raw(self):
        """! Read the raw RGBC color detected by the sensor.

        @return: A tuple containing raw red, green, blue, and clear color data.
        """
        was_active = self.get_active()
        self.set_active(True)
        while not self._valid():
            time.sleep((self._integration_time + 0.9) / 1000.0)
        data = tuple(
            self._read_u16(reg)
            for reg in (
                _REGISTER_RDATA,
                _REGISTER_GDATA,
                _REGISTER_BDATA,
                _REGISTER_CDATA,
            )
        )
        self.set_active(was_active)
        return data

    def get_cycles(self):
        """! Get the persistence cycles of the sensor.

        @return: The persistence cycles or -1 if interrupts are disabled.
        """
        if self._read_u8(_REGISTER_ENABLE) & _ENABLE_AIEN:
            return _CYCLES[self._read_u8(_REGISTER_APERS) & 0x0F]
        return -1

    def set_cycles(self, val: int) -> None:
        """! Set the persistence cycles for the sensor.

        @param val: The number of persistence cycles, or -1 to disable interrupts.
        @raise ValueError: If the value is not one of the permitted cycle values.
        """
        enable = self._read_u8(_REGISTER_ENABLE)
        if val == -1:
            self._write_u8(_REGISTER_ENABLE, enable & ~(_ENABLE_AIEN))
        else:
            if val not in _CYCLES:
                raise ValueError("Only the following cycles are permitted: {0}".format(_CYCLES))
            self._write_u8(_REGISTER_ENABLE, enable | _ENABLE_AIEN)
            self._write_u8(_REGISTER_APERS, _CYCLES.index(val))

    def get_min_value(self):
        """! Get the minimum threshold value (AILT register) of the sensor.

        @return: The minimum threshold value.
        """
        return self._read_u16(_REGISTER_AILT)

    def set_min_value(self, val: int):
        """! Set the minimum threshold value (AILT register) of the sensor.

        @param val: The minimum threshold value to set.
        """
        self._write_u16(_REGISTER_AILT, val)

    def get_max_value(self):
        """! Get the maximum threshold value (AIHT register) of the sensor.

        @return: The maximum threshold value.
        """
        return self._read_u16(_REGISTER_AIHT)

    def set_max_value(self, val: int):
        """! Set the maximum threshold value (AIHT register) of the sensor.

        @param val: The maximum threshold value to set.
        """
        self._write_u16(_REGISTER_AIHT, val)

    def _temperature_and_lux_dn40(self) -> tuple[float, float]:
        """! Convert the raw RGBC values to color temperature in degrees Kelvin and compute lux.

        @return: A tuple containing the computed lux and color temperature, or None if the computation fails.
        """
        # pylint: disable=invalid-name, too-many-locals

        # Initial input values
        atime = self._read_u8(_REGISTER_ATIME)
        atime_ms = (256 - atime) * 2.4
        againx = self.get_gain()
        r, g, b, c = self.get_color_raw()

        # Device specific values (DN40 Table 1 in Appendix I)
        ga = self.get_glass_attenuation()  # Glass Attenuation Factor
        df = 310.0  # Device Factor
        r_coef = 0.136  # |
        g_coef = 1.0  # | used in lux computation
        b_coef = -0.444  # |
        ct_coef = 3810  # Color Temperature Coefficient
        ct_offset = 1391  # Color Temperature Offset

        # Analog/Digital saturation (DN40 3.5)
        saturation = 65535 if 256 - atime > 63 else 1024 * (256 - atime)

        # Ripple saturation (DN40 3.7)
        if atime_ms < 150:
            saturation -= saturation / 4

        # Check for saturation and mark the sample as invalid if true
        if c >= saturation:
            return None, None

        # IR Rejection (DN40 3.1)
        ir = (r + g + b - c) / 2 if r + g + b > c else 0.0
        r2 = r - ir
        g2 = g - ir
        b2 = b - ir

        # Lux Calculation (DN40 3.2)
        g1 = r_coef * r2 + g_coef * g2 + b_coef * b2
        cpl = (atime_ms * againx) / (ga * df)
        cpl = 0.001 if cpl == 0 else cpl
        lux = g1 / cpl

        # ct Calculations (DN40 3.4)
        r2 = 0.001 if r2 == 0 else r2
        ct = ct_coef * b2 / r2 + ct_offset

        return lux, ct

    def get_glass_attenuation(self):
        """! Get the Glass Attenuation factor used to compensate for lower light levels due to glass presence.

        @return: The glass attenuation factor (ga).
        """
        return self._glass_attenuation

    def set_glass_attenuation(self, value: float):
        """! Set the Glass Attenuation factor used to compensate for lower light levels due to glass presence.

        @param value: The glass attenuation factor to set. Must be greater than or equal to 1.
        @raise ValueError: If the value is less than 1.
        """
        if value < 1:
            raise ValueError("Glass attenuation factor must be at least 1.")
        self._glass_attenuation = value

    def _valid(self) -> bool:
        """! Check if the sensor data is valid.

        @return: True if the sensor data is valid, False otherwise.
        """
        return bool(self._read_u8(_REGISTER_STATUS) & 0x01)

    def _read_u8(self, reg: int) -> int:
        """! Read a single byte from the specified register.

        @param reg: The register address to read from.
        @return: The byte value read from the register.
        """
        buf = memoryview(self._BUFFER)
        self._i2c.readfrom_mem_into(self._addr, (reg | _COMMAND_BIT) & 0xFF, buf[0:1])
        return buf[0]

    def _write_u8(self, reg: int, val: int) -> None:
        """! Write a single byte to the specified register.

        @param reg: The register address to write to.
        @param val: The byte value to write to the register.
        """
        buf = memoryview(self._BUFFER)[0:1]
        buf[0] = val & 0xFF
        self._i2c.writeto_mem(self._addr, (reg | _COMMAND_BIT) & 0xFF, buf)

    def _read_u16(self, reg: int) -> int:
        """! Read a 16-bit value from the specified register.

        @param reg: The register address to read from.
        @return: The 16-bit value read from the register.
        """
        buf = memoryview(self._BUFFER)
        self._i2c.readfrom_mem_into(self._addr, (reg | _COMMAND_BIT) & 0xFF, buf[0:2])
        return (buf[1] << 8) | buf[0]

    def _write_u16(self, reg: int, val: int) -> None:
        """! Write a 16-bit value"""
        buf = memoryview(self._BUFFER)[0:2]
        buf[0] = val & 0xFF
        buf[1] = (val >> 8) & 0xFF
        self._i2c.writeto_mem(self._addr, (reg | _COMMAND_BIT) & 0xFF, buf)
