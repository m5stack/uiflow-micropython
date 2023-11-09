# -*- encoding: utf-8 -*-

from machine import I2C
import struct
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import time

try:
    from typing import Union
except ImportError:
    pass


ENCODER8_ADDR = 0x41

CNT_START_REG = 0x00
CNT_END_REG = 0x1F
INC_START_REG = 0x20
INC_END_REG = 0x3F
CNT_RST_START_REG = 0x40
CNT_RST_END_REG = 0x47
BUTTON_START_REG = 0x50
BUTTON_END_REG = 0x57
SWITCH_REG = 0x60
RGB_START_REG = 0x70
RGB_END_REG = 0x8A
FW_VER_REG = 0xFE
I2C_ADDR_REG = 0xFF

TOTAL_LED = 9


class ENCODER8Unit:
    def __init__(self, i2c: Union[I2C, PAHUBUnit], slave_addr: int = ENCODER8_ADDR) -> None:
        """
        Encoder 8 Channel Initialize Function
        Set I2C port
        """
        self.encoder8_i2c = i2c
        self.init_i2c_address(slave_addr)

    def init_i2c_address(self, slave_addr: int = ENCODER8_ADDR) -> None:
        """
        change the i2c address
        slave_addr : 1 to 127
        """
        if slave_addr >= 1 and slave_addr <= 127:
            self.i2c_addr = slave_addr
        self.available()

    def available(self) -> None:
        if self.i2c_addr in self.encoder8_i2c.scan():
            pass
        else:
            raise UnitError("Encoder 8 unit maybe not connect")

    def get_counter_value(self, Channel: int = 1) -> int:
        """
        get counter value
        Channels: 1 - 8
        """
        Channel = min(8, max(Channel, 1)) - 1
        Channel *= 4
        if not (Channel >= CNT_START_REG and Channel <= CNT_END_REG):
            Channel = CNT_START_REG
        buf = self.read_reg_data(Channel, 4)
        return struct.unpack("<i", buf)[0]

    def set_counter_value(self, Channel: int = 1, value: int = 0) -> None:
        """
        set counter value
        Channels: 1 - 8
        value: int
        """
        Channel = min(8, max(Channel, 1)) - 1
        Channel *= 4
        if not (Channel >= CNT_START_REG and Channel <= CNT_END_REG):
            Channel = CNT_START_REG
        self.write_reg_data(Channel, struct.pack("<i", value))

    def get_increment_value(self, Channel: int = 1) -> int:
        """
        get increment value
        Channels: 1 - 8
        """
        Channel = min(8, max(Channel, 1)) - 1
        Channel = INC_START_REG + (Channel * 4)
        if not (Channel >= INC_START_REG and Channel <= INC_END_REG):
            Channel = INC_START_REG
        buf = self.read_reg_data(Channel, 4)
        return struct.unpack("<i", buf)[0]

    def reset_counter_value(self, Channel: int = 1) -> None:
        """
        reset counter value
        Channels: 1 - 8
        """
        Channel = min(8, max(Channel, 1)) - 1
        Channel += CNT_RST_START_REG
        if not (Channel >= CNT_RST_START_REG and Channel <= CNT_RST_END_REG):
            Channel = CNT_RST_START_REG
        self.write_reg_data(Channel, [0x01])

    def get_button_status(self, Channel: int = 1) -> bool:
        """
        get_button_status
        Channels: 1 - 8
        """
        Channel = min(8, max(Channel, 1)) - 1
        Channel += BUTTON_START_REG
        if not (Channel >= BUTTON_START_REG and Channel <= BUTTON_END_REG):
            Channel = BUTTON_START_REG
        return bool(self.read_reg_data(Channel, 1)[0])

    def get_switch_status(self) -> bool:
        """
        Return a switch Status
        """
        return bool(self.read_reg_data(SWITCH_REG, 1)[0])

    def set_led_rgb(self, Channel: int = 1, rgb: int = 0) -> None:
        """
        Set Neo Pixel RGB LED Color
        Channel: 1 - 8
        rgb: 0 - 0xffffff
        """
        Channel = min(8, max(Channel, 1)) - 1
        Channel = RGB_START_REG + (Channel * 3)
        if not (Channel >= RGB_START_REG and Channel <= RGB_END_REG):
            Channel = RGB_START_REG
        self.write_reg_data(Channel, rgb.to_bytes(3, "big"))

    def set_led_rgb_from(self, begin: int = 0, end: int = 0, rgb: int = 0) -> None:
        """
        Set Neo Pixel RGB LED Color
        Channel: 1 - 8
        rgb: 0 - 0xffffff
        """
        begin = min(TOTAL_LED, max(begin, 0))
        end = min(TOTAL_LED, max(end, 0))
        for i in range(begin, end + 1):
            self.set_led_rgb(i, rgb)

    def get_device_status(self, mode: int = 0xFE) -> int:
        """
        read firmware version and i2c address.
        mode : 0xFE and 0xFF
        """
        if mode >= FW_VER_REG and mode <= I2C_ADDR_REG:
            return self.read_reg_data(mode, 1)[0]

    def set_i2c_address(self, addr: int = 0x41) -> None:
        """
        set i2c address.
        addr :  1 to 127
        """
        if addr >= 1 and addr <= 127:
            if addr != self.i2c_addr:
                self.write_reg_data(I2C_ADDR_REG, [addr])
                self.i2c_addr = addr
                time.sleep_ms(50)

    def read_reg_data(self, reg: int = 0, num: int = 0) -> bytearray:
        buf = bytearray(1)
        buf[0] = reg
        time.sleep_ms(1)
        self.encoder8_i2c.writeto(self.i2c_addr, buf)
        buf = bytearray(num)
        self.encoder8_i2c.readfrom_into(self.i2c_addr, buf)
        return buf

    def write_reg_data(self, reg, byte_lst):
        buf = bytearray(1 + len(byte_lst))
        buf[0] = reg
        buf[1:] = bytes(byte_lst)
        time.sleep_ms(1)
        self.encoder8_i2c.writeto(self.i2c_addr, buf)

    def deinit(self):
        pass
