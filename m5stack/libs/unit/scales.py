# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import time
import struct


class ScalesUnit:
    _SCALES_ADDR = 0x26
    ############# BUTTON STATUS ##############
    _SACLES_BUTTON_SHORT = 0x20
    _SACLES_BUTTON_LONG = 0x21
    _SACLES_BUTTON_STATUS = 0x22
    _SACLES_BUTTON_OFFSET = 0x23
    ############## LED CONTROL ###############
    _SACLES_LED_SYNC = 0x25
    _SACLES_LED_RED = 0x50
    _SACLES_LED_GREEN = 0x51
    _SACLES_LED_BLUE = 0x52
    ######## SCALES STATUS & CONTROL #########
    _SACLES_RAW_ADC = 0x10
    _SACLES_GET_WEIGHT = 0x14
    _SACLES_OFFSET_ADC = 0x18
    _SACLES_SOFT_OFFSET = 0x24
    ############## CALIBRATION ###############
    _SACLES_CALI_ZERO = 0x30
    _SACLES_CALI_LOAD = 0x32
    ############# DEVICE STATUS ##############
    _SACLES_FW_VER_REG = 0xFE
    _SACLES_I2C_ADDR_REG = 0xFF

    """
    note:
        en: UNIT Scales is a high precision low-cost I2C port weighing sensor, with a total weighing range of 20kgs. Adopt STM32F030 as the controller, HX711 as sampling chip and 20 kgs weighing sensor. With tare button and programable RGB LED. This Unit offers the customer with a highly integrated weighing solution, suitable for the applications of weighing, item counting, item movement Checking and so on.

    details:
        link: https://docs.m5stack.com/en/unit/UNIT%20Scales
        image: https://static-cdn.m5stack.com/resource/docs/products/unit/UNIT%20Scales/img-94426368-7f2e-43ae-a514-9d38ee161b46.webp
        category: Unit

    example:
        - ../../../examples/unit/scales/scales_cores3_example.py

    m5f2:
        - unit/scales/scales_cores3_example.m5f2
    """

    def __init__(self, i2c: I2C | PAHUBUnit, address: int | list | tuple = _SCALES_ADDR) -> None:
        """
        note:
            en: Initialize the ScalesUnit with I2C communication and an optional I2C address.

        params:
            i2c:
                note: The I2C or PAHUBUnit instance for communication.
            address:
                note: The I2C address or a list/tuple of addresses for the scales unit.
        """
        self.i2c = i2c
        self.i2c_addr = address
        self._available()

    def _available(self) -> None:
        if self.i2c_addr not in self.i2c.scan():
            raise UnitError("Scales unit maybe not connect")

    def get_button_status(self, status) -> int:
        """
        note:
            en: Retrieve the status of a button on the scales unit.

        params:
            status:
                note: The button status identifier.

        returns:
            note: The current status of the specified button.
        """
        status += self._SACLES_BUTTON_SHORT
        if status >= self._SACLES_BUTTON_SHORT and status <= self._SACLES_BUTTON_OFFSET:
            return self.i2c.readfrom_mem(self.i2c_addr, status, 1)[0]

    def set_button_offset(self, enable) -> None:
        """
        note:
            en: Enable or disable the button offset for the scales unit.

        params:
            enable:
                note: The offset enable value (1 to enable, 0 to disable).
        """
        self.i2c.writeto_mem(self.i2c_addr, self._SACLES_BUTTON_OFFSET, bytes([enable]))

    def set_rgbled_sync(self, control) -> None:
        """
        note:
            en: Set synchronization mode for the RGB LED.

        params:
            control:
                note: The control value for synchronization.
        """
        self.i2c.writeto_mem(self.i2c_addr, self._SACLES_LED_SYNC, bytes([control]))

    def get_rgbled_sync(self) -> int:
        """
        note:
            en: Retrieve the synchronization mode of the RGB LED.

        params:
            note:

        returns:
            note: The synchronization mode value.
        """
        return self.i2c.readfrom_mem(self.i2c_addr, self._SACLES_LED_SYNC, 1)[0]

    def set_rgb_led(self, rgb) -> None:
        """
        note:
            en: Set the RGB values for the LED.

        params:
            rgb:
                note: The RGB value as a 24-bit integer.
        """
        self.i2c.writeto_mem(self.i2c_addr, self._SACLES_LED_RED, rgb.to_bytes(3, "big"))

    def get_rgb_led(self) -> list:
        """
        note:
            en: Retrieve the current RGB values of the LED.

        params:
            note:

        returns:
            note: A list containing the RGB values.
        """
        return list(self.i2c.readfrom_mem(self.i2c_addr, self._SACLES_LED_RED, 3))

    def get_scale_value(self, scale) -> int:
        """
        note:
            en: Get the scale value for the specified scale type.

        params:
            scale:
                note: The scale type identifier.

        returns:
            note: The scale value as an integer.
        """
        scale = self._SACLES_RAW_ADC + (scale * 4)
        if scale >= self._SACLES_RAW_ADC and scale <= self._SACLES_OFFSET_ADC:
            byte_val = self.i2c.readfrom_mem(self.i2c_addr, scale, 4)
            if scale == self._SACLES_GET_WEIGHT:
                return int((struct.unpack(">i", byte_val)[0]) / 100)
            return struct.unpack(">i", byte_val)[0]

    def set_raw_offset(self, value) -> None:
        """
        note:
            en: Set the raw offset for the scales unit.

        params:
            value:
                note: The raw offset value as an integer.
        """
        self.i2c.writeto_mem(self.i2c_addr, self._SACLES_OFFSET_ADC, value.to_bytes(4, "big"))

    def set_current_raw_offset(self) -> None:
        """
        note:
            en: Set the current raw offset value for the scales unit.

        params:
            note:
        """
        self.i2c.writeto_mem(self.i2c_addr, self._SACLES_SOFT_OFFSET, bytes([1]))

    def set_calibration_zero(self) -> None:
        """
        note:
            en: Calibrate the scales unit for zero weight.

        params:
            note:
        """
        self.i2c.writeto_mem(self.i2c_addr, self._SACLES_CALI_ZERO, bytes([0, 0]))
        time.sleep_ms(200)

    def set_calibration_load(self, gram) -> None:
        """
        note:
            en: Calibrate the scales unit with a specified weight.

        params:
            gram:
                note: The weight value in grams for calibration.
        """
        self.i2c.writeto_mem(self.i2c_addr, self._SACLES_CALI_LOAD, gram.to_bytes(2, "little"))
        time.sleep_ms(200)

    def get_device_inform(self, mode) -> int:
        """
        note:
            en: Get the device information for a specified mode.

        params:
            mode:
                note: The mode identifier for the requested information.

        returns:
            note: The device information value.
        """
        if mode >= self._SACLES_FW_VER_REG and mode <= self._SACLES_I2C_ADDR_REG:
            return self.i2c.readfrom_mem(self.i2c_addr, mode, 1)[0]

    def set_i2c_address(self, addr) -> None:
        """
        note:
            en: Change the I2C address of the scales unit.

        params:
            addr:
                note: The new I2C address value.
        """
        if addr >= 1 and addr <= 127:
            if addr != self.i2c_addr:
                self.i2c.writeto_mem(self.i2c_addr, self._SACLES_I2C_ADDR_REG, bytes([addr]))
                self.i2c_addr = addr
                time.sleep_ms(200)
