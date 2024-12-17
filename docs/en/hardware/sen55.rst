
SEN55
=====
.. sku:
.. include:: ../refs/hardware.sen55.ref

The SEN5x is a unique sensor module family combining the measurement of critical air quality parameters – particulate matter, VOC, NOx, humidity, and temperature in a single package.

The specific support of the host for SEN55 is as follows:

.. table::
    :widths: auto
    :align: center

    +-------------------+-----------------+
    | Controller        | SEN55           | 
    +===================+=================+
    | AirQ              | |S|             |
    +-------------------+-----------------+

.. |S| unicode:: U+2714

Micropython Example:

    .. literalinclude:: ../../../examples/hardware/sen55/airq_sen55_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |airq_sen55_example.m5f2|

class SEN55
-----------

Constructors
------------

.. class:: SEN55()

    Initialize the SEN55 sensor with I2C communication, setting the power control and ensuring the sensor is connected.

    UIFLOW2:

        |init.png|

Methods
-------

.. method:: SEN55.set_power_state(state)

    Set the power state of the SEN55 sensor.

    :param bool state: The desired power state, True to power on, False to power off.

    UIFLOW2:

        |set_power_state.png|

.. method:: SEN55.get_power_state()

    Get the current power state of the SEN55 sensor.


    UIFLOW2:

        |get_power_state.png|

.. method:: SEN55.available()

    Check if the SEN55 sensor is connected via I2C.


.. method:: SEN55.set_work_mode(mode)

    Set the measurement mode of the SEN55 sensor.

    :param int mode: 1 to start measurement, 0 to stop measurement.

    UIFLOW2:

        |set_work_mode.png|

.. method:: SEN55.get_sensor_data()

    Get the sensor data including PM1.0, PM2.5, PM4.0, PM10.0, CO2, temperature, humidity, VOC, and NOx.


.. method:: SEN55.get_data_ready_flag()

    Check if the sensor data is ready to be read.


    UIFLOW2:

        |get_data_ready_flag.png|

.. method:: SEN55.set_temp_cmp_params(temp_offset, temp_offset_slope, time_constant)

    Set the temperature compensation parameters for the sensor.

    :param int temp_offset: The temperature offset in the sensor&#x27;s compensation algorithm.
    :param int temp_offset_slope: The temperature offset slope in the sensor&#x27;s compensation algorithm.
    :param int time_constant: The time constant for the temperature compensation.

.. method:: SEN55.get_temp_cmp_params()

    Get the current temperature compensation parameters.

.. method:: SEN55.set_warm_start_param(mode)

    Set the warm start parameter for the sensor.

    :param bool mode: True to enable warm start, False to disable it.

.. method:: SEN55.get_warm_start_param()

    Get the current warm start parameter.

.. method:: SEN55.set_voc_algo_tuning_params(voc_index_offset, voc_offset_hours, voc_gain_houes, gate_max_duration_min, std_initial, gain_factor)

    Set the VOC algorithm tuning parameters, including index offset, time offsets, and gain factors.

    :param int voc_index_offset: The VOC index offset, default is 100.
    :param int voc_offset_hours: The VOC offset in hours, default is 12 hours.
    :param int voc_gain_houes: The VOC gain in hours, default is 12 hours.
    :param int gate_max_duration_min: Maximum gate duration in minutes, default is 180 minutes.
    :param int std_initial: The initial standard deviation, default is 50.
    :param int gain_factor: The gain factor for VOC, default is 230.

.. method:: SEN55.get_voc_algo_tuning_params()

    Get the current VOC algorithm tuning parameters.

    :return: A tuple of VOC tuning parameters: index offset, offset hours, gain hours, max gate duration, initial standard deviation, and gain factor.

.. method:: SEN55.set_nox_algo_tuning_params(nox_index_offset, nox_offset_hours, nox_gain_houes, gate_max_duration_min, gain_factor)

    Set the NOx algorithm tuning parameters, including index offset, time offsets, and gain factors. The standard deviation estimate is fixed at 50 for NOx.

    :param int nox_index_offset: The offset value for the NOx index.
    :param int nox_offset_hours: The time offset in hours for the NOx algorithm.
    :param int nox_gain_houes: The gain factor in hours for the NOx algorithm.
    :param int gate_max_duration_min: The maximum gate duration in minutes.
    :param int gain_factor: The gain factor for the NOx algorithm.

