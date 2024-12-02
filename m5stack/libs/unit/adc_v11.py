# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
from driver.ads1110 import ADS1110
from micropython import const
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import time


class ADCV11Unit(ADS1110):
    """
    note:
        en: ADC V1.1 Unit is an A/D conversion module that utilizes the ADS1110 chip, a 16-bit self-calibrating analog-to-digital converter. It is designed with an I2C interface, offering convenient connectivity. The module offers conversion speeds of 8, 16, 32, and 128 samples per second (SPS), providing varying levels of accuracy at 16, 15, 14, and 12 bits of resolution respectively.

    details:
        link: https://docs.m5stack.com/en/unit/Unit-ADC_V1.1
        image: https://static-cdn.m5stack.com/resource/docs/products/unit/Unit-ADC_V1.1/img-240867ba-46d2-4cc6-beb9-79ac68af51d5.webp
        category: Unit

    example:
        - ../../../examples/unit/adcv11/adcv11_core2_example.py

    m5f2:
        - unit/adcv11/adcv11_core2_example.m5f2
    """

    def __init__(self, i2c: I2C | PAHUBUnit) -> None:
        """
        note:
            en: Initialize the ADCV11Unit with an I2C or PAHUBUnit interface.

        params:
            i2c:
                note: The I2C or PAHUBUnit instance used for communication.
        """
        super().__init__(i2c=i2c)
        self._available()
        self.divider_offset = 100 / 610

    def _available(self):
        """
        note:
            en: Check the availability of the ADC V1.1 Unit on the I2C bus.

        raises:
            UnitError:
                note: Raised if the ADC V1.1 Unit is not detected.
        """
        check = False
        for i in range(3):
            if self._i2c_addr in self._i2c.scan():
                check = True
                break
            time.sleep(0.2)
        if not check:
            raise UnitError("ADC V1.1 Unit not found in Grove")

    def get_voltage(self):
        """
        note:
            en: Get the measured voltage from the ADC V1.1 Unit.

        returns:
            float:
                note: The measured voltage value, rounded to two decimal places.
        """
        data = self.get_adc_raw_value()
        vol = (
            data
            * 2.048
            / 2 ** (self.mini_code[self.rate] - 1)
            / self.gain_code[self.gain]
            / self.divider_offset
        )
        return round(vol, 2)
