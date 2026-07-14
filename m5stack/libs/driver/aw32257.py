# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C

try:
    from micropython import const
except ImportError:
    const = lambda x: x

try:
    import time
except ImportError:
    time = None


class AW32257:
    """! AW32257 switch-mode single-cell Li-ion battery charger driver.

    @en The AW32257 integrates a buck charger, boost OTG output, charge status
        reporting, and programmable charge parameters over I2C.
    @cn The AW32257 integrates a buck charger, boost OTG output, charge status
        reporting, and programmable charge parameters over I2C.

    @param i2c I2C port to use.
    @param address AW32257 I2C address. Default is 0x6A.
    """

    DEFAULT_ADDR = const(0x6A)

    # Register map from DS_AW32257_EN_V1.5.
    REG_STATUS = const(0x00)  # STAT/OTG pin status and charge fault bits.
    REG_CONTROL = const(0x01)  # TE, CEN, high-Z, and boost mode control.
    REG_BATTERY_VOLTAGE = const(0x02)  # VOREG and OTG pin control.
    REG_PART_INFO = const(0x03)  # Vendor, part number, and revision code.
    REG_CHARGE_CURRENT = const(0x04)  # RESET, ICHG, and ITERM_CFG.
    REG_VBUS_DPM = const(0x05)  # DPM status, CD pin status, and VBUS DPM.
    REG_SAFETY_LIMIT = const(0x06)  # ISAFE and VSAFE limits.
    REG_TERMINATION = const(0x07)  # Termination algorithm and recharge config.
    REG_VENDOR = const(0x08)  # AWINIC vendor number.
    REG_BOOST_FAULT = const(0x09)  # Boost fault status.
    REG_BOOST_CONFIG = const(0x0A)  # Boost voltage and driver configuration.

    STAT_READY = const(0)
    STAT_CHARGING = const(1)
    STAT_DONE = const(2)
    STAT_FAULT = const(3)

    CHARGE_FAULT_NORMAL = const(0)
    CHARGE_FAULT_VBUS_OVP = const(1)
    CHARGE_FAULT_SLEEP_MODE = const(2)
    CHARGE_FAULT_BAD_ADAPTOR_OR_VBUS_UVLO = const(3)
    CHARGE_FAULT_OUTPUT_OVP = const(4)
    CHARGE_FAULT_THERMAL_SHUTDOWN = const(5)
    CHARGE_FAULT_RESERVED = const(6)
    CHARGE_FAULT_NO_BATTERY = const(7)

    BOOST_FAULT_NORMAL = const(0)
    BOOST_FAULT_VBUS_OVP = const(1)
    BOOST_FAULT_OVER_LOAD = const(2)
    BOOST_FAULT_BATTERY_LOW = const(3)
    BOOST_FAULT_RESERVED_4 = const(4)
    BOOST_FAULT_THERMAL_SHUTDOWN = const(5)
    BOOST_FAULT_RESERVED_6 = const(6)
    BOOST_FAULT_RESERVED_7 = const(7)

    _CHARGE_STATUS = ("ready", "charging", "done", "fault")
    _CHARGE_FAULT = (
        "normal",
        "vbus_ovp",
        "sleep_mode",
        "bad_adaptor_or_vbus_uvlo",
        "output_ovp",
        "thermal_shutdown",
        "reserved",
        "no_battery",
    )
    _BOOST_FAULT = (
        "normal",
        "vbus_ovp",
        "over_load",
        "battery_low",
        "reserved",
        "thermal_shutdown",
        "reserved",
        "reserved",
    )

    # Lookup tables for the HAT 18650C 33 mOhm charge-sense resistor.
    CHARGE_CURRENT_MA = (
        496,
        620,
        868,
        992,
        1116,
        1240,
        1364,
        1488,
        1612,
        1736,
        1860,
        1984,
        2108,
        2232,
        2356,
        2480,
    )
    TERM_CURRENT_MA = (62, 124, 186, 248, 310, 372, 434, 496)
    SAFE_CHARGE_VOLTAGE = (
        4.20,
        4.22,
        4.24,
        4.26,
        4.28,
        4.30,
        4.32,
        4.34,
        4.36,
        4.38,
        4.40,
        4.42,
        4.44,
        4.46,
        4.48,
        4.50,
    )
    RECHARGE_THRESHOLD_MV = (50, 100, 150, 200)
    TERMINATION_PERIODS = (8, 16)
    TERMINATION_COUNTS = (1, 2, 4, 8)
    TERMINATION_DEGLITCH_MS = (8, 16, 32, 64)
    BOOST_VOLTAGE = (5.05, 5.15, 5.25, 5.35)

    _CHARGE_CURRENT_MA = CHARGE_CURRENT_MA
    _TERM_CURRENT_MA = TERM_CURRENT_MA
    _BOOST_VOLTAGE = BOOST_VOLTAGE

    def __init__(self, i2c: I2C, address: int = DEFAULT_ADDR) -> None:
        self.i2c = i2c
        self.addr = address
        self._available()

    def _available(self) -> None:
        """Check whether the AW32257 exists on the I2C bus."""
        if self.addr not in self.i2c.scan():
            raise ValueError("AW32257 not found in I2C bus.")

    def read_register(self, reg: int) -> int:
        """! Read one AW32257 register.

        @param reg Register address.
        @return Register value.
        """
        return self.i2c.readfrom_mem(self.addr, reg, 1)[0]

    def write_register(self, reg: int, value: int) -> None:
        """! Write one AW32257 register.

        @param reg Register address.
        @param value Register value.
        """
        self.i2c.writeto_mem(self.addr, reg, bytes((value & 0xFF,)))

    def update_register(self, reg: int, mask: int, value: int) -> None:
        """! Update selected bits in one AW32257 register.

        @param reg Register address.
        @param mask Bit mask for the field to update.
        @param value Field value already aligned to the target bit position.
        """
        data = self.read_register(reg)
        data = (data & (~mask & 0xFF)) | (value & mask)
        self.write_register(reg, data)

    def get_otg_pin_status(self) -> bool:
        """! Get the live OTG pin logic level from REG00[7].

        @return True if OTG pin is high.
        """
        return bool(self.read_register(self.REG_STATUS) & 0x80)

    def set_stat_enable(self, enable: bool) -> None:
        """! Enable or disable the STAT pin function.

        @param enable [field_switch] True to enable STAT pin indication.
        """
        self.update_register(self.REG_STATUS, 0x40, 0x40 if enable else 0x00)

    def get_stat_enable(self) -> bool:
        """! Get STAT pin function enable state.

        @return True if STAT pin function is enabled.
        """
        return bool(self.read_register(self.REG_STATUS) & 0x40)

    def get_charge_status_code(self) -> int:
        """! Get charger state code from REG00[5:4].

        @return STAT_READY, STAT_CHARGING, STAT_DONE, or STAT_FAULT.
        """
        return (self.read_register(self.REG_STATUS) >> 4) & 0x03

    def get_charge_status(self) -> str:
        """! Get charger state from REG00[5:4].

        @return ready, charging, done, or fault.
        """
        return self._CHARGE_STATUS[self.get_charge_status_code()]

    def get_charge_fault_code(self) -> int:
        """! Get charge-mode fault code from REG00[2:0].

        @return Charge fault code.
        """
        return self.read_register(self.REG_STATUS) & 0x07

    def get_charge_fault(self) -> str:
        """! Get charge-mode fault state from REG00[2:0].

        @return Charge fault text.
        """
        return self._CHARGE_FAULT[self.get_charge_fault_code()]

    def set_charge_termination_enable(self, enable: bool) -> None:
        """! Enable or disable charge current termination detection.

        @param enable [field_switch] True to enable termination detection.
        """
        self.update_register(self.REG_CONTROL, 0x08, 0x08 if enable else 0x00)

    def get_charge_termination_enable(self) -> bool:
        """! Get charge termination detection enable state.

        @return True if charge termination detection is enabled.
        """
        return bool(self.read_register(self.REG_CONTROL) & 0x08)

    def set_charge_enable(self, enable: bool) -> None:
        """! Enable or disable battery charging.

        @param enable [field_switch] True to enable charging. REG01[2] uses
            inverted logic: 0 means enabled, 1 means disabled.
        """
        self.update_register(self.REG_CONTROL, 0x04, 0x00 if enable else 0x04)

    def get_charge_enable(self) -> bool:
        """! Get battery charging enable state.

        @return True if charging is enabled.
        """
        return not bool(self.read_register(self.REG_CONTROL) & 0x04)

    def set_charge_voltage(self, voltage: float) -> None:
        """! Set charge regulation voltage.

        The target voltage is clamped to 3.50V-4.50V and rounded to the nearest
        20 mV register step.

        @param voltage Target voltage in volts. Valid range is 3.50V to 4.50V.
        """
        code = int(round((min(4.5, max(3.5, voltage)) - 3.5) / 0.02))
        self.update_register(self.REG_BATTERY_VOLTAGE, 0xFC, (code & 0x3F) << 2)

    def get_charge_voltage(self) -> float:
        """! Get charge regulation voltage.

        @return Actual selected charge regulation voltage step in volts.
        """
        code = (self.read_register(self.REG_BATTERY_VOLTAGE) >> 2) & 0x3F
        return 4.5 if code > 0x32 else round(3.5 + code * 0.02, 2)

    def set_high_impedance_enable(self, enable: bool) -> None:
        """! Enable or disable high-impedance mode.

        @param enable [field_switch] True to enter high-impedance mode.
        """
        self.update_register(self.REG_CONTROL, 0x02, 0x02 if enable else 0x00)

    def get_high_impedance_enable(self) -> bool:
        """! Get high-impedance mode enable state.

        @return True if high-impedance mode is enabled.
        """
        return bool(self.read_register(self.REG_CONTROL) & 0x02)

    def set_boost_enable(self, enable: bool) -> None:
        """! Enable or disable I2C-controlled boost mode.

        @param enable [field_switch] True to enable boost mode through OPA_MODE.
        """
        self.update_register(self.REG_CONTROL, 0x01, 0x01 if enable else 0x00)

    def get_boost_enable(self) -> bool:
        """! Get I2C-controlled boost mode enable state.

        @return True if OPA_MODE boost control is enabled.
        """
        return bool(self.read_register(self.REG_CONTROL) & 0x01)

    def is_boosting(self) -> bool:
        """! Check whether the chip is operating in boost mode.

        @return True if REG00[3] indicates boost mode.
        """
        return bool(self.read_register(self.REG_STATUS) & 0x08)

    def set_otg_pin_polarity(self, active_high: bool) -> None:
        """! Set OTG pin active polarity in host mode.

        @param active_high True for active-high OTG pin control.
        """
        self.update_register(self.REG_BATTERY_VOLTAGE, 0x02, 0x02 if active_high else 0x00)

    def get_otg_pin_polarity(self) -> bool:
        """! Get OTG pin active polarity in host mode.

        @return True if OTG pin control is active high.
        """
        return bool(self.read_register(self.REG_BATTERY_VOLTAGE) & 0x02)

    def set_otg_pin_enable(self, enable: bool) -> None:
        """! Enable or disable OTG pin control in host mode.

        @param enable [field_switch] True to allow OTG pin boost control.
        """
        self.update_register(self.REG_BATTERY_VOLTAGE, 0x01, 0x01 if enable else 0x00)

    def get_otg_pin_enable(self) -> bool:
        """! Get OTG pin control enable state in host mode.

        @return True if OTG pin boost control is enabled.
        """
        return bool(self.read_register(self.REG_BATTERY_VOLTAGE) & 0x01)

    def get_part_info(self) -> tuple:
        """! Read vendor code, part number code, and revision code.

        @return Tuple of (vendor_code, part_number_code, revision_code).
        """
        data = self.read_register(self.REG_PART_INFO)
        return ((data >> 5) & 0x07, (data >> 3) & 0x03, data & 0x07)

    def reset(self) -> None:
        """! Reset charge parameters except the safety-limit register.

        The datasheet requires at least 32 ms before the next I2C command.
        """
        self.update_register(self.REG_CHARGE_CURRENT, 0x80, 0x80)
        if time is not None:
            try:
                time.sleep_ms(32)
            except AttributeError:
                time.sleep(0.032)

    def set_charge_current(self, current_ma: int) -> None:
        """! Set fast-charge current using the nearest supported code.

        The target current is rounded to the nearest current-table value
        supported by AW32257.

        @param current_ma Target charge current in mA.
        """
        code = self._nearest_index(self.CHARGE_CURRENT_MA, current_ma)
        self.update_register(self.REG_CHARGE_CURRENT, 0x78, (code & 0x0F) << 3)

    def get_charge_current(self) -> int:
        """! Get fast-charge current setting.

        @return Actual selected charge current in mA.
        """
        code = (self.read_register(self.REG_CHARGE_CURRENT) >> 3) & 0x0F
        return self.CHARGE_CURRENT_MA[code]

    def set_termination_current(self, current_ma: int) -> None:
        """! Set charge termination current using the nearest supported code.

        The target current is rounded to the nearest termination-current table
        value supported by AW32257.

        @param current_ma Target termination current in mA.
        """
        code = self._nearest_index(self.TERM_CURRENT_MA, current_ma)
        self.update_register(self.REG_CHARGE_CURRENT, 0x07, code & 0x07)

    def get_termination_current(self) -> int:
        """! Get charge termination current setting.

        @return Actual selected termination current in mA.
        """
        code = self.read_register(self.REG_CHARGE_CURRENT) & 0x07
        return self.TERM_CURRENT_MA[code]

    def set_safety_charge_current(self, current_ma: int) -> None:
        """! Set maximum allowed charge current.

        The target current is rounded to the nearest current-table value
        supported by AW32257.

        @param current_ma Target safety current in mA.
        """
        code = self._nearest_index(self.CHARGE_CURRENT_MA, current_ma)
        self.update_register(self.REG_SAFETY_LIMIT, 0xF0, (code & 0x0F) << 4)

    def get_safety_charge_current(self) -> int:
        """! Get maximum allowed charge current.

        @return Actual selected safety current limit in mA.
        """
        code = (self.read_register(self.REG_SAFETY_LIMIT) >> 4) & 0x0F
        return self.CHARGE_CURRENT_MA[code]

    def set_safety_charge_voltage(self, voltage: float) -> None:
        """! Set maximum allowed charge regulation voltage.

        The target voltage is rounded to the nearest safety-voltage table value
        supported by AW32257.

        @param voltage Target safety voltage in volts. Valid range is 4.20V to 4.50V.
        """
        code = self._nearest_index(self.SAFE_CHARGE_VOLTAGE, voltage)
        self.update_register(self.REG_SAFETY_LIMIT, 0x0F, code & 0x0F)

    def get_safety_charge_voltage(self) -> float:
        """! Get maximum allowed charge regulation voltage.

        @return Actual selected safety voltage limit in volts.
        """
        code = self.read_register(self.REG_SAFETY_LIMIT) & 0x0F
        return self.SAFE_CHARGE_VOLTAGE[code]

    def set_recharge_threshold(self, threshold_mv: int) -> None:
        """! Set automatic recharge threshold below VOREG.

        @param threshold_mv Target recharge threshold in mV. Options are 50, 100, 150, and 200.
        """
        code = self._nearest_index(self.RECHARGE_THRESHOLD_MV, threshold_mv)
        self.update_register(self.REG_TERMINATION, 0x03, code & 0x03)

    def get_recharge_threshold(self) -> int:
        """! Get automatic recharge threshold below VOREG.

        @return Recharge threshold in mV.
        """
        code = self.read_register(self.REG_TERMINATION) & 0x03
        return self.RECHARGE_THRESHOLD_MV[code]

    def set_charge_termination_period(self, periods: int) -> None:
        """! Set termination algorithm counting window.

        @param periods Counting window periods. Options are 8 and 16.
        """
        code = self._nearest_index(self.TERMINATION_PERIODS, periods)
        self.update_register(self.REG_TERMINATION, 0x80, 0x80 if code else 0x00)

    def get_charge_termination_period(self) -> int:
        """! Get termination algorithm counting window.

        @return Counting window periods.
        """
        code = 1 if (self.read_register(self.REG_TERMINATION) & 0x80) else 0
        return self.TERMINATION_PERIODS[code]

    def set_charge_termination_count(self, count: int) -> None:
        """! Set required periods where ICHG is below ITERM.

        @param count Required period count. Options are 1, 2, 4, and 8.
        """
        code = self._nearest_index(self.TERMINATION_COUNTS, count)
        self.update_register(self.REG_TERMINATION, 0x60, (code & 0x03) << 5)

    def get_charge_termination_count(self) -> int:
        """! Get required periods where ICHG is below ITERM.

        @return Required period count.
        """
        code = (self.read_register(self.REG_TERMINATION) >> 5) & 0x03
        return self.TERMINATION_COUNTS[code]

    def set_charge_termination_deglitch_time(self, time_ms: int) -> None:
        """! Set deglitch time for each termination period.

        @param time_ms Deglitch time in ms. Options are 8, 16, 32, and 64.
        """
        code = self._nearest_index(self.TERMINATION_DEGLITCH_MS, time_ms)
        self.update_register(self.REG_TERMINATION, 0x18, (code & 0x03) << 3)

    def get_charge_termination_deglitch_time(self) -> int:
        """! Get deglitch time for each termination period.

        @return Deglitch time in ms.
        """
        code = (self.read_register(self.REG_TERMINATION) >> 3) & 0x03
        return self.TERMINATION_DEGLITCH_MS[code]

    def get_dpm_status(self) -> bool:
        """! Check whether VBUS DPM regulation is active.

        @return True if DPM mode is active.
        """
        return bool(self.read_register(self.REG_VBUS_DPM) & 0x10)

    def get_cd_status(self) -> bool:
        """! Get CD pin logic state.

        @return True if CD pin is high.
        """
        return bool(self.read_register(self.REG_VBUS_DPM) & 0x08)

    def set_vbus_dpm_voltage(self, voltage: float) -> None:
        """! Set VBUS dynamic power management regulation voltage.

        @param voltage Target VBUS DPM voltage in volts. Valid range is 4.25V to 4.775V.
        """
        code = int(round((min(4.775, max(4.25, voltage)) - 4.25) / 0.075))
        self.update_register(self.REG_VBUS_DPM, 0x07, code & 0x07)

    def get_vbus_dpm_voltage(self) -> float:
        """! Get VBUS dynamic power management regulation voltage.

        @return VBUS DPM voltage in volts.
        """
        code = self.read_register(self.REG_VBUS_DPM) & 0x07
        return round(4.25 + code * 0.075, 3)

    def get_vendor_id(self) -> int:
        """! Read AWINIC vendor register.

        @return Vendor ID register value.
        """
        return self.read_register(self.REG_VENDOR)

    def get_boost_fault_code(self) -> int:
        """! Get boost-mode fault code from REG09[2:0].

        @return Boost fault code.
        """
        return self.read_register(self.REG_BOOST_FAULT) & 0x07

    def get_boost_fault(self) -> str:
        """! Get boost-mode fault state from REG09[2:0].

        @return Boost fault text.
        """
        return self._BOOST_FAULT[self.get_boost_fault_code()]

    def set_boost_voltage(self, voltage: float) -> None:
        """! Set boost output voltage using the nearest supported code.

        @param voltage Target boost voltage in volts. Options are 5.05V, 5.15V,
            5.25V, and 5.35V.
        """
        code = self._nearest_index(self.BOOST_VOLTAGE, voltage)
        self.update_register(self.REG_BOOST_CONFIG, 0x03, code & 0x03)

    def get_boost_voltage(self) -> float:
        """! Get boost output voltage setting.

        @return Boost voltage in volts.
        """
        code = self.read_register(self.REG_BOOST_CONFIG) & 0x03
        return self.BOOST_VOLTAGE[code]

    def set_force_pwm_enable(self, enable: bool) -> None:
        """! Enable or disable force PWM modulation in boost mode.

        @param enable [field_switch] True to force PWM modulation.
        """
        self.update_register(self.REG_BOOST_CONFIG, 0x08, 0x08 if enable else 0x00)

    def get_force_pwm_enable(self) -> bool:
        """! Get force PWM modulation enable state.

        @return True if force PWM modulation is enabled.
        """
        return bool(self.read_register(self.REG_BOOST_CONFIG) & 0x08)

    @staticmethod
    def _nearest_index(values, target):
        """Return the index of the lookup-table value nearest to target."""
        best = 0
        diff = abs(values[0] - target)
        for i, value in enumerate(values):
            new_diff = abs(value - target)
            if new_diff < diff:
                best = i
                diff = new_diff
        return best
