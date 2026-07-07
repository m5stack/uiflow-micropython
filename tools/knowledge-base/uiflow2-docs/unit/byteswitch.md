
# ByteSwitch Unit

<!-- .. sku:U191 -->
<!-- .. include:: ../refs/unit.byteswitch.ref -->

Unit ByteSwitch is an 8-switch touch switch input unit equipped with 8 switch inputs and 9 WS2812C RGB LEDs. It uses the STM32 microcontroller and supports I2C communication. The board includes two Port A interfaces and supports cascading multiple Unit ByteSwitch modules, making it suitable for complex systems. It can achieve switch input detection and dynamic lighting feedback, ideal for smart home control, gaming devices, educational platforms, industrial status displays, and interactive exhibitions.

Support the following products:

|ByteSwitchUnit|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from unit import ByteSwitchUnit
import time

title0 = None
label0 = None
label1 = None
i2c0 = None
byteswitch_0 = None

state_byte = None
i = None

def setup():
    global title0, label0, label1, i2c0, byteswitch_0, state_byte, i

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "ByteSwitch CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 4, 87, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 5, 125, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    byteswitch_0 = ByteSwitchUnit(i2c0, 0x46)
    byteswitch_0.set_led_show_mode(ByteSwitchUnit.BYTESWITCH_LED_USER_MODE)
    byteswitch_0.set_indicator_color(0x33FF33)
    for i in range(8):
        byteswitch_0.set_led_color(i, 0xFF0000, ByteSwitchUnit.BYTESWITCH_LED_USER_MODE)
        byteswitch_0.set_indicator_brightness(255)
        time.sleep(0.2)
        if i != 7:
            byteswitch_0.set_led_color(i + 1, 0x000000, ByteSwitchUnit.BYTESWITCH_LED_USER_MODE)
    time.sleep(1)
    for i in range(7, -1, -1):
        byteswitch_0.set_led_color(i, 0x66FF99, ByteSwitchUnit.BYTESWITCH_LED_USER_MODE)
        time.sleep(0.2)
    time.sleep(1)
    byteswitch_0.set_led_show_mode(ByteSwitchUnit.BYTESWITCH_LED_SYS_MODE)
    for i in range(8):
        byteswitch_0.set_led_color(i, 0xFFFFFF, ByteSwitchUnit.BYTESWITCH_LED_SYS_MODE, False)
        byteswitch_0.set_led_color(i, 0xFF0000, ByteSwitchUnit.BYTESWITCH_LED_SYS_MODE, True)

def loop():
    global title0, label0, label1, i2c0, byteswitch_0, state_byte, i
    M5.update()
    state_byte = byteswitch_0.get_byte_switch_status()
    label0.setText(
        str(
            [
                (str("B0:") + str(((state_byte >> 0) & 0x01))),
                (str("B1:") + str(((state_byte >> 1) & 0x01))),
                (str("B2:") + str(((state_byte >> 2) & 0x01))),
                (str("B3:") + str(((state_byte >> 3) & 0x01))),
            ]
        )
    )
    label1.setText(
        str(
            [
                (str("B4:") + str(((state_byte >> 4) & 0x01))),
                (str("B5:") + str(((state_byte >> 5) & 0x01))),
                (str("B6:") + str(((state_byte >> 6) & 0x01))),
                (str("B7:") + str(((state_byte >> 7) & 0x01))),
            ]
        )
    )

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

    |byteswitch_cores3_example.m5f2|

## class ByteSwitchUnit

## Constructors

<!-- .. class:: ByteSwitchUnit(i2c, address) -->

    Initialize the ByteSwitchUnit with a specified I2C address.

    :param I2C i2c: The I2C interface instance for communication.
    :param int address: The I2C address of the ByteSwitchUnit, default is 0x46.

    UIFLOW2:

## Methods

<!-- .. method:: ByteSwitchUnit.get_byte_switch_state() -> int -->

    Get the status of all switchs as an integer, where each bit represents the state of each switch.

    UIFLOW2:

<!-- .. method:: ByteSwitchUnit.get_switch_state(num) -> bool -->

    Get the state of a specific switch.

    :param int num: The index of the switch (0-7).

    UIFLOW2:

<!-- .. method:: ByteSwitchUnit.get_led_show_mode() -> bool -->

    Get the current LED show mode.

    UIFLOW2:

<!-- .. method:: ByteSwitchUnit.set_led_show_mode(mode) -->

    Set the LED show mode.

    :param int mode: The LED show mode to set.

        Options:
            - ``BYTESWITCH_LED_USER_MODE``: 0
            - ``BYTESWITCH_LED_SYS_MODE``: 1

    UIFLOW2:

<!-- .. method:: ByteSwitchUnit.set_led_brightness(num, brightness) -->

    Set the brightness of a specific LED.

    :param int num: The index of the LED (0-7).
    :param int brightness: The brightness level (0-255).

    UIFLOW2:

<!-- .. method:: ByteSwitchUnit.get_led_brightness(num) -> int -->

    Get the brightness of a specific LED.

    :param int num: The index of the LED (0-7).

    UIFLOW2:

<!-- .. method:: ByteSwitchUnit.set_led_color(num, color, led_show_mode, btn_is_pressed) -->

    Set the color of a specific LED.

    :param int num: The index of the LED (0-7).
    :param int color: The RGB888 color value to set.
    :param int led_show_mode: The LED show mode, default is BYTESWITCH_LED_SYS_MODE.
    :param bool btn_is_pressed: Whether the switch is pressed (affects color in SYS mode).

    UIFLOW2:

<!-- .. method:: ByteSwitchUnit.get_led_color(num, led_show_mode, btn_is_pressed) -> int -->

    Get the color of a specific LED.

    :param int num: The index of the LED (0-7).
    :param int led_show_mode: The LED show mode, default is BYTESWITCH_LED_SYS_MODE.
    :param bool btn_is_pressed: Whether the switch is pressed (affects color in SYS mode).

    UIFLOW2:

<!-- .. method:: ByteSwitchUnit.set_indicator_brightness(brightness) -->

    Set the brightness of the indicator LED.

    :param int brightness: The brightness level (0-255).

    UIFLOW2:

<!-- .. method:: ByteSwitchUnit.get_indicator_brightness() -> int -->

    Get the brightness of the indicator LED.

    UIFLOW2:

<!-- .. method:: ByteSwitchUnit.set_indicator_color(color) -->

    Set the color of the indicator LED in RGB888 format.

    :param int color: The RGB888 color value to set.

    UIFLOW2:

<!-- .. method:: ByteSwitchUnit.get_indicator_color() -> int -->

    Get the color of the indicator LED in RGB888 format.

    UIFLOW2:

<!-- .. method:: ByteSwitchUnit.rgb888_to_rgb233(color) -->

    Convert an RGB888 color value to RGB233 format.

    :param int color: The RGB888 color value as a 32-bit integer.

<!-- .. method:: ByteSwitchUnit.set_rgb233(num, color) -->

    Set the color of a specific LED in RGB233 format.

    :param int num: The index of the LED (0-7).
    :param int color: The RGB233 color value to set.

<!-- .. method:: ByteSwitchUnit.get_rgb233(num) -->

    Get the color of a specific LED in RGB233 format.

    :param int num: The index of the LED (0-7).

<!-- .. method:: ByteSwitchUnit.set_irq_enable(enable) -->

    Enable or disable IRQ functionality.

    :param bool enable: Whether to enable (True) or disable (False) IRQ.

<!-- .. method:: ByteSwitchUnit.get_irq_enable() -->

    Get the current IRQ enable status.

<!-- .. method:: ByteSwitchUnit.save_to_flash() -->

    Save the current user settings to flash.

    UIFLOW2:

<!-- .. method:: ByteSwitchUnit.get_firmware_version() -> int -->

    Get the firmware version of the ByteSwitchUnit.

    UIFLOW2:

<!-- .. method:: ByteSwitchUnit.set_i2c_address(new_addr) -->

    Set a new I2C address for the ByteSwitchUnit.

    :param int new_addr: The new I2C address to set. Must be in the range 0x08 to 0x77.

    UIFLOW2:

<!-- .. method:: ByteSwitchUnit.get_i2c_address() -> int -->

    Get the current I2C address of the ByteSwitchUnit.

    UIFLOW2:
