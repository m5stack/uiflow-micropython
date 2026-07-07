# 8Servos Unit

<!-- .. sku: U165 -->

<!-- .. include:: ../refs/unit.servos8.ref -->

This is the driver library for the 8Servos Unit. It is a 8-channel servo
controller that can control up to 8 servos. It can be used to control the
angles of the servos, set the pulse width, and set the mode of the servos.

Support the following products:

    |8Servos Unit|

## UiFlow2 Example

#### servo control

Open the |cores3_servo_example.m5f2| project in UiFlow2.

This example controls the servo angle of the 8Servos Unit.

UiFlow2 Code Block:

Example output:

    None

#### rgb control

Open the |cores3_rgb_example.m5f2| project in UiFlow2.

This example controls the RGB LED of the 8Servos Unit.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### servo control

This example controls the servo angle of the 8Servos Unit.

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
from unit import Servos8Unit
import time

label0 = None
i2c0 = None
servos8_0 = None

def setup():
    global label0, i2c0, servos8_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label(
        "8Servos Unit", 92, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    servos8_0 = Servos8Unit(i2c0, 0x25)
    servos8_0.set_mode(3, 3)
    servos8_0.set_mode(3, 7)

def loop():
    global label0, i2c0, servos8_0
    M5.update()
    servos8_0.set_servo_angle(45, 3)
    servos8_0.set_servo_angle(45, 7)
    time.sleep(1)
    servos8_0.set_servo_angle(150, 3)
    servos8_0.set_servo_angle(150, 7)
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

Example output:

    None

#### rgb control

This example controls the RGB LED of the 8Servos Unit.

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
from unit import Servos8Unit
import time

label0 = None
i2c0 = None
servos8_0 = None

def setup():
    global label0, i2c0, servos8_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label(
        "8Servos Unit", 92, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    servos8_0 = Servos8Unit(i2c0, 0x25)
    servos8_0.set_mode(4, 0)

def loop():
    global label0, i2c0, servos8_0
    M5.update()
    servos8_0.set_rgb_led(0xFF0000, 0)
    time.sleep(1)
    servos8_0.set_rgb_led(0x33FF33, 0)
    time.sleep(1)
    servos8_0.set_rgb_led(0x3366FF, 0)
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

Example output:

    None

## **API**

#### Servos8Unit

## Servos8Unit
Create a servos 8 unit object.

:param i2c: The I2C bus the servos 8 unit is connected to.
:type i2c: machine.I2C | PAHUBUnit
:param int address: The I2C address of the device. Default is 0x25.

:raises UnitError: If the servos 8 unit is not connected.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from hardware import I2C
        from unit import Servos8Unit

        i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
        servos8_0 = Servos8Unit(i2c0, 0x25)

### `get_mode`
Get the current mode of a specific channel.

:param int channel: The channel number (0 to 7) to get the mode for.
:return: The mode of the specified channel.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        servos8_0.get_mode(0)

### `set_mode`
Set the mode of a specific channel.

:param int mode: The mode to set for the channel.
:param int channel: The channel number (0 to 7) to set the mode for.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        servos8_0.set_mode(0, 0)

### `get_digital_input`
Get the digital input value of a specific channel.

:param int channel: The channel number (0 to 7) to get the digital input for.
:return: The digital input value (True or False) of the specified channel.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        servos8_0.get_digital_input(0)

### `set_output_value`
Set the digital output value of a specific channel.

:param int value: The digital output value (0 or 1) to set for the channel.
:param int channel: The channel number (0 to 7) to set the digital output for.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        servos8_0.set_output_value(1, 0)

### `get_8bit_adc_raw`
Get the 8-bit ADC value of a specific channel.

:param int channel: The channel number (0 to 7) to get the 8-bit ADC value for.
:return: The 8-bit ADC value (0 to 255) of the specified channel.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        servos8_0.get_8bit_adc_raw(0)

### `get_12bit_adc_raw`
Get the 12-bit ADC value of a specific channel.

:param int channel: The channel number (0 to 7) to get the 12-bit ADC value for.
:return: The 12-bit ADC value (0 to 4095) of the specified channel.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        servos8_0.get_12bit_adc_raw(0)

### `set_servo_angle`
Set the servo angle of a specific channel.

:param int angle: The servo angle (0 to 180) to set for the channel.
:param int channel: The channel number (0 to 7) to set the servo angle for.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        servos8_0.set_servo_angle(90, 0)

### `get_servo_angle`
Get the servo angle of a specific channel.

:param int channel: The channel number (0 to 7) to get the servo angle for.
:return: The servo angle (0 to 180) of the specified channel.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        servos8_0.get_servo_angle(0)

### `set_servo_pulse`
Set the servo pulse of a specific channel.

:param int pulse: The servo pulse (500 to 2500) to set for the channel.
:param int channel: The channel number (0 to 7) to set the servo pulse for.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        servos8_0.set_servo_pulse(1500, 0)

### `get_servo_pulse`
Get the servo pulse of a specific channel.

:param int channel: The channel number (0 to 7) to get the servo pulse for.
:return: The servo pulse (500 to 2500) of the specified channel.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        servos8_0.get_servo_pulse(0)

### `set_rgb_led`
Set the RGB LED color of a specific channel.

:param int rgb: The RGB color value (0x000000 to 0xffffff) to set for the channel.
:param int channel: The channel number (0 to 7) to set the RGB LED color for.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        servos8_0.set_rgb_led(0xFF0000, 0)

### `get_rgb_led`
Get the RGB LED color of a specific channel.

:param int channel: The channel number (0 to 7) to get the RGB LED color for.
:return: The RGB color value (0x000000 to 0xffffff) of the specified channel.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        servos8_0.get_rgb_led(0)

### `set_pwm_dutycycle`
Set the PWM duty cycle of a specific channel.

:param int duty: The PWM duty cycle (0 to 100) to set for the channel.
:param int channel: The channel number (0 to 7) to set the PWM duty cycle for.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        servos8_0.set_pwm_dutycycle(50, 0)

### `get_input_current`
Get the input current of the servos 8 unit.

:return: The input current in Amperes.
:rtype: float

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        servos8_0.get_input_current()

### `get_device_spec`
Get the device specification.
:param int mode: The mode to get the specification for.
:return: The device specification value.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        servos8_0.get_device_spec(0xFE)

### `set_i2c_address`
Set the I2C address of the servos 8 unit.

:param int addr: The new I2C address (1 to 127) to set for the servos 8 unit.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        servos8_0.set_i2c_address(0x25)
