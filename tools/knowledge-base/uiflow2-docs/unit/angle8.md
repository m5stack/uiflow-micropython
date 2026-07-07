
# Angle8 Unit

<!-- .. sku:U154 -->
<!-- .. include:: ../refs/unit.angle8.ref -->

UNIT 8Angle is an input unit integrating 8 adjustable potentiometers, internal STM32F030 microcomputer as acquisition and communication processor, and the host computer adopts I2C communication interface, each adjustable potentiometer corresponds to 1 RGB LED light, and there is also a physical toggle switch and its corresponding RGB LED light, containing 5V->3V3 DCDC circuit.

Support the following products:

|Angle8Unit|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import Angle8Unit
import m5utils
import time

title0 = None
label0 = None
label1 = None
label2 = None
i2c0 = None
angle8_0 = None

import math

map_value = None

def setup():
    global title0, label0, label1, label2, i2c0, angle8_0, map_value

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "8AngleUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 0, 58, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 0, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 0, 160, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    angle8_0 = Angle8Unit(i2c0, 0x43)
    angle8_0.set_led_rgb_from(1, 9, 0x33FF33, 100, 0)
    map_value = 0

def loop():
    global title0, label0, label1, label2, i2c0, angle8_0, map_value
    M5.update()
    map_value = round(m5utils.remap(angle8_0.get_adc8_raw(8), 0, 255, 0, 100))
    label0.setText(str((str("Switch:") + str((angle8_0.get_switch_status())))))
    label1.setText(str((str("CH1 8bit:") + str((angle8_0.get_adc8_raw(1))))))
    label2.setText(str((str("CH8 map value:") + str(map_value))))
    angle8_0.set_led_rgb_from(1, 9, 0x33FF33, map_value, 0)
    time.sleep(1)

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

    |angle8unit_cores3_example.m5f2|

## class Angle8Unit

## Constructors

<!-- .. class:: Angle8Unit(i2c, address) -->

    Initialize the Angle8Unit with the specified I2C interface and address.

    :param  i2c: The I2C or PAHUBUnit instance for communication.
    :param int address: The I2C address of the device (default is ANGLE8_ADDR).

    UIFLOW2:

## Methods

<!-- .. method:: Angle8Unit.available() -->

    Check if the device is available on the I2C bus.

<!-- .. method:: Angle8Unit.get_adc12_raw(channel) -->

    Get the raw 12-bit ADC value from the specified channel.

    :param int channel: The channel number (1 to 8).

    UIFLOW2:

<!-- .. method:: Angle8Unit.get_adc8_raw(channel) -->

    Get the raw 8-bit ADC value from the specified channel.

    :param int channel: The channel number (1 to 8).

    UIFLOW2:

<!-- .. method:: Angle8Unit.get_switch_status() -->

    Get the status of the switch button.

    UIFLOW2:

<!-- .. method:: Angle8Unit.set_led_rgb(channel, rgb, bright) -->

    Set the RGB color and brightness of the specified LED channel.

    :param int channel: The LED channel number (0 to 8).
    :param int rgb: The RGB color value (0x00 to 0xFFFFFF).
    :param int bright: The brightness level (0 to 100, default is 50).

    UIFLOW2:

<!-- .. method:: Angle8Unit.set_led_rgb_from(begin, end, rgb, bright, per_delay) -->

    Set the RGB color and brightness for a range of LED channels.

    :param int begin: The starting LED channel (0 to 8).
    :param int end: The ending LED channel (0 to 8).
    :param int rgb: The RGB color value (0x00 to 0xFFFFFF).
    :param int bright: The brightness level (0 to 100, default is 50).
    :param int per_delay: The delay in milliseconds between setting each channel (default is 0).

    UIFLOW2:

<!-- .. method:: Angle8Unit.set_angle_sync_bright(channel, rgb) -->

    Set the LED brightness synchronized with the angle value.

    :param int channel: The LED channel number (0 to 8).
    :param int rgb: The RGB color value (0x00 to 0xFFFFFF).

    UIFLOW2:

<!-- .. method:: Angle8Unit.get_device_spec(mode) -->

    Get device specifications such as firmware version or I2C address.

    :param int mode: The register to read (FW_VER_REG or I2C_ADDR_REG).

    UIFLOW2:

<!-- .. method:: Angle8Unit.set_i2c_address(address) -->

    Set a new I2C address for the device.

    :param int address: The new I2C address (1 to 127).

    UIFLOW2:

<!-- .. method:: Angle8Unit.readfrommem(reg, num) -->

    Read a specified number of bytes from a device register.

    :param  reg: The register address to read from.
    :param  num: The number of bytes to read.
