
# Color Unit

<!-- .. sku:U009 -->
<!-- .. include:: ../refs/unit.color.ref -->

Support the following products:

|ColorUnit|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import ColorUnit

title0 = None
label0 = None
label1 = None
label2 = None
i2c0 = None
color_0 = None

def setup():
    global title0, label0, label1, label2, i2c0, color_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "ColorUnit Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("lux:", 2, 59, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("color:", 2, 114, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("saturation:", 2, 166, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    color_0 = ColorUnit(i2c0)

def loop():
    global title0, label0, label1, label2, i2c0, color_0
    M5.update()
    label0.setText(str((str("Iux:") + str((color_0.get_lux())))))
    label1.setText(str((str("color:") + str((color_0.get_color_rgb_bytes())))))
    label2.setText(str((str("saturation:") + str((color_0.get_color_s())))))

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

    |color_core2_example.m5f2|

## class ColorUnit

## Constructors

<!-- .. class:: ColorUnit(i2c, address= _TCS3472_DEFAULT_ADDR) -->

    Initialize ColorUnit sensor with the given I2C interface and address.

    :param I2C i2c: The I2C bus instance for communication.
    :param int address: The I2C address of the sensor, default is _TCS3472_DEFAULT_ADDR(0x29).

    UIFLOW2:

## Methods

<!-- .. method:: ColorUnit.get_lux() -> float -->

    Get the lux value computed from the color channels.

    :return: The computed lux value as a float.

    UIFLOW2:

<!-- .. method:: ColorUnit.get_color_temperature() -> float -->

    Get the color temperature in degrees Kelvin.

    :return: The color temperature as a float in Kelvin.

    UIFLOW2:

<!-- .. method:: ColorUnit.get_color_rgb_bytes() -> tuple -->

    Get the RGB color detected by the sensor.

    :return: A tuple of red, green, and blue component values as bytes (0-255).

    UIFLOW2:

<!-- .. method:: ColorUnit.get_color_r() -> int -->

    Get the red component of the RGB color.

    :return: The red component value (0-255).

    UIFLOW2:

<!-- .. method:: ColorUnit.get_color_g() -> int -->

    Get the green component of the RGB color.

    :return: The green component value (0-255).

    UIFLOW2:

<!-- .. method:: ColorUnit.get_color_b() -> int -->

    Get the blue component of the RGB color.

    :return: The blue component value (0-255).

    UIFLOW2:

<!-- .. method:: ColorUnit.get_color_h() -> int -->

    Get the hue (H) value of the color in degrees.

    :return: The hue value as an integer in the range [0, 360].

    UIFLOW2:

<!-- .. method:: ColorUnit.get_color_s() -> float -->

    Get the saturation (S) value of the color.

    :return: The saturation value as a float in the range [0, 1].

    UIFLOW2:

<!-- .. method:: ColorUnit.get_color_v() -> float -->

    Get the value (V) of the color (brightness).

    :return: The value as a float in the range [0, 1].

    UIFLOW2:

<!-- .. method:: ColorUnit.get_color() -> int -->

    Get the RGB color as an integer value.

    :return: An integer representing the RGB color, with 8 bits per channel.

    UIFLOW2:

<!-- .. method:: ColorUnit.get_color565() -> int -->

    Get the RGB color in 5-6-5 format as an integer.
    :return: An integer representing the RGB color in 5-6-5 format.

    UIFLOW2:

<!-- .. method:: ColorUnit.get_active() -> bool -->

    Get the active state of the sensor.

    :return: True if the sensor is active, False if it is inactive.

    UIFLOW2:

<!-- .. method:: ColorUnit.set_active(val) -->

    Set the active state of the sensor.

    :param bool val: : True to activate the sensor, False to deactivate it.

    UIFLOW2:

<!-- .. method:: ColorUnit.get_integration_time() -> float -->

    Get the integration time of the sensor in milliseconds.

    :return: The integration time as a float.

    UIFLOW2:

<!-- .. method:: ColorUnit.set_integration_time(val) -->

    Set the integration time of the sensor.

    :param float val: : The desired integration time in milliseconds.
    :raise ValueError: If the integration time is out of the allowed range.

    UIFLOW2:

<!-- .. method:: ColorUnit.get_gain() -> int -->

    Get the gain of the sensor.

    :return: The gain value, which should be one of 1, 4, 16, or 60.

    UIFLOW2:

<!-- .. method:: ColorUnit.set_gain(val) -->

    Set the gain of the sensor.

    :param int val: : The desired gain value (1, 4, 16, or 60).
    :raise ValueError: If the gain is not one of the allowed values.

    UIFLOW2:

<!-- .. method:: ColorUnit.read_interrupt() -> bool -->

    Read the interrupt status.

    :return: True if the interrupt is set, False otherwise.

    UIFLOW2:

<!-- .. method:: ColorUnit.clear_interrupt() -->

    Clear the interrupt status of the sensor by writing to the interrupt register.

    UIFLOW2:

<!-- .. method:: ColorUnit.get_color_raw() -->

    Read the raw RGBC color detected by the sensor.

    :return: A tuple containing raw red, green, blue, and clear color data.

    UIFLOW2:

<!-- .. method:: ColorUnit.get_cycles() -->

    Get the persistence cycles of the sensor.

    :return: The persistence cycles or -1 if interrupts are disabled.

    UIFLOW2:

<!-- .. method:: ColorUnit.set_cycles(val) -->

    Set the persistence cycles for the sensor.

    :param int val: : The number of persistence cycles, or -1 to disable interrupts.
    :raise ValueError: If the value is not one of the permitted cycle values.

    UIFLOW2:

<!-- .. method:: ColorUnit.get_min_value() -->

    Get the minimum threshold value (AILT register) of the sensor.

    :return: The minimum threshold value.

    UIFLOW2:

<!-- .. method:: ColorUnit.set_min_value(val) -->

    Set the minimum threshold value (AILT register) of the sensor.

    :param int val: : The minimum threshold value to set.

    UIFLOW2:

<!-- .. method:: ColorUnit.get_max_value() -->

    Get the maximum threshold value (AIHT register) of the sensor.

    :return: The maximum threshold value.

    UIFLOW2:

<!-- .. method:: ColorUnit.set_max_value(val) -->

    Set the maximum threshold value (AIHT register) of the sensor.

    :param int val: : The maximum threshold value to set.

    UIFLOW2:

<!-- .. method:: ColorUnit.get_glass_attenuation() -->

    Get the Glass Attenuation factor used to compensate for lower light levels due to glass presence.

    :return: The glass attenuation factor (ga).

    UIFLOW2:

<!-- .. method:: ColorUnit.set_glass_attenuation(value) -->

    Set the Glass Attenuation factor used to compensate for lower light levels due to glass presence.

    :param float value: : The glass attenuation factor to set. Must be greater than or equal to 1.
    :raise ValueError: If the value is less than 1.

    UIFLOW2:
