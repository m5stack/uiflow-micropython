# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from machine import I2C
from driver.aw32257 import AW32257
from driver.ina226 import INA226
import time

try:
    from micropython import const
except ImportError:
    const = lambda x: x


class HAT18650CHat:
    """Create a HAT18650CHat object.

    The AW32257 controls battery charging and Boost/OTG output. The INA226
    measures battery bus voltage, current, and power.

    :param I2C i2c: I2C bus.
    :param int charger_address: AW32257 I2C address. Default is 0x6A.
    :param int monitor_address: INA226 I2C address. Default is 0x41.
    :param float shunt_resistor: INA226 shunt resistor value in ohms. Default is 0.01.
    :param float max_expected_current: Maximum expected current for INA226 calibration in amps. Default is 10.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from hardware import I2C, Pin
            from hat import HAT18650CHat

            i2c0 = I2C(0, scl=Pin(0), sda=Pin(8), freq=100000)
            hat18650c = HAT18650CHat(i2c0)
    """

    CHARGER_ADDR = AW32257.DEFAULT_ADDR
    MONITOR_ADDR = const(0x41)

    STAT_READY = AW32257.STAT_READY
    STAT_CHARGING = AW32257.STAT_CHARGING
    STAT_DONE = AW32257.STAT_DONE
    STAT_FAULT = AW32257.STAT_FAULT

    CHARGE_FAULT_NORMAL = AW32257.CHARGE_FAULT_NORMAL
    CHARGE_FAULT_VBUS_OVP = AW32257.CHARGE_FAULT_VBUS_OVP
    CHARGE_FAULT_SLEEP_MODE = AW32257.CHARGE_FAULT_SLEEP_MODE
    CHARGE_FAULT_BAD_ADAPTOR_OR_VBUS_UVLO = AW32257.CHARGE_FAULT_BAD_ADAPTOR_OR_VBUS_UVLO
    CHARGE_FAULT_OUTPUT_OVP = AW32257.CHARGE_FAULT_OUTPUT_OVP
    CHARGE_FAULT_THERMAL_SHUTDOWN = AW32257.CHARGE_FAULT_THERMAL_SHUTDOWN
    CHARGE_FAULT_RESERVED = AW32257.CHARGE_FAULT_RESERVED
    CHARGE_FAULT_NO_BATTERY = AW32257.CHARGE_FAULT_NO_BATTERY

    BOOST_FAULT_NORMAL = AW32257.BOOST_FAULT_NORMAL
    BOOST_FAULT_VBUS_OVP = AW32257.BOOST_FAULT_VBUS_OVP
    BOOST_FAULT_OVER_LOAD = AW32257.BOOST_FAULT_OVER_LOAD
    BOOST_FAULT_BATTERY_LOW = AW32257.BOOST_FAULT_BATTERY_LOW
    BOOST_FAULT_RESERVED_4 = AW32257.BOOST_FAULT_RESERVED_4
    BOOST_FAULT_THERMAL_SHUTDOWN = AW32257.BOOST_FAULT_THERMAL_SHUTDOWN
    BOOST_FAULT_RESERVED_6 = AW32257.BOOST_FAULT_RESERVED_6
    BOOST_FAULT_RESERVED_7 = AW32257.BOOST_FAULT_RESERVED_7

    DEFAULT_CHARGE_VOLTAGE = 4.20
    DEFAULT_CHARGE_CURRENT = AW32257.CHARGE_CURRENT_MA[0]
    DEFAULT_TERMINATION_CURRENT = AW32257.TERM_CURRENT_MA[1]

    def __init__(
        self,
        i2c: I2C,
        charger_address: int = CHARGER_ADDR,
        monitor_address: int = MONITOR_ADDR,
        shunt_resistor: float = 0.01,
        max_expected_current: float = 10,
    ) -> None:
        """Initialize the HAT 18650C driver."""
        self.i2c = i2c
        self.charger_addr = charger_address
        self.monitor_addr = monitor_address
        # AW32257 controls charge/Boost registers, INA226 measures the battery bus.
        self.charger = AW32257(i2c, charger_address)
        time.sleep_ms(100)
        self._init_charger()
        self.monitor = INA226(i2c, monitor_address, shunt_resistor=shunt_resistor)
        self.monitor.configure(
            avg=INA226.CFG_AVGMODE_16SAMPLES,
            vbus_conv_time=INA226.CFG_VBUSCT_8244us,
            vshunt_conv_time=INA226.CFG_VSHUNTCT_8244us,
            mode=INA226.CFG_MODE_SANDBVOLT_CONTINUOUS,
        )
        self.monitor.calibrate(max_expected_current=max_expected_current)

    def _init_charger(self) -> None:
        self.charger.set_charge_voltage(self.DEFAULT_CHARGE_VOLTAGE)
        self.charger.set_charge_current(self.DEFAULT_CHARGE_CURRENT)
        self.charger.set_termination_current(self.DEFAULT_TERMINATION_CURRENT)
        self.charger.set_boost_enable(False)
        self.charger.set_charge_enable(True)

    def set_charge_enable(self, enable: bool) -> None:
        """Enable or disable battery charging.

        :param enable: True to enable charging, False to disable charging.
        :type enable: bool

        UiFlow2 Code Block:

            |set_charge_enable.png|

        MicroPython Code Block:

            .. code-block:: python

                hat18650c.set_charge_enable(True)
                hat18650c.set_charge_enable(False)
        """
        self.charger.set_charge_enable(enable)

    def get_charge_enable(self) -> bool:
        """Get battery charging enable state.

        :returns: True if charging is enabled, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |get_charge_enable.png|

        MicroPython Code Block:

            .. code-block:: python

                charge_enable = hat18650c.get_charge_enable()
        """
        return self.charger.get_charge_enable()

    def set_charge_current(self, current_ma: int) -> None:
        """Set fast-charge current.

        The target current is clamped to the HAT 18650C supported table. The
        closest supported table value not greater than the target is used
        internally, so the written value may be lower than the requested value.

        :param current_ma: Target charge current in mA.
        :type current_ma: int

        UiFlow2 Code Block:

            |set_charge_current.png|

        MicroPython Code Block:

            .. code-block:: python

                hat18650c.set_charge_current(1000)
        """
        charge_current_ma = AW32257.CHARGE_CURRENT_MA
        current_ma = min(charge_current_ma[-1], max(charge_current_ma[0], current_ma))
        selected = charge_current_ma[0]
        for value in charge_current_ma:
            if value > current_ma:
                break
            selected = value
        self.charger.set_charge_current(selected)

    def get_charge_current(self) -> int:
        """Get fast-charge current setting.

        Returns the actual selected current-table value.

        :returns: Charge current setting in mA.
        :rtype: int

        UiFlow2 Code Block:

            |get_charge_current.png|

        MicroPython Code Block:

            .. code-block:: python

                current_ma = hat18650c.get_charge_current()
        """
        return self.charger.get_charge_current()

    def set_charge_voltage(self, voltage: float) -> None:
        """Set charge regulation voltage.

        The target voltage is clamped to the valid AW32257 range and rounded to
        the nearest register step, so the written value may be only close to the
        requested value.

        :param voltage: Target charge voltage in volts. Valid range is 3.50V to 4.50V.
        :type voltage: float

        UiFlow2 Code Block:

            |set_charge_voltage.png|

        MicroPython Code Block:

            .. code-block:: python

                hat18650c.set_charge_voltage(4.2)
        """
        self.charger.set_charge_voltage(voltage)

    def get_charge_voltage(self) -> float:
        """Get charge regulation voltage.

        Returns the actual selected voltage step.

        :returns: Charge regulation voltage in volts.
        :rtype: float

        UiFlow2 Code Block:

            |get_charge_voltage.png|

        MicroPython Code Block:

            .. code-block:: python

                voltage = hat18650c.get_charge_voltage()
        """
        return self.charger.get_charge_voltage()

    def set_termination_current(self, current_ma: int) -> None:
        """Set charge termination current.

        The target current is rounded to the nearest termination-current table
        value supported by AW32257.

        :param current_ma: Target termination current in mA. Options are 62 to 496 mA.
        :type current_ma: int

        UiFlow2 Code Block:

            |set_termination_current.png|

        MicroPython Code Block:

            .. code-block:: python

                hat18650c.set_termination_current(124)
        """
        self.charger.set_termination_current(current_ma)

    def get_termination_current(self) -> int:
        """Get charge termination current setting.

        Returns the actual selected termination-current table value.

        :returns: Termination current setting in mA.
        :rtype: int

        UiFlow2 Code Block:

            |get_termination_current.png|

        MicroPython Code Block:

            .. code-block:: python

                current_ma = hat18650c.get_termination_current()
        """
        return self.charger.get_termination_current()

    def set_safety_charge_current(self, current_ma: int) -> None:
        """Set maximum allowed charge current.

        The target current is rounded to the nearest charge-current table value
        supported by AW32257.

        :param current_ma: Target safety current in mA. Valid range is 496 to 2480 mA.
        :type current_ma: int

        UiFlow2 Code Block:

            |set_safety_charge_current.png|

        MicroPython Code Block:

            .. code-block:: python

                hat18650c.set_safety_charge_current(1000)
        """
        self.charger.set_safety_charge_current(current_ma)

    def get_safety_charge_current(self) -> int:
        """Get maximum allowed charge current.

        Returns the actual selected safety-current table value.

        :returns: Safety current limit in mA.
        :rtype: int

        UiFlow2 Code Block:

            |get_safety_charge_current.png|

        MicroPython Code Block:

            .. code-block:: python

                current_ma = hat18650c.get_safety_charge_current()
        """
        return self.charger.get_safety_charge_current()

    def set_safety_charge_voltage(self, voltage: float) -> None:
        """Set maximum allowed charge regulation voltage.

        The target voltage is rounded to the nearest safety-voltage table value
        supported by AW32257.

        :param voltage: Target safety voltage in volts. Valid range is 4.20V to 4.50V.
        :type voltage: float

        UiFlow2 Code Block:

            |set_safety_charge_voltage.png|

        MicroPython Code Block:

            .. code-block:: python

                hat18650c.set_safety_charge_voltage(4.2)
        """
        self.charger.set_safety_charge_voltage(voltage)

    def get_safety_charge_voltage(self) -> float:
        """Get maximum allowed charge regulation voltage.

        Returns the actual selected safety-voltage table value.

        :returns: Safety voltage limit in volts.
        :rtype: float

        UiFlow2 Code Block:

            |get_safety_charge_voltage.png|

        MicroPython Code Block:

            .. code-block:: python

                voltage = hat18650c.get_safety_charge_voltage()
        """
        return self.charger.get_safety_charge_voltage()

    def set_recharge_threshold(self, threshold_mv: int) -> None:
        """Set automatic recharge threshold below VOREG.

        :param threshold_mv: Target recharge threshold in mV. Options are 50, 100, 150, and 200.
        :type threshold_mv: int

        UiFlow2 Code Block:

            |set_recharge_threshold.png|

        MicroPython Code Block:

            .. code-block:: python

                hat18650c.set_recharge_threshold(100)
        """
        self.charger.set_recharge_threshold(threshold_mv)

    def get_recharge_threshold(self) -> int:
        """Get automatic recharge threshold below VOREG.

        :rtype: int

        UiFlow2 Code Block:

            |get_recharge_threshold.png|

        MicroPython Code Block:

            .. code-block:: python

                threshold_mv = hat18650c.get_recharge_threshold()
        """
        return self.charger.get_recharge_threshold()

    def get_charge_status(self) -> str:
        """Get charger status text.

        :returns: Charge status text: ``ready``, ``charging``, ``done``, or ``fault``.
        :rtype: str

        UiFlow2 Code Block:

            |get_charge_status.png|

        MicroPython Code Block:

            .. code-block:: python

                status = hat18650c.get_charge_status()
        """
        return self.charger.get_charge_status()

    def get_charge_status_code(self) -> int:
        """Get charger status code.

        :returns: One of ``STAT_READY``, ``STAT_CHARGING``, ``STAT_DONE``, or ``STAT_FAULT``.
        :rtype: int

        UiFlow2 Code Block:

            |get_charge_status_code.png|

        MicroPython Code Block:

            .. code-block:: python

                status = hat18650c.get_charge_status_code()
        """
        return self.charger.get_charge_status_code()

    def is_charging(self) -> bool:
        """Check whether charging is in progress.

        :returns: True if charging is in progress, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |is_charging.png|

        MicroPython Code Block:

            .. code-block:: python

                charging = hat18650c.is_charging()
        """
        return self.get_charge_status() == "charging"

    def is_charge_done(self) -> bool:
        """Check whether charging is complete.

        :returns: True if charging is complete, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |is_charge_done.png|

        MicroPython Code Block:

            .. code-block:: python

                done = hat18650c.is_charge_done()
        """
        return self.get_charge_status() == "done"

    def get_charge_fault(self) -> str:
        """Get charger fault text.

        :returns: Charge fault text.
        :rtype: str

        UiFlow2 Code Block:

            |get_charge_fault.png|

        MicroPython Code Block:

            .. code-block:: python

                fault = hat18650c.get_charge_fault()
        """
        return self.charger.get_charge_fault()

    def get_charge_fault_code(self) -> int:
        """Get charger fault code.

        :returns: Charge fault code. Use ``CHARGE_FAULT_*`` constants for comparison.
        :rtype: int

        UiFlow2 Code Block:

            |get_charge_fault_code.png|
            |charge_fault_code_option.png|

        MicroPython Code Block:

            .. code-block:: python

                fault = hat18650c.get_charge_fault_code()
                if fault == HAT18650CHat.CHARGE_FAULT_NO_BATTERY:
                    print("No battery")
        """
        return self.charger.get_charge_fault_code()

    def set_boost_enable(self, enable: bool) -> None:
        """Enable or disable AW32257 Boost/OTG mode.

        :param enable: True to enable Boost/OTG mode, False to disable it.
        :type enable: bool

        UiFlow2 Code Block:

            |set_boost_enable.png|

        MicroPython Code Block:

            .. code-block:: python

                hat18650c.set_boost_enable(True)
                hat18650c.set_boost_enable(False)
        """
        self.charger.set_boost_enable(enable)

    def get_boost_enable(self) -> bool:
        """Get AW32257 Boost/OTG enable state.

        :returns: True if Boost/OTG mode is enabled, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |get_boost_enable.png|

        MicroPython Code Block:

            .. code-block:: python

                boost_enable = hat18650c.get_boost_enable()
        """
        return self.charger.get_boost_enable()

    def get_boost_fault(self) -> str:
        """Get Boost/OTG fault text.

        :returns: Boost/OTG fault text.
        :rtype: str

        UiFlow2 Code Block:

            |get_boost_fault.png|

        MicroPython Code Block:

            .. code-block:: python

                fault = hat18650c.get_boost_fault()
        """
        return self.charger.get_boost_fault()

    def get_boost_fault_code(self) -> int:
        """Get Boost/OTG fault code.

        :returns: Boost/OTG fault code. Use ``BOOST_FAULT_*`` constants for comparison.
        :rtype: int

        UiFlow2 Code Block:

            |get_boost_fault_code.png|
            |boost_fault_code_option.png|

        MicroPython Code Block:

            .. code-block:: python

                fault = hat18650c.get_boost_fault_code()
                if fault == HAT18650CHat.BOOST_FAULT_BATTERY_LOW:
                    print("Battery low")
        """
        return self.charger.get_boost_fault_code()

    def get_battery_voltage(self) -> float:
        """Get battery bus voltage from INA226.

        :returns: Battery voltage in volts.
        :rtype: float

        UiFlow2 Code Block:

            |get_battery_voltage.png|

        MicroPython Code Block:

            .. code-block:: python

                voltage = hat18650c.get_battery_voltage()
        """
        return self.monitor.read_bus_voltage()

    def get_battery_current(self) -> float:
        """Get battery current from INA226.

        With the current hardware direction, charging current is usually negative
        and discharging current is usually positive.

        :returns: Battery current in amps.
        :rtype: float

        UiFlow2 Code Block:

            |get_battery_current.png|

        MicroPython Code Block:

            .. code-block:: python

                current = hat18650c.get_battery_current()
        """
        return self.monitor.read_current()

    def get_battery_power(self) -> float:
        """Get battery power from INA226.

        :returns: Battery power in watts.
        :rtype: float

        UiFlow2 Code Block:

            |get_battery_power.png|

        MicroPython Code Block:

            .. code-block:: python

                power = hat18650c.get_battery_power()
        """
        return self.monitor.read_power()
