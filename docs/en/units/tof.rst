ToF Unit
========

.. include:: ../refs/unit.tof.ref

Support the following products:

    |ToFUnit|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/tof/tof_core_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |tof_core_example.m5f2|


class ToFUnit
-------------

Constructors
------------

.. class:: ToFUnit(i2c: I2C, address: int = 0x29, io_timeout_ms: int = 0)

    Create a DLight object.

    :param i2c: the I2C object.
    :param address: the I2C address of the device. Default is 0x23.
    :param io_timeout_ms: the timeout of I2C communication. Default is 0ms.

    UIFLOW2:

        |init.png|


.. _unit.ToFUnit.Methods:

Methods
-------

.. method:: ToFUnit.get_distance() -> float

    Get distance in centimeters.

    :return: distance in millimeters.

    UIFLOW2:

        |get_distance.png|


.. method:: ToFUnit.get_data_ready() -> bool

    Get data ready status.

    :return: data ready status.

    UIFLOW2:

        |get_data_ready.png|


.. method:: ToFUnit.get_range() -> int

    Get distance in millimeters.

    :return: distance in millimeters.

    UIFLOW2:

        |get_range.png|

.. method:: ToFUnit.is_continuous_mode() -> bool

    Get continuous mode status.

    :return: continuous mode status.

    UIFLOW2:

        |is_continuous_mode.png|


.. method:: ToFUnit.get_measurement_timing_budget() -> int

    Get measurement timing budget. The budget is in microseconds.

    :return: measurement timing budget. The budget is in microseconds.

    UIFLOW2:

        |get_measurement_timing_budget.png|


.. method:: ToFUnit.set_measurement_timing_budget(budget_us: int) -> None

    Set measurement timing budget. The budget_us is in microseconds.

    :param budget_us: measurement timing budget in microseconds.

    UIFLOW2:

        |set_measurement_timing_budget.png|


.. method:: ToFUnit.get_signal_rate_limit() -> float

    Get signal rate limit.

    :return: signal rate limit.

    UIFLOW2:

        |get_signal_rate_limit.png|


.. method:: ToFUnit.set_signal_rate_limit(val: float) -> None

    Set signal rate limit.

    :param val: signal rate limit.

    UIFLOW2:

        |set_signal_rate_limit.png|


.. method:: ToFUnit.start_continuous() -> None

    Start continuous mode.

    UIFLOW2:

        |start_continuous.png|


.. method:: ToFUnit.stop_continuous() -> None

    Stop continuous mode.

    UIFLOW2:

        |stop_continuous.png|


.. method:: ToFUnit.set_address(new_address: int) -> None

    Set I2C address.

    :param new_address: new I2C address.

    UIFLOW2:

        |set_address.png|
