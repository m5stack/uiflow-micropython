
# TimerPWR Unit

<!-- .. include:: ../refs/unit.timerpwr.ref -->

The TimerPWR Unit is a timed power supply unit whose main functions are "charging & discharging + timed switching + screen display + boost output." It features an internal STM32 microcontroller that implements RTC and overall control, allowing users to set automatic power on/off times as needed. It is powered via the Type-C interface and can be connected to an external rechargeable battery via a 1.25-2P interface. The unit includes a built-in battery charging circuit supporting a charging current of 330mA. It also features an integrated DCDC boost circuit that provides a 5V/800mA (1400mA @ 1C battery power) power output to external devices via the Grove port. Additionally, the INA3221 sensor is built-in, allowing real-time monitoring of power input and output current and voltage. The unit is equipped with a 0.66-inch OLED display and two side buttons for user interaction, making it easy to view real-time system status and modify settings. Users can set parameters such as power on/off using the side buttons or via the I2C bus through the Grove interface with I2C commands. This product is suitable for smart homes, industrial automation, and timed control devices.

Support the following products:

|TimerPWRUnit|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import TimerPWRUnit
from hardware import *

label0 = None
label1 = None
label2 = None
label3 = None
label4 = None
label5 = None
label6 = None
label7 = None
label8 = None
rect0 = None
rect1 = None
label10 = None
rect2 = None
rect3 = None
label11 = None
label12 = None
label9 = None
i2c0 = None
timerpwr_0 = None

en = None

def timerpwr_0_btna_released_event(args):
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        rect0, \
        rect1, \
        label10, \
        rect2, \
        rect3, \
        label11, \
        label12, \
        label9, \
        i2c0, \
        timerpwr_0, \
        en
    print(timerpwr_0.get_button_status(0))
    rect1.setColor(color=0x00FF00, fill_c=0x00FF00)
    label11.setText(str("A"))
    label11.setColor(0x00FF00, 0x00FF00)

def timerpwr_0_btna_pressed_event(args):
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        rect0, \
        rect1, \
        label10, \
        rect2, \
        rect3, \
        label11, \
        label12, \
        label9, \
        i2c0, \
        timerpwr_0, \
        en
    print(timerpwr_0.get_button_status(0))
    rect1.setColor(color=0xFF0000, fill_c=0xFF0000)
    label11.setText(str("A"))
    label11.setColor(0xFF0000, 0xFF0000)

def timerpwr_0_btnb_released_event(args):
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        rect0, \
        rect1, \
        label10, \
        rect2, \
        rect3, \
        label11, \
        label12, \
        label9, \
        i2c0, \
        timerpwr_0, \
        en
    print(timerpwr_0.get_button_status(1))
    rect2.setColor(color=0x00FF00, fill_c=0x00FF00)
    label12.setText(str("B"))
    label12.setColor(0x00FF00, 0x00FF00)

def timerpwr_0_btnb_pressed_event(args):
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        rect0, \
        rect1, \
        label10, \
        rect2, \
        rect3, \
        label11, \
        label12, \
        label9, \
        i2c0, \
        timerpwr_0, \
        en
    print(timerpwr_0.get_button_status(1))
    rect2.setColor(color=0xFF0000, fill_c=0xFF0000)
    label12.setText(str("B"))
    label12.setColor(0xFF0000, 0xFF0000)

def timerpwr_0_usb_inserted_event(args):
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        rect0, \
        rect1, \
        label10, \
        rect2, \
        rect3, \
        label11, \
        label12, \
        label9, \
        i2c0, \
        timerpwr_0, \
        en
    rect0.setColor(color=0x00FF00, fill_c=0x00FF00)
    label10.setText(str("U"))
    label10.setColor(0x00FF00, 0x00FF00)

