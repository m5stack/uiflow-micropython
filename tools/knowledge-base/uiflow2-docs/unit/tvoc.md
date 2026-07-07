
# TVOC Unit

<!-- .. sku:U088 -->
<!-- .. include:: ../refs/unit.tvoc.ref -->

TVOCUnit is a hardware module for measuring Total Volatile Organic Compounds (TVOC) and equivalent CO2 (eCO2). It is based on the SGP30 sensor and communicates via the I2C interface. The class supports configuration and measurement operations.

Support the following products:

|TVOCUnit|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import TVOCUnit
import time

label3 = None
title0 = None
label0 = None
label1 = None
label2 = None
i2c0 = None
tvoc_0 = None

def setup():
    global label3, title0, label0, label1, label2, i2c0, tvoc_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label3 = Widgets.Label("label3", 0, 193, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    title0 = Widgets.Title(
        "TVOCUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 0, 44, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 0, 95, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 0, 146, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    tvoc_0 = TVOCUnit(i2c0)

def loop():
    global label3, title0, label0, label1, label2, i2c0, tvoc_0
    M5.update()
    label0.setText(str((str("TVOC:") + str((tvoc_0.tvoc())))))
    label1.setText(str((str("CO2:") + str((tvoc_0.co2eq())))))
    label2.setText(str((str("Ethanol:") + str((tvoc_0.raw_ethanol())))))
    label3.setText(str((str("H2:") + str((tvoc_0.raw_h2())))))
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

    |tvoc_cores3_example.m5f2|

## class TVOCUnit

## Constructors

<!-- .. class:: TVOCUnit(i2c, address) -->

    Initialize the TVOCUnit with the specified I2C interface and address.

    :param  i2c: The I2C interface or PAHUBUnit object for communication with the sensor.
    :param int address: The I2C address of the TVOC unit. Defaults to 0x58.

    UIFLOW2:

## Methods

<!-- .. method:: TVOCUnit.available() -->

    Check whether the TVOC/eCO2 unit is available.

<!-- .. method:: TVOCUnit.set_baseline_co2_tvoc(co2eq, tvoc) -->

    Set the baseline values for CO2 and TVOC measurements.

    :param int co2eq: The CO2 equivalent baseline value to be set.
    :param int tvoc: The TVOC baseline value to be set.

    UIFLOW2:

<!-- .. method:: TVOCUnit.set_relative_humidity(humidity_per, temp_c) -->

    Set the relative humidity and temperature for accurate air quality measurement.

    :param float humidity_per: The relative humidity in percentage (%).
    :param float temp_c: The ambient temperature in Celsius (°C).

    UIFLOW2:

<!-- .. method:: TVOCUnit.iaq_init() -->

    Initialize the IAQ (Indoor Air Quality) algorithm for the sensor.

<!-- .. method:: TVOCUnit.measure_iaq() -->

    Measure the CO2 equivalent (CO2eq) and TVOC values.

<!-- .. method:: TVOCUnit.get_iaq_baseline() -->

    Retrieve the IAQ algorithm baseline values for CO2eq and TVOC.

<!-- .. method:: TVOCUnit.set_iaq_baseline(co2eq, tvoc) -->

    Set the previously recorded IAQ algorithm baseline values for CO2eq and TVOC.

    :param  co2eq: The CO2 equivalent baseline value.
    :param  tvoc: The TVOC baseline value.

<!-- .. method:: TVOCUnit.set_absolute_humidity(absolute_humidity) -->

    Set the absolute humidity compensation for the sensor. To disable, set the value to 0.

    :param  absolute_humidity: The absolute humidity value to set.

<!-- .. method:: TVOCUnit.measure_test() -->

    Run the on-chip self-test.

<!-- .. method:: TVOCUnit.get_feature_set() -->

    Retrieve the feature set of the sensor.

<!-- .. method:: TVOCUnit.measure_raw() -->

    Return raw H2 and Ethanol signals for part verification and testing.

<!-- .. method:: TVOCUnit.get_serial() -->

    Retrieve the sensor serial ID.

<!-- .. method:: TVOCUnit.co2eq() -->

    Retrieve the Carbon Dioxide Equivalent (CO2eq) in parts per million (ppm).

    UIFLOW2:

<!-- .. method:: TVOCUnit.baseline_co2eq() -->

    Retrieve the baseline value for CO2eq.

    UIFLOW2:

<!-- .. method:: TVOCUnit.tvoc() -->

    Retrieve the Total Volatile Organic Compound (TVOC) in parts per billion (ppb).

    UIFLOW2:

<!-- .. method:: TVOCUnit.baseline_tvoc() -->

    Retrieve the baseline value for TVOC.

    UIFLOW2:

<!-- .. method:: TVOCUnit.raw_h2() -->

    Retrieve the raw H2 signal value.

    UIFLOW2:

<!-- .. method:: TVOCUnit.raw_ethanol() -->

    Retrieve the raw Ethanol signal value.

    UIFLOW2:

<!-- .. method:: TVOCUnit.convert_r_to_a_humidity(temp_c, r_humidity_perc, fixed_point) -->

    Convert relative humidity to absolute humidity based on the sensor&#x27;s equation.

    :param  temp_c: The ambient temperature in Celsius (°C).
    :param  r_humidity_perc: The relative humidity in percentage (%).
    :param bool fixed_point: Whether to return the value in 8.8 fixed-point format. Defaults to True.
