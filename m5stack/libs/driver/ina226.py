# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
import struct
from micropython import const 


class INA226:
    # Averaging mode
    # Configuration Register: Bit[11:9]
    CFG_AVGMODE_MASK = const(0x0E00)
    CFG_AVGMODE_1SAMPLES = const(0x0000)
    CFG_AVGMODE_4SAMPLES = const(0x0200)
    CFG_AVGMODE_16SAMPLES = const(0x0400)
    CFG_AVGMODE_64SAMPLES = const(0x0600)
    CFG_AVGMODE_128SAMPLES = const(0x0800)
    CFG_AVGMODE_256SAMPLES = const(0x0A00)
    CFG_AVGMODE_512SAMPLES = const(0x0C00)
    CFG_AVGMODE_1024SAMPLES = const(0x0E00)

    # Bus voltage conversion time
    # Configuration Register: Bit[8:6]
    CFG_VBUSCT_MASK = const(0x01C0)
    CFG_VBUSCT_140us = const(0x0000)
    CFG_VBUSCT_204us = const(0x0040)
    CFG_VBUSCT_332us = const(0x0080)
    CFG_VBUSCT_588us = const(0x00C0)
    CFG_VBUSCT_1100us = const(0x0100)
    CFG_VBUSCT_21116us = const(0x0140)
    CFG_VBUSCT_4156us = const(0x0180)
    CFG_AVGMODE_8244us = const(0x01C0)

    # Shunt voltage conversion time
    # Configuration Register: Bit[5:3]
    CFG_VSHUNTCT_MASK = const(0x0038)
    CFG_VSHUNTCT_140us = const(0x0000)
    CFG_VSHUNTCT_204us = const(0x0008)
    CFG_VSHUNTCT_332us = const(0x0010)
    CFG_VSHUNTCT_588us = const(0x0018)
    CFG_VSHUNTCT_1100us = const(0x0020)
    CFG_VSHUNTCT_21116us = const(0x0028)
    CFG_VSHUNTCT_4156us = const(0x0030)
    CFG_VSHUNTCT_8244us = const(0x0038)

    # Operating mode
    # Configuration Register: Bit[2:0]
    CFG_MODE_MASK = const(0x0007)
    CFG_MODE_POWERDOWN = const(0x0000)
    CFG_MODE_SVOLT_TRIGGERED = const(0x0001)
    CFG_MODE_BVOLT_TRIGGERED = const(0x0002)
    CFG_MODE_SANDBVOLT_TRIGGERED = const(0x0003)
    CFG_MODE_ADCOFF = const(0x0004)
    CFG_MODE_SVOLT_CONTINUOUS = const(0x0005)
    CFG_MODE_BVOLT_CONTINUOUS = const(0x0006)
    CFG_MODE_SANDBVOLT_CONTINUOUS = const(0x0007)

    # Register Constants
    REG_CONFIG = const(0x00)  # Configuration
    REG_SHUNT_VOLTAGE = const(0x01)  # Shunt Voltage
    REG_BUS_VOLTAGE = const(0x02)  # Bus Voltage
    REG_POWER = const(0x03)  # Power
    REG_CURRENT = const(0x04)  # Current
    REG_CALIBRATION = const(0x05)  # Calibration

    def __init__(self, i2c: I2C, addr=0x40, shunt_resistor=0.02):
        """
        init
        :param i2c: I2C object
        :param addr: INA226 slave address
        :param shunt_resistor: shunt resistor (unit: Ω)
        """
        self.i2c = i2c
        self.addr = addr
        self.shunt_resistor = shunt_resistor
        self.current_lsb = None
        self.power_lsb = None

    def _write_register(self, reg, value):
        data = value.to_bytes(2, "big")
        self.i2c.writeto_mem(self.addr, reg, data)

    def _read_register(self, reg):
        data = self.i2c.readfrom_mem(self.addr, reg, 2)
        return data

    def configure(self, avg, vbus_conv_time, vshunt_conv_time, mode):
        config = avg | vbus_conv_time | vshunt_conv_time | mode
        self._write_register(self.REG_CONFIG, config)

    def calibrate(self, max_expected_current):
        """
        calibrate INA226
        :param max_expected_current: unit: A
        """
        self.current_lsb = max_expected_current / 32768
        calibration = int(0.00512 / (self.current_lsb * self.shunt_resistor))
        self.power_lsb = (
            self.current_lsb * 25
        )  # The power LSB has a fixed ratio to the Current_LSB of 25
        self._write_register(self.REG_CALIBRATION, calibration)

    def read_shunt_voltage(self):
        """
        unit: V
        """
        raw = self._read_register(self.REG_SHUNT_VOLTAGE)
        raw_value = struct.unpack(">h", raw)[0]
        return raw_value * 2.5e-6  # Full-scale range = 81.92 mV (decimal = 7FFF); LSB: 2.5 μV

    def read_bus_voltage(self):
        """
        unit: V
        """
        raw = self._read_register(self.REG_BUS_VOLTAGE)
        raw_value = struct.unpack(">H", raw)[0]
        return raw_value * 1.25e-3  # Full-scale range = 40.96 V (decimal = 7FFF); LSB = 1.25 mV.

    def read_current(self):
        """
        unit: A
        """
        if self.current_lsb is None:
            raise ValueError("Please call the calibrate() method for calibration first.")

        raw = self._read_register(self.REG_CURRENT)
        raw_value = struct.unpack(">h", raw)[0]
        return raw_value * self.current_lsb  # convert to unit: A

    def read_power(self):
        """
        unit: W
        """
        if self.current_lsb is None:
            raise ValueError("Please call the calibrate() method for calibration first.")

        raw = self._read_register(self.REG_POWER)
        raw_value = struct.unpack(">h", raw)[0]
        return raw_value * self.power_lsb  # convert to unit: W
