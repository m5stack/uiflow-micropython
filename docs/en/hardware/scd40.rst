
SCD40
=========
.. sku:U103
.. include:: ../refs/hardware.scd40.ref

The SCD4x is Sensirion’s next generation miniature CO2 sensor. On-chip signal compensation is realized with the build-in SHT4x humidity and temperature sensor.

The specific support of the host for SCD40 is as follows:

.. table::
    :widths: auto
    :align: center

    +-------------------+-----------------+
    | Controller        | SCD40           | 
    +===================+=================+
    | AirQ              | |S|             |
    +-------------------+-----------------+

.. |S| unicode:: U+2714


Micropython Example:

    .. literalinclude:: ../../../examples/hardware/scd40/airq_scd40_example.py
        :language: python
        :linenos:

UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |airq_scd40_example.m5f2|


class SCD40
-------------

Constructors
------------

.. class:: SCD40()

    Initialize the SCD40 with the I2C interface and address.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: SCD40.available()

    Check if the SCD40 sensor is available on the I2C bus.


.. method:: SCD40.set_start_periodic_measurement()

    Set the sensor into working mode, which takes about 5 seconds per measurement.


    UIFLOW2:

        |set_start_periodic_measurement.png|

.. method:: SCD40.set_stop_periodic_measurement()

    Stop the measurement mode for the sensor.


    UIFLOW2:

        |set_stop_periodic_measurement.png|

.. method:: SCD40.get_sensor_measurement()

    Get temperature, humidity, and CO2 concentration from the sensor.


.. method:: SCD40.is_data_ready()

    Check if the data (temperature, humidity, CO2) is ready from the sensor.

    UIFLOW2:

        |is_data_ready.png|

.. method:: SCD40.get_temperature_offset()

    Get the temperature offset to be added to the reported measurements.


    UIFLOW2:

        |get_temperature_offset.png|

.. method:: SCD40.set_temperature_offset(offset)

    Set the maximum value of 374°C temperature offset.

    :param int offset: The temperature offset to set, default is 0.

    UIFLOW2:

        |set_temperature_offset.png|

.. method:: SCD40.get_sensor_altitude()

    Get the altitude value of the measurement location in meters above sea level.


    UIFLOW2:

        |get_sensor_altitude.png|

.. method:: SCD40.set_sensor_altitude(height)

    Set the altitude value of the measurement location in meters above sea level.

    :param int height: The altitude in meters to set. Must be between 0 and 65535 meters.

    UIFLOW2:

        |set_sensor_altitude.png|

.. method:: SCD40.set_ambient_pressure(ambient_pressure)

    Set the ambient pressure in hPa at any time to adjust CO2 calculations.

    :param int ambient_pressure: The ambient pressure in hPa, constrained to the range [0, 65535].

    UIFLOW2:

        |set_ambient_pressure.png|

.. method:: SCD40.set_force_calibration(target_co2)

    Force the sensor to recalibrate with a given current CO2 level.

    :param int target_co2: The current CO2 concentration to be used for recalibration.

    UIFLOW2:

        |set_force_calibration.png|

.. method:: SCD40.get_calibration_enabled()

    Get whether automatic self-calibration (ASC) is enabled or disabled.


    UIFLOW2:

        |get_calibration_enabled.png|

.. method:: SCD40.set_calibration_enabled(enabled)

    Enable or disable automatic self-calibration (ASC).

    :param bool enabled: Set to True to enable ASC, or False to disable it.

    UIFLOW2:

        |set_calibration_enabled.png|

.. method:: SCD40.set_start_low_periodic_measurement()

    Set the sensor into low power working mode, with about 30 seconds per measurement.


    UIFLOW2:

        |set_start_low_periodic_measurement.png|

.. method:: SCD40.data_isready()

    Check if new data is available from the sensor.

.. method:: SCD40.save_to_eeprom()

    Save temperature offset, altitude offset, and self-calibration enable settings to EEPROM.


    UIFLOW2:

        |save_to_eeprom.png|

.. method:: SCD40.get_serial_number()

    Get a unique serial number for this sensor.


    UIFLOW2:

        |get_serial_number.png|

.. method:: SCD40.set_self_test()

    Perform a self-test, which can take up to 10 seconds.


    UIFLOW2:

        |set_self_test.png|

.. method:: SCD40.set_factory_reset()

    Reset all configuration settings stored in the EEPROM and erase the FRC and ASC algorithm history.


    UIFLOW2:

        |set_factory_reset.png|

.. method:: SCD40.reinit()

    Reinitialize the sensor by reloading user settings from EEPROM.


    UIFLOW2:

        |reinit.png|

.. method:: SCD40.set_single_shot_measurement_all()

    Set the sensor to perform a single-shot measurement for CO2, humidity, and temperature.

.. method:: SCD40.set_single_shot_measurement_ht()

    Set the sensor to perform a single-shot measurement for humidity and temperature.

.. method:: SCD40.set_sleep_mode()

    Put the sensor into sleep mode to reduce current consumption.

.. method:: SCD40.set_wake_up()

    Wake up the sensor from sleep mode into idle mode.

.. method:: SCD40.write_cmd(cmd_wr, value)

    Write a command to the sensor.

    :param int cmd_wr: The command to write to the sensor.
    :param int value: The value to send with the command, if any.

.. method:: SCD40.read_response(num)

    Read the sensor's response.

    :param int num: The number of bytes to read from the sensor.

.. method:: SCD40.check_crc(buf)

    Check the CRC of the received data to ensure it is correct.

    :param bytearray buf: The buffer of bytes to check the CRC.

.. method:: SCD40.crc8(buffer)

    Calculate the CRC-8 checksum for a given buffer.

    :param bytearray buffer: The buffer of bytes to calculate the CRC for.



