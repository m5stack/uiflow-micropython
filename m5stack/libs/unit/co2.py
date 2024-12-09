# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
from .pahub import PAHUBUnit
from micropython import const
from driver.scd40 import SCD40


CO2_I2C_ADDR = const(0x62)

REINIT = const(0x3646)
FACTORYRESET = const(0x3632)
FORCEDRECAL = const(0x362F)
SELFTEST = const(0x3639)
DATAREADY = const(0xE4B8)
STARTPERIODICMEASUREMENT = const(0x21B1)
STOPPERIODICMEASUREMENT = const(0x3F86)
STARTLOWPOWERPERIODICMEASUREMENT = const(0x21AC)
READMEASUREMENT = const(0xEC05)
SERIALNUMBER = const(0x3682)
GETTEMPOFFSET = const(0x2318)
SETTEMPOFFSET = const(0x241D)
GETALTITUDE = const(0x2322)
SETALTITUDE = const(0x2427)
SETPRESSURE = const(0xE000)
PERSISTSETTINGS = const(0x3615)
GETASCE = const(0x2313)
SETASCE = const(0x2416)
SINGLESHOTMEASUREALL = const(0x219D)
SINGLESHOTMEASUREHT = const(0x2196)
POWERDOWN = const(0x36E0)
WAKEUP = const(0x36F6)


