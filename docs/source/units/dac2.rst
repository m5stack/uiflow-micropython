DAC2 Unit
=========

.. include:: ../refs/unit.dac2.ref


The `Dac2` class interfaces with a GP8413 15-bit Digital to
Analog Converter (DAC), capable of converting digital signals into two channels
of analog voltage output, ranging from 0-5V and 0-10V.


Support the following products:

|DAC2Unit|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/dac2/cores3_dac2_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |cores3_dac2_example.m5f2|


class DAC2Unit
--------------

Constructors
------------

.. class:: DAC2Unit(i2c0, addr)

    Create an DAC2Unit object.

    - ``I2C0`` is I2C Port.
    - ``addr`` I2C address of the DAC (default is `0x59`)..

    UIFLOW2:

        |init.png|


.. _unit.DAC2Unit.Methods:

Methods
-------

.. method:: DAC2Unit.setDACOutputVoltageRange(_range)


    Sets the output voltage range of the DAC.

    - ``_range`` The DAC output voltage range, either `DAC2Unit.RANGE_5V` or `DAC2Unit.RANGE_10V`..

    UIFLOW2:

        |setDACOutputVoltageRange.png|

.. method:: DAC2Unit.setVoltage(voltage, channel=Dac2.CHANNEL_BOTH)


    Sets the output voltage of the DAC.

    - ``voltage``  Desired output voltage from 0.0 to range maximum (5V or 10V).
    - ``channel``  The DAC channel to set. Options are `Dac2.CHANNEL_0`, `Dac2.CHANNEL_1`, or `Dac2.CHANNEL_BOTH`.

    UIFLOW2:

        |setVoltage.png|


.. method:: DAC2Unit.setVoltageBoth(voltage0, voltage1)


    Sets the output voltage for both channels.

    - ``voltage0``  Desired output voltage from 0.0 to range maximum (5V or 10V).
    - ``voltage1``  Desired output voltage from 0.0 to range maximum (5V or 10V).

    UIFLOW2:

        |setVoltageBoth.png|
