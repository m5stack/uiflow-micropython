Chain ENV
=========

.. Product SKU: U234.

.. include:: ../refs/chain.env.ref

This library is the driver for Chain ENV.

Support the following products:

    |Chain ENV|

UiFlow2 Example
---------------

Environmental readings
^^^^^^^^^^^^^^^^^^^^^^

Open the |m5basic_chain_env_basic_example.m5f2| project in UiFlow2.

Connect Chain ENV as the first device on M5Stack Basic UART2 (TX=21, RX=22). The screen displays temperature (degrees Celsius), humidity (%), pressure (hPa), and altitude (m), refreshed every 500 ms. Set SEA_LEVEL_PRESSURE_PA to the current local sea-level pressure. The initial Shenzhen test reference is 101330 Pa (1013.3 hPa).

UiFlow2 Code Block:

    |m5basic_chain_env_basic_example.png|

MicroPython Example
-------------------

Environmental readings
^^^^^^^^^^^^^^^^^^^^^^

Connect Chain ENV as the first device on M5Stack Basic UART2 (TX=21, RX=22). The screen displays temperature (degrees Celsius), humidity (%), pressure (hPa), and altitude (m), refreshed every 500 ms. Set SEA_LEVEL_PRESSURE_PA to the current local sea-level pressure. The initial Shenzhen test reference is 101330 Pa (1013.3 hPa).

MicroPython Code Block:

    .. literalinclude:: ../../../examples/chain/env/m5basic_chain_env_basic_example.py
        :language: python
        :linenos:

**API**
-------

ENVChain
^^^^^^^^

.. autoclass:: chain.env.ENVChain
    :members: ODR_1HZ, ODR_1_5625HZ, ODR_2HZ, ODR_3_125HZ, ODR_4HZ, ODR_6_25HZ, ODR_8HZ, ODR_12_5HZ, ODR_16HZ, ODR_25HZ, ODR_32HZ, ODR_50HZ, ODR_64HZ, ODR_100HZ, ODR_128HZ, ODR_200HZ, ODR_VALUES, SENSOR_AHT20, SENSOR_SPA06, ALARM_NONE, ALARM_TEMPERATURE, ALARM_HUMIDITY, ALARM_PRESSURE, ALARM_ALTITUDE, ALARM_ALL, EVENT_TEMPERATURE_HIGH_CLEAR, EVENT_TEMPERATURE_HIGH, EVENT_TEMPERATURE_LOW, EVENT_TEMPERATURE_LOW_CLEAR, EVENT_HUMIDITY_HIGH_CLEAR, EVENT_HUMIDITY_HIGH, EVENT_HUMIDITY_LOW, EVENT_HUMIDITY_LOW_CLEAR, EVENT_PRESSURE_HIGH_CLEAR, EVENT_PRESSURE_HIGH, EVENT_PRESSURE_LOW, EVENT_PRESSURE_LOW_CLEAR, EVENT_ALTITUDE_HIGH_CLEAR, EVENT_ALTITUDE_HIGH, EVENT_ALTITUDE_LOW, EVENT_ALTITUDE_LOW_CLEAR, read_temperature_humidity, read_pressure_temperature_altitude, read_temperature, read_humidity, read_pressure, read_altitude, set_temperature_rate, get_temperature_rate, set_pressure_rate, get_pressure_rate, set_sea_level_pressure, get_sea_level_pressure, set_alarm_mode, get_alarm_mode, set_temperature_alarm_thresh, get_temperature_alarm_thresh, set_humidity_alarm_thresh, get_humidity_alarm_thresh, set_pressure_alarm_thresh, get_pressure_alarm_thresh, set_altitude_alarm_thresh, get_altitude_alarm_thresh, deinit, set_event_callback
    :undoc-members:
    :show-inheritance:
    :member-order: bysource
    :class-doc-from: both
    :exclude-members: read_i2c_mem, write_i2c_mem
