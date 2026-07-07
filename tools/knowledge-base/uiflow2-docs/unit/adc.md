# ADC Unit

<!-- .. include:: ../refs/unit.adc.ref -->

Support the following products:

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
from unit import ADCUnit

label0 = None
i2c0 = None
adc_0 = None

def setup():
    global label0, i2c0, adc_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 16, 16, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    adc_0 = ADCUnit(i2c0)

def loop():
    global label0, i2c0, adc_0
    M5.update()
    label0.setText(str(adc_0.get_voltage()))

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

    |adc_cores3_example.m5f2|

## class ADCUnit

## Constructors

<!-- .. class:: ADCUnit(i2c0) -->

    Create an ADCUnit object.

    parameters is:
        - ``I2C0`` is I2C Port.

    UIFLOW2:

<!-- .. _unit.ADCUnit.Methods: -->

## Methods

<!-- .. method:: ADCUnit.get_value() -->

    Gets the original value read by the adc(16 bit).

    UIFLOW2:

<!-- .. method:: ADCUnit.get_voltage() -->

    Get the voltage value.

    UIFLOW2:

<!-- .. method:: ADCUnit.get_operating_mode() -->

    Get working mode. (Single read or continuous read)

    UIFLOW2:

<!-- .. method:: ADCUnit.get_data_rate() -->

    Get the read rate of the data.

    UIFLOW2:

<!-- .. method:: ADCUnit.get_gain() -->

    Get the gain multiple of the data.

    UIFLOW2:

<!-- .. method:: ADCUnit.operating_mode() -->

    Set working mode (single read or continuous read)

    UIFLOW2:

<!-- .. method:: ADCUnit.data_rate() -->

    Set the data acquisition rate.

    UIFLOW2:

<!-- .. method:: ADCUnit.gain() -->

    Set the gain multiple for reading data.

    UIFLOW2:
