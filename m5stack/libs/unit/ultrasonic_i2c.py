from machine import I2C
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import time

try:
    from typing import Union
except ImportError:
    pass


class ULTRASONIC_I2CUnit:
    def __init__(self, i2c: Union[I2C, PAHUBUnit], addr=0x57):
        self.i2c = i2c
        self.i2c_addr = addr
        self._distance = 0
        self._available()

    def _available(self):
        if not (self.i2c_addr in self.i2c.scan()):
            raise UnitError("Ultrasonic unit maybe not connect")

    def get_target_distance(self, mode=1):
        try:
            self.i2c.writeto(self.i2c_addr, bytearray([0x01]))
            time.sleep_ms(150)
            data = self.i2c.readfrom(self.i2c_addr, 3)
            self._distance = ((data[0] << 16) | (data[1] << 8) | data[2]) / 1000
        except OSError:
            pass
        if mode == 2:
            self._distance = self._distance / 10
        return round(self._distance, 2)
