
# RTC Unit

<!-- .. sku: U155 -->

<!-- .. include:: ../refs/unit.rtc.ref -->

Support the following products:

    |RTCUnit|

## UiFlow2 Example

#### get real time

Open the |rtc_core2_example.m5f2| project in UiFlow2.

This example displays the Real time on the screen and serial.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### get real time

This example displays the Real time on the screen and serial.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from hardware import Pin
from hardware import I2C
from unit import RTC8563Unit
import time

page0 = None
label0 = None
i2c0 = None
rtc_0 = None

str2 = None

def setup():
    global page0, label0, i2c0, rtc_0, str2

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    label0 = m5ui.M5Label(
        "label0",
        x=3,
        y=99,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    rtc_0 = RTC8563Unit(i2c0)
    page0.screen_load()
    rtc_0.set_date_time(3, 49, 15, 0, 2, 2, 26)
    str2 = ""

def loop():
    global page0, label0, i2c0, rtc_0, str2
    M5.update()
    str2 = str("Time: ") + str(
        (
            str((rtc_0.get_date_time(6)))
            + str(
                (
                    str(".")
                    + str(
                        (
                            str((rtc_0.get_date_time(5)))
                            + str(
                                (
                                    str(".")
                                    + str(
                                        (
                                            str((rtc_0.get_date_time(4)))
                                            + str(
                                                (
                                                    str(" ")
                                                    + str(
                                                        (
                                                            str((rtc_0.get_date_time(2)))
                                                            + str(
                                                                (
                                                                    str(":")
                                                                    + str(
                                                                        (
                                                                            str(
                                                                                (
                                                                                    rtc_0.get_date_time(
                                                                                        1
                                                                                    )
                                                                                )
                                                                            )
                                                                            + str(
                                                                                (
                                                                                    str(":")
                                                                                    + str(
                                                                                        (
                                                                                            str(
                                                                                                (
                                                                                                    rtc_0.get_date_time(
                                                                                                        0
                                                                                                    )
                                                                                                )
                                                                                            )
                                                                                            + str(
                                                                                                ""
                                                                                            )
                                                                                        )
                                                                                    )
                                                                                )
                                                                            )
                                                                        )
                                                                    )
                                                                )
                                                            )
                                                        )
                                                    )
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    )
    print(str2)
    label0.set_text(str(str2))
    time.sleep(1)

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

```

Example output:

    None

## **API**

#### Class RTC8563Unit

## RTC8563Unit
Create an RTC8563Unit object.

:param I2C i2c: The I2C port used for communication.
:param int address: The I2C address of the RTC8563/PCF8563.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from machine import I2C, Pin
        from unit import RTC8563Unit

        i2c0 = I2C(0, scl=Pin(26), sda=Pin(32), freq=400000)
        rtc_0 = RTC8563Unit(i2c0)

### `get_date_time`
Getting specific date or time components.

:param int select: The component to get (SECONDS, MINUTES, HOURS, DAY, DATE, MONTH, YEAR).
:returns: The value of the selected component.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        rtc_0.get_date_time(0) # Get seconds

### `set_date_time`
Setting the date and time values.

:param int seconds: Range [0,59].
:param int minutes: Range [0,59].
:param int hours: Range [0,23].
:param int day: Range [0,6] (0 for Sunday).
:param int date: Range [1-31].
:param int month: Range [1-12].
:param int year: Range [0-99] (Last two digits).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        rtc_0.set_date_time(hours=12, minutes=30)

### `datetime`
Setting the complete date and time using a tuple.

:param tuple dt: (year, month, date, hours, minutes, seconds, day).

MicroPython Code Block:

    .. code-block:: python

        rtc_0.datetime((2024, 5, 20, 10, 0, 0, 1))

### `write_now`
Writing the current system time (from ESP32) to the RTC.

MicroPython Code Block:

    .. code-block:: python

        rtc_0.write_now()

### `set_internet_time`
Synchronizing the RTC with network time.

:param str source: Time source ("ntp").
:param str host: NTP server address.
:param float tzone: Timezone offset.
:param bool win: Whether to consider daylight saving time.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        rtc_0.set_internet_time(tzone=8)

### `set_clk_out_frequency`
Setting the frequency of the CLKOUT pin.

:param int frequency: Frequency constant (e.g., CLOCK_CLK_OUT_FREQ_1_HZ).

MicroPython Code Block:

    .. code-block:: python

        rtc_0.set_clk_out_frequency(0x83)

### `check_if_alarm_on`
Checking if the alarm flag is triggered.

:returns: True if alarm is triggered, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        rtc_0.check_if_alarm_on()

### `turn_off_alarm`
Disabling the alarm function.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        rtc_0.turn_off_alarm()

### `clear_alarm_flag`
Clearing the alarm status flag and resetting alarm registers.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        rtc_0.clear_alarm_flag()

### `set_daily_alarm`
Setting a daily or periodic alarm.

:param int hours: Alarm hour.
:param int minutes: Alarm minute.
:param int date: Alarm date.
:param int weekday: Alarm weekday.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        rtc_0.set_daily_alarm(hours=7, minutes=0)

### `set_timer_mode`
Setting the countdown timer mode and initial value.

:param int mode: Timer clock frequency mode.
:param int value: Initial countdown value.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        rtc_0.set_timer_mode(mode=2, value=60)

### `get_timer_value`
Getting the current countdown timer value.

:returns: Current timer value.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        rtc_0.get_timer_value()

### `check_if_timer_on`
Checking if the timer flag is triggered.

:returns: True if timer is triggered, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        rtc_0.check_if_timer_on()

### `turn_off_timer`
Disabling the timer and clearing the timer flag.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        rtc_0.turn_off_timer()

### `clear_timer_flag`
Clearing the timer status flag.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        rtc_0.clear_timer_flag()
