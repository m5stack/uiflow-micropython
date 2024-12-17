# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C, Pin
import time
import struct


class SEN55:
    SEN55_I2C_ADDR = 0x69

    _SEN55_START_MEASUREMENT = 0x0021
    _SEN55_START_MEASUREMENT_RHT_GAS_ONLY = 0x0037
    _SEN55_STOP_MEASUREMENT = 0x0104
    _SEN55_READ_DATA_READY_FLAG = 0x0202
    _SEN55_READ_MEASURED_VALUES = 0x03C4
    _SEN55_TEMP_COMPENSATION_PARAMS = 0x60B2
    _SEN55_WARM_START_PARAMS = 0x60C6
    _SEN55_VOC_ALGORITHM_TUNING_PARAMS = 0x60D0
    _SEN55_NOX_ALGORITHM_TUNING_PARAMS = 0x60E1
    _SEN55_RHT_ACCELERATION_MODE = 0x60F7
    _SEN55_VOC_ALGORITHM_STATE = 0x6181
    _SEN55_START_FAN_CLEANING = 0x5607
    _SEN55_AUTO_CLEANING_INTERVAL = 0x8004
    _SEN55_READ_PRODUCT_NAME = 0xD014
    _SEN55_READ_SERIAL_NUMBER = 0xD033
    _SEN55_READ_FIRMWARE_VERSION = 0xD100
    _SEN55_READ_DEVICE_STATUS = 0xD206
    _SEN55_CLEAR_DEVICE_STATUS = 0xD210
    _SEN55_RESET = 0xD304

    """
    note:
        en: SEN55 is a sensor unit designed to measure various environmental parameters such as particulate matter (PM1.0, PM2.5, PM4.0, PM10.0), CO2, temperature, humidity, VOC (volatile organic compounds), and NOx (nitrogen oxides). It communicates via I2C and supports advanced functions such as tuning algorithms, cleaning the fan, and adjusting measurement modes.

    details:
        link: https://docs.m5stack.com/en/unit/sen55
        image: https://static-cdn.m5stack.com/resource/docs/products/unit/sen55/sen55_01.webp
        category: Unit

    example:
        - ../../../examples/unit/sen55/sen55_cores3_example.py

    m5f2:
        - unit/sen55/sen55_cores3_example.m5f2
    """

    def __init__(self, i2c: I2C, address: int = SEN55_I2C_ADDR) -> None:
        """
        note:
            en: Initialize the SEN55 sensor with I2C communication, setting the power control and ensuring the sensor is connected.

        params:
            i2c:
                note: The I2C object used for communication with the sensor.
            address:
                note: The I2C address of the sensor, default is 0x69.
        """
        self.i2c = i2c
        self.unit_addr = address
        self.power_ctr = Pin(10, Pin.OUT)
        self.set_power_state(True)
        time.sleep_ms(100)
        self.available()
        self.co2 = 0
        self.temperature = 0
        self.humidity = 0

    def set_power_state(self, state: bool) -> None:
        """
        note:
            en: Set the power state of the SEN55 sensor.

        params:
            state:
                note: The desired power state, True to power on, False to power off.
        """
        self.power_ctr(not state)
        time.sleep_ms(100)

    def get_power_state(self) -> bool:
        """
        note:
            en: Get the current power state of the SEN55 sensor.

        params:
            note:

        returns:
            note: Returns True if the sensor is powered on, False if powered off.
        """
        return self.power_ctr() == 0

    def available(self) -> None:
        """
        note:
            en: Check if the SEN55 sensor is connected via I2C.

        params:
            note:

        raises:
            Exception: If the sensor is not found on the I2C bus.
        """
        if self.unit_addr not in self.i2c.scan():
            raise Exception("SEN55 maybe not connect")

    def set_work_mode(self, mode: int) -> None:
        """
        note:
            en: Set the measurement mode of the SEN55 sensor.

        params:
            mode:
                note: 1 to start measurement, 0 to stop measurement.
        """
        cmd = self._SEN55_START_MEASUREMENT if mode == 1 else self._SEN55_STOP_MEASUREMENT
        self.send_cmd(cmd)
        time.sleep_ms(200)

    def get_sensor_data(self) -> None:
        """
        note:
            en: Get the sensor data including PM1.0, PM2.5, PM4.0, PM10.0, CO2, temperature, humidity, VOC, and NOx.

        params:
            note:

        details:
            en: This method sends a command to the sensor, waits for a response, and unpacks the measured values into their respective attributes.
        """
        self.send_cmd(self._SEN55_READ_MEASURED_VALUES)
        time.sleep_ms(20)
        buf = self.read_response(24)
        scale_factors = (1.0, 1.0, 1.0, 1.0, 100.0, 200.0, 10.0, 5.0)
        (
            self.pm1_0,
            self.pm2_5,
            self.pm4_0,
            self.pm10_0,
            self.humidity,
            self.temperature,
            self.voc,
            self.nox,
        ) = (
            raw / scale for raw, scale in zip(struct.unpack_from(">HHHHHHHH", buf), scale_factors)
        )

    def get_data_ready_flag(self) -> bool:
        """
        note:
            en: Check if the sensor data is ready to be read.

        params:
            note:

        returns:
            note: Returns True if the data is ready, False otherwise.
        """
        self.send_cmd(self._SEN55_READ_DATA_READY_FLAG)
        time.sleep_ms(20)
        if self.read_response(3)[1] == 0x01:
            time.sleep_ms(200)
            self.get_sensor_data()
            return True
        return False

    def set_temp_cmp_params(
        self, temp_offset: int, temp_offset_slope: int, time_constant: int
    ) -> None:
        """
        note:
            en: Set the temperature compensation parameters for the sensor.

        params:
            temp_offset:
                note: The temperature offset in the sensor's compensation algorithm.
            temp_offset_slope:
                note: The temperature offset slope in the sensor's compensation algorithm.
            time_constant:
                note: The time constant for the temperature compensation.
        """
        self.send_cmd(
            self._SEN55_TEMP_COMPENSATION_PARAMS,
            [temp_offset * 200, temp_offset_slope * 10000, time_constant],
        )

    def get_temp_cmp_params(self) -> tuple:
        """
        note:
            en: Get the current temperature compensation parameters.

        params:
            note:

        returns:
            note: A tuple containing the temperature offset, offset slope, and time constant.
        """
        self.send_cmd(self._SEN55_TEMP_COMPENSATION_PARAMS)
        buf = self.read_response(9)
        scale_factors = (200, 10000, 1)
        self.temp_offset, self.temp_offset_slope, self.time_constant = (
            raw / scale for raw, scale in zip(struct.unpack_from(">hhh", buf), scale_factors)
        )
        return self.temp_offset, self.temp_offset_slope, self.time_constant

    def set_warm_start_param(self, mode: bool) -> None:
        """
        note:
            en: Set the warm start parameter for the sensor.

        params:
            mode:
                note: True to enable warm start, False to disable it.
        """
        self.send_cmd(self._SEN55_WARM_START_PARAMS, [mode])

    def get_warm_start_param(self) -> bool:
        """
        note:
            en: Get the current warm start parameter.

        params:
            note:

        returns:
            note: True if warm start is enabled, False if disabled.
        """
        self.send_cmd(self._SEN55_WARM_START_PARAMS)
        return self.read_response(3)[1] == 0x01

    def set_voc_algo_tuning_params(
        self,
        voc_index_offset: int = 100,
        voc_offset_hours: int = 12,
        voc_gain_houes: int = 12,
        gate_max_duration_min: int = 180,
        std_initial: int = 50,
        gain_factor: int = 230,
    ) -> None:
        """
        note:
            en: Set the VOC algorithm tuning parameters, including index offset, time offsets, and gain factors.

        params:
            voc_index_offset:
                note: The VOC index offset, default is 100.
            voc_offset_hours:
                note: The VOC offset in hours, default is 12 hours.
            voc_gain_houes:
                note: The VOC gain in hours, default is 12 hours.
            gate_max_duration_min:
                note: Maximum gate duration in minutes, default is 180 minutes.
            std_initial:
                note: The initial standard deviation, default is 50.
            gain_factor:
                note: The gain factor for VOC, default is 230.
        """
        self.send_cmd(
            self._SEN55_VOC_ALGORITHM_TUNING_PARAMS,
            [
                voc_index_offset,
                voc_offset_hours,
                voc_gain_houes,
                gate_max_duration_min,
                std_initial,
                gain_factor,
            ],
        )

    def get_voc_algo_tuning_params(self) -> tuple:
        """
        note:
            en: Get the current VOC algorithm tuning parameters.

        params:
            note:

        return:
            note: A tuple of VOC tuning parameters: index offset, offset hours, gain hours, max gate duration, initial standard deviation, and gain factor.
        """
        self.send_cmd(self._SEN55_VOC_ALGORITHM_TUNING_PARAMS)
        time.sleep_ms(20)
        buf = self.read_response(18)
        (
            self.voc_index_offset,
            self.voc_offset_hours,
            self.voc_gain_houes,
            self.gate_max_duration_min,
            self.std_initial,
            self.gain_factor,
        ) = struct.unpack_from(">hhhhhh", buf)
        return (
            self.voc_index_offset,
            self.voc_offset_hours,
            self.voc_gain_houes,
            self.gate_max_duration_min,
            self.std_initial,
            self.gain_factor,
        )

    def set_nox_algo_tuning_params(
        self,
        nox_index_offset: int = 1,
        nox_offset_hours: int = 12,
        nox_gain_houes: int = 12,
        gate_max_duration_min: int = 720,
        gain_factor: int = 230,
    ) -> None:
        """
        note:
            en: Set the NOx algorithm tuning parameters, including index offset, time offsets, and gain factors. The standard deviation estimate is fixed at 50 for NOx.

        params:
            nox_index_offset:
                note: The offset value for the NOx index.
            nox_offset_hours:
                note: The time offset in hours for the NOx algorithm.
            nox_gain_houes:
                note: The gain factor in hours for the NOx algorithm.
            gate_max_duration_min:
                note: The maximum gate duration in minutes.
            gain_factor:
                note: The gain factor for the NOx algorithm.
        """
        self.send_cmd(
            self._SEN55_NOX_ALGORITHM_TUNING_PARAMS,
            [
                nox_index_offset,
                nox_offset_hours,
                nox_gain_houes,
                gate_max_duration_min,
                50,
                gain_factor,
            ],
        )

    def get_nox_algo_tuning_params(self) -> tuple:
        """
        note:
            en: Get the current NOx algorithm tuning parameters.

        params:
            note:

        return:
            note: A tuple of NOx tuning parameters: index offset, offset hours, gain hours, max gate duration, and gain factor.
        """
        self.send_cmd(self._SEN55_NOX_ALGORITHM_TUNING_PARAMS)
        time.sleep_ms(20)
        buf = self.read_response(18)
        (
            self.nox_index_offset,
            self.nox_offset_hours,
            self.nox_gain_houes,
            self.gate_max_duration_min,
            _,
            self.gain_factor,
        ) = struct.unpack_from(">hhhhhh", buf)
        return (
            self.nox_index_offset,
            self.nox_offset_hours,
            self.nox_gain_houes,
            self.gate_max_duration_min,
            self.gain_factor,
        )

    def set_rht_acceleration_mode(self, mode: int) -> None:
        """
        note:
            en: Set the RHT acceleration mode, which affects how quickly the device accelerates during measurement.

        params:
            mode:
                note: The acceleration mode to set: 0 for low, 1 for high, or 2 for medium.
        """
        self.send_cmd(self._SEN55_RHT_ACCELERATION_MODE, [mode])

    def get_rht_acceleration_mode(self) -> int:
        """
        note:
            en: Get the current RHT acceleration mode. This parameter can be changed in any state of the device, but it is applied only the next time starting a measurement. The parameter needs to be set before a new measurement is started.

        params:
            note:

        return:
            note: The current acceleration mode: 0 for low, 1 for high, or 2 for medium.
        """
        self.send_cmd(self._SEN55_RHT_ACCELERATION_MODE)
        return self.read_response(3)[1]

    def get_voc_algo_state(self) -> bytes:
        """
        note:
            en: Get the current VOC algorithm state.

        params:
            note:

        return:
            note: The VOC algorithm state in bytes.
        """
        self.send_cmd(self._SEN55_VOC_ALGORITHM_STATE)
        return self.read_response(12)

    def set_voc_algo_state(self, state: bytes) -> None:
        """
        note:
            en: Set the VOC algorithm state.

        params:
            state:
                note: The VOC algorithm state to set, represented as bytes.
        """
        self.send_cmd(self._SEN55_VOC_ALGORITHM_STATE, state, True)

    def set_start_fan_cleaning(self) -> None:
        """
        note:
            en: Start the fan cleaning process to remove contaminants from the sensor.

        params:
            note:
        """
        self.send_cmd(self._SEN55_START_FAN_CLEANING)

    def get_auto_cleaning_interval(self) -> tuple:
        """
        note:
            en: Get the current auto cleaning interval.

        params:
            note:

        return:
            note: A tuple of the cleaning interval parameters.
        """
        self.send_cmd(self._SEN55_AUTO_CLEANING_INTERVAL)
        return struct.unpack_from(">hh", self.read_response(6))

    def set_auto_cleaning_interval(self, interval: tuple) -> None:
        """
        note:
            en: Set the auto cleaning interval.

        params:
            interval:
                note: A tuple representing the new auto cleaning interval.
        """
        self.send_cmd(self._SEN55_AUTO_CLEANING_INTERVAL, interval)

    def get_device_status(self) -> bytes:
        """
        note:
            en: Get the current device status.

        params:
            note:

        return:
            note: The device status in bytes.
        """
        self.send_cmd(self._SEN55_READ_DEVICE_STATUS)
        return self.read_response(6)

    def clear_device_status(self) -> None:
        """
        note:
            en: Clear the device status, resetting any error flags or states.

        params:
            note:
        """
        self.send_cmd(self._SEN55_CLEAR_DEVICE_STATUS)

    def get_serial_number(self) -> str:
        """
        note:
            en: Get the unique serial number of the sensor.

        params:
            note:

        return:
            note: The serial number of the sensor as a string.
        """
        self.send_cmd(self._SEN55_READ_SERIAL_NUMBER)
        time.sleep_ms(1)
        buf = self.read_response(48)
        return buf.split(b"\x00", 1)[0].decode()

    def get_product_name(self) -> str:
        """
        note:
            en: Get the product name of the sensor.

        params:
            note:

        return:
            note: The product name of the sensor as a string.
        """
        self.send_cmd(self._SEN55_READ_PRODUCT_NAME)
        time.sleep_ms(1)
        buf = self.read_response(48)
        return buf.split(b"\x00", 1)[0].decode()

    def send_cmd(self, cmd: int, value=None, is_bytes: bool = False) -> None:
        """
        note:
            en: Send a command to the sensor.

        params:
            cmd:
                note: The command to send, represented as a 2-byte value.
            value:
                note: Optional value to include with the command.
            is_bytes:
                note: A flag to indicate if the value is in bytes format.
        """
        packed_value = bytearray(struct.pack(">h", cmd))
        if value is not None:
            if not is_bytes:
                for param in value:
                    packed_param = struct.pack(">h", param)
                    packed_value.extend(packed_param)
                    packed_value.extend(bytes([self.crc8(packed_param)]))
            else:
                for i in range(0, len(value), 2):
                    packed_value.extend(value[i : i + 2])
                    packed_value.extend(bytes([self.crc8(value[i : i + 2])]))
        self.i2c.writeto(self.unit_addr, packed_value)

    def read_response(self, nbytes: int) -> bytes:
        """
        note:
            en: Read the response from the sensor.

        params:
            nbytes:
                note: The number of bytes to read from the sensor.

        return:
            note: The response data as bytes.
        """
        buff = self.i2c.readfrom(self.unit_addr, nbytes)
        return self.check_crc(buff)

    def check_crc(self, buf: bytes) -> bytes:
        """
        note:
            en: Check the CRC of the sensor data to ensure its validity.

        params:
            buf:
                note: The buffer containing sensor data.

        return:
            note: The valid data after CRC check.
        """
        valid_data = bytearray()
        for i in range(0, len(buf), 3):
            data_bytes, crc_byte = buf[i : i + 2], buf[i + 2]
            if self.crc8(data_bytes) == crc_byte:
                valid_data.extend(data_bytes)
            else:
                raise RuntimeError("CRC check failed while reading data")
        return valid_data

    def crc8(self, buffer: bytes) -> int:
        """
        note:
            en: Calculate the CRC-8 checksum for the given buffer.

        params:
            buffer:
                note: The buffer to calculate the checksum for.

        return:
            note: The 8-bit CRC checksum.
        """
        crc = 0xFF
        for byte in buffer:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0x31
                else:
                    crc = crc << 1
        return crc & 0xFF  # return the bottom 8 bits

    def get_pm1_0(self) -> float:
        """
        note:
            en: Get the PM1.0 concentration value in micrograms per cubic meter (µg/m³).

        params:
            note:

        returns:
            float: PM1.0 concentration in µg/m³.
        """
        return self.pm1_0

    def get_pm2_5(self) -> float:
        """
        note:
            en: Get the PM2.5 concentration value in micrograms per cubic meter (µg/m³).

        params:
            note:

        returns:
            float: PM2.5 concentration in µg/m³.
        """
        return self.pm2_5

    def get_pm4_0(self) -> float:
        """
        note:
            en: Get the PM4.0 concentration value in micrograms per cubic meter (µg/m³).

        params:
            note:

        returns:
            float: PM4.0 concentration in µg/m³.
        """
        return self.pm4_0

    def get_pm10_0(self) -> float:
        """
        note:
            en: Get the PM10.0 concentration value in micrograms per cubic meter (µg/m³).

        params:
            note:

        returns:
            float: PM10.0 concentration in µg/m³.
        """
        return self.pm10_0

    def get_humidity(self) -> float:
        """
        note:
            en: Get the humidity value in percentage (%).

        params:
            note:

        returns:
            float: Humidity in percentage.
        """
        return self.humidity

    def get_temperature(self) -> float:
        """
        note:
            en: Get the temperature value in degrees Celsius (°C).

        params:
            note:

        returns:
            float: Temperature in °C.
        """
        return self.temperature

    def get_voc(self) -> float:
        """
        note:
            en: Get the Volatile Organic Compound (VOC) concentration value in parts per billion (ppb).

        params:
            note:

        returns:
            float: VOC concentration in ppb.
        """
        return self.voc

    def get_nox(self) -> float:
        """
        note:
            en: Get the Nitrogen Oxide (NOx) concentration value in parts per billion (ppb).

        params:
            note:

        returns:
            float: NOx concentration in ppb.
        """
        return self.nox
