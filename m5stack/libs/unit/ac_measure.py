from machine import I2C
from micropython import const
import struct
from .pahub import PAHUB
from .unit_helper import UnitError
import time

try:
    from typing import Union
except ImportError:
    pass

AC_MEASURE_ADDR = 0x42

VOLTAGE_STR_REG = 0x00
CURRENT_STR_REG = 0x10
ACTIVE_POWER_STR_REG = 0x20
APPARENT_POWER_STR_REG = 0x30
POWER_FACTOR_STR_REG = 0x40
KWH_STR_REG = 0x50
VOLTAGE_BYTE_REG = 0x60
CURRENT_BYTE_REG = 0x70
ACTIVE_POWER_BYTE_REG = 0x80
APPARENT_POWER_BYTE_REG = 0x90
POWER_FACTOR_BYTE_REG = 0xA0
KWH_BYTE_REG = 0xB0
VOLTAGE_COEFF_REG = 0xC0
CURRENT_COEFF_REG = 0xD0
SAVE_COEFF_REG = 0xE0
DATA_READY_REG = 0xFC
BOOTLOADER_REG = 0xFD
FIRM_VER_REG = 0xFE
I2C_ADDR_REG = 0xFF


class AC_MEASURE:
    def __init__(self, i2c: Union[I2C, PAHUB], slave_addr: int = AC_MEASURE_ADDR) -> None:
        """
        AC Measure Initialize Function
        Set I2C port, AC Measure Slave Address
        """
        self.ac_measure_i2c = i2c
        self.init_i2c_address(slave_addr)

    def init_i2c_address(self, slave_addr: int = AC_MEASURE_ADDR) -> None:
        """
        change the i2c address
        slave_addr : 1 to 127
        """
        if slave_addr >= 0x01 and slave_addr <= 0x7F:
            self.i2c_addr = slave_addr
        if not (self.i2c_addr in self.ac_measure_i2c.scan()):
            raise UnitError("AC Measure unit maybe not connect")

    def get_voltage_str(self) -> str:
        """
        get voltage string value
        """
        return self.ac_measure_i2c.readfrom_mem(self.i2c_addr, VOLTAGE_STR_REG, 7).decode()

    def get_current_str(self) -> str:
        """
        get current string value
        """
        return self.ac_measure_i2c.readfrom_mem(self.i2c_addr, CURRENT_STR_REG, 7).decode()

    def get_active_power_str(self) -> str:
        """
        get active power string value
        """
        return self.ac_measure_i2c.readfrom_mem(self.i2c_addr, ACTIVE_POWER_STR_REG, 7).decode()

    def get_apparent_power_str(self) -> str:
        """
        get apparent power string value
        """
        return self.ac_measure_i2c.readfrom_mem(self.i2c_addr, APPARENT_POWER_STR_REG, 7).decode()

    def get_power_factor_str(self) -> str:
        """
        get power factor string value
        """
        return self.ac_measure_i2c.readfrom_mem(self.i2c_addr, POWER_FACTOR_STR_REG, 4).decode()

    def get_kwh_str(self) -> str:
        """
        get kwh string value
        """
        return self.ac_measure_i2c.readfrom_mem(self.i2c_addr, KWH_STR_REG, 11).decode()

    def get_voltage_byte(self) -> int:
        """
        get voltage raw value
        """
        buf = self.ac_measure_i2c.readfrom_mem(self.i2c_addr, VOLTAGE_BYTE_REG, 2)
        return struct.unpack("<H", buf)[0]

    def get_current_byte(self) -> int:
        """
        get current raw value
        """
        buf = self.ac_measure_i2c.readfrom_mem(self.i2c_addr, CURRENT_BYTE_REG, 2)
        return struct.unpack("<H", buf)[0]

    def get_active_power_byte(self) -> int:
        """
        get active power raw value
        """
        buf = self.ac_measure_i2c.readfrom_mem(self.i2c_addr, ACTIVE_POWER_BYTE_REG, 4)
        return struct.unpack("<I", buf)[0]

    def get_apparent_power_byte(self) -> int:
        """
        get apparent power raw value
        """
        buf = self.ac_measure_i2c.readfrom_mem(self.i2c_addr, APPARENT_POWER_BYTE_REG, 4)
        return struct.unpack("<I", buf)[0]

    def get_power_factor_byte(self) -> int:
        """
        get power factor raw value
        """
        return self.ac_measure_i2c.readfrom_mem(self.i2c_addr, POWER_FACTOR_BYTE_REG, 1)[0]

    def get_kwh_byte(self) -> int:
        """
        get kwh raw value
        """
        buf = self.ac_measure_i2c.readfrom_mem(self.i2c_addr, KWH_BYTE_REG, 4)
        return struct.unpack("<I", buf)[0]

    def get_voltage_coeff(self) -> int:
        """
        get voltage coefficient value
        """
        return self.ac_measure_i2c.readfrom_mem(self.i2c_addr, VOLTAGE_COEFF_REG, 1)[0]

    def set_voltage_coeff(self, value: int) -> None:
        """
        set voltage coefficient value
        value: 0 - 255
        """
        self.ac_measure_i2c.writeto_mem(self.i2c_addr, VOLTAGE_COEFF_REG, bytearray([int(value)]))

    def get_current_coeff(self) -> int:
        """
        get current coefficient value
        """
        return self.ac_measure_i2c.readfrom_mem(self.i2c_addr, CURRENT_COEFF_REG, 1)[0]

    def set_current_coeff(self, value: int) -> None:
        """
        set current coefficient value
        value: 0 - 255
        """
        self.ac_measure_i2c.writeto_mem(self.i2c_addr, CURRENT_COEFF_REG, bytearray([int(value)]))

    def set_save_coeff(self) -> None:
        """
        to save flash in volt and current coefficient value
        """
        self.ac_measure_i2c.writeto_mem(self.i2c_addr, SAVE_COEFF_REG, bytearray([0x01]))
        time.sleep_ms(100)

    def get_data_ready(self) -> bool:
        """
        get data is ready?
        """
        status = self.ac_measure_i2c.readfrom_mem(self.i2c_addr, DATA_READY_REG, 1)[0]
        return True if status == 1 else False

    def set_jump_bootloader(self) -> None:
        """
        set jump to bootloader
        """
        self.ac_measure_i2c.writeto_mem(self.i2c_addr, BOOTLOADER_REG, bytearray([0x01]))

    def get_device_status(self, mode: int) -> int:
        """
        get firmware version and i2c address.
        mode : 0xFE and 0xFF
        """
        if mode >= FIRM_VER_REG and mode <= I2C_ADDR_REG:
            return self.ac_measure_i2c.readfrom_mem(self.i2c_addr, mode, 1)[0]

    def set_i2c_address(self, addr: int) -> None:
        """
        set i2c address.
        addr: 0x01 to 0x7F
        """
        if addr >= 0x01 and addr <= 0x7F:
            if addr != self.i2c_addr:
                self.ac_measure_i2c.writeto_mem(self.i2c_addr, I2C_ADDR_REG, bytearray([addr]))
                self.i2c_addr = addr
                time.sleep_ms(100)
