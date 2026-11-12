ADC Unit
========

.. include:: ../refs/unit.adc.ref

Support the following products:

    |ADC|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/adc/adc_cores3_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |adc_cores3_example.m5f2|


class ADCUnit
-------------

Constructors
------------

.. class:: ADCUnit(i2c0)

    Create an ADCUnit object.

    parameters is:
        - ``I2C0`` is I2C Port.

    UIFLOW2:

        |init.png|


.. _unit.ADCUnit.Methods:

Methods
-------

.. method:: ADCUnit.get_value()

    Gets the original value read by the adc(16 bit).

    UIFLOW2:

        |get_value.png|


.. method:: ADCUnit.get_voltage()

    Get the voltage value.

    UIFLOW2:

        |get_voltage.png|


.. method:: ADCUnit.get_operating_mode()

    Get working mode. (Single read or continuous read)

    UIFLOW2:

        |get_operating_mode.png|


.. method:: ADCUnit.get_data_rate()

    Get the read rate of the data.

    UIFLOW2:

        |get_data_rate.png|


.. method:: ADCUnit.get_gain()

    Get the gain multiple of the data.

    UIFLOW2:

        |get_gain.png|


.. method:: ADCUnit.set_operating_mode(mode)

    Set working mode: ``0`` for continuous conversion or ``1`` for single conversion.

    UIFLOW2:

        |set_operating_mode.png|


.. method:: ADCUnit.set_data_rate(data_rate)

    Set the data acquisition rate in samples per second: ``8``, ``16``, ``32``, or ``128``.

    UIFLOW2:

        |set_data_rate.png|


.. method:: ADCUnit.set_gain(gain)

    Set the gain multiple for reading data: ``1``, ``2``, ``4``, or ``8``.

    UIFLOW2:

        |set_gain.png|
