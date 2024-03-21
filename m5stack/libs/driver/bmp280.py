# Copyright (c) 2020 Sebastian Wicki
# Copyright (c) 2024 M5Stack Technology CO LTD
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
I2C-based driver for the BMP280 temperature and pressure sensor.
"""

from micropython import const
from ustruct import unpack_from
from utime import sleep_ms, sleep_us

_BMP280_I2C_DEFAULT_ADDR = const(0x76)

_BMP280_CHIP_ID = const(0xD0)
_BMP280_CHIP_ID_VALUE = const(0x58)

_BMP280_RESET = const(0xE0)
_BMP280_RESET_VALUE = const(0xB6)

_BMP280_STATUS = const(0xF3)
_BMP280_CONTROL = const(0xF4)
_BMP280_CONTROL_TEMP_SAMPLES_MASK = const(0b1110_0000)
_BMP280_CONTROL_TEMP_SAMPLES_POS = const(5)
_BMP280_CONTROL_PRESS_SAMPLES_MASK = const(0b0001_1100)
_BMP280_CONTROL_PRESS_SAMPLES_POS = const(2)
_BMP280_CONTROL_MODE_MASK = const(0b0000_0011)
_BMP280_CONTROL_MODE_POS = const(0)

_BMP280_CONFIG = const(0xF5)
_BMP280_CONFIG_STANDBY_MASK = const(0b1110_0000)
_BMP280_CONFIG_STANDBY_POS = const(5)
_BMP280_CONFIG_IIR_MASK = const(0b0001_1100)
_BMP280_CONFIG_IIR_POS = const(2)

_BMP280_DATA = const(0xF7)
_BMP280_CALIBRATION = const(0x88)

_BMP280_DATA_LEN = const(6)
_BMP280_CALIBRATION_LEN = const(24)

_BMP280_DURATION_PER_SAMPLE_US = const(2000)
_BMP280_DURATION_STARTUP_US = const(1000)
_BMP280_DURATION_PRESS_STARTUP_US = const(500)

MODE_NORMAL = const(0b11)
MODE_FORCED = const(0b01)
MODE_SLEEP = const(0b00)

TEMP_SAMPLES_SKIP = const(0b000)
TEMP_SAMPLES_1 = const(0b001)
TEMP_SAMPLES_2 = const(0b010)
TEMP_SAMPLES_4 = const(0b011)
TEMP_SAMPLES_8 = const(0b100)
TEMP_SAMPLES_16 = const(0b111)

PRESS_SAMPLES_SKIP = const(0b000)
PRESS_SAMPLES_1 = const(0b001)
PRESS_SAMPLES_2 = const(0b010)
PRESS_SAMPLES_4 = const(0b011)
PRESS_SAMPLES_8 = const(0b100)
PRESS_SAMPLES_16 = const(0b111)

IIR_FILTER_OFF = const(0b0000_0000)
IIR_FILTER_2 = const(0b0000_0100)
IIR_FILTER_4 = const(0b0000_1000)
IIR_FILTER_8 = const(0b0000_1100)
IIR_FILTER_16 = const(0b0001_0000)

STANDBY_0_5_MS = const(0b0000_0000)
STANDBY_62_5_MS = const(0b0010_0000)
STANDBY_125_MS = const(0b0100_0000)
STANDBY_250_MS = const(0b0110_0000)
STANDBY_500_MS = const(0b1000_0000)
STANDBY_1000_MS = const(0b1010_0000)
STANDBY_2000_MS = const(0b1100_0000)
STANDBY_4000_MS = const(0b1110_0000)


class BMP280:
    def __init__(
        self,
        i2c,
        addr=_BMP280_I2C_DEFAULT_ADDR,
        *,
        mode=MODE_NORMAL,
        press_samples=PRESS_SAMPLES_4,
        temp_samples=TEMP_SAMPLES_1,
        iir_filter=IIR_FILTER_16,
        standby_ms=STANDBY_0_5_MS,
    ):
        self.i2c = i2c
        self.addr = addr

        chipid = self.i2c.readfrom_mem(self.addr, _BMP280_CHIP_ID, 1)
        if chipid[0] != _BMP280_CHIP_ID_VALUE:
            raise ValueError("device not found")

        self.reset()
        sleep_ms(10)

        control = bytearray(1)
        control[0] |= (
            temp_samples << _BMP280_CONTROL_TEMP_SAMPLES_POS
        ) & _BMP280_CONTROL_TEMP_SAMPLES_MASK
        control[0] |= (
            press_samples << _BMP280_CONTROL_PRESS_SAMPLES_POS
        ) & _BMP280_CONTROL_PRESS_SAMPLES_MASK
        # MODE_FORCED will be set in the call to measure()
        if mode == MODE_NORMAL:
            control[0] |= (MODE_NORMAL << _BMP280_CONTROL_MODE_POS) & _BMP280_CONTROL_MODE_MASK
        self.i2c.writeto_mem(self.addr, _BMP280_CONTROL, control)

        config = bytearray(1)
        config[0] |= (standby_ms << _BMP280_CONFIG_STANDBY_POS) & _BMP280_CONFIG_STANDBY_MASK
        config[0] |= (iir_filter << _BMP280_CONFIG_IIR_POS) & _BMP280_CONFIG_IIR_MASK
        self.i2c.writeto_mem(self.addr, _BMP280_CONFIG, config)

        calibration = self.i2c.readfrom_mem(
            self.addr, _BMP280_CALIBRATION, _BMP280_CALIBRATION_LEN
        )
        (self._T1,) = unpack_from("<H", calibration, 0)
        (self._T2,) = unpack_from("<h", calibration, 2)
        (self._T3,) = unpack_from("<h", calibration, 4)
        (self._P1,) = unpack_from("<H", calibration, 6)
        (self._P2,) = unpack_from("<h", calibration, 8)
        (self._P3,) = unpack_from("<h", calibration, 10)
        (self._P4,) = unpack_from("<h", calibration, 12)
        (self._P5,) = unpack_from("<h", calibration, 14)
        (self._P6,) = unpack_from("<h", calibration, 16)
        (self._P7,) = unpack_from("<h", calibration, 18)
        (self._P8,) = unpack_from("<h", calibration, 20)
        (self._P9,) = unpack_from("<h", calibration, 22)

        if mode == MODE_NORMAL:
            # wait for initial measurement to complete
            sleep_us(self._measure_delay_us(temp_samples, press_samples))

    def reset(self):
        self.i2c.writeto_mem(self.addr, _BMP280_RESET, bytes([_BMP280_RESET_VALUE]))

    def _measure_delay_us(self, temp_os, press_os):
        """
        Returns the measurement delay in microseconds for the given oversampling
        register values for temperature and pressure.
        """
        temp_dur_us = _BMP280_DURATION_PER_SAMPLE_US * ((1 << temp_os) >> 1)
        press_dur_us = _BMP280_DURATION_PER_SAMPLE_US * ((1 << press_os) >> 1)
        press_dur_us += _BMP280_DURATION_PRESS_STARTUP_US if press_os else 0
        return _BMP280_DURATION_STARTUP_US + temp_dur_us + press_dur_us

    def _measure_prepare(self):
        """
        Sets up a measurement if the sensor is in sleep mode. Returns two
        booleans indicating whether temperature and pressure measurements are
        enabled.
        """
        control = bytearray(1)
        # read out values from control register so see if we have to force
        # a measurement, and if so, how long we have to wait for the result
        self.i2c.readfrom_mem_into(self.addr, _BMP280_CONTROL, control)
        mode = (control[0] & _BMP280_CONTROL_MODE_MASK) >> _BMP280_CONTROL_MODE_POS

        temp_samples = (
            control[0] & _BMP280_CONTROL_TEMP_SAMPLES_MASK
        ) >> _BMP280_CONTROL_TEMP_SAMPLES_POS

        temp_en = bool(temp_samples)
        press_samples = (
            control[0] & _BMP280_CONTROL_PRESS_SAMPLES_MASK
        ) >> _BMP280_CONTROL_PRESS_SAMPLES_POS
        press_en = bool(press_samples)

        # if sensor was in sleep mode, force a measurement now
        if mode == MODE_SLEEP:
            control[0] |= MODE_FORCED
            self.i2c.writeto_mem(self.addr, _BMP280_CONTROL, control)
            # wait for measurement to complete
            sleep_us(self._measure_delay_us(temp_samples, press_samples))
        return (temp_en, press_en)

    def measure(self):
        """
        Returns the temperature (in °C) and the pressure (in Pa) as a 2-tuple
        in the form of:

        (temperature, pressure)

        This function will wake up the sensor for a single measurement if the
        sensor is in sleep mode.
        """
        temp_en, press_en = self._measure_prepare()

        # Datasheet 3.11.3: Compute t_fine, temperature and pressure
        d = self.i2c.readfrom_mem(self.addr, _BMP280_DATA, _BMP280_DATA_LEN)
        p_raw = (d[0] << 12) | (d[1] << 4) | (d[2] >> 4)
        t_raw = (d[3] << 12) | (d[4] << 4) | (d[5] >> 4)

        # t_fine
        var1 = (((t_raw >> 3) - (self._T1 << 1)) * self._T2) >> 11
        var2 = (((((t_raw >> 4) - self._T1) * ((t_raw >> 4) - self._T1)) >> 12) * self._T3) >> 14
        t_fine = var1 + var2

        # temperature
        temperature = 0.0
        if temp_en:
            temperature = ((t_fine * 5 + 128) >> 8) / 100.0

        # pressure
        pressure = 0.0
        if press_en:
            var1 = t_fine - 128000
            var2 = var1 * var1 * self._P6
            var2 = var2 + ((var1 * self._P5) << 17)
            var2 = var2 + (self._P4 << 35)
            var1 = ((var1 * var1 * self._P3) >> 8) + ((var1 * self._P2) << 12)
            var1 = (((1 << 47) + var1) * self._P1) >> 33
            if var1 != 0:
                p = 1048576 - p_raw
                p = (((p << 31) - var2) * 3125) // var1
                var1 = (self._P9 * (p >> 13) * (p >> 13)) >> 25
                var2 = (self._P8 * p) >> 19
                p = ((p + var1 + var2) >> 8) + (self._P7 << 4)
            else:
                p = 0
            pressure = p / 256.0

        return (temperature, pressure)
