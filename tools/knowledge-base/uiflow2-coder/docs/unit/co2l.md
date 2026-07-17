
# CO2L Unit

UNIT CO2L is a digital air CO2 concentration detection unit with a single-measurement low-power mode, built-in Sensirion's SCD41 sensor and power buck circuitry, and I2C communication. The unit is suitable for the measurement of air ambient conditions with a typical accuracy of ± (40 ppm + 5 % reading) for CO2 measurements over a measuring range of 400 ppm – 5000 ppm while measuring ambient temperature and humidity.

Support the following products:

CO2LUnit

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import CO2LUnit

title0 = None
label0 = None
label1 = None
label2 = None
label3 = None
i2c0 = None
co2l_0 = None

def setup():
    global title0, label0, label1, label2, label3, i2c0, co2l_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "CO2LUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 1, 44, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 1, 95, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 1, 146, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("label3", 1, 198, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    co2l_0 = CO2LUnit(i2c0)
    co2l_0.set_start_periodic_measurement()

def loop():
    global title0, label0, label1, label2, label3, i2c0, co2l_0
    if co2l_0.is_data_ready():
        label0.setText(str("Data is ready."))
        label1.setText(str((str("CO2 ppm:") + str((co2l_0.co2)))))
        label2.setText(str((str("Humidity:") + str((co2l_0.humidity)))))
        label3.setText(str((str("Temperature:") + str((co2l_0.temperature)))))
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

## class CO2LUnit

## Constructors

### `class CO2LUnit(i2c, address)`

    Initialize the CO2LUnit with the I2C interface and address.

    - Parameter `i2c`: I2C interface or PAHUBUnit instance for communication.
    - Parameter `address` (`int`): I2C address of the CO2 sensor, default is 0x62.

## Methods

### `CO2LUnit.available()`

    Check if the CO2 unit is available on the I2C bus.

### `CO2LUnit.set_start_periodic_measurement()`

    Set the sensor into working mode, which takes about 5 seconds per measurement.

### `CO2LUnit.set_stop_periodic_measurement()`

    Stop the measurement mode for the sensor.

### `CO2LUnit.get_sensor_measurement()`

    Get temperature, humidity, and CO2 concentration from the sensor.

### `CO2LUnit.is_data_ready()`

    Check if the data (temperature, humidity, CO2) is ready from the sensor.

### `CO2LUnit.get_temperature_offset()`

    Get the temperature offset to be added to the reported measurements.

### `CO2LUnit.set_temperature_offset(offset)`

    Set the maximum value of 374°C temperature offset.

    - Parameter `offset` (`int`): The temperature offset to set, default is 0.

### `CO2LUnit.get_sensor_altitude()`

    Get the altitude value of the measurement location in meters above sea level.

### `CO2LUnit.set_sensor_altitude(height)`

    Set the altitude value of the measurement location in meters above sea level.

    - Parameter `height` (`int`): The altitude in meters to set. Must be between 0 and 65535 meters.

### `CO2LUnit.set_ambient_pressure(ambient_pressure)`

    Set the ambient pressure in hPa at any time to adjust CO2 calculations.

    - Parameter `ambient_pressure` (`int`): The ambient pressure in hPa, constrained to the range [0, 65535].

### `CO2LUnit.set_force_calibration(target_co2)`

    Force the sensor to recalibrate with a given current CO2 level.

    - Parameter `target_co2` (`int`): The current CO2 concentration to be used for recalibration.

### `CO2LUnit.get_calibration_enabled()`

    Get whether automatic self-calibration (ASC) is enabled or disabled.

### `CO2LUnit.set_calibration_enabled(enabled)`

    Enable or disable automatic self-calibration (ASC).

    - Parameter `enabled` (`bool`): Set to True to enable ASC, or False to disable it.

### `CO2LUnit.set_start_low_periodic_measurement()`

    Set the sensor into low power working mode, with about 30 seconds per measurement.

### `CO2LUnit.data_isready()`

    Check if new data is available from the sensor.

### `CO2LUnit.save_to_eeprom()`

    Save temperature offset, altitude offset, and self-calibration enable settings to EEPROM.

### `CO2LUnit.get_serial_number()`

    Get a unique serial number for this sensor.

### `CO2LUnit.set_self_test()`

    Perform a self-test, which can take up to 10 seconds.

### `CO2LUnit.set_factory_reset()`

    Reset all configuration settings stored in the EEPROM and erase the FRC and ASC algorithm history.

### `CO2LUnit.reinit()`

    Reinitialize the sensor by reloading user settings from EEPROM.

### `CO2LUnit.set_single_shot_measurement_all()`

    Set the sensor to perform a single-shot measurement for CO2, humidity, and temperature.

### `CO2LUnit.set_single_shot_measurement_ht()`

    Set the sensor to perform a single-shot measurement for humidity and temperature.

### `CO2LUnit.set_sleep_mode()`

    Put the sensor into sleep mode to reduce current consumption.

### `CO2LUnit.set_wake_up()`

    Wake up the sensor from sleep mode into idle mode.

### `CO2LUnit.write_cmd(cmd_wr, value)`

    Write a command to the sensor.

    - Parameter `cmd_wr` (`int`): The command to write to the sensor.
    - Parameter `value` (`int`): The value to send with the command, if any.

### `CO2LUnit.read_response(num)`

    Read the sensor's response.

    - Parameter `num` (`int`): The number of bytes to read from the sensor.

### `CO2LUnit.check_crc(buf)`

    Check the CRC of the received data to ensure it is correct.

    - Parameter `buf` (`bytearray`): The buffer of bytes to check the CRC.

### `CO2LUnit.crc8(buffer)`

    Calculate the CRC-8 checksum for a given buffer.

    - Parameter `buffer` (`bytearray`): The buffer of bytes to calculate the CRC for.