class CO2Unit:
    """
    note:
        en: CO2Unit is a hardware module designed for measuring CO2 concentration, temperature, and humidity.
        It communicates via I2C and provides functions for calibration, measurement, and configuration.

    details:
        link: https://docs.m5stack.com/en/unit/co2unit
        image: https://static-cdn.m5stack.com/resource/docs/products/unit/co2unit/co2unit_01.webp
        category: Unit

    example:
        - ../../../examples/unit/co2unit/co2unit_cores3_example.py

    m5f2:
        - unit/co2unit/co2unit_cores3_example.m5f2
    """

    def __init__(self, i2c: I2C | PAHUBUnit, address: int = CO2_I2C_ADDR) -> None:
        """
        note:
            en: Initialize the CO2Unit with the I2C interface and address.

        params:
            i2c:
                note: I2C interface or PAHUBUnit instance for communication.
            address:
                note: I2C address of the CO2 sensor, default is 0x62.
        """
        self.co2_i2c = i2c
        self.unit_addr = address
        self.available()
        self.co2 = 0
        self.temperature = 0
        self.humidity = 0

    def available(self) -> None:
        """
        note:
            en: Check if the CO2 unit is available on the I2C bus.

        params:
            note:
        """
        if self.unit_addr not in self.co2_i2c.scan():
            raise UnitError("CO2 unit may not be connected")

    def set_start_periodic_measurement(self) -> None:
        """
        note:
            en: Set the sensor into working mode, which takes about 5 seconds per measurement.

        params:
            note:
        """
        try:
            self.write_cmd(STARTPERIODICMEASUREMENT)
            time.sleep_ms(1)
        except:
            raise OSError(
                "Indicates that the block cannot be executed while a periodic measurement is running"
            )

    def set_stop_periodic_measurement(self) -> None:
        """
        note:
            en: Stop the measurement mode for the sensor.

        params:
            note:
        """
        self.write_cmd(STOPPERIODICMEASUREMENT)
        time.sleep(0.5)

    def get_sensor_measurement(self) -> None:
        """
        note:
            en: Get temperature, humidity, and CO2 concentration from the sensor.

        params:
            note:
        """
        self.write_cmd(READMEASUREMENT)
        time.sleep_ms(1)
        buf = self.read_response(9)
        self.co2 = (buf[0] << 8) | buf[1]
        temp = (buf[3] << 8) | buf[1]
        self.temperature = round((-45 + 175 * (temp / (2**16 - 1))), 2)
        humi = (buf[6] << 8) | buf[7]
        self.humidity = round((100 * (humi / (2**16 - 1))), 2)

    def is_data_ready(self) -> bool:
        """
        note:
            en: Check if the data (temperature, humidity, CO2) is ready from the sensor.

        params:
            note:

        returns:
            note: True if data is ready, otherwise False.
        """
        if self.data_isready():
            self.get_sensor_measurement()
            return True
        else:
            return False

    def get_temperature_offset(self) -> float:
        """
        note:
            en: Get the temperature offset to be added to the reported measurements.

        params:
            note:

        returns:
            note: The temperature offset in degrees Celsius.
        """
        try:
            self.write_cmd(GETTEMPOFFSET)
            buf = self.read_response(3)
            temp = (buf[0] << 8) | buf[1]
            time.sleep_ms(1)
            return 175.0 * temp / 2**16
        except:
            raise OSError(
                "Indicates that the block cannot be executed while a periodic measurement is running"
            )

    def set_temperature_offset(self, offset: int = 0) -> None:
        """
        note:
            en: Set the maximum value of 374°C temperature offset.

        params:
            offset:
                note: The temperature offset to set, default is 0.
        """
        try:
            offset = min(374, offset)
            temp = int(offset * (2**16 / 175))
            self.write_cmd(SETTEMPOFFSET, temp)
            time.sleep_ms(1)
        except:
            raise OSError(
                "Indicates that the block cannot be executed while a periodic measurement is running"
            )

    def get_sensor_altitude(self) -> int:
        """
        note:
            en: Get the altitude value of the measurement location in meters above sea level.

        params:
            note:

        returns:
            note: The altitude value in meters.
        """
        try:
            self.write_cmd(GETALTITUDE)
            time.sleep_ms(1)
            buf = self.read_response(3)
            return (buf[0] << 8) | buf[1]
        except:
            raise OSError(
                "Indicates that the block cannot be executed while a periodic measurement is running"
            )

    def set_sensor_altitude(self, height: int) -> None:
        """
        note:
            en: Set the altitude value of the measurement location in meters above sea level.

        params:
            height:
                note: The altitude in meters to set. Must be between 0 and 65535 meters.
        """
        try:
            height = min(65535, max(height, 0))
            self.write_cmd(SETALTITUDE, int(height))
            time.sleep_ms(1)
        except:
            raise OSError(
                "Indicates that the block cannot be executed while a periodic measurement is running"
            )

    def set_ambient_pressure(self, ambient_pressure: int) -> None:
        """
        note:
            en: Set the ambient pressure in hPa at any time to adjust CO2 calculations.

        params:
            ambient_pressure:
                note: The ambient pressure in hPa, constrained to the range [0, 65535].
        """
        ambient_pressure = min(65535, max(ambient_pressure, 0))
        self.write_cmd(SETPRESSURE, int(ambient_pressure))
        time.sleep_ms(1)

    def set_force_calibration(self, target_co2: int) -> None:
        """
        note:
            en: Force the sensor to recalibrate with a given current CO2 level.

        params:
            target_co2:
                note: The current CO2 concentration to be used for recalibration.
        """
        try:
            self.set_stop_periodic_measurement()
            self.write_cmd(FORCEDRECAL, int(target_co2))
            time.sleep(0.5)
            buf = self.read_response(3)
            correction = struct.unpack_from(">h", buf[0:2])[0]
            if correction == 0xFFFF:
                raise RuntimeError(
                    "Forced recalibration failed. Make sure sensor is active for 3 minutes first"
                )
        except:
            raise OSError(
                "Indicates that the block cannot be executed while a periodic measurement is running"
            )

    def get_calibration_enabled(self) -> bool:
        """
        note:
            en: Get whether automatic self-calibration (ASC) is enabled or disabled.

        params:
            note:

        returns:
            note: True if ASC is enabled, otherwise False.
        """
        try:
            self.write_cmd(GETASCE)
            time.sleep_ms(1)
            buf = self.read_response(3)
            return buf[1] == 1
        except:
            raise OSError(
                "Indicates that the block cannot be executed while a periodic measurement is running"
            )

    def set_calibration_enabled(self, enabled: bool) -> None:
        """
        note:
            en: Enable or disable automatic self-calibration (ASC).

        params:
            enabled:
                note: Set to True to enable ASC, or False to disable it.
        """
        try:
            enabled = min(1, max(enabled, 0))
            self.write_cmd(SETASCE, enabled)
            time.sleep_ms(1)
        except:
            raise OSError(
                "Indicates that the block cannot be executed while a periodic measurement is running"
            )

    def set_start_low_periodic_measurement(self) -> None:
        """
        note:
            en: Set the sensor into low power working mode, with about 30 seconds per measurement.

        params:
            note:
        """
        try:
            self.write_cmd(STARTLOWPOWERPERIODICMEASUREMENT)
        except:
            raise OSError(
                "Indicates that the block cannot be executed while a periodic measurement is running"
            )

    def data_isready(self) -> bool:
        """
        note:
            en: Check if new data is available from the sensor.

        params:
            note:

        returns:
            note: True if new data is available, otherwise False.
        """
        try:
            self.write_cmd(DATAREADY)
            time.sleep_ms(1)
            buf = self.read_response(3)
            return not ((buf[0] & 0x07 == 0) and (buf[1] == 0))
        except:
            raise OSError(
                "Indicates that the block cannot be executed while a periodic measurement is running"
            )

    def save_to_eeprom(self) -> None:
        """
        note:
            en: Save temperature offset, altitude offset, and self-calibration enable settings to EEPROM.

        params:
            note:
        """
        try:
            self.write_cmd(PERSISTSETTINGS)
            time.sleep(0.8)
        except:
            raise OSError(
                "Indicates that the block cannot be executed while a periodic measurement is running"
            )

    def get_serial_number(self) -> tuple:
        """
        note:
            en: Get a unique serial number for this sensor.

        params:
            note:

        returns:
            note: A tuple representing the unique serial number of the sensor.
        """
        try:
            self.write_cmd(SERIALNUMBER)
            time.sleep_ms(1)
            buf = self.read_response(9)
            return (buf[0], buf[1], buf[3], buf[4], buf[6], buf[7])
        except:
            raise OSError(
                "Indicates that the block cannot be executed while a periodic measurement is running"
            )

    def set_self_test(self) -> None:
        """
        note:
            en: Perform a self-test, which can take up to 10 seconds.

        params:
            note:
        """
        try:
            self.set_stop_periodic_measurement()
            self.write_cmd(SELFTEST)
            time.sleep(10)
            buf = self.read_response(3)
            if (buf[0] != 0) or (buf[1] != 0):
                raise RuntimeError("Self test failed")
        except:
            raise OSError(
                "Indicates that the block cannot be executed while a periodic measurement is running"
            )

    def set_factory_reset(self) -> None:
        """
        note:
            en: Reset all configuration settings stored in the EEPROM and erase the FRC and ASC algorithm history.

        params:
            note:
        """
        try:
            self.set_stop_periodic_measurement()
            self.write_cmd(FACTORYRESET)
            time.sleep(1.2)
        except:
            raise OSError(
                "Indicates that the block cannot be executed while a periodic measurement is running"
            )

    def reinit(self) -> None:
        """
        note:
            en: Reinitialize the sensor by reloading user settings from EEPROM.

        params:
            note:
        """
        try:
            self.set_stop_periodic_measurement()
            self.write_cmd(REINIT)
            time.sleep_ms(20)
        except:
            raise OSError(
                "Indicates that the block cannot be executed while a periodic measurement is running"
            )

    def set_single_shot_measurement_all(self) -> None:
        """
        note:
            en: Set the sensor to perform a single-shot measurement for CO2, humidity, and temperature.

        params:
            note:
        """
        try:
            self.write_cmd(SINGLESHOTMEASUREALL)
            time.sleep(5)
        except:
            raise OSError(
                "Indicates that the block cannot be executed while a periodic measurement is running"
            )

    def set_single_shot_measurement_ht(self) -> None:
        """
        note:
            en: Set the sensor to perform a single-shot measurement for humidity and temperature.

        params:
            note:
        """
        try:
            self.write_cmd(SINGLESHOTMEASUREHT)
            time.sleep_ms(50)
        except:
            raise OSError(
                "Indicates that the block cannot be executed while a periodic measurement is running"
            )

    def set_sleep_mode(self) -> None:
        """
        note:
            en: Put the sensor into sleep mode to reduce current consumption.

        params:
            note:
        """
        try:
            self.write_cmd(POWERDOWN)
            time.sleep_ms(1)
        except:
            raise OSError(
                "Indicates that the block cannot be executed while a periodic measurement is running"
            )

    def set_wake_up(self) -> None:
        """
        note:
            en: Wake up the sensor from sleep mode into idle mode.

        params:
            note:
        """
        try:
            self.write_cmd(WAKEUP)
            time.sleep_ms(20)
        except:
            raise OSError(
                "Indicates that the block cannot be executed while a periodic measurement is running"
            )

    def write_cmd(self, cmd_wr: int, value: int = None) -> None:
        """
        note:
            en: Write a command to the sensor.

        params:
            cmd_wr:
                note: The command to write to the sensor.
            value:
                note: The value to send with the command, if any.
        """
        if value is not None:
            byte_val = struct.pack(">h", value)
            crc8 = self.crc8(byte_val)
            self.co2_i2c.writeto(self.unit_addr, struct.pack(">hhb", cmd_wr, value, crc8))
        else:
            self.co2_i2c.writeto(self.unit_addr, struct.pack(">h", cmd_wr))

    def read_response(self, num: int) -> bytearray:
        """
        note:
            en: Read the sensor's response.

        params:
            num:
                note: The number of bytes to read from the sensor.

        returns:
            note: The read response as a bytearray.
        """
        buff = self.co2_i2c.readfrom(self.unit_addr, num)
        self.check_crc(buff)
        return buff

    def check_crc(self, buf: bytearray) -> bool:
        """
        note:
            en: Check the CRC of the received data to ensure it is correct.

        params:
            buf:
                note: The buffer of bytes to check the CRC.

        returns:
            note: True if the CRC check passes, otherwise raises an error.
        """
        for i in range(0, len(buf), 3):
            if self.crc8(buf[i : (i + 2)]) != buf[i + 2]:
                raise RuntimeError("CRC check failed while reading data")
        return True

    def crc8(self, buffer: bytearray) -> int:
        """
        note:
            en: Calculate the CRC-8 checksum for a given buffer.

        params:
            buffer:
                note: The buffer of bytes to calculate the CRC for.

        returns:
            note: The CRC-8 checksum as an integer.
        """
        crc = 0xFF
        for byte in buffer:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0x31
                else:
                    crc = crc << 1
        return crc & 0xFF  # Return the bottom 8 bits
