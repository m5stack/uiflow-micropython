DAC2 Hat
========

.. include:: ../refs/hat.dac2.ref

The following products are supported:

    |DAC2Hat|

Micropython Example:

    .. literalinclude:: ../../../examples/hat/dac2/stickc_plus2_dac2_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |stickc_plus2_dac2_example.m5f2|


class DAC2Hat
-------------

Constructors
------------

.. class:: DAC2Hat(i2c, address: int | list | tuple = 0x59)

    Create a DAC2 Hat object.

    :param i2c: I2C object
    :param address: I2C address of the DAC2 Hat

    UIFLOW2:

        |init.png|


DAC2Hat class inherits DAC2Unit class, See :ref:`unit.DAC2Unit.Methods <unit.DAC2Unit.Methods>` for more details.
