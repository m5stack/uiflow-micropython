DLight Hat
==========

.. include:: ../refs/hat.dlight.ref

The following products are supported:

    |DLightHAT|


Micropython Example:

    .. literalinclude:: ../../../examples/hat/dlight/stickc_plus2_dlight_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |stickc_plus2_dlight_example.m5f2|


class DLightHat
---------------

Constructors
------------

.. class:: DLightHat(i2c, address: int = 0x23)

    Create a DLightHat object.

    :param i2c: I2C object
    :param address: the I2C address of the device. Default is 0x23.

    UIFLOW2:

        |init.png|


DLightHat class inherits DLightUnit class, See :ref:`unit.DLightUnit.Methods <unit.DLightUnit.Methods>` for more details.
