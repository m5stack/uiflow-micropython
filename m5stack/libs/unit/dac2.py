# -*- encoding: utf-8 -*-
"""
@File    :   _dac2.py
@Time    :   2023/12/27
@Author  :   TONG YIHAN
@E-mail  :   icyqwq@gmail.com
@License :   (C)Copyright 2015-2023, M5STACK
"""

# Import necessary libraries
from machine import I2C
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import struct
import sys

if sys.platform != "esp32":
    from typing import Union


class DAC2Unit:
    """! DAC2 is a Digital to Analog Converter, GP8413 15bit DAC.

    @en DAC2 is a Digital to Analog Converter, includes GP8413 15bit DAC. The GP8413, through the I2C interface, linearly converts to two channels of analog voltage output, 0-5V and 0-10V.
    @cn DAC2 是一个数字模拟转换器，包含GP8413 15位DAC。GP8413通过I2C接口线性转换为两个通道的模拟电压输出，0-5V和0-10V。

    @attr RANGE_5V output from 0 to 5V
    @attr RANGE_10V output from 0 to 10V
    @color #0FE6D7
    @link https://docs.m5stack.com/en/unit/dac
    @image https://static-cdn.m5stack.com/resource/docs/products/unit/dac/dac_01.webp
    """

    RANGE_5V = 0
    RANGE_10V = 1
    CHANNEL_0 = (0,)
    CHANNEL_1 = (1,)
    CHANNEL_BOTH = (2,)

    def __init__(self, i2c: Union[I2C, PAHUBUnit], addr=0x59):
        """! Initialize the DAC.

        @param port I2C port to use.
        @param addr I2C address of the sensor.
        """
        self.i2c = i2c
        self.addr = addr
        self._available()
        self._range = self.RANGE_5V
        self.setDACOutputVoltageRange(self._range)

    def _available(self):
        """! Check if sensor is available on the I2C bus.

        Raises:
            Exception: If the sensor is not found.
        """
        if not (self.addr in self.i2c.scan()):
            raise UnitError("DAC2 Unit not found.")

    def setDACOutputVoltageRange(self, _range: int = 0):
        """!

        @en Set the DAC %1 output voltage range to %2.
        @cn 设置DAC %1 输出电压范围为 %2。

        @param range The DAC range to set.
        """
        data = 0x00
        self._range = _range
        if _range == self.RANGE_5V:
            self.i2c.writeto_mem(self.addr, 0x01, struct.pack("b", data))
        else:  # _range == self.RANGE_10V:
            data = 0x11
            self.i2c.writeto_mem(self.addr, 0x01, struct.pack("b", data))

    def setVoltage(self, voltage: float, channel: int = 2):
        """!
        @en Set %1 channel %3 to %2 V.
        @cn 设置DAC %1 通道 %3 的输出电压为 %1 V。

        @param voltage The DAC voltage to set, from 0.0 to range.
        @param channel [field_dropdown] The DAC channel to set.
               @options {
                        [Channel 0, CHANNEL_0]
                    [Channel 1, CHANNEL_1]
                    [Both Channel, CHANNEL_BOTH]
                           }
        """
        if self._range == self.RANGE_5V:
            max_voltage = 5.0
        else:  # self._range == self.RANGE_10V:
            max_voltage = 10.0
        if voltage > max_voltage:
            voltage = max_voltage
        elif voltage < 0.0:
            voltage = 0.0
        data = int((voltage / max_voltage) * 0xFFFF)
        if channel == self.CHANNEL_BOTH:
            self.i2c.writeto_mem(self.addr, 0x02, struct.pack("<HH", data, data))
        elif channel == self.CHANNEL_0:
            self.i2c.writeto_mem(self.addr, 0x02, struct.pack("<H", data))
        elif channel == self.CHANNEL_1:
            self.i2c.writeto_mem(self.addr, 0x04, struct.pack("<H", data))

    def setVoltageBoth(self, voltage0: float, voltage1: float):
        """!
        @en Set the DAC %1 channel 0 %2 V, channel 1 %3 V.
        @cn 设置 %1 通道0的电压为 %2 V，通道1的电压为 %3 V。

        @param voltage0 The DAC voltage of channel 0 to set.
        @param voltage1 The DAC voltage of channel 1 to set.
        """

        if self._range == self.RANGE_5V:
            max_voltage = 5.0
        else:  # self._range == self.RANGE_10V:
            max_voltage = 10.0
        if voltage0 > max_voltage:
            voltage0 = max_voltage
        elif voltage0 < 0.0:
            voltage0 = 0.0
        if voltage1 > max_voltage:
            voltage1 = max_voltage
        elif voltage1 < 0.0:
            voltage1 = 0.0
        data0 = int((voltage0 / max_voltage) * 0xFFFF)
        data1 = int((voltage1 / max_voltage) * 0xFFFF)
        self.i2c.writeto_mem(self.addr, 0x02, struct.pack("<HH", data0, data1))
