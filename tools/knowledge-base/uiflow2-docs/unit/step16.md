# Step16 Unit

<!-- .. sku: U198 -->

<!-- .. include:: ../refs/unit.step16.ref -->

This library is the driver for Unit Step16.

Support the following products:

    |Unit Step16|

## UiFlow2 Example

#### Read Encoder

Open the |cores3_step16_unit_example.m5f2| project in UiFlow2.

This example shows how to read and display encoder readings.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Read Encoder

This example shows how to read and display encoder readings.

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
from unit import Step16Unit

title0 = None
label1 = None
label_val = None
i2c0 = None
step16_0 = None
val = None

def setup():
    global title0, label1, label_val, i2c0, step16_0, val
    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("UnitStep16 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label1 = Widgets.Label(
        "Encoder Value:", 10, 55, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24
    )
    label_val = Widgets.Label("0", 205, 55, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    step16_0 = Step16Unit(i2c0, 0x48)
    print((str("i2c addr: ") + str((step16_0.get_addr()))))
    print((str("version: ") + str((step16_0.get_firmware_version()))))
    step16_0.set_led_mode(Step16Unit.AUTO_OFF, 5)
    step16_0.set_led_brightness(80)
    print((str("rgb brightness: ") + str((step16_0.get_rgb_brightness()))))
    print((str("rgb value: ") + str((step16_0.get_rgb_value()))))
    if step16_0.get_rgb_power():
        print("RGB power on")
    else:
        print("RG B power off")
    step16_0.set_rgb_power(True)
    step16_0.set_rgb_value(0x3333FF)

def loop():
    global title0, label1, label_val, i2c0, step16_0, val
    M5.update()
    val = step16_0.get_encoder_value()
    label_val.setText(str(val))

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

#### Step16Unit

## Step16Unit
Create an Step16Unit object.

:param I2C i2c: I2C port,
:param int | list | tuple addr: Step16Unit Slave Address

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from unit import Step16Unit

        unit_step16_0 = Step16Unit(i2c0, 0x48)

### `get_encoder_value`
Get the current encoder value (0~15).

:returns: Encoder value.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        value = unit_step16_0.get_encoder_value()

### `set_encoder_cw_increase`
Configure whether clockwise rotation increases encoder value.

:param enable:
    - True: Clockwise rotation increases the encoder value.
    - False: Clockwise rotation decreases the encoder value.
:type enable: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_step16_0.set_encoder_cw_increase(True)
        unit_step16_0.set_encoder_cw_increase(False)

### `get_encoder_cw_increase`
Get current encoder direction mode.

:returns: 1 for increasing clockwise, 0 for decreasing.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        direction = unit_step16_0.get_encoder_cw_increase()

### `set_led_mode`
Set LED display mode.

:param mode: LED mode type.
    0 = always off,
    1 = always on,
    2 = auto-off mode with `seconds` as timeout.
:type mode: int
:param seconds: Timeout in seconds if `mode` is 2 (auto-off).
:type seconds: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_step16_0.set_led_mode(0)         # Always off
        unit_step16_0.set_led_mode(1)         # Always on
        unit_step16_0.set_led_mode(2, 10)     # Auto-off after 10 seconds

### `get_led_mode`
Get LED display mode.

The LED mode values:

- `0x00` : Always Off.
- `0xFE` : Always On.
- `0x00` ~ `0xFD` : Auto off times in seconds.

:returns: LED display mode.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_step16_0.get_led_mode()

### `set_led_brightness`
Set LED brightness (0~100).

:param brightness int: Brightness level.
:type brightness: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_step16_0.set_led_brightness(80)

### `get_led_brightness`
Get current LED brightness.

:returns: Brightness level.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        brightness = unit_step16_0.get_led_brightness()
        print("Brightness:", brightness)

### `set_rgb_power`
Turn the RGB light power ON or OFF.

:param enable: True to turn on the RGB light, False to turn it off.
:type enable: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_step16_0.set_rgb_power(True)   # Turn ON RGB light
        unit_step16_0.set_rgb_power(False)  # Turn OFF RGB light

### `get_rgb_power`
Get the current power status of the RGB light.

:returns: True if the RGB light is ON, False if OFF.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        power_on = unit_step16_0.get_rgb_power()

### `set_rgb_brightness`
Set the brightness of the RGB light (0~100%).

:param brightness: Brightness percentage (0~100).
:type brightness: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_step16_0.set_rgb_brightness(80)  # Set RGB brightness to 80%

### `get_rgb_brightness`
Get the current RGB brightness level (0~100%).

:returns: Current RGB brightness percentage (0~100).
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        brightness = unit_step16_0.get_rgb_brightness()
        print("RGB Brightness:", brightness)

### `set_rgb_value`
Set RGB LED color using a 24-bit integer.

:param color: A 24-bit integer representing the RGB color (e.g., 0xFF8040 for R=255, G=128, B=64).
              Format is (R << 16) | (G << 8) | B.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_step16_0.set_rgb_value()

### `get_rgb_value`
Get current RGB LED color.

:returns: Tuple of (r, g, b)
:rtype: tuple

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        r, g, b = unit_step16_0.get_rgb_value()

### `save_led_config`
Save current LED mode and brightness settings.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_step16_0.save_led_config()

### `save_rgb_config`
Save current RGB color settings.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_step16_0.save_rgb_config()

### `set_addr`
Set the device's I2C address.

:param new_addr: New I2C address (0x08~0x77).
:type new_addr: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        unit_step16_0.set_addr(0x49)

### `get_addr`
Get the current I2C device address.

:returns: I2C address.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        addr = unit_step16_0.get_addr()

### `get_firmware_version`
Get the firmware version.

:returns:  firmware version.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        addr = unit_step16_0.get_firmware_version()
