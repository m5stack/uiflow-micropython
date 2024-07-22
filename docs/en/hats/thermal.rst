Thermal Hat
===========

.. include:: ../refs/hat.thermal.ref

The following products are supported:

    |ThermalHat|


Micropython Example:

    .. literalinclude:: ../../../examples/hat/thermal/stickc_plus2_thermal_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |stickc_plus2_thermal_example.m5f2|


class ThermalHat
----------------

Constructors
------------

.. class:: ThermalHat(i2c, address: int = 0x33)

    Create a ThermalHat object.

    :param i2c: I2C object
    :param address: the I2C address of the device. Default is 0x33.

    UIFLOW2:

        |init.png|


ThermalHat class inherits ThermalUnit class, See :ref:`unit.ThermaltUnit.Methods <unit.ThermaltUnit.Methods>` for more details.