def timerpwr_0_usb_removed_event(args):
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        rect0, \
        rect1, \
        label10, \
        rect2, \
        rect3, \
        label11, \
        label12, \
        label9, \
        i2c0, \
        timerpwr_0, \
        en
    rect0.setColor(color=0xFF0000, fill_c=0xFF0000)
    label10.setText(str("U"))
    label10.setColor(0xFF0000, 0xFF0000)

def timerpwr_0_not_charging_event(args):
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        rect0, \
        rect1, \
        label10, \
        rect2, \
        rect3, \
        label11, \
        label12, \
        label9, \
        i2c0, \
        timerpwr_0, \
        en
    rect3.setColor(color=0xFF0000, fill_c=0xFF0000)
    label9.setText(str("C"))
    label9.setColor(0xFF0000, 0xFF0000)

def timerpwr_0_charging_event(args):
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        rect0, \
        rect1, \
        label10, \
        rect2, \
        rect3, \
        label11, \
        label12, \
        label9, \
        i2c0, \
        timerpwr_0, \
        en
    rect3.setColor(color=0x00FF00, fill_c=0x00FF00)
    label9.setText(str("C"))
    label9.setColor(0x00FF00, 0x00FF00)

def btnA_wasClicked_event(state):  # noqa: N802
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        rect0, \
        rect1, \
        label10, \
        rect2, \
        rect3, \
        label11, \
        label12, \
        label9, \
        i2c0, \
        timerpwr_0, \
        en
    timerpwr_0.sleep_cycle(0, 0, 30, 0, 0, 10)

def setup():
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        rect0, \
        rect1, \
        label10, \
        rect2, \
        rect3, \
        label11, \
        label12, \
        label9, \
        i2c0, \
        timerpwr_0, \
        en

    M5.begin()
    label0 = Widgets.Label("OUT", 13, 4, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu9)
    label1 = Widgets.Label("label1", 9, 24, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu9)
    label2 = Widgets.Label("label2", 9, 42, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu9)
    label3 = Widgets.Label("BAT", 54, 4, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu9)
    label4 = Widgets.Label("label4", 49, 24, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu9)
    label5 = Widgets.Label("label5", 49, 42, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu9)
    label6 = Widgets.Label("USB", 93, 4, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu9)
    label7 = Widgets.Label("label7", 88, 24, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu9)
    label8 = Widgets.Label("label8", 88, 42, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu9)
    rect0 = Widgets.Rectangle(6, 98, 24, 24, 0x00FF00, 0x00FF00)
    rect1 = Widgets.Rectangle(37, 98, 24, 24, 0x00FF00, 0x00FF00)
    label10 = Widgets.Label("U", 13, 103, 1.0, 0xFFFFFF, 0x00FF00, Widgets.FONTS.DejaVu12)
    rect2 = Widgets.Rectangle(67, 98, 24, 24, 0x00FF00, 0x00FF00)
    rect3 = Widgets.Rectangle(97, 98, 24, 24, 0x00FF00, 0x00FF00)
    label11 = Widgets.Label("A", 45, 103, 1.0, 0xFFFFFF, 0x00FF00, Widgets.FONTS.DejaVu12)
    label12 = Widgets.Label("B", 75, 103, 1.0, 0xFFFFFF, 0x00FF00, Widgets.FONTS.DejaVu12)
    label9 = Widgets.Label("C", 105, 103, 1.0, 0xFFFFFF, 0x00FF00, Widgets.FONTS.DejaVu12)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btnA_wasClicked_event)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    timerpwr_0 = TimerPWRUnit(i2c0, 0x56)
    timerpwr_0.set_callback(timerpwr_0.EVENT_BUTTONA_RELEASED, timerpwr_0_btna_released_event)
    timerpwr_0.set_callback(timerpwr_0.EVENT_BUTTONA_PRESSED, timerpwr_0_btna_pressed_event)
    timerpwr_0.set_callback(timerpwr_0.EVENT_BUTTONB_RELEASED, timerpwr_0_btnb_released_event)
    timerpwr_0.set_callback(timerpwr_0.EVENT_BUTTONB_PRESSED, timerpwr_0_btnb_pressed_event)
    timerpwr_0.set_callback(timerpwr_0.EVENT_USB_INSERTED, timerpwr_0_usb_inserted_event)
    timerpwr_0.set_callback(timerpwr_0.EVENT_USB_REMOVED, timerpwr_0_usb_removed_event)
    timerpwr_0.set_callback(timerpwr_0.EVENT_NOT_CHARGING, timerpwr_0_not_charging_event)
    timerpwr_0.set_callback(timerpwr_0.EVENT_CHARGING, timerpwr_0_charging_event)
    en = True
    timerpwr_0.set_wakeup_trigger(timerpwr_0.TRIG_ALL)
    timerpwr_0.set_sleep_trigger(timerpwr_0.TRIG_ALL)

