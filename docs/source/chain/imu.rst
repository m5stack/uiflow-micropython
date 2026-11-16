Chain IMU
=========

.. Product SKU: U235.

.. include:: ../refs/chain.imu.ref

This library is the driver for Chain IMU.

Support the following products:

    |Chain IMU|

UiFlow2 Example
---------------

IMU sensor display
^^^^^^^^^^^^^^^^^^

Open the |m5core_chain_imu_basic_example.m5f2| project in UiFlow2.

Connect Chain IMU as the first device on M5Stack Basic UART2 (TX=21, RX=22). The screen has a centered "Chain IMU" title, three X/Y/Z columns for acceleration (m/s2) and angular velocity (rad/s), and a temperature reading (degrees Celsius) at the bottom. Readings refresh every 100 ms. Acceleration and angular velocity are rounded to two decimal places, and temperature to one decimal place.

UiFlow2 Code Block:

    |m5core_chain_imu_basic_example.png|

MicroPython Example
-------------------

IMU sensor display
^^^^^^^^^^^^^^^^^^

Connect Chain IMU as the first device on M5Stack Basic UART2 (TX=21, RX=22). The screen has a centered "Chain IMU" title, three X/Y/Z columns for acceleration (m/s2) and angular velocity (rad/s), and a temperature reading (degrees Celsius) at the bottom. Readings refresh every 100 ms. Acceleration and angular velocity are rounded to two decimal places, and temperature to one decimal place.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/chain/imu/m5core_chain_imu_basic_example.py
        :language: python
        :linenos:

**API**
-------

IMUChain
^^^^^^^^

.. autoclass:: chain.imu.IMUChain
    :members: ACCEL_RANGE_2G, ACCEL_RANGE_4G, ACCEL_RANGE_8G, ACCEL_RANGE_16G, GYRO_RANGE_125DPS, GYRO_RANGE_250DPS, GYRO_RANGE_500DPS, GYRO_RANGE_1000DPS, GYRO_RANGE_2000DPS, ODR_POWER_DOWN, ODR_1_6HZ, ODR_12_5HZ, ODR_26HZ, ODR_52HZ, ODR_104HZ, ODR_208HZ, ODR_416HZ, ODR_833HZ, ODR_1660HZ, ODR_3330HZ, ODR_6660HZ, ACCEL_RANGES, GYRO_RANGES, ACCEL_ODR_VALUES, GYRO_ODR_VALUES, ALARM_NONE, ALARM_ACCEL, ALARM_GYRO, ALARM_TEMPERATURE, ALARM_ALL, EVENT_ACCEL_CLEAR, EVENT_ACCEL_TRIGGER, EVENT_GYRO_CLEAR, EVENT_GYRO_TRIGGER, EVENT_TEMPERATURE_HIGH_CLEAR, EVENT_TEMPERATURE_HIGH, EVENT_TEMPERATURE_LOW, EVENT_TEMPERATURE_LOW_CLEAR, read_accel, read_gyro, read_accel_raw, read_gyro_raw, read_temperature, set_accel_range, get_accel_range, set_gyro_range, get_gyro_range, set_accel_odr, get_accel_odr, set_gyro_odr, get_gyro_odr, set_alarm_mode, get_alarm_mode, set_motion_alarm_thresh, get_motion_alarm_thresh, set_temperature_alarm_thresh, get_temperature_alarm_thresh, deinit, set_event_callback
    :undoc-members:
    :show-inheritance:
    :member-order: bysource
    :class-doc-from: both
    :exclude-members: read_i2c_mem, write_i2c_mem
