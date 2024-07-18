DAC Hat
=======

.. include:: ../refs/hat.dac.ref

The following products are supported:

    |DAC|


Micropython Example:

    .. literalinclude:: ../../../examples/hat/dac/stickc_plus2_dac_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |stickc_plus2_dac_example.m5f2|


class DACHat
------------

Constructors
------------

.. class:: DACHat(i2c: I2C, address: int = 0x60, vdd: float = 5.0, vout: float = 3.3)

    Create a DAC Hat object.

    :param i2c: I2C object
    :param address: I2C address of the DAC Hat
    :param vdd: VDD voltage of the DAC Hat
    :param vout: VOUT voltage of the DAC Hat

    UIFLOW2:

        |init.png|


DACHat class inherits DACUnit class, See :ref:`unit.DACUnit.Methods <unit.DACUnit.Methods>` for more details.
