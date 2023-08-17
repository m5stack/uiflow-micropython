# Copyright (c) 2023 Sebastian Wicki
# SPDX-License-Identifier: MIT
"""
I2C-based driver for the QMP6988 temperature and pressure sensor.
"""
from micropython import const
from struct import unpack_from
from time import sleep_ms

I2C_DEFAULT_ADDR = const(0x70)

_QMP6988_CHIP_ID = const(0xD1)
_QMP6988_CHIP_ID_VALUE = const(0x5C)

_QMP6988_RESET = const(0xE0)
_QMP6988_RESET_VALUE = const(0xE6)

_QMP6988_IIR = const(0xF1)
_QMP6988_IIR_FILTER_MASK = const(0b0000_0011)
_QMP6988_IIR_FILTER_POS = const(0)

_QMP6988_DEVICE_STATUS = const(0xF3)
_QMP6988_DEVICE_STATUS_MEASURE_MASK = const(0b0000_1000)
_QMP6988_DEVICE_STATUS_MEASURE_POS = const(3)

_QMP6988_CONTROL = const(0xF4)
_QMP6988_CONTROL_TEMP_SAMPLES_MASK = const(0b1110_0000)
_QMP6988_CONTROL_TEMP_SAMPLES_POS = const(5)
_QMP6988_CONTROL_PRESS_SAMPLES_MASK = const(0b0001_1100)
_QMP6988_CONTROL_PRESS_SAMPLES_POS = const(2)
_QMP6988_CONTROL_PWR_MODE_MASK = const(0b0000_0011)
_QMP6988_CONTROL_PWR_MODE_POS = const(0)

_QMP6988_IO_SETUP = const(0xF5)
_QMP6988_IO_SETUP_STANDBY_MASK = const(0b1110_0000)
_QMP6988_IO_SETUP_STANDBY_POS = const(5)

_QMP6988_DATA = const(0xF7)
_QMP6988_CALIBRATION = const(0xA0)

_QMP6988_DATA_LEN = const(6)
_QMP6988_CALIBRATION_LEN = const(25)

PWR_MODE_NORMAL = const(0b11)
PWR_MODE_FORCED = const(0b01)
PWR_MODE_SLEEP = const(0b00)

TEMP_SAMPLES_SKIP = const(0b000)
TEMP_SAMPLES_1 = const(0b001)
TEMP_SAMPLES_2 = const(0b010)
TEMP_SAMPLES_4 = const(0b011)
TEMP_SAMPLES_8 = const(0b100)
TEMP_SAMPLES_16 = const(0b101)
TEMP_SAMPLES_32 = const(0b110)
TEMP_SAMPLES_64 = const(0b111)

PRESS_SAMPLES_SKIP = const(0b000)
PRESS_SAMPLES_1 = const(0b001)
PRESS_SAMPLES_2 = const(0b010)
PRESS_SAMPLES_4 = const(0b011)
PRESS_SAMPLES_8 = const(0b100)
PRESS_SAMPLES_16 = const(0b101)
PRESS_SAMPLES_32 = const(0b110)
PRESS_SAMPLES_64 = const(0b111)

IIR_FILTER_OFF = const(0b000)
IIR_FILTER_2 = const(0b001)
IIR_FILTER_4 = const(0b010)
IIR_FILTER_8 = const(0b011)
IIR_FILTER_16 = const(0b100)
IIR_FILTER_32 = const(0b101)

STANDBY_1_MS = const(0b000)
STANDBY_5_5_MS = const(0b001)
STANDBY_50_MS = const(0b010)
STANDBY_250_MS = const(0b011)
STANDBY_500_MS = const(0b100)
STANDBY_1000_MS = const(0b101)
STANDBY_2000_MS = const(0b110)
STANDBY_4000_MS = const(0b111)


