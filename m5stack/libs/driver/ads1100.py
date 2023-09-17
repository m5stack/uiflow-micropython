from micropython import const
from machine import I2C
import time

try:
    from typing_extensions import Literal
except ImportError:
    pass

_ADS1100_DEFAULT_ADDRESS = const(0x48)

_ST_BSY_BIT = const(0b10000000)
_SC_BIT = const(0b00010000)
_DR_BIT = const(0b00001100)
_PGA_BIT = const(0b00000011)

_DATA_RATE = (128, 32, 16, 8)

_GAINS = (1, 2, 4, 8)


class ADS1100:
    """Driver for the ADS1100 ADC Converter."""

    CONTINUOUS = const(0)
    SINGLE = const(1)

    # Global buffer to prevent allocations and heap fragmentation.
    # Note this is not thread-safe or re-entrant by design!
    _BUFFER = bytearray(3)

    def __init__(self, i2c: I2C, address: int = _ADS1100_DEFAULT_ADDRESS):
        self._i2c = i2c
        self._addr = address
        self._config = 0x8C
        self._mode = self.CONTINUOUS
        self._rate = 8
        self._gain = 1

    def get_value(self) -> int:
        """Read the adc value detected by the ads1100."""
        self._i2c.writeto(self._addr, self._config.to_bytes(1, "big"))
        time.sleep(0.1)
        self._read()
        self._config = self._BUFFER[2]
        if self._config & _SC_BIT == 0 or (
            self._config & _SC_BIT > 0 and self._config & _ST_BSY_BIT == 0
        ):
            return ((self._BUFFER[0] << 8) | (self._BUFFER[1])) & 0xFFFF
        return None

    def get_voltage(self) -> float:
        """The voltage value computed from the adc value."""
        min_code = {8: -32768, 16: -16384, 32: -8192, 128: -2048}
        voltage = 0
        value = self.get_value()
        if value is not None:
            voltage = ((value / (-1 * min_code.get(self._rate) * self._gain)) * 3.3) * 4
        return voltage

    def get_raw_value(self):
        self._i2c.writeto(self._addr, self._config.to_bytes(1, "big"))
        time.sleep(0.1)
        self._read()
        self._config = self._BUFFER[2]
        return self._BUFFER

    def get_operating_mode(self) -> Literal[0, 1]:
        """The conversion mode of the ads1100"""
        return self._mode

    def set_operating_mode(self, mode: Literal[0, 1]) -> None:
        self._mode = mode
        self._config = (self._config & (~_SC_BIT)) | (mode << 4)
        self._i2c.writeto(self._addr, self._config.to_bytes(1, "big"))

    def get_data_rate(self):
        return self._rate

    def set_data_rate(self, data_rate):
        """The rate of the ads1100.

        Should be a value of 8, 16, 32, or 128.
        """
        if data_rate not in _DATA_RATE:
            raise ValueError(
                "DATA RATE should be one of the following values: {0}".format(_DATA_RATE)
            )
        self._rate = data_rate
        self._config = (self._config & (~_DR_BIT)) | (_DATA_RATE.index(data_rate) << 2)
        self._i2c.writeto(self._addr, self._config.to_bytes(1, "big"))

    def get_gain(self):
        return self._gain

    def set_gain(self, gain):
        """The gain of the ads1100.
        Should be a value of 1, 2, 4, or 8.
        """
        if gain not in _GAINS:
            raise ValueError("Gain should be one of the following values: {0}".format(_GAINS))
        self._gain = gain
        self._config = (self._config & (~_PGA_BIT)) | _GAINS.index(gain)
        self._i2c.writeto(self._addr, self._config.to_bytes(1, "big"))

    def _read(self) -> None:
        self._i2c.readfrom_into(self._addr, self._BUFFER)
