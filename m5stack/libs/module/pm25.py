# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
import M5
from driver.sht30 import SHT30
from driver.sht20 import SHT20
from collections import namedtuple
from .mbus import i2c1
import struct
import sys

if sys.platform != "esp32":
    from typing import Literal

MBusIO = namedtuple("MBusIO", ["bus_tx", "bus_rx", "en"])

iomap = {
    M5.BOARD.M5Stack: MBusIO(17, 16, 13),
    M5.BOARD.M5StackCore2: MBusIO(14, 13, 19),
    M5.BOARD.M5StackCoreS3: MBusIO(17, 16, 7),
}.get(M5.getBoard())


class PM25Module:
    def __init__(self, id: Literal[0, 1, 2]):
        """
        label:
            en: Init %1 with UART
        """
        self.uart = machine.UART(
            id, baudrate=9600, tx=machine.Pin(iomap.bus_tx), rx=machine.Pin(iomap.bus_rx)
        )
        self.i2c = i2c1
        self.sht30 = self.sht20 = None
        if 0x44 in self.i2c.scan():
            self.sht30 = SHT30(self.i2c)
            print("SHT30 sensor detected")
        elif 0x40 in self.i2c.scan():
            self.sht20 = SHT20(self.i2c)
            print("SHT20 sensor detected")
        self.data_len = 32
        self.data_buffer = bytearray(self.data_len)
        self.pm_data = [0] * 16
        self.mode = 1
        self.enable_pin = machine.Pin(iomap.en, machine.Pin.OUT)
        self.set_module_power(1)
        self.set_module_mode(1)

    def set_module_power(self, state):
        """
        label:
            en: Set %1 power state to %2
        params:
            state:
                name: state
                type: bool
                default: 'False'
                field: switch
        """
        self.enable_pin(state)

    def get_module_power(self):
        """
        label:
            en: Get %1 power state (return True / False)
        """
        return self.enable_pin() == 1

    def set_module_mode(self, mode):
        """
        label:
            en: Set %1 work mode to %2
        params:
            mode:
                name: mode
                field: dropdown
                options:
                    Active mode: '1'
                    Passive mode: '0'
        """
        if mode == 1:  # 主动模式
            data_to_send = bytearray([0x42, 0x4D, 0xE1, 0x00, 0x01, 0x01, 0x71])
        elif mode == 0:
            data_to_send = bytearray([0x42, 0x4D, 0xE1, 0x00, 0x00, 0x01, 0x70])
        self.uart.write(data_to_send)
        self.mode = mode

    def refresh_data(self) -> bool:
        """
        label:
            en: Refresh  %1 data
        """
        if self._read_data():
            self.pm_data = struct.unpack_from(">HHHHHHHHHHHH", self.data_buffer, 4)
            return True
        else:
            return False

    def request_air_data(self):
        """
        label:
            en: Request %1 air data
        """
        if self.mode == 0:
            self.uart.write(bytes([0x42, 0x4D, 0xE2, 0x00, 0x00, 0x01, 0x71]))

    def _read_data(self):
        """
        label:
            en: ' %1 _read_data'
        """
        resp_buf = bytearray()
        if self.uart.any() >= 32:
            buf = self.uart.read()
            resp_buf.extend(buf)
            if resp_buf[0:2] == bytearray([0x42, 0x4D]):
                if len(resp_buf) == 32:
                    if self._validate_data() is True:
                        self.data_buffer = resp_buf
                        return True

    def _validate_data(self):
        """
        label:
            en: ' %1 _validate_data'
        """
        checksum = sum(self.data_buffer[:30]) & 0xFFFF
        check_code = (self.data_buffer[30] << 8) | self.data_buffer[31]
        return checksum == check_code

    def get_pm_data(self, data_num: int) -> int:
        """
        label:
            en: Get %1 %2 data
        params:
            data_num:
                name: data_num
                field: dropdown
                options:
                    PM1.0 Concentration(Std): 0
                    PM2.5 Concentration(Std): 1
                    PM10 Concentration(Std): 2
                    PM1.0 Concentration(Env): 3
                    PM2.5 Concentration(Env): 4
                    PM10 Concentration(Env): 5
                    Particels more than 0.3um in 0.1 liters of air: 6
                    Particels more than 0.5um in 0.1 liters of air: 7
                    Particels more than 1.0um in 0.1 liters of air: 8
                    Particels more than 2.5um in 0.1 liters of air: 9
                    Particels more than 5.0um in 0.1 liters of air: 10
                    Particels more than 10um in 0.1 liters of air: 11
        """
        return self.pm_data[data_num]

    def get_temperature(self):
        """
        label:
            en: Get %1 env temperature
        """
        if self.sht30:
            return round(self.sht30.measure()[0], 2)
        elif self.sht20:
            return round(self.sht20.temperature, 2)

    def get_humidity(self):
        """
        label:
            en: Get %1 env humidity
        """
        if self.sht30:
            return round(self.sht30.measure()[1], 2)
        elif self.sht20:
            return round(self.sht20.humidity, 2)
