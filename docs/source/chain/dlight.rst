Chain DLight
============

.. Product SKU: U236.

.. include:: ../refs/chain.dlight.ref

This library is the driver for Chain DLight.

Support the following products:

    |Chain DLight|

UiFlow2 Example
---------------

DLight illuminance display
^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |m5core_chain_dlight_basic_example.m5f2| project in UiFlow2.

Connect Chain DLight as the first device on M5Stack Basic UART2 (TX=21, RX=22). The screen displays the live illuminance in lux.

UiFlow2 Code Block:

    |m5core_chain_dlight_basic_example.png|

MicroPython Example
-------------------

DLight illuminance display
^^^^^^^^^^^^^^^^^^^^^^^^^^

Connect Chain DLight as the first device on M5Stack Basic UART2 (TX=21, RX=22). The screen displays the live illuminance in lux.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/chain/dlight/m5core_chain_dlight_basic_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

DLightChain
^^^^^^^^^^^

.. autoclass:: chain.dlight.DLightChain
    :members: GAIN_1X, GAIN_3X, GAIN_6X, GAIN_9X, GAIN_18X, RESOLUTION_16BIT, RESOLUTION_17BIT, RESOLUTION_18BIT, RESOLUTION_19BIT, RESOLUTION_20BIT, MEASUREMENT_INTERVAL_50MS, MEASUREMENT_INTERVAL_100MS, MEASUREMENT_INTERVAL_500MS, MEASUREMENT_INTERVAL_1000MS, MEASUREMENT_INTERVAL_2000MS, EVENT_LOW, EVENT_HIGH, deinit, read_lux, enable_threshold_detection, disable_threshold_detection, is_threshold_detection_enabled, set_alarm_thresh, get_alarm_thresh, set_gain, get_gain, set_resolution, get_resolution, set_measurement_interval_ms, get_measurement_interval_ms, enable_event_reporting, disable_event_reporting, is_event_reporting_enabled, set_event_callback
    :undoc-members:
    :show-inheritance:
    :member-order: bysource
    :class-doc-from: both
    :exclude-members: read_i2c_mem, write_i2c_mem
