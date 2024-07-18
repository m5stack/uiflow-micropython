ADC Hat
=======

.. include:: ../refs/hat.adc.ref

The following products are supported:

    |ADC|


Micropython Example:

    .. literalinclude:: ../../../examples/hat/adc/stickc_plus2_adc_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |stickc_plus2_adc_example.m5f2|


class CANUnit
-------------

Constructors
------------

.. class:: ADCHat(i2c, address: int = 0x48)

    Create an instance of the ADC Hat.

    :param i2c: I2C bus
    :param address: I2C address of the ADC Hat

    UIFLOW2:

        |init.png|


ADCHat class inherits ADCUnit class, See :ref:`unit.ADCUnit.Methods <unit.ADCUnit.Methods>` for more details.
