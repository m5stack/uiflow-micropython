# SPDX-FileCopyrightText: 2017 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT AND BSD-3-Clause

import struct
import time
import math
from micropython import const
from collections import namedtuple


# Memory map
_BME68X_REG_STATUS = const(0x73)
_BME68X_REG_VARIANT = const(0xF0)
_BME68X_REG_SOFTRESET = const(0xE0)
_BME68X_REG_CHIPID = const(0xD0)
_BME68X_REG_CONFIG = const(0x75)
_BME68X_REG_CTRL_MEAS = const(0x74)
_BME68X_REG_CTRL_HUM = const(0x72)
_BME68X_REG_CTRL_GAS_0 = const(0x70)
_BME68X_REG_CTRL_GAS_1 = const(0x71)
_BME68X_REG_GAS_WAIT_SHARED = const(0x6E)
_BME68X_REG_GAS_WAIT_0 = const(0x64)
_BME68X_REG_RES_HEAT_0 = const(0x5A)
_BME68X_REG_IDAC_HEAT_0 = const(0x50)
_BME68X_REG_MEAS_STATUS = const(0x1D)

_BME68X_REG_COEFF_ADDR1 = const(0x8A)
_BME68X_REG_COEFF_ADDR2 = const(0xE1)


# Mask
_BME68X_ENABLE_HEATER = const(0x00)
_BME68X_DISABLE_HEATER = const(0x01)
_BME68X_DISABLE_GAS_MEAS = const(0x00)
_BME68X_ENABLE_GAS_MEAS_L = const(0x01)
_BME68X_ENABLE_GAS_MEAS_H = const(0x02)
_BME68X_SLEEP_MODE = const(0)
_BME68X_FORCED_MODE = const(1)
_BME68X_VARIANT_GAS_LOW = const(0x00)
_BME68X_VARIANT_GAS_HIGH = const(0x01)
_BME68X_HCTRL_MSK = const(0x08)
_BME68X_HCTRL_POS = const(3)
_BME68X_NBCONV_MSK = const(0x0F)
_BME68X_RUN_GAS_MSK = const(0x30)
_BME68X_RUN_GAS_POS = const(4)
_BME68X_MODE_MSK = const(0x03)
_BME68X_PERIOD_POLL = const(10000)
_BME68X_OSH_MSK = const(0x07)


# Default value
_BME68X_RUNGAS = const(0x10)
_BME68X_CHIPID = const(0x61)


BME68xCalculationData = namedtuple(
    "BME68xCalculationData",
    [
        "par_h1",
        "par_h2",
        "par_h3",
        "par_h4",
        "par_h5",
        "par_h6",
        "par_h7",
        "par_g1",
        "par_g2",
        "par_g3",
        "par_t1",
        "par_t2",
        "par_t3",
        "par_p1",
        "par_p2",
        "par_p3",
        "par_p4",
        "par_p5",
        "par_p6",
        "par_p7",
        "par_p8",
        "par_p9",
        "par_p10",
        "t_fine",
        "res_heat_range",
        "res_heat_val",
        "range_sw_err",
    ],
)


class BME68xData:
    status: int = 0
    gas_index: int = 0
    meas_index: int = 0
    res_heat: int = 0
    idac: int = 0
    gas_wait: int = 0
    pressure: float = 0.0
    temperature: float = 0.0
    humidity: float = 0.0
    gas_resistance: int = 0


