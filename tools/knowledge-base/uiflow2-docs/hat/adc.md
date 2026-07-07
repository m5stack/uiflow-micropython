# ADC Hat

<!-- .. include:: ../refs/hat.adc.ref -->

The following products are supported:

    |ADC|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from hat import ADCHat

label0 = None
i2c0 = None
hat_adc_0 = None

def setup():
    global label0, i2c0, hat_adc_0

    M5.begin()
    label0 = Widgets.Label("label0", 39, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(26), sda=Pin(0), freq=100000)
    hat_adc_0 = ADCHat(i2c0)

def loop():
    global label0, i2c0, hat_adc_0
    M5.update()
    label0.setText(str(hat_adc_0.get_voltage()))

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

    |stickc_plus2_adc_example.m5f2|

## class CANUnit

## Constructors

<!-- .. class:: ADCHat(i2c, address: int = 0x48) -->

    Create an instance of the ADC Hat.

    :param i2c: I2C bus
    :param address: I2C address of the ADC Hat

    UIFLOW2:

ADCHat class inherits ADCUnit class, See :ref:`unit.ADCUnit.Methods <unit.ADCUnit.Methods>` for more details.
