
# CO2 Unit

<!-- .. sku:U103 -->
<!-- .. include:: ../refs/unit.co2.ref -->

CO2Unit is a hardware module designed for measuring CO2 concentration, temperature, and humidity.
It communicates via I2C and provides functions for calibration, measurement, and configuration.

Support the following products:

|CO2Unit|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import CO2Unit

title0 = None
label0 = None
label1 = None
label2 = None
label3 = None
i2c0 = None
co2_0 = None

def setup():
    global title0, label0, label1, label2, label3, i2c0, co2_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("CO2Unit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("label0", 1, 44, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 1, 95, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 1, 146, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("label3", 1, 198, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    co2_0 = CO2Unit(i2c0)
    co2_0.set_start_periodic_measurement()

def loop():
    global title0, label0, label1, label2, label3, i2c0, co2_0
    if co2_0.is_data_ready():
        label0.setText(str("Data is ready."))
        label1.setText(str((str("CO2 ppm:") + str((co2_0.co2)))))
        label2.setText(str((str("Humidity:") + str((co2_0.humidity)))))
        label3.setText(str((str("Temperature:") + str((co2_0.temperature)))))
    else:
        label0.setText(str("Data not ready."))

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

    |co2_cores3_example.m5f2|

## class CO2Unit

## Constructors

<!-- .. class:: CO2Unit(i2c, address) -->

    Initialize the CO2Unit with the I2C interface and address.

    :param  i2c: I2C interface or PAHUBUnit instance for communication.
    :param int address: I2C address of the CO2 sensor, default is 0x62.

    UIFLOW2:

## Methods

<!-- .. method:: CO2Unit.available() -->

    Check if the CO2 unit is available on the I2C bus.

<!-- .. method:: CO2Unit.set_start_periodic_measurement() -->

    Set the sensor into working mode, which takes about 5 seconds per measurement.

    UIFLOW2:

<!-- .. method:: CO2Unit.set_stop_periodic_measurement() -->

    Stop the measurement mode for the sensor.

    UIFLOW2:

<!-- .. method:: CO2Unit.get_sensor_measurement() -->

    Get temperature, humidity, and CO2 concentration from the sensor.

<!-- .. method:: CO2Unit.is_data_ready() -->

    Check if the data (temperature, humidity, CO2) is ready from the sensor.

    UIFLOW2:

<!-- .. method:: CO2Unit.get_temperature_offset() -->

    Get the temperature offset to be added to the reported measurements.

    UIFLOW2:

<!-- .. method:: CO2Unit.set_temperature_offset(offset) -->

    Set the maximum value of 374°C temperature offset.

    :param int offset: The temperature offset to set, default is 0.

    UIFLOW2:

<!-- .. method:: CO2Unit.get_sensor_altitude() -->

    Get the altitude value of the measurement location in meters above sea level.

    UIFLOW2:

<!-- .. method:: CO2Unit.set_sensor_altitude(height) -->

    Set the altitude value of the measurement location in meters above sea level.

    :param int height: The altitude in meters to set. Must be between 0 and 65535 meters.

    UIFLOW2:

<!-- .. method:: CO2Unit.set_ambient_pressure(ambient_pressure) -->

    Set the ambient pressure in hPa at any time to adjust CO2 calculations.

    :param int ambient_pressure: The ambient pressure in hPa, constrained to the range [0, 65535].

    UIFLOW2:

<!-- .. method:: CO2Unit.set_force_calibration(target_co2) -->

    Force the sensor to recalibrate with a given current CO2 level.

    :param int target_co2: The current CO2 concentration to be used for recalibration.

    UIFLOW2:

<!-- .. method:: CO2Unit.get_calibration_enabled() -->

    Get whether automatic self-calibration (ASC) is enabled or disabled.

    UIFLOW2:

<!-- .. method:: CO2Unit.set_calibration_enabled(enabled) -->

    Enable or disable automatic self-calibration (ASC).

    :param bool enabled: Set to True to enable ASC, or False to disable it.

    UIFLOW2:

<!-- .. method:: CO2Unit.set_start_low_periodic_measurement() -->

    Set the sensor into low power working mode, with about 30 seconds per measurement.

    UIFLOW2:

<!-- .. method:: CO2Unit.data_isready() -->

    Check if new data is available from the sensor.

<!-- .. method:: CO2Unit.save_to_eeprom() -->

    Save temperature offset, altitude offset, and self-calibration enable settings to EEPROM.

    UIFLOW2:

<!-- .. method:: CO2Unit.get_serial_number() -->

    Get a unique serial number for this sensor.

    UIFLOW2:

<!-- .. method:: CO2Unit.set_self_test() -->

    Perform a self-test, which can take up to 10 seconds.

    UIFLOW2:

<!-- .. method:: CO2Unit.set_factory_reset() -->

    Reset all configuration settings stored in the EEPROM and erase the FRC and ASC algorithm history.

    UIFLOW2:

<!-- .. method:: CO2Unit.reinit() -->

    Reinitialize the sensor by reloading user settings from EEPROM.

    UIFLOW2:

<!-- .. method:: CO2Unit.set_single_shot_measurement_all() -->

    Set the sensor to perform a single-shot measurement for CO2, humidity, and temperature.

<!-- .. method:: CO2Unit.set_single_shot_measurement_ht() -->

    Set the sensor to perform a single-shot measurement for humidity and temperature.

<!-- .. method:: CO2Unit.set_sleep_mode() -->

    Put the sensor into sleep mode to reduce current consumption.

<!-- .. method:: CO2Unit.set_wake_up() -->

    Wake up the sensor from sleep mode into idle mode.

<!-- .. method:: CO2Unit.write_cmd(cmd_wr, value) -->

    Write a command to the sensor.

    :param int cmd_wr: The command to write to the sensor.
    :param int value: The value to send with the command, if any.

<!-- .. method:: CO2Unit.read_response(num) -->

    Read the sensor's response.

    :param int num: The number of bytes to read from the sensor.

<!-- .. method:: CO2Unit.check_crc(buf) -->

    Check the CRC of the received data to ensure it is correct.

    :param bytearray buf: The buffer of bytes to check the CRC.

<!-- .. method:: CO2Unit.crc8(buffer) -->

    Calculate the CRC-8 checksum for a given buffer.

    :param bytearray buffer: The buffer of bytes to calculate the CRC for.
