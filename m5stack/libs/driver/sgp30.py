# Copyright (c) 2017 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
I2C-based driver for the SGP30 Sensirion air[VoC] quality sensor.
"""

from math import exp
from time import sleep_ms
from micropython import const

# General SGP30 settings
SGP30_DEFAULT_I2C_ADDR = const(0x58)
SGP30_WORD_LEN = const(2)
SGP30_CRC8_POLYNOMIAL = const(0x31)
SGP30_CRC8_INIT = const(0xFF)
SGP30_CRC8_FINAL_XOR = const(0xFF)
SGP30_MEASURE_TEST_PASS = const(0xD400)

# SGP30 feature set measurement commands (Hex Codes)
# From datasheet section 6.3
SGP30_CMD_IAQ_INIT_HEX = [0x20, 0x03]
SGP30_CMD_IAQ_INIT_WORDS = const(0)
SGP30_CMD_IAQ_INIT_MAX_MS = const(10)
SGP30_CMD_MEASURE_IAQ_HEX = [0x20, 0x08]
SGP30_CMD_MEASURE_IAQ_WORDS = const(2)
SGP30_CMD_MEASURE_IAQ_MS = const(12)
SGP30_CMD_GET_IAQ_BASELINE_HEX = [0x20, 0x15]
SGP30_CMD_GET_IAQ_BASELINE_WORDS = const(2)
SGP30_CMD_GET_IAQ_BASELINE_MAX_MS = const(10)
SGP30_CMD_SET_IAQ_BASELINE_HEX = [0x20, 0x1E]
SGP30_CMD_SET_IAQ_BASELINE_WORDS = const(0)
SGP30_CMD_SET_IAQ_BASELINE_MAX_MS = const(10)
SGP30_CMD_SET_ABSOLUTE_HUMIDITY_HEX = [0x20, 0x61]
SGP30_CMD_SET_ABSOLUTE_HUMIDITY_WORDS = const(0)
SGP30_CMD_SET_ABSOLUTE_HUMIDITY_MAX_MS = const(10)
SGP30_CMD_MEASURE_TEST_HEX = [0x20, 0x32]
SGP30_CMD_MEASURE_TEST_WORDS = const(1)
SGP30_CMD_MEASURE_TEST_MAX_MS = const(220)
SGP30_CMD_GET_FEATURE_SET_HEX = [0x20, 0x2F]
SGP30_CMD_GET_FEATURE_SET_WORDS = const(1)
SGP30_CMD_GET_FEATURE_SET_MAX_MS = const(10)
SGP30_CMD_MEASURE_RAW_HEX = [0x20, 0x50]
SGP30_CMD_MEASURE_RAW_WORDS = const(2)
SGP30_CMD_MEASURE_RAW_MAX_MS = const(25)
SGP30_CMD_GET_TVOC_INCEPTIVE_HEX = [0x20, 0xB3]
SGP30_CMD_GET_TVOC_INCEPTIVE_WORDS = const(1)
SGP30_CMD_GET_TVOC_INCEPTIVE_MAX_MS = const(10)
SGP30_CMD_SET_TVOC_BASELINE_HEX = [0x20, 0x77]
SGP30_CMD_SET_TVOC_BASELINE_WORDS = const(0)
SGP30_CMD_SET_TVOC_BASELINE_MAX_MS = const(10)

# TODO: Soft Reset (datasheet section 6.4)

# Obtaining Serial ID (datasheet section 6.5)
SGP30_CMD_GET_SERIAL_ID_HEX = [0x36, 0x82]
SGP30_CMD_GET_SERIAL_ID_WORDS = const(3)
SGP30_CMD_GET_SERIAL_ID_MAX_MS = const(10)


class SGP30:
    """
    A driver for the SGP30 gas sensor.

    :param i2c: The "I2C" object to use. This is the only required parameter.
    :param int address: (optional) The I2C address of the device.
    :param boolean measure_test: (optional) Whether to run on-chip test during initialisation.
    :param boolean iaq_init: (optional) Whether to initialise SGP30 algorithm / baseline.
    """

    def __init__(self, i2c, addr=SGP30_DEFAULT_I2C_ADDR, measure_test=False, iaq_init=True):
        """Initialises the sensor and display stats"""
        self._i2c = i2c
        if addr not in self._i2c.scan():
            raise IOError("No SGP30 device found on I2C bus")
        self.addr = addr
        self.serial = self.get_serial()
        self.feature_set = self.get_feature_set()
        if measure_test:
            if SGP30_MEASURE_TEST_PASS != self.measure_test():
                raise RuntimeError("Device failed the on-chip test")
        if iaq_init:
            self.iaq_init()

    def iaq_init(self):
        """
        note:
            en: Initialize the IAQ (Indoor Air Quality) algorithm for the sensor.

        params:
            note:
        """
        self._i2c_read_words_from_cmd(
            SGP30_CMD_IAQ_INIT_HEX, SGP30_CMD_IAQ_INIT_MAX_MS, SGP30_CMD_IAQ_INIT_WORDS
        )

    def measure_iaq(self):
        """
        note:
            en: Measure the CO2 equivalent (CO2eq) and TVOC values.

        params:
            note:

        returns:
            note: A tuple containing CO2eq and TVOC values.
        """
        return self._i2c_read_words_from_cmd(
            SGP30_CMD_MEASURE_IAQ_HEX,
            SGP30_CMD_MEASURE_IAQ_MS,
            SGP30_CMD_MEASURE_IAQ_WORDS,
        )

    def get_iaq_baseline(self):
        """
        note:
            en: Retrieve the IAQ algorithm baseline values for CO2eq and TVOC.

        params:
            note:

        returns:
            note: A tuple containing baseline values for CO2eq and TVOC.
        """
        return self._i2c_read_words_from_cmd(
            SGP30_CMD_GET_IAQ_BASELINE_HEX,
            SGP30_CMD_GET_IAQ_BASELINE_MAX_MS,
            SGP30_CMD_GET_IAQ_BASELINE_WORDS,
        )

    def set_iaq_baseline(self, co2eq, tvoc):
        """
        note:
            en: Set the previously recorded IAQ algorithm baseline values for CO2eq and TVOC.

        params:
            co2eq:
                note: The CO2 equivalent baseline value.
            tvoc:
                note: The TVOC baseline value.
        """
        if co2eq == 0 and tvoc == 0:
            raise ValueError("Invalid baseline values used")
        buffer = []
        for value in [tvoc, co2eq]:
            arr = [value >> 8, value & 0xFF]
            arr.append(generate_crc(arr))
            buffer += arr
        self._i2c_read_words_from_cmd(
            SGP30_CMD_SET_IAQ_BASELINE_HEX + buffer,
            SGP30_CMD_SET_IAQ_BASELINE_MAX_MS,
            SGP30_CMD_SET_IAQ_BASELINE_WORDS,
        )

    def set_absolute_humidity(self, absolute_humidity):
        """
        note:
            en: Set the absolute humidity compensation for the sensor. To disable, set the value to 0.

        params:
            absolute_humidity:
                note: The absolute humidity value to set.
        """
        buffer = []
        arr = [absolute_humidity >> 8, absolute_humidity & 0xFF]
        arr.append(generate_crc(arr))
        buffer += arr
        self._i2c_read_words_from_cmd(
            SGP30_CMD_SET_ABSOLUTE_HUMIDITY_HEX + buffer,
            SGP30_CMD_SET_ABSOLUTE_HUMIDITY_MAX_MS,
            SGP30_CMD_SET_ABSOLUTE_HUMIDITY_WORDS,
        )

    def measure_test(self):
        """
        note:
            en: Run the on-chip self-test.

        params:
            note:

        returns:
            note: The result of the self-test.
        """
        return self._i2c_read_words_from_cmd(
            SGP30_CMD_MEASURE_TEST_HEX,
            SGP30_CMD_MEASURE_TEST_MAX_MS,
            SGP30_CMD_MEASURE_TEST_WORDS,
        )[0]

    def get_feature_set(self):
        """
        note:
            en: Retrieve the feature set of the sensor.

        params:
            note:

        returns:
            note: The feature set value.
        """
        return self._i2c_read_words_from_cmd(
            SGP30_CMD_GET_FEATURE_SET_HEX,
            SGP30_CMD_GET_FEATURE_SET_MAX_MS,
            SGP30_CMD_GET_FEATURE_SET_WORDS,
        )[0]

    def measure_raw(self):
        """
        note:
            en: Return raw H2 and Ethanol signals for part verification and testing.

        params:
            note:

        returns:
            note: A tuple containing raw H2 and Ethanol signals.
        """
        return self._i2c_read_words_from_cmd(
            SGP30_CMD_MEASURE_RAW_HEX,
            SGP30_CMD_MEASURE_RAW_MAX_MS,
            SGP30_CMD_MEASURE_RAW_WORDS,
        )

    # TODO: Get TVOC inceptive baseline
    # TODO: Set TVOC baseline
    # TODO: Soft Reset (datasheet section 6.4)

    def get_serial(self):
        """
        note:
            en: Retrieve the sensor serial ID.

        params:
            note:

        returns:
            note: The serial ID as a hexadecimal string.
        """
        serial = self._i2c_read_words_from_cmd(
            SGP30_CMD_GET_SERIAL_ID_HEX,
            SGP30_CMD_GET_SERIAL_ID_MAX_MS,
            SGP30_CMD_GET_SERIAL_ID_WORDS,
        )
        return hex(int.from_bytes(bytearray(serial), "large"))

    def co2eq(self):
        """
        note:
            en: Retrieve the Carbon Dioxide Equivalent (CO2eq) in parts per million (ppm).

        params:
            note:

        returns:
            note: The CO2eq value in ppm.
        """
        return self.measure_iaq()[0]

    def baseline_co2eq(self):
        """
        note:
            en: Retrieve the baseline value for CO2eq.

        params:
            note:

        returns:
            note: The baseline CO2eq value.
        """
        return self.get_iaq_baseline()[0]

    def tvoc(self):
        """
        note:
            en: Retrieve the Total Volatile Organic Compound (TVOC) in parts per billion (ppb).

        params:
            note:

        returns:
            note: The TVOC value in ppb.
        """
        return self.measure_iaq()[1]

    def baseline_tvoc(self):
        """
        note:
            en: Retrieve the baseline value for TVOC.

        params:
            note:

        returns:
            note: The baseline TVOC value.
        """
        return self.get_iaq_baseline()[1]

    def raw_h2(self):
        """
        note:
            en: Retrieve the raw H2 signal value.

        params:
            note:

        returns:
            note: The raw H2 signal value.
        """
        return self.measure_raw()[0]

    def raw_ethanol(self):
        """
        note:
            en: Retrieve the raw Ethanol signal value.

        params:
            note:

        returns:
            note: The raw Ethanol signal value.
        """
        return self.measure_raw()[1]

    def _i2c_read_words_from_cmd(self, command, delay, reply_size):
        """
        note:
            en: Execute an I2C command query and retrieve the response, including CRC validation.

        params:
            command:
                note: The command to send to the sensor.
            delay:
                note: The delay in milliseconds before reading the response.
            reply_size:
                note: The size of the expected response in words.

        returns:
            note: A list of response words from the sensor.
        """
        self._i2c.writeto(self.addr, bytes(command))
        sleep_ms(delay)
        if not reply_size:
            return None
        crc_result = bytearray(reply_size * (SGP30_WORD_LEN + 1))
        self._i2c.readfrom_into(self.addr, crc_result)
        result = []
        for i in range(reply_size):
            word = [crc_result[3 * i], crc_result[3 * i + 1]]
            crc = crc_result[3 * i + 2]
            if generate_crc(word) != crc:
                raise RuntimeError("CRC Error")
            result.append(word[0] << 8 | word[1])
        return result

    def convert_r_to_a_humidity(self, temp_c, r_humidity_perc, fixed_point=True):
        """
        note:
            en: Convert relative humidity to absolute humidity based on the sensor's equation.

        params:
            temp_c:
                note: The ambient temperature in Celsius (°C).
            r_humidity_perc:
                note: The relative humidity in percentage (%).
            fixed_point:
                note: Whether to return the value in 8.8 fixed-point format. Defaults to True.

        returns:
            note: The absolute humidity value, either in g/m³ or fixed-point format.
        """
        a_humidity_gm3 = 216.7 * (
            (r_humidity_perc / 100 * 6.112 * exp(17.62 * temp_c / (243.12 + temp_c)))
            / (273.15 + temp_c)
        )
        if fixed_point:
            a_humidity_gm3 = (int(a_humidity_gm3) << 8) + (int(a_humidity_gm3 % 1 * 256))
        return a_humidity_gm3


def generate_crc(data):
    """
    note:
        en: Calculate an 8-bit CRC checksum based on the sensor's specified algorithm.

    params:
        data:
            note: The data array for which to calculate the CRC checksum.

    returns:
        note: The calculated 8-bit CRC checksum.
    """
    crc = SGP30_CRC8_INIT
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ SGP30_CRC8_POLYNOMIAL
            else:
                crc <<= 1
    return crc & 0xFF