def loop():
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        rect0, \
        rect1, \
        label10, \
        rect2, \
        rect3, \
        label11, \
        label12, \
        label9, \
        i2c0, \
        timerpwr_0, \
        en
    M5.update()
    label1.setText(str(timerpwr_0.get_grove_voltage()))
    label2.setText(str(timerpwr_0.get_battery_current()))
    label4.setText(str(timerpwr_0.get_battery_voltage()))
    label5.setText(str(timerpwr_0.get_battery_current()))
    label7.setText(str(timerpwr_0.get_usb_voltage()))
    label8.setText(str(timerpwr_0.get_usb_current()))
    timerpwr_0.tick()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

```

UIFLOW2 Example:

<!-- .. only:: builder_html -->

    |atoms3_timerpwr_example.m5f2|

## class TimerPWRUnit

## Constructors

<!-- .. class:: TimerPWRUnit(i2c, address) -->

    Create a TimerPWR object.

    :param  i2c: I2C object
    :param int address: I2C address, 0x56 by default

    UIFLOW2:

## Methods

<!-- .. method:: TimerPWRUnit.get_firmware_version() -->

    Get firmware version.

    :return (int): Firmware version.

    UIFLOW2:

<!-- .. method:: TimerPWRUnit.get_battery_voltage() -->

    Get battery voltage.

    :return (int): Battery voltage, in millivolt.

    UIFLOW2:

<!-- .. method:: TimerPWRUnit.get_battery_current() -->

    Get battery current.

    :return (int): Battery current, in milliamperes.

    UIFLOW2:

<!-- .. method:: TimerPWRUnit.get_usb_voltage() -->

    Get USB voltage.

    :return (int): USB voltage, in millivolt.

    UIFLOW2:

<!-- .. method:: TimerPWRUnit.get_usb_current() -->

    Get USB current.

    :return (int): USB current, in milliamperes.

    UIFLOW2:

<!-- .. method:: TimerPWRUnit.get_grove_voltage() -->

    Get Grove voltage.

    :return (int): Grove voltage, in millivolt.

    UIFLOW2:

<!-- .. method:: TimerPWRUnit.get_grove_current() -->

    Get Grove current.

    :return (int): Grove current, in milliamperes.

    UIFLOW2:

<!-- .. method:: TimerPWRUnit.is_charging() -->

    Check if the battery is charging.

    :return (bool): True if charging, False if not.

    UIFLOW2:

<!-- .. method:: TimerPWRUnit.get_button_status(btn) -->

    Get button status.

    :param int btn: button index.

        Options:
            - ``A``: 0
            - ``B``: 1

    :return (bool): True if pressed, False if not.

    UIFLOW2:

<!-- .. method:: TimerPWRUnit.save_data_to_flash() -->

    Save data to flash.

    UIFLOW2:

<!-- .. method:: TimerPWRUnit.get_grove_output_status() -->

    Get Grove output status

    :return (bool): True if enabled, False if disabled.

    UIFLOW2:

<!-- .. method:: TimerPWRUnit.set_grove_output_status(enable) -->

    Set Grove output status.

    :param bool enable: Enable or disable Grove output.

        Options:
            - ``Enable``: True
            - ``Disable``: False

    UIFLOW2:

<!-- .. method:: TimerPWRUnit.get_oled_backlight_status() -->

    Get OLED backlight status.

    :return (bool): True if enabled, False if disabled.

    UIFLOW2:

<!-- .. method:: TimerPWRUnit.set_oled_backlight_status(enable) -->

    Set OLED backlight status.

    :param bool enable: Enable or disable OLED backlight.

        Options:
            - ``Enable``: True
            - ``Disable``: False

    UIFLOW2:

<!-- .. method:: TimerPWRUnit.sleep_once(whours, wmintues, wseconds, shours, smintues, sseconds) -->

    Set sleep once after hours, mintues, seconds and wake up in hours, mintues, seconds.

    :param int whours: Hours to wait before sleep.
    :param int wmintues: Mintues to wait before sleep.
    :param int wseconds: Seconds to wait before sleep.
    :param int shours: Hours to wait before wake up.
    :param int smintues: Mintues to wait before wake up.
    :param int sseconds: Seconds to wait before wake up.

    UIFLOW2:

<!-- .. method:: TimerPWRUnit.set_power_on_time(hours, mintues, seconds) -->

    Set power on time.

    :param int hours: Hours to power on.
    :param int mintues: Mintues to power on.
    :param int seconds: Seconds to power on.

<!-- .. method:: TimerPWRUnit.set_power_off_time(hours, mintues, seconds) -->

    Set power off time.

    :param int hours: Hours to power off.
    :param int mintues: Mintues to power off.
    :param int seconds: Seconds to power off.

<!-- .. method:: TimerPWRUnit.sleep_cycle(whours, wmintues, wseconds, shours, smintues, sseconds) -->

    Set sleep cycle after hours, mintues, seconds and wake up in hours, mintues, seconds.

    :param int whours: Hours to wait before sleep.
    :param int wmintues: Mintues to wait before sleep.
    :param int wseconds: Seconds to wait before sleep.
    :param int shours: Hours to wait before wake up.
    :param int smintues: Mintues to wait before wake up.
    :param int sseconds: Seconds to wait before wake up.

    UIFLOW2:

<!-- .. method:: TimerPWRUnit.set_cycle_sleep(enable) -->

    Set cycle sleep.

    :param bool enable: Enable or disable cycle sleep.

        Options:
            - ``Enable``: True
            - ``Disable``: False

<!-- .. method:: TimerPWRUnit.set_wakeup_trigger(trigger) -->

    Set wake-up trigger.

    :param  trigger: Set wake-up trigger.

        Options:
            - ``ALL``: timerpwrunit_0.TRIG_ALL
            - ``TIMER``: timerpwrunit_0.TRIG_TIMER
            - ``BUTTON``: timerpwrunit_0.TRIG_BUTTON
            - ``NONE``: timerpwrunit_0.TRIG_NONE

    UIFLOW2:

<!-- .. method:: TimerPWRUnit.set_sleep_trigger(trigger) -->

    Set sleep trigger.

    :param  trigger: Set sleep trigger.

        Options:
            - ``ALL``: timerpwrunit_0.TRIG_ALL
            - ``TIMER``: timerpwrunit_0.TRIG_TIMER
            - ``BUTTON``: timerpwrunit_0.TRIG_BUTTON
            - ``I2C``: timerpwrunit_0.TRIG_I2C
            - ``NONE``: timerpwrunit_0.TRIG_NONE

    UIFLOW2:

<!-- .. method:: TimerPWRUnit.set_callback(event, callback) -->

    Set callback function.

    :param  event: event type.

        Options:
            - ``USB inserted``: timerpwrunit_0.EVENT_USB_INSERTED
            - ``USB removed``: timerpwrunit_0.EVENT_USB_REMOVED
            - ``Button A pressed``: timerpwrunit_0.EVENT_BUTTONA_PRESSED
            - ``Button A released``: timerpwrunit_0.EVENT_BUTTONA_RELEASED
            - ``Button B pressed``: timerpwrunit_0.EVENT_BUTTONB_PRESSED
            - ``Button B released``: timerpwrunit_0.EVENT_BUTTONB_RELEASED
            - ``Not charging``: timerpwrunit_0.EVENT_NOT_CHARGING
            - ``Charging``: timerpwrunit_0.EVENT_CHARGING

    :param  callback: callback function.

    UIFLOW2:

<!-- .. method:: TimerPWRUnit.tick() -->

    Update status in loop.

    UIFLOW2:

## Constants

<!-- .. data:: TimerPWRUnit._SLEEP_COMMAND_REG -->
<!-- .. data:: TimerPWRUnit._CYCLE_REG -->
<!-- .. data:: TimerPWRUnit._GROVE_OUTPUT_REG -->
<!-- .. data:: TimerPWRUnit._OLED_BACKLIGHT_REG -->
<!-- .. data:: TimerPWRUnit._WAKE_UP_TRIGGER_REG -->
<!-- .. data:: TimerPWRUnit._SLEEP_TRIGGER_REG -->
<!-- .. data:: TimerPWRUnit._POWER_ON_TIME_REG -->
<!-- .. data:: TimerPWRUnit._POWER_OFF_TIME_REG -->
<!-- .. data:: TimerPWRUnit._BUTTON_STATUS_REG -->
<!-- .. data:: TimerPWRUnit._USB_VOLTAGE_REG -->
<!-- .. data:: TimerPWRUnit._USB_CURRENT_REG -->
<!-- .. data:: TimerPWRUnit._GROVE_VOLTAGE_REG -->
<!-- .. data:: TimerPWRUnit._GROVE_CURRENT_REG -->
<!-- .. data:: TimerPWRUnit._BATTERY_VOLTAGE_REG -->
<!-- .. data:: TimerPWRUnit._BATTERY_CURRENT_REG -->
<!-- .. data:: TimerPWRUnit._CHARGING_STATUS_REG -->
<!-- .. data:: TimerPWRUnit._SAVE_DATA_TO_FLASH_REG -->
<!-- .. data:: TimerPWRUnit._FW_VERSION_REG -->
<!-- .. data:: TimerPWRUnit._I2C_ADDRESS_REG -->

    register address.

<!-- .. data:: TimerPWRUnit.TRIG_ALL -->
<!-- .. data:: TimerPWRUnit.TRIG_TIMER -->
<!-- .. data:: TimerPWRUnit.TRIG_BUTTON -->
<!-- .. data:: TimerPWRUnit.TRIG_I2C -->
<!-- .. data:: TimerPWRUnit.TRIG_NONE -->

    trigger type.

<!-- .. data:: TimerPWRUnit.EVENT_USB_INSERTED -->
<!-- .. data:: TimerPWRUnit.EVENT_USB_REMOVED -->
<!-- .. data:: TimerPWRUnit.EVENT_BUTTONA_RELEASED -->
<!-- .. data:: TimerPWRUnit.EVENT_BUTTONA_PRESSED -->
<!-- .. data:: TimerPWRUnit.EVENT_BUTTONB_RELEASED -->
<!-- .. data:: TimerPWRUnit.EVENT_BUTTONB_PRESSED -->
<!-- .. data:: TimerPWRUnit.EVENT_NOT_CHARGING -->
<!-- .. data:: TimerPWRUnit.EVENT_CHARGING -->

    event type.

<!-- .. data:: TimerPWRUnit._USB -->
<!-- .. data:: TimerPWRUnit._BUTTON_A -->
<!-- .. data:: TimerPWRUnit._BUTTON_B -->
<!-- .. data:: TimerPWRUnit._CHARGING -->

    index.