class QMP6988:
    def __init__(
        self,
        i2c,
        addr=I2C_DEFAULT_ADDR,
        *,
        power_mode=PWR_MODE_NORMAL,
        press_samples=PRESS_SAMPLES_8,
        temp_samples=TEMP_SAMPLES_1,
        iir_filter=IIR_FILTER_4,
        standby_ms=STANDBY_1_MS,
    ):
        self.i2c = i2c
        self.addr = addr

        chipid = self.i2c.readfrom_mem(self.addr, _QMP6988_CHIP_ID, 1)
        if chipid[0] != _QMP6988_CHIP_ID_VALUE:
            raise ValueError("device not found")

        self.reset()

        # read OTP values (datasheet section 4.3)
        calibration = self.i2c.readfrom_mem(
            self.addr, _QMP6988_CALIBRATION, _QMP6988_CALIBRATION_LEN
        )
        (self.b00,) = unpack_from(">h", calibration, 0)
        (self.bt1,) = unpack_from(">h", calibration, 2)
        (self.bt2,) = unpack_from(">h", calibration, 4)
        (self.bp1,) = unpack_from(">h", calibration, 6)
        (self.b11,) = unpack_from(">h", calibration, 8)
        (self.bp2,) = unpack_from(">h", calibration, 10)
        (self.b12,) = unpack_from(">h", calibration, 12)
        (self.b21,) = unpack_from(">h", calibration, 14)
        (self.bp3,) = unpack_from(">h", calibration, 16)
        (self.a0,) = unpack_from(">h", calibration, 18)
        (self.a1,) = unpack_from(">h", calibration, 20)
        (self.a2,) = unpack_from(">h", calibration, 22)
        b00_a0_ex = calibration[24]
        self.b00 = (self.b00 << 4) | ((b00_a0_ex >> 4) & 0xF)
        self.a0 = (self.a0 << 4) | (b00_a0_ex & 0xF)

        # K = A + S * OTP / 32767 (datasheet section 4.3)
        self.a1 = -6.30e-03 + 4.30e-04 * self.a1 / 32767
        self.a2 = -1.90e-11 + 1.20e-10 * self.a2 / 32767

        self.bt1 = 1.00e-01 + 9.10e-02 * self.bt1 / 32767
        self.bt2 = 1.20e-08 + 1.20e-06 * self.bt2 / 32767

        self.bp1 = 3.30e-02 + 1.90e-02 * self.bp1 / 32767
        self.b11 = 2.10e-07 + 1.40e-07 * self.b11 / 32767

        self.bp2 = -6.30e-10 + 3.50e-10 * self.bp2 / 32767
        self.b12 = 2.90e-13 + 7.60e-13 * self.b12 / 32767

        self.b21 = 2.10e-15 + 1.20e-14 * self.b21 / 32767
        self.bp3 = 1.30e-16 + 7.90e-17 * self.bp3 / 32767

        # K = OTP / 16 (datasheet section 4.3)
        self.a0 = self.a0 / 16
        self.b00 = self.b00 / 16

        # set standby time
        setup = bytearray(1)
        setup[0] |= (standby_ms << _QMP6988_IO_SETUP_STANDBY_POS) & _QMP6988_IO_SETUP_STANDBY_MASK
        self.i2c.writeto_mem(self.addr, _QMP6988_IO_SETUP, setup)

        # set power mode and oversampling
        control = bytearray(1)
        control[0] |= (
            temp_samples << _QMP6988_CONTROL_TEMP_SAMPLES_POS
        ) & _QMP6988_CONTROL_TEMP_SAMPLES_MASK
        control[0] |= (
            press_samples << _QMP6988_CONTROL_PRESS_SAMPLES_POS
        ) & _QMP6988_CONTROL_PRESS_SAMPLES_MASK
        # PWR_MODE_FORCED will be set in the call to measure()
        if power_mode == PWR_MODE_NORMAL:
            control[0] |= (
                power_mode << _QMP6988_CONTROL_PWR_MODE_POS
            ) & _QMP6988_CONTROL_PWR_MODE_MASK
        self.i2c.writeto_mem(self.addr, _QMP6988_CONTROL, control)

        # set filter
        filter = bytearray(1)
        filter[0] |= (iir_filter << _QMP6988_IIR_FILTER_POS) & _QMP6988_IIR_FILTER_MASK
        self.i2c.writeto_mem(self.addr, _QMP6988_IIR, filter)

    def reset(self):
        try:
            self.i2c.writeto_mem(self.addr, _QMP6988_RESET, bytes([_QMP6988_RESET_VALUE]))
        except OSError:
            # It seems that that the device immediately resets upon soft-reset
            # without finishing the I2C transaction, causing an ETIMEDOUT here.
            # Thus, we silently ignore those errors and instead read back the
            # the expected value after reset (ensuring that the device is online
            # again)
            pass
        sleep_ms(10)
        reset = self.i2c.readfrom_mem(self.addr, _QMP6988_RESET, 1)
        if reset != b"\0":
            raise RuntimeError("device not ready")

    def _measure_prepare(self):
        """
        Sets up a measurement if the sensor is in sleep mode. Returns two
        booleans indicating whether temperature and pressure measurements are
        enabled.
        (temp_en, press_en)
        """
        # read out values from control register so see if we have to force
        # a measurement
        control = bytearray(1)
        self.i2c.readfrom_mem_into(self.addr, _QMP6988_CONTROL, control)
        mode = (control[0] & _QMP6988_CONTROL_PWR_MODE_MASK) >> _QMP6988_CONTROL_PWR_MODE_POS

        temp_en = (
            (control[0] & _QMP6988_CONTROL_TEMP_SAMPLES_MASK) >> _QMP6988_CONTROL_TEMP_SAMPLES_POS
        ) != TEMP_SAMPLES_SKIP

        press_en = (
            (control[0] & _QMP6988_CONTROL_PRESS_SAMPLES_MASK)
            >> _QMP6988_CONTROL_PRESS_SAMPLES_POS
        ) != PRESS_SAMPLES_SKIP

        # force measurement and wait for it to finish
        if mode != PWR_MODE_NORMAL:
            control[0] |= PWR_MODE_FORCED
            self.i2c.writeto_mem(self.addr, _QMP6988_CONTROL, control)

        status = bytearray(1)
        for i in range(100):
            # skip initial sleep in normal mode, we expect it to be ready
            if i > 0 or mode != PWR_MODE_NORMAL:
                sleep_ms(10)
            self.i2c.readfrom_mem_into(self.addr, _QMP6988_DEVICE_STATUS, status)
            measure = (
                status[0] & _QMP6988_DEVICE_STATUS_MEASURE_MASK
            ) >> _QMP6988_DEVICE_STATUS_MEASURE_POS
            if measure == 0:
                break
        else:
            raise RuntimeError("device not ready")

        return temp_en, press_en

    def measure(self):
        """
        Returns the temperature (in °C) and the pressure (in Pa) as a 2-tuple
        in the form of:

        (temperature, pressure)

        This function will wake up the sensor for a single measurement if the
        sensor is in sleep mode.
        """
        temp_en, press_en = self._measure_prepare()

        # Compensation based on datasheet section 4.3
        d = self.i2c.readfrom_mem(self.addr, _QMP6988_DATA, _QMP6988_DATA_LEN)
        dp = ((d[0] << 16) | (d[1] << 8) | d[2]) - 2 ** 23
        dt = ((d[3] << 16) | (d[4] << 8) | d[5]) - 2 ** 23

        tr = self.a0 + (self.a1 * dt) + (self.a2 * (dt ** 2))

        pr = (
            self.b00
            + (self.bt1 * tr)
            + (self.bp1 * dp)
            + (self.b11 * tr * dp)
            + (self.bt2 * tr ** 2)
            + (self.bp2 * dp ** 2)
            + (self.b12 * dp * (tr ** 2))
            + (self.b21 * (dp ** 2) * tr)
            + (self.bp3 * (dp ** 3))
        )

        temperature = (tr / 256) if temp_en else 0.0
        pressure = pr if press_en else 0.0

        return (temperature, pressure)
