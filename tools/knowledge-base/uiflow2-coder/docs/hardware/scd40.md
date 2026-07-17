
# SCD40

The SCD4x is Sensirion’s next generation miniature CO2 sensor. On-chip signal compensation is realized with the build-in SHT4x humidity and temperature sensor.

The specific support of the host for SCD40 is as follows:

     Controller         SCD40           |
     AirQ               S             |

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from hardware import *

label0 = None
rotary = None

def btnA_wasClicked_event(state):  # noqa: N802
    global label0, rotary
    rotary.reset_rotary_value()
    label0.setText(str(rotary.get_rotary_value()))

def setup():
    global label0, rotary

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("0", 96, 80, 1.0, 0xFFA000, 0x222222, Widgets.FONTS.DejaVu72)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btnA_wasClicked_event)

    rotary = Rotary()

def loop():
    global label0, rotary
    M5.update()
    if rotary.get_rotary_status():
        label0.setText(str(rotary.get_rotary_value()))

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

## class SCD40

## Constructors

### `class SCD40()`

    Initialize the SCD40 with the I2C interface and address.

## Methods

### `SCD40.available()`

    Check if the SCD40 sensor is available on the I2C bus.

### `SCD40.set_start_periodic_measurement()`

    Set the sensor into working mode, which takes about 5 seconds per measurement.

### `SCD40.set_stop_periodic_measurement()`

    Stop the measurement mode for the sensor.

### `SCD40.get_sensor_measurement()`

    Get temperature, humidity, and CO2 concentration from the sensor.

### `SCD40.is_data_ready()`

    Check if the data (temperature, humidity, CO2) is ready from the sensor.

### `SCD40.get_temperature_offset()`

    Get the temperature offset to be added to the reported measurements.

### `SCD40.set_temperature_offset(offset)`

    Set the maximum value of 374°C temperature offset.

    - Parameter `offset` (`int`): The temperature offset to set, default is 0.

### `SCD40.get_sensor_altitude()`

    Get the altitude value of the measurement location in meters above sea level.

### `SCD40.set_sensor_altitude(height)`

    Set the altitude value of the measurement location in meters above sea level.

    - Parameter `height` (`int`): The altitude in meters to set. Must be between 0 and 65535 meters.

### `SCD40.set_ambient_pressure(ambient_pressure)`

    Set the ambient pressure in hPa at any time to adjust CO2 calculations.

    - Parameter `ambient_pressure` (`int`): The ambient pressure in hPa, constrained to the range [0, 65535].

### `SCD40.set_force_calibration(target_co2)`

    Force the sensor to recalibrate with a given current CO2 level.

    - Parameter `target_co2` (`int`): The current CO2 concentration to be used for recalibration.

### `SCD40.get_calibration_enabled()`

    Get whether automatic self-calibration (ASC) is enabled or disabled.

### `SCD40.set_calibration_enabled(enabled)`

    Enable or disable automatic self-calibration (ASC).

    - Parameter `enabled` (`bool`): Set to True to enable ASC, or False to disable it.

### `SCD40.set_start_low_periodic_measurement()`

    Set the sensor into low power working mode, with about 30 seconds per measurement.

### `SCD40.data_isready()`

    Check if new data is available from the sensor.

### `SCD40.save_to_eeprom()`

    Save temperature offset, altitude offset, and self-calibration enable settings to EEPROM.

### `SCD40.get_serial_number()`

    Get a unique serial number for this sensor.

### `SCD40.set_self_test()`

    Perform a self-test, which can take up to 10 seconds.

### `SCD40.set_factory_reset()`

    Reset all configuration settings stored in the EEPROM and erase the FRC and ASC algorithm history.

### `SCD40.reinit()`

    Reinitialize the sensor by reloading user settings from EEPROM.

### `SCD40.set_single_shot_measurement_all()`

    Set the sensor to perform a single-shot measurement for CO2, humidity, and temperature.

### `SCD40.set_single_shot_measurement_ht()`

    Set the sensor to perform a single-shot measurement for humidity and temperature.

### `SCD40.set_sleep_mode()`

    Put the sensor into sleep mode to reduce current consumption.

### `SCD40.set_wake_up()`

    Wake up the sensor from sleep mode into idle mode.

### `SCD40.write_cmd(cmd_wr, value)`

    Write a command to the sensor.

    - Parameter `cmd_wr` (`int`): The command to write to the sensor.
    - Parameter `value` (`int`): The value to send with the command, if any.

### `SCD40.read_response(num)`

    Read the sensor's response.

    - Parameter `num` (`int`): The number of bytes to read from the sensor.

### `SCD40.check_crc(buf)`

    Check the CRC of the received data to ensure it is correct.

    - Parameter `buf` (`bytearray`): The buffer of bytes to check the CRC.

### `SCD40.crc8(buffer)`

    Calculate the CRC-8 checksum for a given buffer.

    - Parameter `buffer` (`bytearray`): The buffer of bytes to calculate the CRC for.
