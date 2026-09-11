# SPDX-FileCopyrightText: 2022 Bosch Sensortec GmbH
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: BSD-3-Clause

"""BMM350 magnetometer accessed through direct I2C."""

import math
import time


BMM350_ADDR = 0x14

_CHIP_ID = 0x00
_PMU_AGGR = 0x04
_PMU_AXIS = 0x05
_PMU_CMD = 0x06
_MAG_DATA = 0x31
_OTP_CMD = 0x50
_OTP_MSB = 0x52
_OTP_LSB = 0x53
_OTP_STATUS = 0x55
_CMD = 0x7E


def _signed(value, bits):
    sign = 1 << (bits - 1)
    return value - (1 << bits) if value & sign else value


def _u24(data, offset):
    return data[offset] | (data[offset + 1] << 8) | (data[offset + 2] << 16)


class BMM350:
    """BMM350 device using direct I2C."""

    def __init__(self, i2c, address=BMM350_ADDR, output_data_rate_hz=100):
        self._i2c = i2c
        self.address = address

        time.sleep_ms(3)
        self._write(_CMD, 0xB6)
        time.sleep_ms(24)
        if self._read(_CHIP_ID) != 0x33:
            raise OSError("No BMM350 device was found at address 0x%x" % address)

        self._otp = self._read_otp()
        self._load_compensation(self._otp)
        self._write(_OTP_CMD, 0x80)
        self._write(_PMU_CMD, 0x07)
        time.sleep_ms(14)
        self._write(_PMU_CMD, 0x05)
        time.sleep_ms(18)
        self.set_output_data_rate(output_data_rate_hz)
        self._write(_PMU_AXIS, 0x07)
        self._write(_PMU_CMD, 0x01)
        time.sleep_ms(38)

    def _read(self, reg, size=1):
        value = self._i2c.readfrom_mem(self.address, reg, size + 2)
        result = value[2 : 2 + size]
        return result[0] if size == 1 else bytes(result)

    def _write(self, reg, value):
        self._i2c.writeto_mem(self.address, reg, bytes((value,)))

    def _read_otp(self):
        words = []
        for address in range(32):
            self._write(_OTP_CMD, 0x20 | address)
            for _ in range(20):
                time.sleep_us(300)
                status = self._read(_OTP_STATUS)
                if status & 0xE0:
                    raise OSError("BMM350 OTP read failed: 0x%02x" % status)
                if status & 0x01:
                    break
            else:
                raise OSError("BMM350 OTP read timed out")
            words.append((self._read(_OTP_MSB) << 8) | self._read(_OTP_LSB))
        return words

    def _load_compensation(self, otp):
        off_x = otp[0x0E] & 0x0FFF
        off_y = ((otp[0x0E] & 0xF000) >> 4) | (otp[0x0F] & 0x00FF)
        off_z = (otp[0x0F] & 0x0F00) | (otp[0x10] & 0x00FF)
        self._offset = tuple(_signed(v, 12) for v in (off_x, off_y, off_z))

        self._temp_offset = _signed(otp[0x0D] & 0xFF, 8) / 5.0
        self._sensitivity = (
            _signed((otp[0x10] >> 8) & 0xFF, 8) / 256.0,
            _signed(otp[0x11] & 0xFF, 8) / 256.0,
            _signed((otp[0x11] >> 8) & 0xFF, 8) / 256.0,
        )
        self._temp_sensitivity = _signed((otp[0x0D] >> 8) & 0xFF, 8) / 512.0
        self._tco = tuple(_signed(otp[i] & 0xFF, 8) / 32.0 for i in (0x12, 0x13, 0x14))
        self._tcs = tuple(_signed((otp[i] >> 8) & 0xFF, 8) / 16384.0 for i in (0x12, 0x13, 0x14))
        self._t0 = _signed(otp[0x18], 16) / 512.0 + 23.0
        self._cross = (
            _signed(otp[0x15] & 0xFF, 8) / 800.0,
            _signed((otp[0x15] >> 8) & 0xFF, 8) / 800.0,
            _signed(otp[0x16] & 0xFF, 8) / 800.0,
            _signed((otp[0x16] >> 8) & 0xFF, 8) / 800.0,
        )

    def set_output_data_rate(self, output_data_rate_hz):
        rates = {400: 0x02, 200: 0x03, 100: 0x04, 50: 0x05, 25: 0x06}
        if output_data_rate_hz not in rates:
            raise ValueError("BMM350 ODR must be 25, 50, 100, 200, or 400 Hz")
        averaging = 0 if output_data_rate_hz == 400 else 1 if output_data_rate_hz == 200 else 2
        self._write(_PMU_AGGR, rates[output_data_rate_hz] | (averaging << 4))
        self._write(_PMU_CMD, 0x02)
        time.sleep_ms(1)
        self.output_data_rate_hz = output_data_rate_hz

    def read(self, raw=False):
        """Return magnetic data and temperature; raw returns signed register counts."""
        data = self._read(_MAG_DATA, 12)
        raw_values = tuple(_signed(_u24(data, i), 24) for i in (0, 3, 6, 9))

        if raw:
            return raw_values[:3], raw_values[3]

        field = [
            raw_values[0] * 0.007069979,
            raw_values[1] * 0.007069979,
            raw_values[2] * 0.007174964,
        ]
        temperature = raw_values[3] * 0.000981282 - 25.49
        temperature = (1.0 + self._temp_sensitivity) * temperature + self._temp_offset
        delta_t = temperature - self._t0
        for axis in range(3):
            field[axis] *= 1.0 + self._sensitivity[axis]
            field[axis] += self._offset[axis] + self._tco[axis] * delta_t
            denominator = 1.0 + self._tcs[axis] * delta_t
            if math.fabs(denominator) > 1e-9:
                field[axis] /= denominator

        cross_xy, cross_yx, cross_zx, cross_zy = self._cross
        denominator = 1.0 - cross_yx * cross_xy
        x = (field[0] - cross_xy * field[1]) / denominator
        y = (field[1] - cross_yx * field[0]) / denominator
        z = (
            field[2]
            + (
                field[0] * (cross_yx * cross_zy - cross_zx)
                - field[1] * (cross_zy - cross_xy * cross_zx)
            )
            / denominator
        )
        return (x, y, z), temperature