class BME68X:
    """Driver from BME680 air quality sensor

    :param int refresh_rate: Maximum number of readings per second. Faster
                             property reads will be from the previous reading.
    """

    _BME68X_SAMPLERATES = (0, 1, 2, 4, 8, 16)
    _BME68X_FILTERSIZES = (0, 1, 3, 7, 15, 31, 63, 127)

    def __init__(self, *, refresh_rate: int = 10) -> None:
        """Check the BME680 was found, read the coefficients and enable the
        sensor for continuous reads.
        """
        self.soft_reset()

        # Check device ID.
        chip_id = self._read_byte(_BME68X_REG_CHIPID)
        if chip_id != _BME68X_CHIPID:
            raise RuntimeError("Failed to find BME680! Chip ID 0x%x" % chip_id)

        # Get variant
        self._variant_id = self._read_byte(_BME68X_REG_VARIANT)

        self._read_calibration()
        self._sensor_data = [BME68xData(), BME68xData(), BME68xData()]

        self.sea_level_pressure = 1013.25
        """Pressure in hectoPascals at sea level. Used to calibrate :attr:`altitude`."""

        # Default oversampling and filter register values.
        self._pressure_oversample = 0b011
        self._temp_oversample = 0b100
        self._humidity_oversample = 0b010
        self._filter = 0b010

        self._t_fine = 0

        self._last_reading = 0
        self._min_refresh_time = refresh_rate  # unused

        # Copy required parameters from reference bme68x_dev struct
        self._amb_temp = 25
        self.set_tph()
        # heater 320 deg C for 150 msec
        self.set_gas_heater(320, 150)
        self.set_op_mode(1)
        self._op_mode = 1
        self.meas_dur_us = self.get_meas_dur()

    def soft_reset(self) -> None:
        """Perform a soft reset of the sensor."""
        self._write(_BME68X_REG_SOFTRESET, [0xB6])
        time.sleep(0.005)

    def set_op_mode(self, op_mode: int) -> None:
        """
        * @brief This API is used to set the operation mode of the sensor
        """
        tmp_pow_mode: int = 0
        pow_mode: int = _BME68X_FORCED_MODE
        reg_addr: int = _BME68X_REG_CTRL_MEAS
        # Call until in sleep
        try:
            # was a do {} while() loop
            while pow_mode != _BME68X_SLEEP_MODE:
                tmp_pow_mode = self._read_byte(_BME68X_REG_CTRL_MEAS)
                # Put to sleep before changing mode
                pow_mode = tmp_pow_mode & _BME68X_MODE_MSK
                if pow_mode != _BME68X_SLEEP_MODE:
                    tmp_pow_mode &= ~_BME68X_MODE_MSK  # Set to sleep
                    self._write(reg_addr, [tmp_pow_mode])
                    # dev->delay_us(_BME68X_PERIOD_POLL, dev->intf_ptr)  # HELP
                    time.sleep_us(_BME68X_PERIOD_POLL)
            # Already in sleep
            if op_mode != _BME68X_SLEEP_MODE:
                tmp_pow_mode = (tmp_pow_mode & ~_BME68X_MODE_MSK) | (op_mode & _BME68X_MODE_MSK)
                self._write(reg_addr, [tmp_pow_mode])
        except Exception as exc:
            raise exc

    def get_op_mode(self) -> int:
        """
        * @brief This API is used to get the operation mode of the sensor
        """
        return self._read_byte(_BME68X_REG_CTRL_MEAS) & _BME68X_MODE_MSK

    def get_tph(self) -> tuple:
        self._bme_get_conf()
        return self.os_temp, self.os_pres, self.os_hum

    def set_tph(self, temperature=2, pressure=5, humidity=1) -> None:
        self._bme_get_conf()
        self.os_hum = humidity
        self.os_temp = temperature
        self.os_pres = pressure
        self._bme_set_conf()

    def _bme_get_conf(self):
        data = self._read(_BME68X_REG_CTRL_GAS_1, 5)
        self.os_hum = data[1] & _BME68X_OSH_MSK
        self.filter = self.get_bits(data[4], 0x1C, 2)
        self.os_temp = self.get_bits(data[3], 0xE0, 5)
        self.os_pres = self.get_bits(data[3], 0x1C, 2)
        if self.get_bits(data[0], 0x80, 7):
            self.odr = 8
        else:
            self.odr = self.get_bits(data[4], 0xE0, 5)

    def _bme_set_conf(self):
        # Configure only in the sleep mode
        op_mode = self.get_op_mode()
        self.set_op_mode(0)
        data = self._read(_BME68X_REG_CTRL_GAS_1, 5)

        # boundary check
        self.filter = 7 if self.filter > 7 else self.filter
        self.os_temp = 5 if self.os_temp > 5 else self.os_temp
        self.os_pres = 5 if self.os_pres > 5 else self.os_pres
        self.os_hum = 5 if self.os_hum > 5 else self.os_hum
        self.odr = 8 if self.odr > 8 else self.odr

        # write
        data[4] = self.set_bits(data[4], 0x1C, 2, self.filter)
        data[3] = self.set_bits(data[3], 0xE0, 5, self.os_temp)
        data[3] = self.set_bits(data[3], 0x1C, 2, self.os_pres)
        data[1] = (data[1] & 0x07) | (self.os_hum & 0x07)

        odr20 = 0
        odr3 = 1
        if self.odr != 8:
            odr20 = self.odr
            odr3 = 0
        data[4] = self.set_bits(data[4], 0xE0, 5, odr20)
        data[0] = self.set_bits(data[0], 0x80, 7, odr3)

        self._write(_BME68X_REG_CTRL_GAS_1, data)

        if op_mode != 0:
            self.set_op_mode(op_mode)

    @staticmethod
    def get_bits(value, mask, pos):
        return value & (mask >> pos)

    @staticmethod
    def set_bits(value, mask, pos, new_value):
        return (value & ~(mask)) | ((new_value << pos) & mask)

    def get_meas_dur(self) -> int:
        meas_dur = 0
        meas_cycles = 0
        os_to_meas_cycles = (0, 1, 2, 4, 8, 16)

        self._bme_get_conf()

        self.os_temp = 5 if self.os_temp > 5 else self.os_temp
        self.os_pres = 5 if self.os_pres > 5 else self.os_pres
        self.os_hum = 5 if self.os_hum > 5 else self.os_hum

        meas_cycles = os_to_meas_cycles[self.os_temp]
        meas_cycles += os_to_meas_cycles[self.os_pres]
        meas_cycles += os_to_meas_cycles[self.os_hum]

        # TPH measurement duration
        meas_dur = meas_cycles * 1963
        meas_dur += 477 * 4  # TPH switching duration
        meas_dur += 477 * 5  # Gas measurement duration

        if self._op_mode != 2:
            meas_dur += 1000

        return meas_dur

    @property
    def pressure_oversample(self) -> int:
        """The oversampling for pressure sensor"""
        self._pressure_oversample = (self._read_byte(_BME68X_REG_CTRL_MEAS) & 0x1C) >> 2
        return self._BME68X_SAMPLERATES[self._pressure_oversample]

    @pressure_oversample.setter
    def pressure_oversample(self, sample_rate: int) -> None:
        if sample_rate in self._BME68X_SAMPLERATES:
            self._pressure_oversample = self._BME68X_SAMPLERATES.index(sample_rate)
        else:
            raise RuntimeError("Invalid oversample")
        rate = self._read_byte(_BME68X_REG_CTRL_MEAS) & 0xE0
        rate |= self._pressure_oversample << 2
        self._write(_BME68X_REG_CTRL_MEAS, [rate & 0xFC])

    @property
    def humidity_oversample(self) -> int:
        """The oversampling for humidity sensor"""
        self._humidity_oversample = self._read_byte(_BME68X_REG_CTRL_HUM) & 0x07
        return self._BME68X_SAMPLERATES[self._humidity_oversample]

    @humidity_oversample.setter
    def humidity_oversample(self, sample_rate: int) -> None:
        if sample_rate in self._BME68X_SAMPLERATES:
            self._humidity_oversample = self._BME68X_SAMPLERATES.index(sample_rate)
        else:
            raise RuntimeError("Invalid oversample")
        rate = self._read_byte(_BME68X_REG_CTRL_HUM) & 0xF8
        rate |= self._humidity_oversample
        self._write(_BME68X_REG_CTRL_HUM, [rate])

    @property
    def temperature_oversample(self) -> int:
        """The oversampling for temperature sensor"""
        self._temp_oversample = (self._read_byte(_BME68X_REG_CTRL_MEAS) & 0xE0) >> 5
        return self._BME68X_SAMPLERATES[self._temp_oversample]

    @temperature_oversample.setter
    def temperature_oversample(self, sample_rate: int) -> None:
        if sample_rate in self._BME68X_SAMPLERATES:
            self._temp_oversample = self._BME68X_SAMPLERATES.index(sample_rate)
        else:
            raise RuntimeError("Invalid oversample")
        rate = self._read_byte(_BME68X_REG_CTRL_MEAS) & 0x1C
        rate |= self._temp_oversample << 5
        self._write(_BME68X_REG_CTRL_MEAS, [rate & 0xFC])

    @property
    def filter_size(self) -> int:
        """The filter size for the built in IIR filter"""
        self._filter = (self._read_byte(_BME68X_REG_CONFIG) & 0x1C) >> 2
        return self._BME68X_FILTERSIZES[self._filter]

    @filter_size.setter
    def filter_size(self, size: int) -> None:
        if size in self._BME68X_FILTERSIZES:
            self._filter = self._BME68X_FILTERSIZES.index(size)
        else:
            raise RuntimeError("Invalid size")
        size = self._read_byte(_BME68X_REG_CONFIG) & 0xE3
        size |= self._filter << 2
        self._write(_BME68X_REG_CONFIG, [size])

    def gas_conversion(self, enable: bool = True) -> None:
        if self._variant_id == 0x01:
            rate = self._read_byte(_BME68X_REG_CTRL_GAS_1)
            if enable:
                rate |= _BME68X_RUNGAS << 1
            else:
                rate &= ~(_BME68X_RUNGAS << 1)
            self._write(_BME68X_REG_CTRL_GAS_1, [rate])

    @property
    def temperature(self) -> float:
        """The compensated temperature in degrees Celsius."""
        if time.ticks_diff(self._last_reading, time.ticks_ms()) * time.ticks_diff(0, 1) < 2000:
            return self._sensor_data[0].temperature
        if self._op_mode == 1:
            self.set_op_mode(1)
            self._read_field_data(0)
            self._last_reading = time.ticks_ms()
            return self._sensor_data[0].temperature
        else:
            return self._sensor_data[0].temperature

    @property
    def pressure(self) -> float:
        """The barometric pressure in hectoPascals"""
        if time.ticks_diff(self._last_reading, time.ticks_ms()) * time.ticks_diff(0, 1) < 2000:
            return self._sensor_data[0].pressure / 100
        if self._op_mode == 1:
            self.set_op_mode(1)
            self._read_field_data(0)
            self._last_reading = time.ticks_ms()
            return self._sensor_data[0].pressure / 100
        else:
            return self._sensor_data[0].pressure / 100

    @property
    def humidity(self) -> float:
        """The relative humidity in RH %"""
        if time.ticks_diff(self._last_reading, time.ticks_ms()) * time.ticks_diff(0, 1) < 2000:
            return self._sensor_data[0].humidity
        if self._op_mode == 1:
            self.set_op_mode(1)
            self._read_field_data(0)
            self._last_reading = time.ticks_ms()
            return self._sensor_data[0].humidity
        else:
            return self._sensor_data[0].humidity

    @property
    def altitude(self) -> float:
        """The altitude based on current :attr:`pressure` vs the sea level pressure
        (:attr:`sea_level_pressure`) - which you must enter ahead of time)"""
        pressure = self.pressure  # in Si units for hPascal
        return 44330 * (1.0 - math.pow(pressure / self.sea_level_pressure, 0.1903))

    @property
    def gas(self) -> int:
        """The gas resistance in ohms"""
        return self._sensor_data[0].gas_resistance

    def calc_gas_resistance_high(self, gas_res_adc, gas_range):
        var1 = 262144 >> gas_range
        var2 = gas_res_adc - 512
        var2 *= 3
        var2 += 4096

        calc_gas_res = 1000000.0 * var1 / var2

        return calc_gas_res

    def calc_gas_resistance_low(self, gas_res_adc, gas_range):
        lookup_k1_range = (
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            -1.0,
            0.0,
            -0.8,
            0.0,
            0.0,
            -0.2,
            -0.5,
            0.0,
            -1.0,
            0.0,
            0.0,
        )
        lookup_k2_range = (
            0.0,
            0.0,
            0.0,
            0.0,
            0.1,
            0.7,
            0.0,
            -0.8,
            -0.1,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        )
        var1 = 1340.0 + (5.0 * self._calibration.range_sw_err)
        var2 = var1 * (1.0 + lookup_k1_range[gas_range] / 100.0)
        var3 = 1.0 + (lookup_k2_range[gas_range] / 100.0)
        gas_res_f = gas_res_adc
        gas_range_f = 1 << gas_range

        calc_gas_res = 1.0 / (
            var3 * (0.000000125) * gas_range_f * (((gas_res_f - 512.0) / var2) + 1.0)
        )

        return calc_gas_res

    def calc_temperature(self, temp_adc):
        var1 = ((temp_adc / 16384.0) - (self._calibration.par_t1 / 1024.0)) * (
            self._calibration.par_t2
        )
        var2 = (
            ((temp_adc / 131072.0) - (self._calibration.par_t1 / 8192.0))
            * ((temp_adc / 131072.0) - (self._calibration.par_t1 / 8192.0))
        ) * (self._calibration.par_t3 * 16.0)
        self._t_fine = var1 + var2
        calc_temp = self._t_fine / 5120.0
        return calc_temp

    def calc_pressure(self, pres_adc):
        var1 = (self._t_fine / 2.0) - 64000.0
        var2 = var1 * var1 * (self._calibration.par_p6 / 131072.0)
        var2 += var1 * self._calibration.par_p5 * 2.0
        var2 = (var2 / 4.0) + (self._calibration.par_p4 * 65536.0)
        var1 = (
            ((self._calibration.par_p3 * var1 * var1) / 16384.0)
            + (self._calibration.par_p2 * var1)
        ) / 524288.0
        var1 = (1.0 + (var1 / 32768.0)) * self._calibration.par_p1
        calc_pres = 1048576.0 - pres_adc

        if int(var1) != 0:
            calc_pres = ((calc_pres - (var2 / 4096.0)) * 6250.0) / var1
            var1 = (self._calibration.par_p9 * calc_pres * calc_pres) / 2147483648.0
            var2 = calc_pres * (self._calibration.par_p8 / 32768.0)
            var3 = (calc_pres / 256.0) ** 3 * (self._calibration.par_p10 / 131072.0)
            calc_pres = (
                calc_pres + (var1 + var2 + var3 + (self._calibration.par_p7 * 128.0)) / 16.0
            )
        else:
            calc_pres = 0

        return calc_pres

    def calc_humidity(self, hum_adc):
        temp_comp = self._t_fine / 5120.0
        var1 = float(hum_adc) - (
            (self._calibration.par_h1 * 16.0) + ((self._calibration.par_h3 / 2.0) * temp_comp)
        )
        var2 = var1 * (
            (self._calibration.par_h2 / 262144.0)
            * (
                1.0
                + ((self._calibration.par_h4 / 16384.0) * temp_comp)
                + ((self._calibration.par_h5 / 1048576.0) * temp_comp * temp_comp)
            )
        )
        var3 = self._calibration.par_h6 / 16384.0
        var4 = self._calibration.par_h7 / 2097152.0
        calc_hum = var2 + ((var3 + (var4 * temp_comp)) * var2 * var2)

        if calc_hum > 100.0:
            calc_hum = 100.0
        elif calc_hum < 0.0:
            calc_hum = 0.0

        return calc_hum

    def _read_field_data(self, index) -> BME68xData:
        data = self._read(_BME68X_REG_MEAS_STATUS + index * 17, 17)
        status = data[0] & 0x80
        gas_index = data[0] & 0x0F
        meas_index = data[1]
        res_heat = None
        idac = None
        gas_wait = None
        pressure = self._read24(data[2:5]) / 16
        temperature = self._read24(data[5:8]) / 16
        humidity = struct.unpack(">H", bytes(data[8:10]))[0]
        gas_resistance = None

        adc_gas_res_low = (data[13] * 4) | (data[14] // 64)
        adc_gas_res_high = (data[15] * 4) | (data[16] // 64)
        gas_range_l = data[14] & 0x0F
        gas_range_h = data[16] & 0x0F
        if self._variant_id == 0x01:
            status |= data[16] & 0x20
            status |= data[16] & 0x10
        else:
            status |= data[14] & 0x20
            status |= data[14] & 0x10

        if status & 0x80:
            data = self._read(0x5A + gas_index, 1)
            res_heat = data[0]

            data = self._read(0x50 + gas_index, 1)
            idac = data[0]

            data = self._read(0x64 + gas_index, 1)
            gas_wait = data[0]

            temperature = self.calc_temperature(temperature)
            pressure = self.calc_pressure(pressure)
            humidity = self.calc_humidity(humidity)
            if self._variant_id == 0x01:
                gas_resistance = self.calc_gas_resistance_high(adc_gas_res_high, gas_range_h)
            else:
                gas_resistance = self.calc_gas_resistance_low(adc_gas_res_low, gas_range_l)

            self._sensor_data[0].status = status
            self._sensor_data[0].gas_index = gas_index
            self._sensor_data[0].meas_index = meas_index
            self._sensor_data[0].res_heat = res_heat
            self._sensor_data[0].idac = idac
            self._sensor_data[0].gas_wait = gas_wait
            self._sensor_data[0].pressure = pressure
            self._sensor_data[0].temperature = temperature
            self._sensor_data[0].humidity = humidity
            self._sensor_data[0].gas_resistance = gas_resistance

        return None

    def _read_all_field_data(self) -> list[BME68xData]:
        data = []
        for i in range(3):
            field_data = self._read_field_data(i)
            if field_data is not None:
                data.append(field_data)
        return data

    def _read_calibration(self) -> None:
        """Read & save the calibration coefficients"""

        # Calibration data is stored at the following addresses:
        # +------------+------------+------------+------------+------------+------------+
        # | 0x8A       | 0x8B       | 0x8C       | 0x8D       | 0x8E       | 0x8F       |
        # +------------+------------+------------+------------+------------+------------+
        # | par_t2 LSB | par_t2 MSB | par_t3     |            | par_p1 LSB | par_p1 MSB |
        # +------------+------------+------------+------------+------------+------------+
        # | 0x90       | 0x91       | 0x92       | 0x93       | 0x94       | 0x95       |
        # +------------+------------+------------+------------+------------+------------+
        # | par_p2 LSB | par_p2 MSB | par_p3     |            | par_p4 LSB | par_p4 MSB |
        # +------------+------------+------------+------------+------------+------------+
        # | 0x96       | 0x97       | 0x98       | 0x99       | 0x9A       | 0x9B       |
        # +------------+------------+------------+------------+------------+------------+
        # | par_p5 LSB | par_p5 MSB | par_p7     | par_p6     |            |            |
        # +------------+------------+------------+------------+------------+------------+
        # | 0x9C       | 0x9D       | 0x9E       | 0x9F       | 0xA0       | 0xA1       |
        # +------------+------------+------------+------------+------------+------------+
        # | par_p8 LSB | par_p8 MSB | par_p9 LSB | par_p9 MSB | par_p10    |            |
        # +------------+------------+------------+------------+------------+------------+

        # +------------+------------+------------+------------+------------+------------+
        # | 0xE1       | 0xE2       | 0xE3       | 0xE4       | 0xE5       | 0xE6       |
        # +------------+------------+------------+------------+------------+------------+
        # | par_h2 MSB | par_h1 LSB | par_h1 MSB | par_h3     | par_h4     | par_h5     |
        # +------------+------------+------------+------------+------------+------------+
        # | 0xE7       | 0xE8       | 0xE9       | 0xEA       | 0xEB       | 0xEC       |
        # +------------+------------+------------+------------+------------+------------+
        # | par_h6     | par_h7     | par_t1 LSB | par_t1 MSB | par_g2 LSB | par_g2 MSB |
        # +------------+------------+------------+------------+------------+------------+
        # | 0xED       | 0xEE       | 0xEF       | 0xF0       | 0xF1       | 0xF2       |
        # +------------+------------+------------+------------+------------+------------+
        # | par_g1     | par_g3     |            |            |            |            |
        # +------------+------------+------------+------------+------------+------------+

        # 0 par_t2 int16_t h
        # 1 par_t3 int8_t  b
        # 2 unused uint8_t B
        # 3 par_p1 uint16_t H
        # 4 par_p2 int16_t h
        # 5 par_p3 int8_t b
        # 6 unused uint8_t B
        # 7 par_p4 int16_t h
        # 8 par_p5 int16_t h
        # 9 par_p7 int8_t b
        # 10 par_p6 int8_t b
        # 11 unused uint8_t B
        # 12 unused uint8_t B
        # 13 par_p8 int16_t h
        # 14 par_p9 int16_t h
        # 15 par_p10 uint8_t B
        # 16 unused uint8_t B

        # 17 unused uint8_t B
        # 18 unused uint8_t B
        # 19 unused uint8_t B
        # 20 par_h3 int8_t b
        # 21 par_h4 int8_t b
        # 22 par_h5 int8_t b
        # 23 par_h6 uint8_t B
        # 24 par_h7 int8_t b
        # 25 par_t1 uint16_t H
        # 26 par_g2 int16_t h
        # 27 par_g1 int8_t b
        # 28 par_g3 int8_t b

        coeff = self._read(_BME68X_REG_COEFF_ADDR1, 24)
        coeff += self._read(_BME68X_REG_COEFF_ADDR2, 14)
        coeff = struct.unpack("<hbBHhbBhhbbBBhhBBBBBbbbBbHhbb", coeff)

        par_h2 = (coeff[17] << 4) | (coeff[18] >> 4)
        par_h1 = (coeff[19] << 4) | (coeff[18] & 0x0F)
        heat_range = (self._read_byte(0x02) & 0x30) / 16
        heat_val = self._read_byte(0x00)
        sw_err = (self._read_byte(0x04) & 0xF0) / 16
        self._calibration = BME68xCalculationData(
            par_h1=par_h1,
            par_h2=par_h2,
            par_h3=coeff[20],
            par_h4=coeff[21],
            par_h5=coeff[22],
            par_h6=coeff[23],
            par_h7=coeff[24],
            par_g1=coeff[27],
            par_g2=coeff[26],
            par_g3=coeff[28],
            par_t1=coeff[25],
            par_t2=coeff[0],
            par_t3=coeff[1],
            par_p1=coeff[3],
            par_p2=coeff[4],
            par_p3=coeff[5],
            par_p4=coeff[7],
            par_p5=coeff[8],
            par_p6=coeff[10],
            par_p7=coeff[9],
            par_p8=coeff[13],
            par_p9=coeff[14],
            par_p10=coeff[15],
            t_fine=0,  # unused
            res_heat_range=heat_range,
            res_heat_val=heat_val,
            range_sw_err=sw_err,
        )

    def _read_byte(self, register: int) -> int:
        """Read a byte register value and return it"""
        return self._read(register, 1)[0]

    def _read(self, register: int, length: int) -> bytearray:
        raise NotImplementedError()

    def _write(self, register: int, values: bytearray) -> None:
        raise NotImplementedError()

    def set_gas_heater(self, heater_temp: int, heater_time: int) -> bool:
        """
        *  @brief  Enable and configure gas reading + heater
        *  @param  heater_temp
        *          Desired temperature in degrees Centigrade
        *  @param  heater_time
        *          Time to keep heater on in milliseconds
        *  @return True on success, False on failure
        """
        if (heater_temp == 0) or (heater_time == 0):
            return False
        # enable = BME68X_ENABLE
        try:
            self._set_heatr_conf(heater_temp, heater_time)
        except Exception:
            return False
        return True

    def _set_heatr_conf(self, heater_temp: int, heater_time: int) -> None:
        # restrict to BME68X_FORCED_MODE
        op_mode: int = _BME68X_FORCED_MODE
        # restrict to enable = True
        enable: bool = True
        nb_conv: int = 0
        hctrl: int = _BME68X_ENABLE_HEATER
        run_gas: int = 0
        ctrl_gas_data_0: int = 0
        ctrl_gas_data_1: int = 0
        ctrl_gas_addr_0: int = _BME68X_REG_CTRL_GAS_0
        ctrl_gas_addr_1: int = _BME68X_REG_CTRL_GAS_1
        try:
            self.set_op_mode(_BME68X_SLEEP_MODE)
            self._set_conf(heater_temp, heater_time, op_mode)
            ctrl_gas_data_0 = self._read_byte(ctrl_gas_addr_0)
            ctrl_gas_data_1 = self._read_byte(ctrl_gas_addr_1)
            if enable:
                hctrl = _BME68X_ENABLE_HEATER
                if self._variant_id == _BME68X_VARIANT_GAS_HIGH:
                    run_gas = _BME68X_ENABLE_GAS_MEAS_H
                else:
                    run_gas = _BME68X_ENABLE_GAS_MEAS_L
            else:
                hctrl = _BME68X_DISABLE_HEATER
                run_gas = _BME68X_DISABLE_GAS_MEAS

            ctrl_gas_data_0 = self.bme_set_bits(
                ctrl_gas_data_0, _BME68X_HCTRL_MSK, _BME68X_HCTRL_POS, hctrl
            )
            ctrl_gas_data_1 = self.bme_set_bits_pos_0(ctrl_gas_data_1, _BME68X_NBCONV_MSK, nb_conv)
            ctrl_gas_data_1 = self.bme_set_bits(
                ctrl_gas_data_1, _BME68X_RUN_GAS_MSK, _BME68X_RUN_GAS_POS, run_gas
            )
            self._write(ctrl_gas_addr_0, [ctrl_gas_data_0])
            self._write(ctrl_gas_addr_1, [ctrl_gas_data_1])
            # HELP check this
            self.set_op_mode(_BME68X_FORCED_MODE)
        except Exception as exc:
            self.set_op_mode(_BME68X_FORCED_MODE)
            raise exc

    def _set_conf(self, heater_temp: int, heater_time: int, op_mode: int) -> None:
        """
        This internal API is used to set heater configurations
        """
        try:
            if op_mode != _BME68X_FORCED_MODE:
                raise Exception("_set_conf not forced mode")
            rh_reg_addr: int = _BME68X_REG_RES_HEAT_0
            rh_reg_data: int = self._calc_res_heat(heater_temp)
            gw_reg_addr: int = _BME68X_REG_GAS_WAIT_0
            gw_reg_data: int = self._calc_gas_wait(heater_time)
            self._write(rh_reg_addr, [rh_reg_data])
            self._write(gw_reg_addr, [gw_reg_data])
        except Exception as exc:
            raise exc

    def _calc_res_heat(self, temp: int) -> int:
        """
        This internal API is used to calculate the heater resistance value using float
        """
        gh1: int = self._calibration.par_g1
        gh2: int = self._calibration.par_g2
        gh3: int = self._calibration.par_g3
        htr: int = self._calibration.res_heat_range
        htv: int = self._calibration.res_heat_val
        amb: int = self._amb_temp

        temp = min(temp, 400)  # Cap temperature

        var1: int = ((int(amb) * gh3) / 10) * 256
        var2: int = (gh1 + 784) * (((((gh2 + 154009) * temp * 5) / 100) + 3276800) / 10)
        var3: int = var1 + (var2 / 2)
        var4: int = var3 / (htr + 4)
        var5: int = (131 * htv) + 65536
        heatr_res_x100: int = int(((var4 / var5) - 250) * 34)
        heatr_res: int = int((heatr_res_x100 + 50) / 100)

        return heatr_res

    def _calc_res_heat(self, temp: int) -> int:
        """
        This internal API is used to calculate the heater resistance value
        """
        gh1: float = float(self._calibration.par_g1)
        gh2: float = float(self._calibration.par_g2)
        gh3: float = float(self._calibration.par_g3)
        htr: float = float(self._calibration.res_heat_range)
        htv: float = float(self._calibration.res_heat_val)
        amb: float = float(self._amb_temp)

        temp = min(temp, 400)  # Cap temperature

        var1: float = (gh1 / (16.0)) + 49.0
        var2: float = ((gh2 / (32768.0)) * (0.0005)) + 0.00235
        var3: float = gh3 / (1024.0)
        var4: float = var1 * (1.0 + (var2 * float(temp)))
        var5: float = var4 + (var3 * amb)
        res_heat: int = int(3.4 * ((var5 * (4 / (4 + htr)) * (1 / (1 + (htv * 0.002)))) - 25))
        return res_heat

    def _calc_gas_wait(self, dur: int) -> int:
        """
        This internal API is used to calculate the gas wait
        """
        factor: int = 0
        durval: int = 0xFF  # Max duration

        if dur >= 0xFC0:
            return durval
        while dur > 0x3F:
            dur = dur / 4
            factor += 1
        durval = int(dur + (factor * 64))
        return durval

    @staticmethod
    def _read24(arr) -> float:
        """Parse an unsigned 24-bit value as a floating point and return it."""
        ret = 0.0
        # print([hex(i) for i in arr])
        for b in arr:
            ret *= 256.0
            ret += float(b & 0xFF)
        return ret

    @staticmethod
    def bme_set_bits(reg_data, bitname_msk, bitname_pos, data):
        """
        Macro to set bits
        data2 = data << bitname_pos
        set masked bits from data2 in reg_data
        """
        return (reg_data & ~bitname_msk) | ((data << bitname_pos) & bitname_msk)

    @staticmethod
    def bme_set_bits_pos_0(reg_data, bitname_msk, data):
        """
        Macro to set bits starting from position 0
        set masked bits from data in reg_data
        """
        return (reg_data & ~bitname_msk) | (data & bitname_msk)


class BME68X_I2C(BME68X):
    def __init__(self, i2c, address=0x77, debug=False, *, refresh_rate=10):
        self._i2c = i2c
        self._address = address
        self._debug = debug
        super().__init__(refresh_rate=refresh_rate)

    def _read(self, register, length):
        result = bytearray(length)
        self._i2c.readfrom_mem_into(self._address, register & 0xFF, result)
        if self._debug:
            print("\t${:x} read ".format(register), " ".join(["{:02x}".format(i) for i in result]))
        return result

    def _write(self, register, values):
        if self._debug:
            print("\t${:x} write".format(register), " ".join(["{:02x}".format(i) for i in values]))
        for value in values:
            self._i2c.writeto_mem(self._address, register, bytearray([value & 0xFF]))
            register += 1
