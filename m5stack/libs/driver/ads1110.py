# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
from micropython import const
import struct
import time

ADDRESS = const(0x48)

MODE_CONTIN = const(0x00)
MODE_SINGLE = const(0x10)

SPS_240 = const(0x00)
SPS_60 = const(0x04)
SPS_30 = const(0x08)
SPS_15 = const(0x0C)
SPS_MASK = const(0x0C)

GAIN_ONE = const(0x00)
GAIN_TWO = const(0x01)
GAIN_FOUR = const(0x02)
GAIN_EIGHT = const(0x03)
GAIN_MASK = const(0x03)

NO_EFFECT = const(0x00)
START = const(0x80)


class ADS1110:
    """
    note:
        en: EXT.IO2 is an IO extended unit, based on STM32F030 main controller, using I2C communication interface and providing 8 IO expansion. Each IO supports independent configuration of digital I/O, ADC, SERVO control, RGB LED control modes. Supports configuration of device I2C address, which means that users can mount multiple EXT.IO2 UNITs on the same I2C BUS to extend more IO resources. Suitable for multiple digital/analog signal acquisition, with lighting/servo control applications.

    details:
        link: https://docs.m5stack.com/en/unit/extio2
        image: https://static-cdn.m5stack.com/resource/docs/products/unit/extio2/extio2_01.webp
        category: Unit

    example:
        - ../../../examples/unit/extio2/extio2_core2_example.py

    m5f2:
        - unit/extio2/extio2_core2_example.m5f2
    """

    def __init__(self, i2c: I2C, address: int = ADDRESS) -> None:
        """
        note:
            en: Initialize the ADS1110 with the given I2C interface and address.

        params:
            i2c:
                note: The I2C interface used for communication.
            address:
                note: The I2C address of the ADS1110. Default is ADDRESS.
        """
        self._i2c = i2c
        self._i2c_addr = address
        self.start = NO_EFFECT
        self.mode = MODE_CONTIN
        self.rate = SPS_15
        self.gain = GAIN_ONE
        self.mini_code = {SPS_15: 16, SPS_30: 15, SPS_60: 14, SPS_240: 12}
        self.gain_code = {GAIN_ONE: 1, GAIN_TWO: 2, GAIN_FOUR: 4, GAIN_EIGHT: 8}

    def set_gain(self, gain):
        """
        note:
            en: Set the gain configuration for the ADC.

        params:
            gain:
                note: The gain value to configure.
        """
        self.gain = gain
        self.set_config()

    def set_sample_rate(self, rate):
        """
        note:
            en: Configure the ADC's sampling rate.

        params:
            rate:
                note: The sample rate to set.
        """
        self.rate = rate
        self.set_config()

    def set_mode(self, mode):
        """
        note:
            en: Set the ADC's operating mode.

        params:
            mode:
                note: The mode to configure, e.g., continuous or single conversion.
        """
        self.mode = mode
        self.set_config()

    def start_single_conversion(self):
        """
        note:
            en: Trigger a single conversion on the ADC.
        """
        self.start = START
        self.set_config()
        self.start = NO_EFFECT

    def set_config(self):
        """
        note:
            en: Update the ADC configuration register with the current settings.

        params:
            note:

        """
        value = 0x00
        value |= self.gain | self.rate | self.mode | self.start
        self._i2c.writeto(self._i2c_addr, bytearray([value]))

    def get_adc_raw_value(self):
        """
        note:
            en: Read the raw ADC value.

        params:
            note:

        returns:
            note: The raw ADC value as an integer.
        """
        buf = bytearray(2)
        self._i2c.readfrom_into(self._i2c_addr, buf)
        return struct.unpack(">h", buf)[0]
