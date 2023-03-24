from machine import I2C
from micropython import const
import time

# Register and command constants:
_REGISTER_ENABLE   = const(0x00)
_REGISTER_ATIME    = const(0x01)
_REGISTER_WTIME    = const(0x03)
_REGISTER_AILT     = const(0x04)
_REGISTER_AILTH    = const(0x05)
_REGISTER_AIHT     = const(0x06)
_REGISTER_AIHTH    = const(0x07)
_REGISTER_APERS    = const(0x0C)
_REGISTER_CONFIG   = const(0x0D)
_REGISTER_CONTROL  = const(0x0F)
_REGISTER_SENSORID = const(0x12)
_REGISTER_STATUS   = const(0x13)
_REGISTER_CDATA    = const(0x14)
_REGISTER_CDATAH   = const(0x15)
_REGISTER_RDATA    = const(0x16)
_REGISTER_RDATAH   = const(0x17)
_REGISTER_GDATA    = const(0x18)
_REGISTER_GDATAH   = const(0x19)
_REGISTER_BDATA    = const(0x1A)
_REGISTER_BDATAH   = const(0x1B)

# Select Command Register. Must write as 1 when addressing COMMAND register.
_COMMAND_BIT = const(0x80)

# Enable Register Fields
_ENABLE_AIEN = const(0x10)
_ENABLE_WEN  = const(0x08)
_ENABLE_AEN  = const(0x02)
_ENABLE_PON  = const(0x01)

_GAINS = (1, 4, 16, 60)
_CYCLES = (0, 1, 2, 3, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60)
_INTEGRATION_TIME_THRESHOLD_LOW = 2.4
_INTEGRATION_TIME_THRESHOLD_HIGH = 614.4

_TCS3472_DEFAULT_ADDR = const(0x29)