.. method:: SEN55.get_nox_algo_tuning_params()

    Get the current NOx algorithm tuning parameters.
    
    :return: A tuple of NOx tuning parameters: index offset, offset hours, gain hours, max gate duration, and gain factor.

.. method:: SEN55.set_rht_acceleration_mode(mode)

    Set the RHT acceleration mode, which affects how quickly the   device accelerates during measurement.

    :param int mode: The acceleration mode to set: 0 for low, 1 for high, or 2 for medium.

.. method:: SEN55.get_rht_acceleration_mode()

    Get the current RHT acceleration mode. This parameter can be changed in any state of the device, but it is applied only the next time starting a measurement. The parameter needs to be set before a new measurement is started.

    :return: The current acceleration mode: 0 for low, 1 for high, or 2 for medium.

.. method:: SEN55.get_voc_algo_state() -> bytes

    Get the current VOC algorithm state.

    :return: The VOC algorithm state in bytes.

.. method:: SEN55.set_voc_algo_state(state)

    Set the VOC algorithm state.

    :param bytes state: The VOC algorithm state to set, represented as bytes.


.. method:: SEN55.set_start_fan_cleaning()

    Start the fan cleaning process to remove contaminants from the sensor.

.. method:: SEN55.get_auto_cleaning_interval() -> tuple

    Get the current auto cleaning interval.

    :return: A tuple of the cleaning interval parameters.

.. method:: SEN55.set_auto_cleaning_interval(interval)

    Set the auto cleaning interval.

    :param tuple interval: A tuple representing the new auto cleaning interval.

.. method:: SEN55.get_device_status() -> bytes

    Get the current device status.

    :return: The device status in bytes.

.. method:: SEN55.clear_device_status()

    Clear the device status, resetting any error flags or states.

.. method:: SEN55.get_serial_number() -> str

    Get the unique serial number of the sensor.

    :return: The serial number of the sensor as a string.

.. method:: SEN55.get_product_name() -> str

    Get the product name of the sensor.

    :return: The product name of the sensor as a string.

.. method:: SEN55.send_cmd(cmd, value, is_bytes)

    Send a command to the sensor.

    :param int cmd: The command to send, represented as a 2-byte value.
    :param  value: Optional value to include with the command.
    :param bool is_bytes: A flag to indicate if the value is in bytes format.

.. method:: SEN55.read_response(nbytes) -> bytes

    Read the response from the sensor.

    :return: The response data as bytes.
    :param int nbytes: The number of bytes to read from the sensor.

.. method:: SEN55.get_pm1_0() -> float

    Get the PM1.0 concentration value in micrograms per cubic meter (µg/m³).

    :return: PM1.0 concentration in µg/m³.

    UIFLOW2:

        |get_pm1_0.png|

.. method:: SEN55.get_pm2_5() -> float

    Get the PM2.5 concentration value in micrograms per cubic meter (µg/m³).

    :return: PM2.5 concentration in µg/m³.

    UIFLOW2:

        |get_pm2_5.png|

.. method:: SEN55.get_pm4_0() -> float

    Get the PM4.0 concentration value in micrograms per cubic meter (µg/m³).

    :return: PM4.0 concentration in µg/m³.

    UIFLOW2:

        |get_pm4_0.png|

.. method:: SEN55.get_pm10_0() -> float

    Get the PM10.0 concentration value in micrograms per cubic meter (µg/m³).

    :return: PM10.0 concentration in µg/m³.

    UIFLOW2:

        |get_pm10_0.png|

.. method:: SEN55.get_humidity() -> float

    Get the humidity value in percentage (%).

    :return: Humidity in percentage.

    UIFLOW2:

        |get_humidity.png|

.. method:: SEN55.get_temperature() -> float

    Get the temperature value in degrees Celsius (°C).

    :return: Temperature in °C.

    UIFLOW2:

        |get_temperature.png|

.. method:: SEN55.get_voc() -> float

    Get the Volatile Organic Compound (VOC) concentration value in parts per billion (ppb).

    :return: VOC concentration in ppb.

    UIFLOW2:

        |get_voc.png|

.. method:: SEN55.get_nox() -> float

    Get the Nitrogen Oxide (NOx) concentration value in parts per billion (ppb).

    :return: NOx concentration in ppb.

    UIFLOW2:

        |get_nox.png|