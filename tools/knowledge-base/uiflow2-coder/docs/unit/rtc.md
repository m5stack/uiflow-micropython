
# RTC Unit

Support the following products:

    RTCUnit

## MicroPython Example

#### get real time

This example displays the Real time on the screen and serial.

```python
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

## **API**

#### Class RTC8563Unit

## `RTC8563Unit`
Create an RTC8563Unit object.

- Parameter `i2c` (`I2C`): The I2C port used for communication.
- Parameter `address` (`int`): The I2C address of the RTC8563/PCF8563.

```python
from machine import I2C, Pin
from unit import RTC8563Unit

i2c0 = I2C(0, scl=Pin(26), sda=Pin(32), freq=400000)
rtc_0 = RTC8563Unit(i2c0)
```

### `get_date_time`
Getting specific date or time components.

- Parameter `select` (`int`): The component to get (SECONDS, MINUTES, HOURS, DAY, DATE, MONTH, YEAR).
- Returns: The value of the selected component.
- Return type: int

```python
rtc_0.get_date_time(0) # Get seconds
```

### `set_date_time`
Setting the date and time values.

- Parameter `seconds` (`int`): Range [0,59].
- Parameter `minutes` (`int`): Range [0,59].
- Parameter `hours` (`int`): Range [0,23].
- Parameter `day` (`int`): Range [0,6] (0 for Sunday).
- Parameter `date` (`int`): Range [1-31].
- Parameter `month` (`int`): Range [1-12].
- Parameter `year` (`int`): Range [0-99] (Last two digits).

```python
rtc_0.set_date_time(hours=12, minutes=30)
```

### `datetime`
Setting the complete date and time using a tuple.

- Parameter `dt` (`tuple`): (year, month, date, hours, minutes, seconds, day).

```python
rtc_0.datetime((2024, 5, 20, 10, 0, 0, 1))
```

### `write_now`
Writing the current system time (from ESP32) to the RTC.

```python
rtc_0.write_now()
```

### `set_internet_time`
Synchronizing the RTC with network time.

- Parameter `source` (`str`): Time source ("ntp").
- Parameter `host` (`str`): NTP server address.
- Parameter `tzone` (`float`): Timezone offset.
- Parameter `win` (`bool`): Whether to consider daylight saving time.

```python
rtc_0.set_internet_time(tzone=8)
```

### `set_clk_out_frequency`
Setting the frequency of the CLKOUT pin.

- Parameter `frequency` (`int`): Frequency constant (e.g., CLOCK_CLK_OUT_FREQ_1_HZ).

```python
rtc_0.set_clk_out_frequency(0x83)
```

### `check_if_alarm_on`
Checking if the alarm flag is triggered.

- Returns: True if alarm is triggered, False otherwise.
- Return type: bool

```python
rtc_0.check_if_alarm_on()
```

### `turn_off_alarm`
Disabling the alarm function.

```python
rtc_0.turn_off_alarm()
```

### `clear_alarm_flag`
Clearing the alarm status flag and resetting alarm registers.

```python
rtc_0.clear_alarm_flag()
```

### `set_daily_alarm`
Setting a daily or periodic alarm.

- Parameter `hours` (`int`): Alarm hour.
- Parameter `minutes` (`int`): Alarm minute.
- Parameter `date` (`int`): Alarm date.
- Parameter `weekday` (`int`): Alarm weekday.

```python
rtc_0.set_daily_alarm(hours=7, minutes=0)
```

### `set_timer_mode`
Setting the countdown timer mode and initial value.

- Parameter `mode` (`int`): Timer clock frequency mode.
- Parameter `value` (`int`): Initial countdown value.

```python
rtc_0.set_timer_mode(mode=2, value=60)
```

### `get_timer_value`
Getting the current countdown timer value.

- Returns: Current timer value.
- Return type: int

```python
rtc_0.get_timer_value()
```

### `check_if_timer_on`
Checking if the timer flag is triggered.

- Returns: True if timer is triggered, False otherwise.
- Return type: bool

```python
rtc_0.check_if_timer_on()
```

### `turn_off_timer`
Disabling the timer and clearing the timer flag.

```python
rtc_0.turn_off_timer()
```

### `clear_timer_flag`
Clearing the timer status flag.

```python
rtc_0.clear_timer_flag()
```
