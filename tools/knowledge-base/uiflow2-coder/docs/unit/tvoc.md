
# TVOC Unit

TVOCUnit is a hardware module for measuring Total Volatile Organic Compounds (TVOC) and equivalent CO2 (eCO2). It is based on the SGP30 sensor and communicates via the I2C interface. The class supports configuration and measurement operations.

Support the following products:

TVOCUnit

Micropython Example:

```python
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

## class TVOCUnit

## Constructors

### `class TVOCUnit(i2c, address)`

    Initialize the TVOCUnit with the specified I2C interface and address.

    - Parameter `i2c`: The I2C interface or PAHUBUnit object for communication with the sensor.
    - Parameter `address` (`int`): The I2C address of the TVOC unit. Defaults to 0x58.

## Methods

### `TVOCUnit.available()`

    Check whether the TVOC/eCO2 unit is available.

### `TVOCUnit.set_baseline_co2_tvoc(co2eq, tvoc)`

    Set the baseline values for CO2 and TVOC measurements.

    - Parameter `co2eq` (`int`): The CO2 equivalent baseline value to be set.
    - Parameter `tvoc` (`int`): The TVOC baseline value to be set.

### `TVOCUnit.set_relative_humidity(humidity_per, temp_c)`

    Set the relative humidity and temperature for accurate air quality measurement.

    - Parameter `humidity_per` (`float`): The relative humidity in percentage (%).
    - Parameter `temp_c` (`float`): The ambient temperature in Celsius (°C).

### `TVOCUnit.iaq_init()`

    Initialize the IAQ (Indoor Air Quality) algorithm for the sensor.

### `TVOCUnit.measure_iaq()`

    Measure the CO2 equivalent (CO2eq) and TVOC values.

### `TVOCUnit.get_iaq_baseline()`

    Retrieve the IAQ algorithm baseline values for CO2eq and TVOC.

### `TVOCUnit.set_iaq_baseline(co2eq, tvoc)`

    Set the previously recorded IAQ algorithm baseline values for CO2eq and TVOC.

    - Parameter `co2eq`: The CO2 equivalent baseline value.
    - Parameter `tvoc`: The TVOC baseline value.

### `TVOCUnit.set_absolute_humidity(absolute_humidity)`

    Set the absolute humidity compensation for the sensor. To disable, set the value to 0.

    - Parameter `absolute_humidity`: The absolute humidity value to set.

### `TVOCUnit.measure_test()`

    Run the on-chip self-test.

### `TVOCUnit.get_feature_set()`

    Retrieve the feature set of the sensor.

### `TVOCUnit.measure_raw()`

    Return raw H2 and Ethanol signals for part verification and testing.

### `TVOCUnit.get_serial()`

    Retrieve the sensor serial ID.

### `TVOCUnit.co2eq()`

    Retrieve the Carbon Dioxide Equivalent (CO2eq) in parts per million (ppm).

### `TVOCUnit.baseline_co2eq()`

    Retrieve the baseline value for CO2eq.

### `TVOCUnit.tvoc()`

    Retrieve the Total Volatile Organic Compound (TVOC) in parts per billion (ppb).

### `TVOCUnit.baseline_tvoc()`

    Retrieve the baseline value for TVOC.

### `TVOCUnit.raw_h2()`

    Retrieve the raw H2 signal value.

### `TVOCUnit.raw_ethanol()`

    Retrieve the raw Ethanol signal value.

### `TVOCUnit.convert_r_to_a_humidity(temp_c, r_humidity_perc, fixed_point)`

    Convert relative humidity to absolute humidity based on the sensor&#x27;s equation.

    - Parameter `temp_c`: The ambient temperature in Celsius (°C).
    - Parameter `r_humidity_perc`: The relative humidity in percentage (%).
    - Parameter `fixed_point` (`bool`): Whether to return the value in 8.8 fixed-point format. Defaults to True.
