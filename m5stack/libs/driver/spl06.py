# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

"""SPL06-001 pressure and temperature sensor driver."""

import math
import time


SPL06_ADDR = 0x76

_PRESSURE_DATA = 0x00
_PRESSURE_CFG = 0x06
_TEMPERATURE_CFG = 0x07
_MEAS_CFG = 0x08
_CFG_REG = 0x09
_RESET = 0x0C
_ID = 0x0D
_COEFFICIENTS = 0x10
_COEF_SOURCE = 0x28

_SCALE = (524288.0, 1572864.0, 3670016.0, 7864320.0, 253952.0, 516096.0, 1040384.0, 2088960.0)


def _signed(value, bits):
    sign = 1 << (bits - 1)
    return value - (1 << bits) if value & sign else value


def _u24(data, offset=0):
    return (data[offset] << 16) | (data[offset + 1] << 8) | data[offset + 2]


class SPL06:
    """SPL06-001 driver using continuous pressure and temperature measurements."""

    def __init__(
        self, i2c, address=SPL06_ADDR, pressure_oversampling=8, temperature_oversampling=8
    ):
        self._i2c = i2c
        self.address = address
        if address not in i2c.scan():
            raise OSError("No SPL06 device was found at address 0x%x" % address)
        if (self._read(_ID) & 0xF0) != 0x10:
            raise OSError("Unexpected SPL06 product ID")

        self._write(_RESET, 0x89)
        time.sleep_ms(40)
        self._read_coefficients()
        self.configure(pressure_oversampling, temperature_oversampling)

    def _read(self, register, size=1):
        data = self._i2c.readfrom_mem(self.address, register, size)
        return data[0] if size == 1 else data

    def _write(self, register, value):
        self._i2c.writeto_mem(self.address, register, bytes((value,)))

    def _read_coefficients(self):
        data = self._read(_COEFFICIENTS, 18)
        self.c0 = _signed((data[0] << 4) | (data[1] >> 4), 12)
        self.c1 = _signed(((data[1] & 0x0F) << 8) | data[2], 12)
        self.c00 = _signed((data[3] << 12) | (data[4] << 4) | (data[5] >> 4), 20)
        self.c10 = _signed(((data[5] & 0x0F) << 16) | (data[6] << 8) | data[7], 20)
        values = []
        for index in range(8, 18, 2):
            values.append(_signed((data[index] << 8) | data[index + 1], 16))
        self.c01, self.c11, self.c20, self.c21, self.c30 = values

    def configure(self, pressure_oversampling=8, temperature_oversampling=8):
        oversampling = (1, 2, 4, 8, 16, 32, 64, 128)
        try:
            pressure_code = oversampling.index(pressure_oversampling)
            temperature_code = oversampling.index(temperature_oversampling)
        except ValueError:
            raise ValueError("SPL06 oversampling must be 1, 2, 4, 8, 16, 32, 64, or 128")

        temperature_source = self._read(_COEF_SOURCE) & 0x80
        self._write(_PRESSURE_CFG, 0x30 | pressure_code)
        self._write(_TEMPERATURE_CFG, temperature_source | 0x30 | temperature_code)
        shift = (0x04 if pressure_code > 3 else 0) | (0x08 if temperature_code > 3 else 0)
        self._write(_CFG_REG, shift)
        self._write(_MEAS_CFG, 0x07)
        self._pressure_scale = _SCALE[pressure_code]
        self._temperature_scale = _SCALE[temperature_code]
        time.sleep_ms(50)

    def read(self):
        """Return compensated temperature in Celsius and pressure in hPa."""
        data = self._read(_PRESSURE_DATA, 6)
        raw_pressure = _signed(_u24(data), 24) / self._pressure_scale
        raw_temperature = _signed(_u24(data, 3), 24) / self._temperature_scale
        temperature = self.c0 * 0.5 + self.c1 * raw_temperature
        pressure = (
            self.c00
            + raw_pressure * (self.c10 + raw_pressure * (self.c20 + raw_pressure * self.c30))
            + raw_temperature * self.c01
            + raw_temperature * raw_pressure * (self.c11 + raw_pressure * self.c21)
        )
        return temperature, pressure / 100.0

    def read_temperature(self):
        """Read and return compensated temperature in degrees Celsius."""
        return self.read()[0]

    def read_pressure(self):
        """Read and return compensated atmospheric pressure in hPa."""
        return self.read()[1]

    @staticmethod
    def altitude(pressure_hpa, sea_level_pressure=1013.25):
        if pressure_hpa <= 0 or sea_level_pressure <= 0:
            return float("nan")
        return 44330.0 * (1.0 - math.pow(pressure_hpa / sea_level_pressure, 0.190294957))
