
# Heart Unit

<!-- .. include:: ../refs/unit.heart.ref -->

MAX30100 is a complete pulse oximetry and heart-rate sensor system solution designed for the demanding requirements of wearable devices.

Support the following products:

|HeartUnit|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import HeartUnit

label0 = None
labelHeart = None
i2c0 = None
heart_0 = None

def setup():
    global label0, labelHeart, i2c0, heart_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Heart Rate", 57, 18, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu40)
    labelHeart = Widgets.Label("label1", 82, 111, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu56)

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
    heart_0 = HeartUnit(i2c0, 0x57)
    heart_0.start()

def loop():
    global label0, labelHeart, i2c0, heart_0
    M5.update()
    labelHeart.setText(str(heart_0.get_heart_rate()))

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            heart_0.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

```

UIFLOW2 Example:

<!-- .. only:: builder_html -->

    |core_heart_unit_example.m5f2|

## class HeartUnit

## Constructors

<!-- .. class:: HeartUnit(i2c, address) -->

    Initialize the HeartUnit.

    - ``i2c``: I2C port to use.
    - ``address``: I2C address of the HeartUnit.

    UIFLOW2:

## Methods

<!-- .. method:: HeartUnit.stop() -->

    Stop the HeartUnit.

    UIFLOW2:

<!-- .. method:: HeartUnit.start() -->

    Start the HeartUnit.

    UIFLOW2:

<!-- .. method:: HeartUnit.deinit() -->

    Deinitialize the HeartUnit.

    UIFLOW2:

<!-- .. method:: HeartUnit.get_heart_rate() -->

    Get the heart rate.

    UIFLOW2:

<!-- .. method:: HeartUnit.get_spo2() -->

    Get the SpO2.

    UIFLOW2:

<!-- .. method:: HeartUnit.get_ir() -->

    Get the IR value.

    UIFLOW2:

<!-- .. method:: HeartUnit.get_red() -->

    Get the red value.

    UIFLOW2:

<!-- .. method:: HeartUnit.set_mode(mode) -->

    Set the mode of the HeartUnit.

    :param int mode: The detect mode of the HeartUnit.
        Options:
        - ``HeartUnit.MODE_HR_ONLY``: Only heart rate
        - ``HeartUnit.MODE_SPO2_HR``: Heart rate and SpO2

    UIFLOW2:

<!-- .. method:: HeartUnit.set_led_current(led_current) -->

    Set the LED current of the HeartUnit.

    :param int led_current: The LED current of the HeartUnit.
        Options:
        - ``HeartUnit.LED_CURRENT_0MA``: 0mA
        - ``HeartUnit.LED_CURRENT_4_4MA``: 4.4mA
        - ``HeartUnit.LED_CURRENT_7_6MA``: 7.6mA
        - ``HeartUnit.LED_CURRENT_11MA``: 11mA
        - ``HeartUnit.LED_CURRENT_14_2MA``: 14.2mA
        - ``HeartUnit.LED_CURRENT_17_4MA``: 17.4mA
        - ``HeartUnit.LED_CURRENT_20_8MA``: 20.8mA
        - ``HeartUnit.LED_CURRENT_24MA``: 24mA
        - ``HeartUnit.LED_CURRENT_27_1MA``: 27.1mA
        - ``HeartUnit.LED_CURRENT_30_6MA``: 30.6mA
        - ``HeartUnit.LED_CURRENT_33_8MA``: 33.8mA
        - ``HeartUnit.LED_CURRENT_37MA``: 37mA
        - ``HeartUnit.LED_CURRENT_40_2MA``: 40.2mA
        - ``HeartUnit.LED_CURRENT_43_6MA``: 43.6mA
        - ``HeartUnit.LED_CURRENT_46_8MA``: 46.8mA
        - ``HeartUnit.LED_CURRENT_50MA``: 50mA

    UIFLOW2:

<!-- .. method:: HeartUnit.set_pulse_width(pulse_width) -->

    Set the pulse width of the HeartUnit.

    :param int pulse_width: The pulse width of the HeartUnit.
        Options:
        - ``HeartUnit.PULSE_WIDTH_200US_ADC_13``: 200us
        - ``HeartUnit.PULSE_WIDTH_400US_ADC_14``: 400us
        - ``HeartUnit.PULSE_WIDTH_800US_ADC_15``: 800us
        - ``HeartUnit.PULSE_WIDTH_1600US_ADC_16``: 1600us

    UIFLOW2:

<!-- .. method:: HeartUnit.set_sampling_rate(sampling_rate) -->

    Set the sampling rate of the HeartUnit.

    :param int sampling_rate: The sampling rate of the HeartUnit.
        Options:
        - ``HeartUnit.SAMPLING_RATE_50HZ``: 50Hz
        - ``HeartUnit.SAMPLING_RATE_100HZ``: 100Hz
        - ``HeartUnit.SAMPLING_RATE_167HZ``: 167Hz
        - ``HeartUnit.SAMPLING_RATE_200HZ``: 200Hz
        - ``HeartUnit.SAMPLING_RATE_400HZ``: 400Hz
        - ``HeartUnit.SAMPLING_RATE_600HZ``: 600Hz
        - ``HeartUnit.SAMPLING_RATE_800HZ``: 800Hz
        - ``HeartUnit.SAMPLING_RATE_1000HZ``: 1000Hz

    UIFLOW2:

## Constants

<!-- .. data:: HeartUnit.MODE_HR_ONLY -->

    Detect heart rate only.

<!-- .. data:: HeartUnit.MODE_SPO2_HR -->

    Detect heart rate and SpO2.
