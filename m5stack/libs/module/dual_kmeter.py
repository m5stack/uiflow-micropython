from .mbus import i2c1
import struct


_DUAL_KMETER_DEFAULT_ADDRESS = 0x11

_TEMP_CELSIUS_REG = const(0x00)
_TEMP_FAHREN_REG = const(0x04)
_TEMP_INT_CELSIUS_REG = const(0x10)
_TEMP_INT_FAHREN_REG = const(0x14)
_KMETER_SELECT_REG = const(0x20)
_TEMP_READY_REG = const(0x30)
_TEMP_STR_CELSIUS_REG = const(0x40)
_TEMP_STR_FAHREN_REG = const(0x50)
_TEMP_INTSTR_CELSIUS_REG = const(0x60)
_FTEMP_INTSTR_FAHREN_REG = const(0x70)
_FIRMWARE_VERSION_REG = const(0xFE)


class DualKmeterBase:
    CELSIUS = const(0)
    FAHRENHEIT = const(1)

    def __init__(self, i2c, address: int = _DUAL_KMETER_DEFAULT_ADDRESS):
        self._i2c = i2c
        self._addr = address

    def get_thermocouple_temperature(self, scale=0) -> int:
        reg = _TEMP_CELSIUS_REG if scale == DualKmeter.CELSIUS else _TEMP_FAHREN_REG
        buff = self._i2c.readfrom_mem(self._addr, reg, 4)
        return round((self._int_convert(buff) / 100), 2)

    def get_kmeter_temperature(self, scale=0) -> int:
        reg = _TEMP_INT_CELSIUS_REG if scale == DualKmeter.CELSIUS else _TEMP_INT_FAHREN_REG
        buff = self._i2c.readfrom_mem(self._addr, reg, 4)
        return round(self._int_convert(buff) / 100, 2)

    def get_kmeter_channel(self) -> int:
        return self._i2c.readfrom_mem(self._addr, _KMETER_SELECT_REG, 1)[0]

    def set_kmeter_channel(self, channel) -> None:
        channel = max(min(channel, 1), 0)
        return self._i2c.writeto_mem(self._addr, _KMETER_SELECT_REG, bytes([channel]))

    def is_ready(self) -> bool:
        status = self._i2c.readfrom_mem(self._addr, _TEMP_READY_REG, 1)[0]
        return True if status == 0 else False

    def get_thermocouple_temperature_string(self, scale=0):
        reg = _TEMP_STR_CELSIUS_REG if scale == DualKmeter.CELSIUS else _TEMP_STR_FAHREN_REG
        return "{:+.2f}".format(float(self._i2c.readfrom_mem(self._addr, reg, 8)))

    def get_kmeter_temperature_string(self, scale=0):
        reg = _TEMP_INTSTR_CELSIUS_REG if scale == DualKmeter.CELSIUS else _FTEMP_INTSTR_FAHREN_REG
        return "{:+.2f}".format(float(self._i2c.readfrom_mem(self._addr, reg, 8)))

    def get_fw_ver(self) -> int:
        return self._i2c.readfrom_mem(self._addr, _FIRMWARE_VERSION_REG, 1)[0]

    def set_address(self, address: int) -> None:
        self._addr = address

    def _int_convert(self, value) -> int:
        return struct.unpack("<i", value)[0]


class DualKmeter(DualKmeterBase):
    def __init__(self, address: int = _DUAL_KMETER_DEFAULT_ADDRESS):
        super().__init__(i2c1, address)
