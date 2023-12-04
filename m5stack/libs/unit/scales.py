from machine import I2C
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import time
import struct

try:
    from typing import Union
except ImportError:
    pass


SCALES_ADDR = 0x26

############# BUTTON STATUS ##############
BUTTON_SHORT = 0x20
BUTTON_LONG = 0x21
BUTTON_STATUS = 0x22
BUTTON_OFFSET = 0x23

############## LED CONTROL ###############
LED_SYNC = 0x25
LED_RED = 0x50
LED_GREEN = 0x51
LED_BLUE = 0x52

######## SCALES STATUS & CONTROL #########
RAW_ADC = 0x10
GET_WEIGHT = 0x14
OFFSET_ADC = 0x18
SOFT_OFFSET = 0x24

############## CALIBRATION ###############
CALI_ZERO = 0x30
CALI_LOAD = 0x32

############# DEVICE STATUS ##############
FW_VER_REG = 0xFE
I2C_ADDR_REG = 0xFF


class SCALESUnit:
    def __init__(self, i2c: Union[I2C, PAHUBUnit], addr=SCALES_ADDR) -> None:
        self.i2c = i2c
        self.i2c_addr = addr
        self._available()

    def _available(self) -> None:
        if not (self.i2c_addr in self.i2c.scan()):
            raise UnitError("Scales unit maybe not connect")

    def get_button_status(self, status) -> int:
        status += BUTTON_SHORT
        if status >= BUTTON_SHORT and status <= BUTTON_OFFSET:
            return self.i2c.readfrom_mem(self.i2c_addr, status, 1)[0]

    def set_button_offset(self, enable) -> None:
        self.i2c.writeto_mem(self.i2c_addr, BUTTON_OFFSET, bytes([enable]))

    def set_rgbled_sync(self, control) -> None:
        self.i2c.writeto_mem(self.i2c_addr, LED_SYNC, bytes([control]))

    def get_rgbled_sync(self) -> int:
        return self.i2c.readfrom_mem(self.i2c_addr, LED_SYNC, 1)[0]

    def set_rgb_led(self, rgb) -> None:
        self.i2c.writeto_mem(self.i2c_addr, LED_RED, rgb.to_bytes(3, "big"))

    def get_rgb_led(self) -> list:
        return list(self.i2c.readfrom_mem(self.i2c_addr, LED_RED, 3))

    def get_scale_value(self, scale) -> int:
        scale = RAW_ADC + (scale * 4)
        if scale >= RAW_ADC and scale <= OFFSET_ADC:
            byte_val = self.i2c.readfrom_mem(self.i2c_addr, scale, 4)
            if scale == GET_WEIGHT:
                return int((struct.unpack(">i", byte_val)[0]) / 100)
            return struct.unpack(">i", byte_val)[0]

    def set_raw_offset(self, value) -> None:
        self.i2c.writeto_mem(self.i2c_addr, OFFSET_ADC, value.to_bytes(4, "big"))

    def set_current_raw_offset(self) -> None:
        self.i2c.writeto_mem(self.i2c_addr, SOFT_OFFSET, bytes([1]))

    def set_calibration_zero(self) -> None:
        self.i2c.writeto_mem(self.i2c_addr, CALI_ZERO, bytes([0, 0]))
        time.sleep_ms(200)

    def set_calibration_load(self, gram) -> None:
        self.i2c.writeto_mem(self.i2c_addr, CALI_LOAD, gram.to_bytes(2, "little"))
        time.sleep_ms(200)

    def get_device_inform(self, mode) -> int:
        if mode >= FW_VER_REG and mode <= I2C_ADDR_REG:
            return self.i2c.readfrom_mem(self.i2c_addr, mode, 1)[0]

    def set_i2c_address(self, addr):
        if addr >= 1 and addr <= 127:
            if addr != self.i2c_addr:
                self.i2c.writeto_mem(self.i2c_addr, I2C_ADDR_REG, bytes([addr]))
                self.i2c_addr = addr
                time.sleep_ms(200)
