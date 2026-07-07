# MQ Unit

<!-- .. sku: U199 -->

<!-- .. include:: ../refs/unit.mq.ref -->

This is the driver library of MQ Unit, which is used to obtain data from the
MQ sensor.

Support the following products:

    |MQ|

## UiFlow2 Example

#### get MQ ADC value

Open the |mq_core2_example.m5f2| project in UiFlow2.

This example gets the ADC value of the MQ Unit and displays it on the screen.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### get MQ ADC value

This example gets the ADC value of the MQ Unit and displays it on the screen.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from hardware import I2C
from hardware import Pin
from unit import MQUnit

page0 = None
label0 = None
label1 = None
label2 = None
i2c0 = None
mq_0 = None

valid = None

def setup():
    global page0, label0, label1, label2, i2c0, mq_0, valid

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    label0 = m5ui.M5Label(
        "Valid Flag:",
        x=1,
        y=76,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label1 = m5ui.M5Label(
        "ADC 8bits:0",
        x=1,
        y=111,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label2 = m5ui.M5Label(
        "ADC 12bits:0",
        x=1,
        y=145,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    mq_0 = MQUnit(i2c0, 0x11)
    mq_0.set_mq_mode(1)
    page0.screen_load()

def loop():
    global page0, label0, label1, label2, i2c0, mq_0, valid
    M5.update()
    valid = mq_0.get_valid_tags()
    if valid:
        label0.set_text(str((str("Valid Flag:") + str(valid))))
        label1.set_text(str((str("ADC 8bits:") + str((mq_0.get_adc_value(0))))))
        label2.set_text(str((str("ADC 12bits:") + str((mq_0.get_adc_value(1))))))
    else:
        label0.set_text(str("Valid Flag: Wait heating"))

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

#### MQUnit

## MQUnit
Create a MQUnit object.

:param I2C i2c: The I2C bus the MQ Unit is connected to.
:param int address: The I2C address of the device. Default is 0x11.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from hardware import I2C
        from unit import MQUnit

        i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
        tof_0 = MQUnit(i2c0)

### `set_mq_mode`
Set the working mode of the MQ sensor.

:param int mode: Working mode value.

Option:
    - 0 : Measurement off
    - 1 : Continuous heating mode
    - 2 : Pin Level Switching Mode

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        mq_0.set_mq_mode(1)

### `get_mq_mode`
Get the current working mode of the MQ sensor.

:returns: Current working mode value.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        mode = mq_0.get_mq_mode()

### `set_led_status`
Set the LED status.

:param int status: When the LED is set to on, it lights up when a valid tag is detected, and the brightness is proportional to the ADC value, and it turns off when no tag is detected.

MicroPython Code Block:

    .. code-block:: python

        mq_0.set_led_status(1)

### `get_led_status`
Get the LED status.

:returns: True if LED status is on, False otherwise.
:rtype: bool

MicroPython Code Block:

    .. code-block:: python

        led_on = mq_0.get_led_status()

### `set_heat_time`
Set heater high and low level time.

:param int high_level_time: Time for high heating level.
:param int low_level_time: Time for low heating level.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        mq_0.set_heat_time(30, 5)

### `get_heat_time`
Get heater high and low level time.

:returns: [high_level_time, low_level_time]
:rtype: [int, int]

MicroPython Code Block:

    .. code-block:: python

        times = mq_0.get_heat_time()

### `get_adc_value`
Get ADC value.

:param int precision: 0 for 8-bit, 1 for 12-bit.
:returns: ADC value.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        value = mq_0.get_adc_value(1)

### `get_valid_tags`
Check if valid tags are detected.

:returns: True if valid tags detected, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        valid = mq_0.get_valid_tags()

### `get_ntc_adc_value`
Get internal NTC ADC value.

:param int precision: 0 for 8-bit, 1 for 12-bit.
:returns: NTC ADC value.
:rtype: int

MicroPython Code Block:

    .. code-block:: python

        ntc = mq_0.get_ntc_adc_value(1)

### `get_ntc_res_value`
Get internal NTC resistance value.

:returns: Resistance value.
:rtype: int

MicroPython Code Block:

    .. code-block:: python

        res = mq_0.get_ntc_res_value()

### `get_voltage`
Get voltage value from a specific channel.

:param int channle: Channel number.
:returns: Voltage value.
:rtype: int

MicroPython Code Block:

    .. code-block:: python

        voltage = mq_0.get_voltage(0)

### `get_firmware_version`
Get firmware version.

:returns: Firmware version.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        ver = mq_0.get_firmware_version()

### `get_i2c_address`
Get current I2C address.

:returns: MQ Unit I2C address, Default is 0x11.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        addr = mq_0.get_i2c_address()

### `set_i2c_address`
Set new I2C address.

:param int addr: New I2C address (0x08~0x77).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        mq_0.set_i2c_address(0x3A)
