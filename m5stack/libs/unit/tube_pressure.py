# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import ADC

RAW12BIT = 12
RAW16BIT = 16


class TubePressureUnit:
    def __init__(self, port: tuple) -> None:
        self._adc = ADC(port[0])
        self._adc.atten(ADC.ATTN_11DB)

    def get_pressure(self):
        mv = self._adc.read_uv()
        mv /= 1000000
        pressure = (mv - 0.1) / 3.0 * 300.0 - 100.0
        return round(pressure, 2)

    def get_voltage(self):
        mv = self._adc.read_uv() / 1000000
        return round(mv, 3)

    def get_analog_value(self, bits: int = RAW16BIT):
        data = 0
        max = 0
        min = 65536 if bits == RAW16BIT else 4096
        for i in range(0, 10):
            newdata = self._adc.read_u16() if bits == RAW16BIT else self._adc.read()
            data += newdata
            if newdata > max:
                max = newdata
            if newdata < min:
                min = newdata
        data -= max + min
        data >>= 3
        return data