class TCS3472:
    def __init__(self, i2c: I2C, address: int=_TCS3472_DEFAULT_ADDR):
        self._i2c = i2c
        self._addr = address
        self._active = False
        self._BUFFER = bytearray(2)
        self.set_integration_time(2.4)
        self._glass_attenuation = None
        self.set_glass_attenuation(1.0)
        # Check sensor ID is expectd value.
        sensor_id = self._read_u8(_REGISTER_SENSORID)
        if sensor_id not in (0x4d, 0x44, 0x10):
            raise RuntimeError("incorrect sensor id({0:#0X})".format(sensor_id))

    def get_lux(self):
        """The lux value computed from the color channels."""
        return self._temperature_and_lux_dn40()[0]

    def get_color_temperature(self):
        """The color temperature in degrees Kelvin."""
        return self._temperature_and_lux_dn40()[1]

    def get_color_rgb_bytes(self):
        """Read the RGB color detected by the sensor.  Returns a 3-tuple of
        red, green, blue component values as bytes (0-255).
        """
        r, g, b, clear = self.get_color_raw()

        # Avoid divide by zero errors ... if clear = 0 return black
        if clear == 0:
            return (0, 0, 0)

        # Each color value is normalized to clear, to obtain int values between 0 and 255.
        # A gamma correction of 2.5 is applied to each value as well, first dividing by 255,
        # since gamma is applied to values between 0 and 1
        red   = int(pow((int((r / clear) * 256) / 255), 2.5) * 255)
        green = int(pow((int((g / clear) * 256) / 255), 2.5) * 255)
        blue  = int(pow((int((b / clear) * 256) / 255), 2.5) * 255)

        # Handle possible 8-bit overflow
        red   = min(red,   255)
        green = min(green, 255)
        blue  = min(blue,  255)
        return (red, green, blue)

    def get_color_r(self) -> int:
        r, _, _, clear = self.get_color_raw()
        # Avoid divide by zero errors ... if clear = 0 return black
        if clear == 0:
            return 0
        red   = int(pow((int((r / clear) * 256) / 255), 2.5) * 255)
        return min(red,   255)

    def get_color_g(self) -> int:
        _, g, _, clear = self.get_color_raw()
        # Avoid divide by zero errors ... if clear = 0 return black
        if clear == 0:
            return 0
        green = int(pow((int((g / clear) * 256) / 255), 2.5) * 255)
        return min(green, 255)

    def get_color_b(self) -> int:
        _, _, b, clear = self.get_color_raw()
        # Avoid divide by zero errors ... if clear = 0 return black
        if clear == 0:
            return 0
        blue  = int(pow((int((b / clear) * 256) / 255), 2.5) * 255)
        return min(blue, 255)

    def get_color_h(self) -> int:
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
        rgb = self.get_color_rgb_bytes()
        c_max = max(rgb[0], rgb[1], rgb[2])
        c_min = min(rgb[0], rgb[1], rgb[2])
        if c_max == 0:
            return 0
        else:
            return (1.0 - c_min / c_max)

    def get_color_v(self) -> float:
        rgb = self.get_color_rgb_bytes()
        c_max = max(rgb[0], rgb[1], rgb[2])
        return c_max / 255

    def get_color(self):
        """Read the RGB color detected by the sensor. Returns an int with 8 bits per channel.
        Examples: Red = 16711680 (0xff0000), Green = 65280 (0x00ff00),
        Blue = 255 (0x0000ff), SlateGray = 7372944 (0x708090)
        """
        r, g, b = self.get_color_rgb_bytes()
        return (r << 16) | (g << 8) | b

    def get_color565(self):
        """Read the RGB color detected by the sensor. Returns an int with 8 bits per channel.
        Examples: Red = 16252928 (0xf80000), Green = 64512 (0x00fc00),
        Blue = 248 (0x0000f8), SlateGray = 7372944 (0x708090)
        """
        r, g, b = self.get_color_rgb_bytes()
        return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | ((b & 0xF8) >> 3)

    def get_active(self) -> bool:
        """The active state of the sensor.  Boolean value that will
        enable/activate the sensor with a value of True and disable with a
        value of False.
        """
        return self._active

    def set_active(self, val: bool) -> None:
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

    def get_integration_time(self):
        """The integration time of the sensor in milliseconds."""
        return self._integration_time

    def set_integration_time(self, val: float):
        if (
            not _INTEGRATION_TIME_THRESHOLD_LOW
            <= val
            <= _INTEGRATION_TIME_THRESHOLD_HIGH
        ):
            raise ValueError(
                "Integration Time must be between '{0}' and '{1}'".format(
                    _INTEGRATION_TIME_THRESHOLD_LOW, _INTEGRATION_TIME_THRESHOLD_HIGH
                )
            )
        cycles = int(val / 2.4)
        self._integration_time = (
            cycles * 2.4
        )  # pylint: disable=attribute-defined-outside-init
        self._write_u8(_REGISTER_ATIME, 256 - cycles)

    def get_gain(self):
        """The gain of the sensor.  Should be a value of 1, 4, 16, or 60.
        """
        return _GAINS[self._read_u8(_REGISTER_CONTROL) & 0x11]

    def set_gain(self, val: int):
        if val not in _GAINS:
            raise ValueError(
                "Gain should be one of the following values: {0}".format(_GAINS)
            )
        self._write_u8(_REGISTER_CONTROL, _GAINS.index(val))

    def read_interrupt(self):
        """True if the interrupt is set. Can be set to False (and only False)
        to clear the interrupt.
        """
        return bool(self._read_u8(_REGISTER_STATUS) & _ENABLE_AIEN)

    def clear_interrupt(self):
        self._i2c.write(b"\xe6")

    def get_color_raw(self):
        """Read the raw RGBC color detected by the sensor.  Returns a 4-tuple of
        16-bit red, green, blue, clear component byte values (0-65535).
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
        """The persistence cycles of the sensor."""
        if self._read_u8(_REGISTER_ENABLE) & _ENABLE_AIEN:
            return _CYCLES[self._read_u8(_REGISTER_APERS) & 0x0F]
        return -1

    def set_cycles(self, val: int):
        enable = self._read_u8(_REGISTER_ENABLE)
        if val == -1:
            self._write_u8(_REGISTER_ENABLE, enable & ~(_ENABLE_AIEN))
        else:
            if val not in _CYCLES:
                raise ValueError(
                    "Only the following cycles are permitted: {0}".format(_CYCLES)
                )
            self._write_u8(_REGISTER_ENABLE, enable | _ENABLE_AIEN)
            self._write_u8(_REGISTER_APERS, _CYCLES.index(val))

    def get_min_value(self):
        """The minimum threshold value (AILT register) of the
        sensor as a 16-bit unsigned value.
        """
        return self._read_u16(_REGISTER_AILT)

    def set_min_value(self, val: int):
        self._write_u16(_REGISTER_AILT, val)

    def get_max_value(self):
        """The minimum threshold value (AIHT register) of the
        sensor as a 16-bit unsigned value.
        """
        return self._read_u16(_REGISTER_AIHT)

    def set_max_value(self, val: int):
        self._write_u16(_REGISTER_AIHT, val)

    def _temperature_and_lux_dn40(self) -> tuple[float, float]:
        """Converts the raw R/G/B values to color temperature in degrees
        Kelvin using the algorithm described in DN40 from Taos (now AMS).
        Also computes lux. Returns tuple with both values or tuple of Nones
        if computation can not be done.
        """
        # pylint: disable=invalid-name, too-many-locals

        # Initial input values
        ATIME = self._read_u8(_REGISTER_ATIME)
        ATIME_ms = (256 - ATIME) * 2.4
        AGAINx = self.get_gain()
        R, G, B, C = self.get_color_raw()

        # Device specific values (DN40 Table 1 in Appendix I)
        GA = self.get_glass_attenuation() # Glass Attenuation Factor
        DF = 310.0  # Device Factor
        R_Coef = 0.136  # |
        G_Coef = 1.0  # | used in lux computation
        B_Coef = -0.444  # |
        CT_Coef = 3810  # Color Temperature Coefficient
        CT_Offset = 1391  # Color Temperatuer Offset

        # Analog/Digital saturation (DN40 3.5)
        SATURATION = 65535 if 256 - ATIME > 63 else 1024 * (256 - ATIME)

        # Ripple saturation (DN40 3.7)
        if ATIME_ms < 150:
            SATURATION -= SATURATION / 4

        # Check for saturation and mark the sample as invalid if true
        if C >= SATURATION:
            return None, None

        # IR Rejection (DN40 3.1)
        IR = (R + G + B - C) / 2 if R + G + B > C else 0.0
        R2 = R - IR
        G2 = G - IR
        B2 = B - IR

        # Lux Calculation (DN40 3.2)
        G1 = R_Coef * R2 + G_Coef * G2 + B_Coef * B2
        CPL = (ATIME_ms * AGAINx) / (GA * DF)
        CPL = 0.001 if CPL == 0 else CPL
        lux = G1 / CPL

        # CT Calculations (DN40 3.4)
        R2 = 0.001 if R2 == 0 else R2
        CT = CT_Coef * B2 / R2 + CT_Offset

        return lux, CT

    def get_glass_attenuation(self):
        """The Glass Attenuation (FA) factor used to compensate for lower light
        levels at the device due to the possible presence of glass. The GA is
        the inverse of the glass transmissivity (T), so :math:`GA = 1/T`. A transmissivity
        of 50% gives GA = 1 / 0.50 = 2. If no glass is present, use GA = 1.
        See Application Note: DN40-Rev 1.0 – Lux and CCT Calculations using
        ams Color Sensors for more details.
        """
        return self._glass_attenuation

    def set_glass_attenuation(self, value: float):
        if value < 1:
            raise ValueError("Glass attenuation factor must be at least 1.")
        self._glass_attenuation = value

    def _valid(self) -> bool:
        # Check if the status bit is set and the chip is ready.
        return bool(self._read_u8(_REGISTER_STATUS) & 0x01)

    def _read_u8(self, reg: int) -> int:
        buf = memoryview(self._BUFFER)
        self._i2c.readfrom_mem_into(self._addr, (reg | _COMMAND_BIT) & 0xFF, buf[0:1])
        return buf[0]

    def _write_u8(self, reg: int, val: int) -> None:
        buf = memoryview(self._BUFFER)[0:1]
        buf[0] = val & 0xFF
        self._i2c.writeto_mem(self._addr, (reg | _COMMAND_BIT) & 0xFF, buf)

    def _read_u16(self, reg: int) -> int:
        buf = memoryview(self._BUFFER)
        self._i2c.readfrom_mem_into(self._addr, (reg | _COMMAND_BIT) & 0xFF, buf[0:2])
        return (buf[1] << 8) | buf[0]

    def _write_u16(self, reg: int, val: int) -> None:
        buf = memoryview(self._BUFFER)[0:2]
        buf[0] = val & 0xFF
        buf[1] = (val >> 8) & 0xFF
        self._i2c.writeto_mem(self._addr, (reg | _COMMAND_BIT) & 0xFF, buf)
