# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from machine import I2C
from micropython import const
import struct
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import time


hub_addr = [0x40, 0x50, 0x60, 0x70, 0x80, 0xA0]

PBHUB_ADDR = 0x61
FW_VER_REG = 0xFE
I2C_ADDR_REG = 0xFF


class PBHUBUnit:
    def __init__(
        self, i2c: I2C | PAHUBUnit, addr=PBHUB_ADDR, address: int | list | tuple = PBHUB_ADDR
    ):
        # TODO: 2.0.6 移除 addr 参数
        address = addr
        self.i2c_addr = address
        self.pbhub_i2c = i2c
        self.init_i2c_address(address)

    def _available(self):
        if self.i2c_addr not in self.pbhub_i2c.scan():
            raise UnitError("Pb.hub unit maybe not connect")

    def digital_read(self, num, pos):
        # 2.0.3添加
        return self.digitalRead(num, pos)

    def digitalRead(self, num, pos):  # noqa: N802
        # TODO: 2.0.6移除
        """
        digital read.
        num :  0 to 5
        pos : 0 or 1
        return : 0 or 1
        """
        num = max(min(num, 5), 0)
        offset = 0x04 if pos else 0x05
        data = self.read_reg((hub_addr[num] | offset), 1)[0] > 0
        return data

    def digital_write(self, num, pos, value):
        # 2.0.3添加
        self.digitalWrite(num, pos, value)

    def digitalWrite(self, num, pos, value):  # noqa: N802
        # TODO: 2.0.6移除
        """
        digital write.
        num :  0 to 5
        pos : 0 or 1
        value : 0 or 1
        """
        num = max(min(num, 5), 0)
        value = 1 if value > 0 else 0
        offset = 0x00 if pos else 0x01
        self.write_mem_list(hub_addr[num] | offset, [value])

    def pwm_read(self, num, pos):
        # 2.0.3添加
        return self.pwmRead(num, pos)

    def pwmRead(self, num, pos):  # noqa: N802
        # TODO: 2.0.6移除
        """
        pwm read.
        num :  0 to 5
        pos : 0 or 1
        return : 0 to 100
        """
        num = max(min(num, 5), 0)
        offset = 0x02 if pos else 0x03
        data = self.read_reg((hub_addr[num] | offset), 1)[0]
        data = self.map(data, 0, 255, 0, 100)
        return data

    def pwm_write(self, num, pos, value):
        # 2.0.3添加
        self.pwmWrite(num, pos, value)

    def pwmWrite(self, num, pos, value):  # noqa: N802
        # TODO: 2.0.6移除
        """
        pwm write.
        num :  0 to 5
        pos : 0 or 1
        value : 0 to 100
        """
        num = max(min(num, 5), 0)
        value = max(min(value, 100), 0)
        value = self.map(value, 0, 100, 0, 255)
        offset = 0x02 if pos else 0x03
        self.write_mem_list(hub_addr[num] | offset, [value])

    def analog_read(self, num):
        # 2.0.3添加
        return self.analogRead(num)

    def analogRead(self, num):  # noqa: N802
        # TODO: 2.0.6移除
        """
        analog read.
        num :  0 to 5
        return : 0 to 4095
        """
        num = max(min(num, 5), 0)
        offset = 0x06
        data = self.read_reg((hub_addr[num] | offset), 2)
        data = struct.unpack("<h", data)[0]
        return data

    def set_rgb_led_num(self, num, length):
        # 2.0.3添加
        self.setRgbNum(num, length)

    # default: 16
    def setRgbNum(self, num, length):  # noqa: N802
        # TODO: 2.0.6移除
        """
        set RGB Max length.
        num :  0 to 5
        length : 0 to 74
        """
        num = max(min(num, 5), 0)
        self.write_mem_list(hub_addr[num] | 0x08, [(length & 0xFF), ((length >> 8) & 0xFF)])

    def set_rgb_color_pos(self, num, led, color_in):
        # 2.0.3添加
        self.setColorPos(num, led, color_in)

    def setColorPos(self, num, led, color_in):  # noqa: N802
        # TODO: 2.0.6移除
        """
        set RGB led Color.
        num :  0 to 5
        led : 0 to max led
        color_in : 0 to 0xfffff
        """
        num = max(min(num, 5), 0)
        out_buf = led.to_bytes(2, "little") + color_in.to_bytes(3, "big")
        self.pbhub_i2c.writeto_mem(self.i2c_addr, hub_addr[num] | 0x09, out_buf)

    def set_rgb_color(self, num, begin, count, color_in):
        # 2.0.3添加
        self.setColor(num, begin, count, color_in)

    def setColor(self, num, begin, count, color_in):  # noqa: N802
        # TODO: 2.0.6移除
        """
        set RGB led Color.
        num :  0 to 5
        begin :  0 to 74
        pos : begin + (0 to 74)
        color_in : 0 to 0xfffff
        """
        num = max(min(num, 5), 0)
        out_buf = (
            begin.to_bytes(2, "little") + count.to_bytes(2, "little") + color_in.to_bytes(3, "big")
        )
        self.pbhub_i2c.writeto_mem(self.i2c_addr, hub_addr[num] | 0x0A, out_buf)

    def set_rgb_brightness(self, num, value):
        # 2.0.3添加
        self.setBrightness(num, value)

    def setBrightness(self, num, value):  # noqa: N802
        # TODO: 2.0.6移除
        """
        set RGB led brightness.
        num :  0 to 5
        value :  0 to 100
        """
        num = max(min(num, 5), 0)
        self.write_mem_list(hub_addr[num] | 0x0B, [value])

    def set_servo_angle(self, num, pos, value):
        # 2.0.3添加
        self.setServoAngle(num, pos, value)

    def setServoAngle(self, num, pos, value):  # noqa: N802
        # TODO: 2.0.6移除
        """
        set servo angle.
        num :  0 to 5
        pos : 0 or 1
        value : 0 to 180
        """
        num = max(min(num, 5), 0)
        value = max(min(value, 180), 0)
        offset = 0x0C if pos else 0x0D
        self.write_mem_list(hub_addr[num] | offset, [value])

    def set_servo_pulse(self, num, pos, value):
        # 2.0.3添加
        self.setServoPulse(num, pos, value)

    def setServoPulse(self, num, pos, value):  # noqa: N802
        # TODO: 2.0.6移除
        """
        set servo pulse.
        num :  0 to 5
        pos : 0 or 1
        value : 500 to 2500
        """
        num = max(min(num, 5), 0)
        value = max(min(value, 2500), 500)
        offset = 0x0E if pos else 0x0F
        self.write_mem_list(hub_addr[num] | offset, [(value & 0xFF), ((value >> 8) & 0xFF)])

    def read_status(self, mode):
        """
        read firmware version and i2c address.
        mode : 0xFE and 0xFF
        """
        if mode >= FW_VER_REG and mode <= I2C_ADDR_REG:
            return self.read_reg(mode, 1)[0]

    def init_i2c_address(self, slave_addr=PBHUB_ADDR):
        """
        change the i2c address
        slave_addr : 1 to 127
        """
        if slave_addr >= 1 and slave_addr <= 127:
            self.i2c_addr = slave_addr
        self._available()

    def set_i2c_address(self, addr):
        """
        set i2c address.
        addr :  1 to 127
        """
        if addr >= 1 and addr <= 127:
            if addr != self.i2c_addr:
                self.write_mem_list(I2C_ADDR_REG, [addr])
                self.i2c_addr = addr

    def write_mem_list(self, reg, data):
        buf = bytearray(data)
        self.pbhub_i2c.writeto_mem(self.i2c_addr, reg, buf)

    def read_reg(self, reg, num):
        buf = bytearray(1)
        buf[0] = reg
        time.sleep_ms(1)
        self.pbhub_i2c.writeto(self.i2c_addr, buf)
        buf = bytearray(num)
        self.pbhub_i2c.readfrom_into(self.i2c_addr, buf)
        return buf

    def map(self, x, in_min, in_max, out_min, out_max):
        return round((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def deinit(self):
        pass
