# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
import struct
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import time


class AC_MEASUREUnit:
    """
    note:
        en: AC Measure Unit is a single-phase AC measurement module with isolation capabilities. It utilizes the STM32+HLW8032 scheme to monitor high-precision current, voltage, power, and other data in real time. The module features a built-in AC isolation chip, B0505ST16-W5, and communicates with the STM32 through the EL357 optocoupler isolation chip.

    details:
        link: https://docs.m5stack.com/en/unit/AC%20Measure%20Unit
        image: https://static-cdn.m5stack.com/resource/docs/products/unit/AC%20Measure%20Unit/img-28a2411d-d63c-4596-b474-2db9d9b6dcc5.webp
        category: Unit

    example:
        - ../../../examples/unit/acmeasure/acmeasure_cores3_example.py

    m5f2:
        - unit/acmeasure/acmeasure_cores3_example.m5f2
    """

    _AC_MEASURE_ADDR = 0x42
    _ACMEASURE_VOLTAGE_STR_REG = 0x00
    _ACMEASURE_CURRENT_STR_REG = 0x10
    _ACMEASURE_ACTIVE_POWER_STR_REG = 0x20
    _ACMEASURE_APPARENT_POWER_STR_REG = 0x30
    _ACMEASURE_POWER_FACTOR_STR_REG = 0x40
    _ACMEASURE_KWH_STR_REG = 0x50
    _ACMEASURE_VOLTAGE_BYTE_REG = 0x60
    _ACMEASURE_CURRENT_BYTE_REG = 0x70
    _ACMEASURE_ACTIVE_POWER_BYTE_REG = 0x80
    _ACMEASURE_APPARENT_POWER_BYTE_REG = 0x90
    _ACMEASURE_POWER_FACTOR_BYTE_REG = 0xA0
    _ACMEASURE_KWH_BYTE_REG = 0xB0
    _ACMEASURE_VOLTAGE_COEFF_REG = 0xC0
    _ACMEASURE_CURRENT_COEFF_REG = 0xD0
    _ACMEASURE_SAVE_COEFF_REG = 0xE0
    _ACMEASURE_DATA_READY_REG = 0xFC
    _ACMEASURE_BOOTLOADER_REG = 0xFD
    _ACMEASURE_FIRM_VER_REG = 0xFE
    _ACMEASURE_I2C_ADDR_REG = 0xFF

    def __init__(
        self, i2c: I2C | PAHUBUnit, address: int | list | tuple = _AC_MEASURE_ADDR
    ) -> None:
        """
        note:
            en: Initialize the AC_MEASUREUnit with I2C communication and set the slave address.

        params:
            i2c:
                note: The I2C object or PAHUBUnit for communication.
            address:
                note: The I2C slave address of the AC Measure unit, default is _AC_MEASURE_ADDR.
        """
        self.ac_measure_i2c = i2c
        self.init_i2c_address(address)

    def init_i2c_address(self, slave_addr: int = _AC_MEASURE_ADDR) -> None:
        """
        note:
            en: Initialize the I2C address for the AC Measure unit.

        params:
            slave_addr:
                note: The I2C address of the AC Measure unit, should be between 1 and 127.
        """
        if slave_addr >= 0x01 and slave_addr <= 0x7F:
            self.i2c_addr = slave_addr
        if self.i2c_addr not in self.ac_measure_i2c.scan():
            raise UnitError("AC Measure unit maybe not connect")

    def get_voltage_str(self) -> str:
        """
        note:
            en: Get the voltage string value from the AC Measure unit.

        params:
            en:

        returns:
            note: The voltage value as a string.
        """
        return self.ac_measure_i2c.readfrom_mem(
            self.i2c_addr, self._ACMEASURE_VOLTAGE_STR_REG, 7
        ).decode()

    def get_current_str(self) -> str:
        """
        note:
            en: Get the current string value from the AC Measure unit.

        params:
            en:

        returns:
            note: The current value as a string.
        """
        return self.ac_measure_i2c.readfrom_mem(
            self.i2c_addr, self._ACMEASURE_CURRENT_STR_REG, 7
        ).decode()

    def get_active_power_str(self) -> str:
        """
        note:
            en: Get the active power string value from the AC Measure unit.

        params:
            en:

        returns:
            note: The active power value as a string.
        """
        return self.ac_measure_i2c.readfrom_mem(
            self.i2c_addr, self._ACMEASURE_ACTIVE_POWER_STR_REG, 7
        ).decode()

    def get_apparent_power_str(self) -> str:
        """
        note:
            en: Get the apparent power string value from the AC Measure unit.

        params:
            en:

        returns:
            note: The apparent power value as a string.
        """
        return self.ac_measure_i2c.readfrom_mem(
            self.i2c_addr, self._ACMEASURE_APPARENT_POWER_STR_REG, 7
        ).decode()

    def get_power_factor_str(self) -> str:
        """
        note:
            en: Get the power factor string value from the AC Measure unit.

        params:
            en:

        returns:
            note: The power factor value as a string.
        """
        return self.ac_measure_i2c.readfrom_mem(
            self.i2c_addr, self._ACMEASURE_POWER_FACTOR_STR_REG, 4
        ).decode()

    def get_kwh_str(self) -> str:
        """
        note:
            en: Get the kWh string value from the AC Measure unit.

        params:
            en:

        returns:
            note: The kWh value as a string.
        """
        return self.ac_measure_i2c.readfrom_mem(
            self.i2c_addr, self._ACMEASURE_KWH_STR_REG, 11
        ).decode()

    def get_voltage_byte(self) -> int:
        """
        note:
            en: Get the raw voltage value from the AC Measure unit.

        params:
            en:

        returns:
            note: The raw voltage value as an integer.
        """
        buf = self.ac_measure_i2c.readfrom_mem(self.i2c_addr, self._ACMEASURE_VOLTAGE_BYTE_REG, 2)
        return struct.unpack("<H", buf)[0]

    def get_current_byte(self) -> int:
        """
        note:
            en: Get the raw current value from the AC Measure unit.

        params:
            en:

        returns:
            note: The raw current value as an integer.
        """
        buf = self.ac_measure_i2c.readfrom_mem(self.i2c_addr, self._ACMEASURE_CURRENT_BYTE_REG, 2)
        return struct.unpack("<H", buf)[0]

    def get_active_power_byte(self) -> int:
        """
        note:
            en: Get the raw active power value from the AC Measure unit.

        params:
            en:

        returns:
            note: The raw active power value as an integer.
        """
        buf = self.ac_measure_i2c.readfrom_mem(
            self.i2c_addr, self._ACMEASURE_ACTIVE_POWER_BYTE_REG, 4
        )
        return struct.unpack("<I", buf)[0]

    def get_apparent_power_byte(self) -> int:
        """
        note:
            en: Get the raw apparent power value from the AC Measure unit.

        params:
            en:

        returns:
            note: The raw apparent power value as an integer.
        """
        buf = self.ac_measure_i2c.readfrom_mem(
            self.i2c_addr, self._ACMEASURE_APPARENT_POWER_BYTE_REG, 4
        )
        return struct.unpack("<I", buf)[0]

    def get_power_factor_byte(self) -> int:
        """
        note:
            en: Get the raw power factor value from the AC Measure unit.

        params:
            en:

        returns:
            note: The raw power factor value as an integer.
        """
        return self.ac_measure_i2c.readfrom_mem(
            self.i2c_addr, self._ACMEASURE_POWER_FACTOR_BYTE_REG, 1
        )[0]

    def get_kwh_byte(self) -> int:
        """
        note:
            en: Get the raw kWh value from the AC Measure unit.

        params:
            en:

        returns:
            note: The raw kWh value as an integer.
        """
        buf = self.ac_measure_i2c.readfrom_mem(self.i2c_addr, self._ACMEASURE_KWH_BYTE_REG, 4)
        return struct.unpack("<I", buf)[0]

    def get_voltage_coeff(self) -> int:
        """
        note:
            en: Get the voltage coefficient value from the AC Measure unit.

        params:
            en:

        returns:
            note: The voltage coefficient value as an integer.
        """
        return self.ac_measure_i2c.readfrom_mem(
            self.i2c_addr, self._ACMEASURE_VOLTAGE_COEFF_REG, 1
        )[0]

    def set_voltage_coeff(self, value: int) -> None:
        """
        note:
            en: Set the voltage coefficient value for the AC Measure unit.

        params:
            value:
                note: The voltage coefficient value to set, between 0 and 255.
        """
        self.ac_measure_i2c.writeto_mem(
            self.i2c_addr, self._ACMEASURE_VOLTAGE_COEFF_REG, bytearray([int(value)])
        )

    def get_current_coeff(self) -> int:
        """
        note:
            en: Get the current coefficient value from the AC Measure unit.

        params:
            en:

        returns:
            note: The current coefficient value as an integer.
        """
        return self.ac_measure_i2c.readfrom_mem(
            self.i2c_addr, self._ACMEASURE_CURRENT_COEFF_REG, 1
        )[0]

    def set_current_coeff(self, value: int) -> None:
        """
        note:
            en: Set the current coefficient value for the AC Measure unit.

        params:
            value:
                note: The current coefficient value to set, between 0 and 255.
        """
        self.ac_measure_i2c.writeto_mem(
            self.i2c_addr, self._ACMEASURE_CURRENT_COEFF_REG, bytearray([int(value)])
        )

    def set_save_coeff(self) -> None:
        """
        note:
            en: Save the voltage and current coefficient values to flash memory.

        params:
            en:

        """
        self.ac_measure_i2c.writeto_mem(
            self.i2c_addr, self._ACMEASURE_SAVE_COEFF_REG, bytearray([0x01])
        )
        time.sleep_ms(100)

    def get_data_ready(self) -> bool:
        """
        note:
            en: Check if the AC Measure unit's data is ready.

        params:
            en:

        returns:
            note: True if data is ready, False otherwise.
        """
        status = self.ac_measure_i2c.readfrom_mem(
            self.i2c_addr, self._ACMEASURE_DATA_READY_REG, 1
        )[0]
        return True if status == 1 else False

    def set_jump_bootloader(self) -> None:
        """
        note:
            en: Set the AC Measure unit to jump to the bootloader.

        params:
            en:
        """
        self.ac_measure_i2c.writeto_mem(
            self.i2c_addr, self._ACMEASURE_BOOTLOADER_REG, bytearray([0x01])
        )

    def get_device_status(self, mode: int) -> int:
        """
        note:
            en: Get the firmware version or I2C address based on the specified mode.

        params:
            mode:
                note: The mode to select the desired status (0xFE for firmware version, 0xFF for I2C address).

        returns:
            note: The requested device status as an integer.
        """
        if mode >= self._ACMEASURE_FIRM_VER_REG and mode <= self._ACMEASURE_I2C_ADDR_REG:
            return self.ac_measure_i2c.readfrom_mem(self.i2c_addr, mode, 1)[0]

    def set_i2c_address(self, addr: int) -> None:
        """
        note:
            en: Set a new I2C address for the AC Measure unit.

        params:
            addr:
                note: The new I2C address to set, between 0x01 and 0x7F.
        """
        if addr >= 0x01 and addr <= 0x7F:
            if addr != self.i2c_addr:
                self.ac_measure_i2c.writeto_mem(
                    self.i2c_addr, self._ACMEASURE_I2C_ADDR_REG, bytearray([addr])
                )
                self.i2c_addr = addr
                time.sleep_ms(100)


class ACMeasureUnit(AC_MEASUREUnit):
    def __init__(
        self, i2c: I2C | PAHUBUnit, address: int | list | tuple = AC_MEASUREUnit._AC_MEASURE_ADDR
    ) -> None:
        super().__init__(i2c, address)
