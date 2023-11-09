from .mbus import i2c1
from .module_helper import ModuleError
import struct
import time

DEV_I2C_ADDR = 0x26
RELAY_REG = 0x10
ADC_8BIT_REG = 0x20
ADC_16BIT_REG = 0x30
I2C_ADDR_REG = 0xFF


class Relay_Stack:
    def __init__(self, i2c, addr):
        self.i2c = i2c
        self.i2c_addr = addr

    def _available(self):
        if not (self.i2c_addr in self.i2c.scan()):
            raise ModuleError("4 relay module maybe not connect")

    def get_relay_status(self, num):
        """
        get RELAY Status.
        reg: 0x10
        num: select only 1 to 4
        return 0 or 1
        """
        num = min(4, max(num, 1))
        return (self.i2c.readfrom_mem(self.i2c_addr, RELAY_REG, 1)[0] >> (num - 1)) & 0x01

    def set_relay_state(self, num, state):
        """
        Set RELAY State.
        reg: 0x10
        num: select only 1 to 4
        state: value is 0 or 1
        """
        num = min(4, max(num, 1))
        data = self.i2c.readfrom_mem(self.i2c_addr, RELAY_REG, 1)[0]
        if state:
            data |= 0x01 << (num - 1)
        else:
            data &= ~(0x01 << (num - 1))
        self.i2c.writeto_mem(self.i2c_addr, RELAY_REG, bytes([data]))

    def set_all_relay_state(self, state):
        """
        Set All RELAY State.
        reg: 0x10
        state: value is 0 or 1
        """
        state = min(1, max(state, 0))
        data = 0x0F if state else 0x00
        self.i2c.writeto_mem(self.i2c_addr, RELAY_REG, bytes([data]))

    # ************************# Version 1.1 #****************************#
    def get_adc_8bit_value(self, volt=0):
        """
        get adc raw/volt 8bit value
        """
        val = self.i2c.readfrom_mem(self.i2c_addr, ADC_8BIT_REG, 1)[0]
        if volt:
            val = (3.3 / 255) * val * 8
            return round(val, 2)
        else:
            return val

    def get_adc_12bit_value(self, volt=0):
        """
        get adc raw/volt 12bit value
        """
        buf = self.i2c.readfrom_mem(self.i2c_addr, ADC_16BIT_REG, 2)
        val = struct.unpack("<H", buf)[0]
        if volt:
            val = (3.3 / 4095) * val * 8
            return round(val, 2)
        else:
            return val

    def set_i2c_address(self, addr):
        """
        set i2c address.
        addr :  1 to 127
        """
        if addr >= 1 and addr <= 127:
            if addr != self.i2c_addr:
                self.i2c.writeto_mem(self.i2c_addr, I2C_ADDR_REG, bytes([addr]))
                self.i2c_addr = addr
                time.sleep_ms(100)


# *******************************************************************#


class Relay4Module(Relay_Stack):
    def __init__(self, address: int = DEV_I2C_ADDR):
        super().__init__(i2c1, address)
        self._available()
