# NCIR2 Unit

<!-- .. sku: U150 -->

<!-- .. include:: ../refs/unit.ncir2.ref -->

This library is the driver for Unit NCIR2.

Support the following products:

    |Unit NCIR2|

## UiFlow2 Example

#### Infrared Temperature Display

Open the |m5cores3_ncir2_base_example.m5f2| project in UiFlow2.

This example uses the M5Stack CoreS3 board with the NCIR2 infrared temperature sensor to measure temperature in real time and display the current value along with the low and high temperature alarm thresholds on screen.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Infrared Temperature Display

This example uses the M5Stack CoreS3 board with the NCIR2 infrared temperature sensor to measure temperature in real time and display the current value along with the low and high temperature alarm thresholds on screen.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from unit import NCIR2Unit
import time

title0 = None
label_temp = None
label_la = None
label_ha = None
label_temp_val = None
label_la_val = None
label_ha_val = None
i2c0 = None
ncir2_0 = None
last_time = None

def setup():
    global \
        title0, \
        label_temp, \
        label_la, \
        label_ha, \
        label_temp_val, \
        label_la_val, \
        label_ha_val, \
        i2c0, \
        ncir2_0, \
        last_time
    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("Temperature meassure", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_temp = Widgets.Label("Temp: ", 10, 116, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    label_la = Widgets.Label(
        "low temp alarm value: ", 10, 50, 1.0, 0x0000FF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_ha = Widgets.Label(
        "high temp alarm value: ", 10, 80, 1.0, 0xFF0000, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_temp_val = Widgets.Label(" ", 95, 116, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    label_la_val = Widgets.Label(" ", 232, 50, 1.0, 0x0000FF, 0x222222, Widgets.FONTS.DejaVu18)
    label_ha_val = Widgets.Label(" ", 239, 80, 1.0, 0xFF0000, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    ncir2_0 = NCIR2Unit(i2c0, 0x5A)
    last_time = time.ticks_ms()
    label_la_val.setText(str(ncir2_0.get_temperature_threshold(0x20)))
    label_ha_val.setText(str(ncir2_0.get_temperature_threshold(0x22)))

def loop():
    global \
        title0, \
        label_temp, \
        label_la, \
        label_ha, \
        label_temp_val, \
        label_la_val, \
        label_ha_val, \
        i2c0, \
        ncir2_0, \
        last_time
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) > 500:
        last_time = time.ticks_ms()
        label_temp.setText(str((str((ncir2_0.get_temperature_value)) + str(" C"))))

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

Example output:

    None

## **API**

#### NCIR2Unit

<!-- .. class:: unit.hbridge.NCIR2Unit -->

    Create an NCIR2Unit object.

    :param I2C | PAHUBUnit i2c: I2C port,
    :param int address: NCIR2Unit Slave Address, Default is 0x5A.

    UiFlow2 Code Block:

    MicroPython Code Block:

<!-- .. code-block:: python -->

            from unit import NCIR2Unit

            unit_ncir2_0 = NCIR2Unit(i2c0, 0x5A)

<!-- .. method:: get_temperature_value() -->

        Get object temperature.

        :returns: object temperature(unit: ℃)
        :rtype: float

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.get_temperature_value()

<!-- .. method:: get_emissivity_value() -->

        Get current emissivity.

        :returns: emissivity.
        :rtype: float

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.get_emissivity_value()

<!-- .. method:: set_emissivity_value(emissive) -->

        Set the emissivity.

        According to the material being measured; it affects temperature measurement accuracy.

        - A black body has an emissivity of 1.00 (ideal emitter).
        - Shiny metals often have low emissivity values (below 0.1).
        - Dark, rough surfaces like electrical tape or human skin typically have high emissivity (above 0.95).

        :param: int emissive: The emissivity, range: 0 ~ 1.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.set_emissivity_value(emissive)

<!-- .. method:: get_temperature_threshold(alarm_reg) -->

        Get temperature alaram threshold.

        :param: int alarm_reg: ALARM_LOW_TEMP_REG: Low temperature alarm threshold register, ALARM_HIGH_TEMP_REG: High temperature alarm threshold register.
        :returns: alarm threshold.
        :rtype: float

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.get_temperature_threshold(alarm_reg)

<!-- .. method:: set_temperature_threshold(alarm_reg, temp) -->

        Set temperature alarm threshold.

        :param: int alarm_reg: temperature alarm register, ALARM_LOW_TEMP_REG: Low temperature alarm threshold register, ALARM_HIGH_TEMP_REG: High temperature alarm threshold register.
        :param: float temp: alarm threshold.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.set_temperature_threshold(alarm_reg, temp)

<!-- .. method:: get_temp_alarm_led(alarm_reg) -->

        Get temperature alaram RGB LED value.

        :param: int alarm_reg: temperature alarm RGB LED register, RGB_LOW_TEMP_REG: Low temperature alarm RGB LED value register, RGB_HIGH_TEMP_REG: High temperature alarm RGB LED value register.
        :returns: temperature alarm RGB LED value.
        :rtype: list, RGB color list in the format [R, G, B], values from 0 to 255.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.get_temp_alarm_led(alarm_reg)

<!-- .. method:: set_temp_alarm_led(alarm_reg, rgb) -->

        Set temperature alaram RGB LED value.

        :param: int alarm_reg: temperature alarm RGB LED register, RGB_LOW_TEMP_REG: Low temperature alarm RGB LED value register, RGB_HIGH_TEMP_REG: High temperature alarm RGB LED value register.
        :param int rgb: RGB color value (24-bit, range: 0 ~ 0xFFFFFF).

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.set_temp_alarm_led(alarm_reg, rgb)

<!-- .. method:: get_temp_buzzer_freq(alarm_reg) -->

        Get the buzzer frequency for temperature alarm.

        :param: int alarm_reg: temperature alarm buzzer frequency register, LOW_TEMP_FREQ_REG: Low temperature alarm buzzer frequency register, HIGH_TEMP_FREQ_REG: High temperature alarm buzzer frequency register.
        :returns: buzzer frequency.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.get_temp_buzzer_freq(alarm_reg)

<!-- .. method:: set_temp_buzzer_freq(alarm_reg, freq) -->

        Set the buzzer frequency for temperature alarm.

        :param: int alarm_reg: temperature alarm buzzer frequency register, LOW_TEMP_FREQ_REG: Low temperature alarm buzzer frequency register, HIGH_TEMP_FREQ_REG: High temperature alarm buzzer frequency register.
        :param: int freq: buzzer frequency, range: 20~20000Hz

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.set_temp_buzzer_freq(alarm_reg, freq)

<!-- .. method:: get_temp_alarm_interval(alarm_reg) -->

        Get the buzzer alarm interval.

        :param: int alarm_reg: buzzer alarm interval register, LOW_ALARM_INTER_REG: Low temperature alarm interval register, HIGH_ALARM_INTER_REG: High temperature alarm interval register.
        :returns: buzzer alarm interval. (unit: ms)
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.get_temp_alarm_interval(alarm_reg)

<!-- .. method:: set_temp_alarm_interval(alarm_reg, interval) -->

        Set the buzzer alarm interval.

        :param: int alarm_reg: buzzer alarm interval register, LOW_ALARM_INTER_REG: Low temperature alarm interval register, HIGH_ALARM_INTER_REG: High temperature alarm interval register.
        :param: int interval: alarm interval, range: 1 ~ 5000(unit: ms).

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.set_temp_alarm_interval(alarm_reg, interval)

<!-- .. method:: get_temp_buzzer_duty(duty_reg) -->

        Get the duty cycle of the temperature alarm buzzer signal.

        :param int duty_reg: Duty cycle register for the temperature alarm buzzer signal. LOW_ALARM_DUTY_REG: Register for low temperature alarm duty cycle. HIGH_ALARM_DUTY_REG: Register for high temperature alarm duty cycle.
        :returns: duty cycle.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.get_temp_buzzer_duty(duty_reg)

<!-- .. method:: set_temp_buzzer_duty(duty_reg, duty) -->

        Set the duty cycle of the temperature alarm buzzer signal.

        :param int duty_reg: Duty cycle register for the temperature alarm buzzer signal. LOW_ALARM_DUTY_REG: Register for low temperature alarm duty cycle. HIGH_ALARM_DUTY_REG: Register for high temperature alarm duty cycle.
        :param: int duty: Temperature alarm buzzer signal duty cycle, range: 0 ~ 255.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.set_temp_buzzer_duty(duty_reg, duty)

<!-- .. method:: get_buzzer_freq() -->

        Get the frequeny of the buzzer signal.

        :returns: frequeny(Hz)
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.get_buzzer_freq()

<!-- .. method:: set_buzzer_freq(freq) -->

        Set the frequeny of the buzzer signal.

        :param: int freq: buzzer signal frequency, range: 20 ~ 20000 (Hz).

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.set_buzzer_freq(freq)

<!-- .. method:: get_buzzer_duty() -->

        Get the duty cycle of the buzzer signal.

        :returns: Duty cycle
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.get_buzzer_duty()

<!-- .. method:: set_buzzer_duty(duty) -->

        Set the duty cycle of the buzzer signal.

        :param: int duty: Duty cycle, range: 0 ~ 255.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.set_buzzer_duty(duty)

<!-- .. method:: get_buzzer_control() -->

        Get the buzzer control status

        :returns: Returns the current buzzer control status
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.get_buzzer_control()

<!-- .. method:: set_buzzer_control(ctrl) -->

        Set the buzzer control status

        :param: int ctrl: Control value, 0 to turn off the buzzer, 1 to turn on the buzzer

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.set_buzzer_control(ctrl)

<!-- .. method:: get_rgb_led() -->

        Get the current RGB LED value

        :returns: The current RGB LED values in the format [r, g, b]
        :rtype: list

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.get_rgb_led()

<!-- .. method:: set_rgb_led(rgb) -->

        Set the RGB LED value

        :param: int rgb: RGB value in the range of 0 ~ 0xFFFFFF

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.set_rgb_led(rgb)

<!-- .. method:: get_button_status() -->

        Get the button status

        :returns: Button status, either 0 (not pressed) or 1 (pressed)
        :rtype: bool

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.get_button_status()

<!-- .. method:: save_config_setting() -->

        Save configuration settings

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.save_config_setting()

<!-- .. method:: get_chip_temperature() -->

        Get the chip temperature

        :returns: Chip temperature in Celsius (°C)
        :rtype: float

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.get_chip_temperature()

<!-- .. method:: get_device_spec(mode) -->

        Get device specifications

        :returns: Device specifications
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.get_device_spec()

<!-- .. method:: set_i2c_address(addr) -->

        Set the I2C address of the device

        :param: int addr: I2C address range: 1 ~ 127.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                unit_ncir2_0.set_i2c_address(addr)
