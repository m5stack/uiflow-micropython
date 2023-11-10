from machine import I2C
import struct
from .pahub import PAHUBUnit
from .unit_helper import UnitError

try:
    from typing import Union
except ImportError:
    pass

HBRIDGE_ADDR = 0x20

DIRECTION_REG = 0x00
PWM8BIT_REG = 0x01
PWM16BIT_REG = 0x02
PWMFREQ_REG = 0x04
ADC8BIT_REG = 0x10
ADC16BIT_REG = 0x20
VIN_CURRENT_REG = 0x30
I2C_ADDR_REG = 0xFF
FW_VER_REG = 0xFE


class HBRIDGEUnit:
    def __init__(self, i2c: Union[I2C, PAHUBUnit], slave_addr=HBRIDGE_ADDR):
        """
        Hbridge Initialize Function
        Set I2C port, Hbridge Slave Address
        """
        self.hbridge_i2c = i2c
        self.init_i2c_address(slave_addr)

    def init_i2c_address(self, slave_addr=HBRIDGE_ADDR):
        """
        init the i2c address
        slave_addr : 0x20 to 0x2F
        """
        if slave_addr >= 0x20 and slave_addr <= 0x2F:
            self.i2c_addr = slave_addr
        if not (self.i2c_addr in self.hbridge_i2c.scan()):
            raise UnitError("Hbridge unit maybe not connect")

    def get_driver_config(self, reg=0):
        """
        get driver config value
        """
        leng = 1
        if reg > 1:
            leng = 2
            buf = self.read_reg(reg, leng)
            return struct.unpack("<H", buf)[0]
        else:
            return self.read_reg(reg, leng)[0]

    def set_direction(self, dir=0):
        """
        set direction
        dir : 0 stop, 1 forward, 2 reverse
        """
        self.write_mem_list(DIRECTION_REG, [dir])

    def set_8bit_pwm(self, duty=0):
        """
        set 8bit pwm dutycycle
        duty : 0 to 255
        """
        self.write_mem_list(PWM8BIT_REG, [duty])

    def set_16bit_pwm(self, duty=0):
        """
        set 16bit pwm dutycycle
        duty : 0 to 65535
        """
        self.write_mem_list(PWM16BIT_REG, [(duty & 0xFF), ((duty >> 8) & 0xFF)])

    def set_percentage_pwm(self, duty=0, res=8):
        """
        set 8bit or 16bit pwm dutycycle
        duty : 0 to 100%
        resolution: 8 or 16 bit
        """
        duty = max(min(duty, 100), 0)
        if res == 8:
            duty = self.map(duty, 0, 100, 0, 255)
        else:
            duty = self.map(duty, 0, 100, 0, 65535)
        self.write_mem_list(PWM8BIT_REG, [duty])

    def set_pwm_freq(self, freq=0):
        """
        set direction
        duty : 0 to 65535
        """
        freq = max(min(freq, 10000), 100)
        self.write_mem_list(PWMFREQ_REG, [(freq & 0xFF), ((freq >> 8) & 0xFF)])

    def get_adc_value(self, raw=0, res=8):
        """
        get adc value
        """
        leng = 1
        if res > 8:
            leng = 2
            buf = self.read_reg(ADC16BIT_REG, leng)
            val = struct.unpack("<H", buf)[0]
            res = 4095
        else:
            val = self.read_reg(ADC8BIT_REG, leng)[0]
            res = 255
        if raw:
            return val
        else:
            val = (3.3 / res) * val * 11
            return round(val, 2)

    #############################support v1.1################################
    def get_vin_current(self):
        """
        get vin current.
        """
        buf = self.read_reg(VIN_CURRENT_REG, 4)
        return struct.unpack("<f", buf)[0]

    #############################support v1.1################################

    def get_device_status(self, mode):
        """
        get firmware version and i2c address.
        mode : 0xFE and 0xFF
        """
        if mode >= FW_VER_REG and mode <= I2C_ADDR_REG:
            return self.read_reg(mode, 1)[0]

    def write_mem_list(self, reg, data):
        buf = bytearray(data)
        self.hbridge_i2c.writeto_mem(self.i2c_addr, reg, buf)

    def read_reg(self, reg, num):
        return self.hbridge_i2c.readfrom_mem(self.i2c_addr, reg, num)

    def map(self, x, in_min, in_max, out_min, out_max):
        return round((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def deinit(self):
        pass


"""
if __name__ == "__main__":
    import unit
    hbridge = unit.get(unit.HBRIDGE, unit.PORTA)
    hbridge.get_driver_config(0)
    hbridge.get_driver_config(1)
"""
