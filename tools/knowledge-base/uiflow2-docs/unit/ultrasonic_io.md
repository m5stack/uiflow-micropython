
# UltrasoundIO Unit

<!-- .. sku:U098-B2 -->
<!-- .. include:: ../refs/unit.ultrasonic_io.ref -->

UNIT SONIC IO is a GPIO interface ultrasonic range sensor. This module features an RCWL-9620 ultrasonic distance measurement chip with a 16mm probe, which the ranging accuracy can reach 2cm-450cm (accuracy up to ±2%). This sensor determines the distance to a target by measuring time lapses between the transmitting and receiving of the pulse signal, users can directly obtain the distance value through IO control mode. It is ideal to apply in robotics obstacle avoidance, fluid level detection, and other applications that require you to perform measurements.

Support the following products:

|UltrasoundIOUnit|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import UltrasoundIOUnit

title1 = None
label0 = None
i2c0 = None
sonic_io_0 = None

def setup():
    global title1, label0, i2c0, sonic_io_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title1 = Widgets.Title(
        "UltrasoundUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 2, 116, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    sonic_io_0 = UltrasoundIOUnit(port=(8, 9))

def loop():
    global title1, label0, i2c0, sonic_io_0
    M5.update()
    label0.setText(str((str("Distance:") + str((sonic_io_0.get_target_distance(1))))))

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

    |ultrasonicio_cores3_example.m5f2|

## class UltrasoundIOUnit

## Constructors

<!-- .. class:: UltrasoundIOUnit(port, echo_timeout_us) -->

    Initialize the ultrasonic unit with the specified port and echo timeout.

    :param  port: A tuple representing the port pins for trigger (output) and echo (input).
    :param int echo_timeout_us: Timeout for the echo signal in microseconds, default is 1,000,000.

    UIFLOW2:

## Methods

<!-- .. method:: UltrasoundIOUnit.tx_pulse_rx_echo() -->

    Send a trigger pulse and wait to receive the echo response.

<!-- .. method:: UltrasoundIOUnit.get_target_distance(mode) -->

    Calculate the distance to the target based on echo response time.

    :param int mode: The unit of measurement for the distance. Use 1 for millimeters, 2 for centimeters.

    :returns: The distance to the target in the specified unit.

    UIFLOW2:
