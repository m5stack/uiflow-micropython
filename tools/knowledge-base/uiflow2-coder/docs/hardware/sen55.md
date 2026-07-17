
# SEN55

The SEN5x is a unique sensor module family combining the measurement of critical air quality parameters – particulate matter, VOC, NOx, humidity, and temperature in a single package.

The specific support of the host for SEN55 is as follows:

     Controller         SEN55           |
     AirQ               S             |

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from hardware import *
import time

sen55 = None

def setup():
    global sen55

    M5.begin()
    Widgets.fillScreen(0xFFFFFF)

    sen55 = SEN55()
    sen55.set_power_state(True)
    sen55.set_work_mode(1)
    time.sleep(1)

def loop():
    global sen55
    M5.update()
    if sen55.get_data_ready_flag():
        print(sen55.get_pm1_0())
        print(sen55.get_pm2_5())
        print(sen55.get_pm4_0())
        print(sen55.get_pm10_0())
        print(sen55.get_humidity())
        print(sen55.get_temperature())
        print(sen55.get_voc())
        print(sen55.get_nox())
    time.sleep_ms(100)

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

## class SEN55

## Constructors

### `class SEN55()`

    Initialize the SEN55 sensor with I2C communication, setting the power control and ensuring the sensor is connected.

## Methods

### `SEN55.set_power_state(state)`

    Set the power state of the SEN55 sensor.

    - Parameter `state` (`bool`): The desired power state, True to power on, False to power off.

### `SEN55.get_power_state()`

    Get the current power state of the SEN55 sensor.

### `SEN55.available()`

    Check if the SEN55 sensor is connected via I2C.

### `SEN55.set_work_mode(mode)`

    Set the measurement mode of the SEN55 sensor.

    - Parameter `mode` (`int`): 1 to start measurement, 0 to stop measurement.

### `SEN55.get_sensor_data()`

    Get the sensor data including PM1.0, PM2.5, PM4.0, PM10.0, CO2, temperature, humidity, VOC, and NOx.

### `SEN55.get_data_ready_flag()`

    Check if the sensor data is ready to be read.

### `SEN55.set_temp_cmp_params(temp_offset, temp_offset_slope, time_constant)`

    Set the temperature compensation parameters for the sensor.

    - Parameter `temp_offset` (`int`): The temperature offset in the sensor&#x27;s compensation algorithm.
    - Parameter `temp_offset_slope` (`int`): The temperature offset slope in the sensor&#x27;s compensation algorithm.
    - Parameter `time_constant` (`int`): The time constant for the temperature compensation.

### `SEN55.get_temp_cmp_params()`

    Get the current temperature compensation parameters.

### `SEN55.set_warm_start_param(mode)`

    Set the warm start parameter for the sensor.

    - Parameter `mode` (`bool`): True to enable warm start, False to disable it.

### `SEN55.get_warm_start_param()`

    Get the current warm start parameter.

### `SEN55.set_voc_algo_tuning_params(voc_index_offset, voc_offset_hours, voc_gain_houes, gate_max_duration_min, std_initial, gain_factor)`

    Set the VOC algorithm tuning parameters, including index offset, time offsets, and gain factors.

    - Parameter `voc_index_offset` (`int`): The VOC index offset, default is 100.
    - Parameter `voc_offset_hours` (`int`): The VOC offset in hours, default is 12 hours.
    - Parameter `voc_gain_houes` (`int`): The VOC gain in hours, default is 12 hours.
    - Parameter `gate_max_duration_min` (`int`): Maximum gate duration in minutes, default is 180 minutes.
    - Parameter `std_initial` (`int`): The initial standard deviation, default is 50.
    - Parameter `gain_factor` (`int`): The gain factor for VOC, default is 230.

### `SEN55.get_voc_algo_tuning_params()`

    Get the current VOC algorithm tuning parameters.

    - Returns: A tuple of VOC tuning parameters: index offset, offset hours, gain hours, max gate duration, initial standard deviation, and gain factor.

### `SEN55.set_nox_algo_tuning_params(nox_index_offset, nox_offset_hours, nox_gain_houes, gate_max_duration_min, gain_factor)`

    Set the NOx algorithm tuning parameters, including index offset, time offsets, and gain factors. The standard deviation estimate is fixed at 50 for NOx.

    - Parameter `nox_index_offset` (`int`): The offset value for the NOx index.
    - Parameter `nox_offset_hours` (`int`): The time offset in hours for the NOx algorithm.
    - Parameter `nox_gain_houes` (`int`): The gain factor in hours for the NOx algorithm.
    - Parameter `gate_max_duration_min` (`int`): The maximum gate duration in minutes.
    - Parameter `gain_factor` (`int`): The gain factor for the NOx algorithm.

### `SEN55.get_nox_algo_tuning_params()`

    Get the current NOx algorithm tuning parameters.

    - Returns: A tuple of NOx tuning parameters: index offset, offset hours, gain hours, max gate duration, and gain factor.

### `SEN55.set_rht_acceleration_mode(mode)`

    Set the RHT acceleration mode, which affects how quickly the   device accelerates during measurement.

    - Parameter `mode` (`int`): The acceleration mode to set: 0 for low, 1 for high, or 2 for medium.

### `SEN55.get_rht_acceleration_mode()`

    Get the current RHT acceleration mode. This parameter can be changed in any state of the device, but it is applied only the next time starting a measurement. The parameter needs to be set before a new measurement is started.

    - Returns: The current acceleration mode: 0 for low, 1 for high, or 2 for medium.

### `SEN55.get_voc_algo_state() -> bytes`

    Get the current VOC algorithm state.

    - Returns: The VOC algorithm state in bytes.

### `SEN55.set_voc_algo_state(state)`

    Set the VOC algorithm state.

    - Parameter `state` (`bytes`): The VOC algorithm state to set, represented as bytes.

### `SEN55.set_start_fan_cleaning()`

    Start the fan cleaning process to remove contaminants from the sensor.

### `SEN55.get_auto_cleaning_interval() -> tuple`

    Get the current auto cleaning interval.

    - Returns: A tuple of the cleaning interval parameters.

### `SEN55.set_auto_cleaning_interval(interval)`

    Set the auto cleaning interval.

    - Parameter `interval` (`tuple`): A tuple representing the new auto cleaning interval.

### `SEN55.get_device_status() -> bytes`

    Get the current device status.

    - Returns: The device status in bytes.

### `SEN55.clear_device_status()`

    Clear the device status, resetting any error flags or states.

### `SEN55.get_serial_number() -> str`

    Get the unique serial number of the sensor.

    - Returns: The serial number of the sensor as a string.

### `SEN55.get_product_name() -> str`

    Get the product name of the sensor.

    - Returns: The product name of the sensor as a string.

### `SEN55.send_cmd(cmd, value, is_bytes)`

    Send a command to the sensor.

    - Parameter `cmd` (`int`): The command to send, represented as a 2-byte value.
    - Parameter `value`: Optional value to include with the command.
    - Parameter `is_bytes` (`bool`): A flag to indicate if the value is in bytes format.

### `SEN55.read_response(nbytes) -> bytes`

    Read the response from the sensor.

    - Returns: The response data as bytes.
    - Parameter `nbytes` (`int`): The number of bytes to read from the sensor.

### `SEN55.get_pm1_0() -> float`

    Get the PM1.0 concentration value in micrograms per cubic meter (µg/m³).

    - Returns: PM1.0 concentration in µg/m³.

### `SEN55.get_pm2_5() -> float`

    Get the PM2.5 concentration value in micrograms per cubic meter (µg/m³).

    - Returns: PM2.5 concentration in µg/m³.

### `SEN55.get_pm4_0() -> float`

    Get the PM4.0 concentration value in micrograms per cubic meter (µg/m³).

    - Returns: PM4.0 concentration in µg/m³.

### `SEN55.get_pm10_0() -> float`

    Get the PM10.0 concentration value in micrograms per cubic meter (µg/m³).

    - Returns: PM10.0 concentration in µg/m³.

### `SEN55.get_humidity() -> float`

    Get the humidity value in percentage (%).

    - Returns: Humidity in percentage.

### `SEN55.get_temperature() -> float`

    Get the temperature value in degrees Celsius (°C).

    - Returns: Temperature in °C.

### `SEN55.get_voc() -> float`

    Get the Volatile Organic Compound (VOC) concentration value in parts per billion (ppb).

    - Returns: VOC concentration in ppb.

### `SEN55.get_nox() -> float`

    Get the Nitrogen Oxide (NOx) concentration value in parts per billion (ppb).

    - Returns: NOx concentration in ppb.
