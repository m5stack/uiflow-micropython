# SPDX-FileCopyrightText: 2018 Mikey Sklar for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
from micropython import const

# Internal constants:
_MLX90614_I2CADDR = const(0x5A)

# RAM
_MLX90614_RAWIR1 = const(0x04)
_MLX90614_RAWIR2 = const(0x05)
_MLX90614_TA = const(0x06)
_MLX90614_TOBJ1 = const(0x07)
_MLX90614_TOBJ2 = const(0x08)

# EEPROM
_MLX90614_TOMAX = const(0x20)
_MLX90614_TOMIN = const(0x21)
_MLX90614_PWMCTRL = const(0x22)
_MLX90614_TARANGE = const(0x23)
_MLX90614_EMISS = const(0x24)
_MLX90614_CONFIG = const(0x25)
_MLX90614_ADDR = const(0x0E)
_MLX90614_ID1 = const(0x3C)
_MLX90614_ID2 = const(0x3D)
_MLX90614_ID3 = const(0x3E)
_MLX90614_ID4 = const(0x3F)


class MLX90614:
    def __init__(self, i2c: I2C, address: int = _MLX90614_I2CADDR) -> None:
        self._i2c = i2c
        self._addr = address
        self.buf = bytearray(2)
        self.buf[0] = _MLX90614_CONFIG

    def get_ambient_temperature(self) -> float:
        """Ambient Temperature in Celsius."""
        return self._read_temp(_MLX90614_TA)

    def get_object_temperature(self) -> float:
        """Object Temperature in Celsius."""
        return self._read_temp(_MLX90614_TOBJ1)

    def _read_temp(self, register: int) -> float:
        temp = self._read_16(register)
        temp *= 0.02
        temp -= 273.15
        return temp

    def _read_16(self, register: int) -> int:
        # Read and return a 16-bit unsigned big endian value read from the
        # specified 16-bit register address.
        self._i2c.readfrom_mem_into(self._addr, register, self.buf)
        return self.buf[1] << 8 | self.buf[0]
