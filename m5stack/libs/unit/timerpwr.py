# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import struct
import micropython
import time
from .unit_helper import UnitError


class TimerPWRUnit:
    """
    note:
        en: The TimerPWR Unit is a timed power supply unit whose main functions are "charging & discharging + timed switching + screen display + boost output." It features an internal STM32 microcontroller that implements RTC and overall control, allowing users to set automatic power on/off times as needed. It is powered via the Type-C interface and can be connected to an external rechargeable battery via a 1.25-2P interface. The unit includes a built-in battery charging circuit supporting a charging current of 330mA. It also features an integrated DCDC boost circuit that provides a 5V/800mA (1400mA @ 1C battery power) power output to external devices via the Grove port. Additionally, the INA3221 sensor is built-in, allowing real-time monitoring of power input and output current and voltage. The unit is equipped with a 0.66-inch OLED display and two side buttons for user interaction, making it easy to view real-time system status and modify settings. Users can set parameters such as power on/off using the side buttons or via the I2C bus through the Grove interface with I2C commands. This product is suitable for smart homes, industrial automation, and timed control devices.
    details:
        color: '#0fb1d2'
        link: https://docs.m5stack.com/en/unit/Unit-TimerPWR
        image: https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/products/unit/Unit-TimerPWR/4.webp
        category: Unit
    example:
        - ../../../examples/unit/timerpwr/atoms3_timerpwr_example.py
    """

    """
    constant: register address.
    """
    _SLEEP_COMMAND_REG = 0x40
    _CYCLE_REG = 0x41

    _GROVE_OUTPUT_REG = 0x00
    _OLED_BACKLIGHT_REG = 0x01

    _WAKE_UP_TRIGGER_REG = 0x20
    _SLEEP_TRIGGER_REG = 0x21

    _POWER_ON_TIME_REG = 0x30
    _POWER_OFF_TIME_REG = 0x80

    _BUTTON_STATUS_REG = 0x10

    _USB_VOLTAGE_REG = 0x60
    _USB_CURRENT_REG = 0x64

    _GROVE_VOLTAGE_REG = 0x68
    _GROVE_CURRENT_REG = 0x6C

    _BATTERY_VOLTAGE_REG = 0x70
    _BATTERY_CURRENT_REG = 0x74

    _CHARGING_STATUS_REG = 0x90

    _SAVE_DATA_TO_FLASH_REG = 0xF0

    _FW_VERSION_REG = 0xFE
    _I2C_ADDRESS_REG = 0xFF

    """
    constant: trigger type.
    """
    TRIG_ALL = 0b0000_0011
    TRIG_TIMER = 0b0000_0001
    TRIG_BUTTON = 0b0000_0010
    TRIG_I2C = 0b0000_0100
    TRIG_NONE = 0b0000_0000

    """
    constant: event type.
    """
    EVENT_USB_INSERTED = 0x01
    EVENT_USB_REMOVED = 0x02
    EVENT_BUTTONA_RELEASED = 0x03
    EVENT_BUTTONA_PRESSED = 0x04
    EVENT_BUTTONB_RELEASED = 0x05
    EVENT_BUTTONB_PRESSED = 0x06
    EVENT_NOT_CHARGING = 0x07
    EVENT_CHARGING = 0x08

    """
    constant: index.
    """
    _USB = 0x00
    _BUTTON_A = 0x01
    _BUTTON_B = 0x02
    _CHARGING = 0x03

    def __init__(self, i2c, address: int | list | tuple = 0x56):
        """
        note:
            en: Create a TimerPWR object.
        label:
            en: Init %1 I2C address %2
        params:
            i2c:
                name: i2c
                field: i2c
                note: I2C object
            address:
                name: address
                field: dropdown
                options:
                    '0x40': '0x40'
                note: I2C address, 0x56 by default
        """
        self._i2c = i2c
        self._address = address
        if self._address not in self._i2c.scan():
            raise UnitError("TimerPWR unit maybe not connect")
        usb_status = (
            self.EVENT_USB_INSERTED if self.get_usb_voltage() > 4900 else self.EVENT_USB_REMOVED
        )
        self.last_status = [
            usb_status,
            self.get_button_status(btn=0),
            self.get_button_status(btn=1),
            self.is_charging(),
        ]  # usb status, buttonA status, buttonB status, charging status
        self.callbacks = {
            self.EVENT_USB_INSERTED: None,
            self.EVENT_USB_REMOVED: None,
            self.EVENT_BUTTONA_PRESSED: None,
            self.EVENT_BUTTONA_RELEASED: None,
            self.EVENT_BUTTONB_PRESSED: None,
            self.EVENT_BUTTONB_RELEASED: None,
            self.EVENT_NOT_CHARGING: None,
            self.EVENT_CHARGING: None,
        }

    def get_firmware_version(self) -> int:
        """
        note:
            en: Get firmware version.
        label:
            en: get %1 firmware version (return int)
        return:
            note: Firmware version.

        """
        return self._i2c.readfrom_mem(self._address, self._FW_VERSION_REG, 1)[0]

    def get_battery_voltage(self) -> int:
        """
        note:
            en: Get battery voltage.
        label:
            en: get %1 battery voltage in millivolt(return int)
        return:
            note: Battery voltage, in millivolt.
        """
        buf = self._i2c.readfrom_mem(self._address, self._BATTERY_VOLTAGE_REG, 4)
        return struct.unpack("<i", buf)[0] * 10

    def get_battery_current(self) -> int:
        """
        note:
            en: Get battery current.
        label:
            en: get %1 battery current in milliamperes(return int)
        return:
            note: Battery current, in milliamperes.
        """
        buf = self._i2c.readfrom_mem(self._address, self._BATTERY_CURRENT_REG, 4)
        return struct.unpack("<i", buf)[0] // 100

    def get_usb_voltage(self) -> int:
        """
        note:
            en: Get USB voltage.
        label:
            en: get %1 usb voltage in millivolt(return int)
        return:
            note: USB voltage, in millivolt.
        """
        buf = self._i2c.readfrom_mem(self._address, self._USB_VOLTAGE_REG, 4)
        return struct.unpack("<i", buf)[0] * 10

    def get_usb_current(self) -> int:
        """
        note:
            en: Get USB current.
        label:
            en: get %1 usb current in milliamperes(return int)
        return:
            note: USB current, in milliamperes.
        """
        buf = self._i2c.readfrom_mem(self._address, self._USB_CURRENT_REG, 4)
        return struct.unpack("<i", buf)[0] // 100

    def get_grove_voltage(self) -> int:
        """
        note:
            en: Get Grove voltage.
        label:
            en: get %1 grove voltage in millivolt(return int)
        return:
            note: Grove voltage, in millivolt.
        """
        buf = self._i2c.readfrom_mem(self._address, self._GROVE_VOLTAGE_REG, 4)
        return struct.unpack("<i", buf)[0] * 10

    def get_grove_current(self) -> int:
        """
        note:
            en: Get Grove current.
        label:
            en: get %1 grove current in milliamperes(return int)
        return:
            note: Grove current, in milliamperes.
        """
        buf = self._i2c.readfrom_mem(self._address, self._GROVE_CURRENT_REG, 4)
        return struct.unpack("<i", buf)[0] // 100

    def is_charging(self) -> bool:
        """
        note:
            en: Check if the battery is charging.
        label:
            en: '%1 is battery charging (return True or False)'
        return:
            note: True if charging, False if not.
        """
        return bool(self._i2c.readfrom_mem(self._address, self._CHARGING_STATUS_REG, 1)[0])

    def get_button_status(self, btn=0) -> bool:
        """
        note:
            en: Get button status.
        label:
            en: get %1 button %2 status (return True or False)
        params:
            btn:
                name: btn
                field: dropdown
                options:
                    A: '0'
                    B: '1'
        return:
            note: True if pressed, False if not.
        """
        status = self._i2c.readfrom_mem(self._address, self._BUTTON_STATUS_REG + btn, 1)[0]
        return True if status == 0 else False

    def save_data_to_flash(self) -> None:
        """
        note:
            en: Save data to flash.
        label:
            en: Save %1 data to flash
        """
        self._i2c.writeto_mem(self._address, self._SAVE_DATA_TO_FLASH_REG, b"\x01")
        time.sleep(0.1)

    def get_grove_output_status(self) -> bool:
        """
        note:
            en: Get Grove output status
        label:
            en: get %1 Grove output status (return True or False)
        return:
            note: True if enabled, False if disabled.
        """
        return bool(self._i2c.readfrom_mem(self._address, self._GROVE_OUTPUT_REG, 1)[0])

    def set_grove_output_status(self, enable: bool) -> None:
        """
        note:
            en: Set Grove output status.
        label:
            en: Set %1 Grove output %2
        params:
            enable:
                name: enable
                field: dropdown
                options:
                    Enable: 'True'
                    Disable: 'False'
                note: Enable or disable Grove output.
        """
        self._i2c.writeto_mem(
            self._address, self._GROVE_OUTPUT_REG, b"\x01" if enable else b"\x00"
        )

    def get_oled_backlight_status(self) -> bool:
        """
        note:
            en: Get OLED backlight status.
        label:
            en: get %1 Grove oled backlight status (return True or False)
        return:
            note: True if enabled, False if disabled.
        """
        return bool(self._i2c.readfrom_mem(self._address, self._OLED_BACKLIGHT_REG, 1)[0])

    def set_oled_backlight_status(self, enable: bool) -> None:
        """
        note:
            en: Set OLED backlight status.
        label:
            en: Set %1 oled backlight %2
        params:
            enable:
                name: enable
                field: dropdown
                options:
                    Enable: 'True'
                    Disable: 'False'
                note: Enable or disable OLED backlight.
        """
        self._i2c.writeto_mem(
            self._address, self._OLED_BACKLIGHT_REG, b"\x01" if enable else b"\x00"
        )

    def sleep_once(
        self,
        whours: int = 0,
        wmintues: int = 0,
        wseconds: int = 5,
        shours: int = 0,
        smintues: int = 0,
        sseconds: int = 5,
    ) -> None:
        """
        note:
            en: Set sleep once after hours, mintues, seconds and wake up in hours, mintues, seconds.
        label:
            en: set %1 sleep once after hours (0 ~ 255) %2 mintues (0 ~ 59) %3 seconds (0
                ~ 59) %4 and wake up in hours (0 ~ 255) %5 mintues (0 ~ 59) %6 seconds (0
                ~ 59) %7
        params:
            whours:
                name: whours
                type: int
                default: '0'
                field: number
                note: Hours to wait before sleep.
            wmintues:
                name: wmintues
                type: int
                default: '0'
                field: number
                note: Mintues to wait before sleep.
            wseconds:
                name: wseconds
                type: int
                default: '5'
                field: number
                note: Seconds to wait before sleep.
            shours:
                name: shours
                type: int
                default: '0'
                field: number
                note: Hours to wait before wake up.
            smintues:
                name: param_6f3
                type: int
                default: '0'
                field: number
                note: Mintues to wait before wake up.
            sseconds:
                name: sseconds
                type: int
                default: '5'
                field: number
                note: Seconds to wait before wake up.
        """
        self.set_power_on_time(whours, wmintues, wseconds)
        self.set_power_off_time(shours, smintues, sseconds)
        self.save_data_to_flash()
        self._i2c.writeto_mem(self._address, self._SLEEP_COMMAND_REG, b"\x01")

    def set_power_on_time(self, hours: int = 0, mintues: int = 0, seconds: int = 5) -> None:
        """
        note:
            en: Set power on time.
        label:
            en: set %1 power on time hours (0 ~ 255) %2 mintues (0 ~ 59) %3 seconds (0 ~ 59) %4
        params:
            hours:
                name: hours
                type: int
                default: '0'
                field: number
                note: Hours to power on.
            mintues:
                name: mintues
                type: int
                default: '0'
                field: number
                note: Mintues to power on.
            seconds:
                name: seconds
                type: int
                default: '5'
                field: number
                note: Seconds to power on.
        """
        buf = struct.pack(">BBB", hours, mintues, seconds)
        self._i2c.writeto_mem(self._address, self._POWER_ON_TIME_REG, buf)

    def set_power_off_time(self, hours: int = 0, mintues: int = 0, seconds: int = 5) -> None:
        """
        note:
            en: Set power off time.
        label:
            en: set %1 power off time hours (0 ~ 255) %2 mintues (0 ~ 59) %3 seconds (0 ~ 59) %4
        params:
            hours:
                name: hours
                type: int
                default: '0'
                field: number
                note: Hours to power off.
            mintues:
                name: mintues
                type: int
                default: '0'
                field: number
                note: Mintues to power off.
            seconds:
                name: seconds
                type: int
                default: '5'
                field: number
                note: Seconds to power off.
        """
        buf = struct.pack(">BBB", hours, mintues, seconds)
        self._i2c.writeto_mem(self._address, self._POWER_OFF_TIME_REG, buf)

    def sleep_cycle(
        self,
        whours: int = 0,
        wmintues: int = 0,
        wseconds: int = 5,
        shours: int = 0,
        smintues: int = 0,
        sseconds: int = 5,
    ) -> None:
        """
        note:
            en: Set sleep cycle after hours, mintues, seconds and wake up in hours, mintues, seconds.
        label:
            en: set %1 sleep cycle after hours (0 ~ 255) %2 mintues (0 ~ 59) %3 seconds (0
                ~ 59) %4 and wake up in hours (0 ~ 255) %5 mintues (0 ~ 59) %6 seconds (0
                ~ 59) %7
        params:
            whours:
                name: whours
                type: int
                default: '0'
                field: number
                note: Hours to wait before sleep.
            wmintues:
                name: wmintues
                type: int
                default: '0'
                field: number
                note: Mintues to wait before sleep.
            wseconds:
                name: wseconds
                type: int
                default: '5'
                field: number
                note: Seconds to wait before sleep.
            shours:
                name: shours
                type: int
                default: '0'
                field: number
                note: Hours to wait before wake up.
            smintues:
                name: param_6f3
                type: int
                default: '0'
                field: number
                note: Mintues to wait before wake up.
            sseconds:
                name: sseconds
                type: int
                default: '5'
                field: number
                note: Seconds to wait before wake up.
        """
        self.set_power_on_time(whours, wmintues, wseconds)
        self.set_power_off_time(shours, smintues, sseconds)
        self.save_data_to_flash()
        self._i2c.writeto_mem(self._address, self._CYCLE_REG, b"\x01")

    def set_cycle_sleep(self, enable: bool) -> None:
        """
        note:
            en: Set cycle sleep.
        label:
            en: set %1 cycle sleep %2
        params:
            enable:
                name: enable
                field: dropdown
                options:
                    Enable: 'True'
                    Disable: 'False'
                note: Enable or disable cycle sleep.
        """
        self._i2c.writeto_mem(self._address, self._CYCLE_REG, b"\x01" if enable else b"\x00")

    def set_wakeup_trigger(self, trigger) -> None:
        """
        note:
            en: Set wake-up trigger.
        label:
            en: set %1 wake-up trigger %2
        params:
            trigger:
                name: trigger
                field: dropdown
                options:
                    ALL: timerpwrunit_0.TRIG_ALL
                    TIMER: timerpwrunit_0.TRIG_TIMER
                    BUTTON: timerpwrunit_0.TRIG_BUTTON
                    NONE: timerpwrunit_0.TRIG_NONE
                note: Set wake-up trigger.
        """
        self._i2c.writeto_mem(self._address, self._WAKE_UP_TRIGGER_REG, bytes([trigger]))

    def set_sleep_trigger(self, trigger) -> None:
        """
        note: Set sleep trigger.
        label:
            en: set %1 sleep trigger %2
        params:
            trigger:
                name: trigger
                field: dropdown
                options:
                    ALL: timerpwrunit_0.TRIG_ALL
                    TIMER: timerpwrunit_0.TRIG_TIMER
                    BUTTON: timerpwrunit_0.TRIG_BUTTON
                    I2C: timerpwrunit_0.TRIG_I2C
                    NONE: timerpwrunit_0.TRIG_NONE
                note: Set sleep trigger.
        """
        self._i2c.writeto_mem(self._address, self._SLEEP_TRIGGER_REG, bytes([trigger]))

    def set_callback(self, event, callback) -> None:
        """
        note:
            en: Set callback function.
        params:
            event:
                name: event
                field: dropdown
                options:
                    USB inserted: timerpwrunit_0.EVENT_USB_INSERTED
                    USB removed: timerpwrunit_0.EVENT_USB_REMOVED
                    Button A pressed: timerpwrunit_0.EVENT_BUTTONA_PRESSED
                    Button A released: timerpwrunit_0.EVENT_BUTTONA_RELEASED
                    Button B pressed: timerpwrunit_0.EVENT_BUTTONB_PRESSED
                    Button B released: timerpwrunit_0.EVENT_BUTTONB_RELEASED
                    Not charging: timerpwrunit_0.EVENT_NOT_CHARGING
                    Charging: timerpwrunit_0.EVENT_CHARGING
            callback:
                name: callback
                type: function
        """
        self.callbacks[event] = callback

    def tick(self):
        """
        note:
            en: Update status in loop.
        label:
            en: '%1 update in loop'
        """
        usb_status = (
            self.EVENT_USB_INSERTED if self.get_usb_voltage() > 4900 else self.EVENT_USB_REMOVED
        )

        if usb_status != self.last_status[self._USB] and self.callbacks[usb_status]:
            self.last_status[self._USB] = usb_status
            micropython.schedule(self.callbacks[usb_status], (self, usb_status))

        charging_status = self.is_charging()
        if charging_status != self.last_status[self._CHARGING]:
            print(
                "charging status=%d, last staus=%d"
                % (charging_status, self.last_status[self._CHARGING])
            )
            callback = self.callbacks[self.EVENT_NOT_CHARGING + int(charging_status)]
            self.last_status[self._CHARGING] = charging_status
            callback and micropython.schedule(callback, (self, charging_status))

        for btn in range(2):
            status = self.get_button_status(btn=btn)
            callback = self.callbacks[self.EVENT_BUTTONA_RELEASED + btn * 2 + int(status)]
            if status != self.last_status[self._BUTTON_A + btn] and callback:
                # print("btn%d status=%d, last staus=%d" % (btn, status, self.last_status[btn]))
                self.last_status[self._BUTTON_A + btn] = status
                micropython.schedule(callback, (self, status))
