# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import ADC

RAW12BIT = 12
RAW16BIT = 16


class TubePressureUnit:
    """Create an TubePressureUnit object.

    :param tuple port: The port of the tube pressure.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import TubePressureUnit

            tube_pressure_0 = TubePressureUnit((32, 26))
    """

    def __init__(self, port: tuple) -> None:
        self._adc = ADC(port[0])
        self._adc.atten(ADC.ATTN_11DB)

    def get_pressure(self):
        """Getting the pressure value of the tube pressure.

        :returns: pressure value.
        :rtype: float

        UiFlow2 Code Block:

            |get_pressure.png|

        MicroPython Code Block:

            .. code-block:: python

                tube_pressure_0.get_pressure()
        """
        mv = self._adc.read_uv()
        mv /= 1000000
        pressure = (mv - 0.1) / 3.0 * 300.0 - 100.0
        return round(pressure, 2)

    def get_voltage(self):
        """Getting the voltage value of the tube pressure.

        :returns: voltage value.
        :rtype: float

        UiFlow2 Code Block:

            |get_voltage.png|

        MicroPython Code Block:

            .. code-block:: python

                tube_pressure_0.get_voltage()
        """
        mv = self._adc.read_uv() / 1000000
        return round(mv, 3)

    def get_analog_value(self, bits: int = RAW16BIT):
        """Getting the analog value of the tube pressure.

        :param int bits: The bits of the analog value.
        :returns: analog value.
        :rtype: int

        UiFlow2 Code Block:

            |get_analog_value.png|

        MicroPython Code Block:

            .. code-block:: python

                tube_pressure_0.get_analog_value()
        """
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
