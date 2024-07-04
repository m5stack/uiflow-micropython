DLight Unit
===========

.. include:: ../refs/unit.dlight.ref

Support the following products:

    |Dlight|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/dlight/dlight_core_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |dlight_core_example.m5f2|


class DLight
------------

Constructors
------------

.. class:: DLightUnit(i2c, address: int = 0x23)

    Create a DLight object.

    :param i2c: the I2C object.
    :param address: the I2C address of the device. Default is 0x23.

    UIFLOW2:

        |init.svg|


.. _unit.DLightUnit.Methods:

Methods
-------

.. method:: DLightUnit.get_lux()

   Get light lux.

    UIFLOW2:

        |get_lux.svg|


.. method:: DLightUnit.configure()

    Configure the measurement mode (continuous measurement/single measurement) and resolution.

    UIFLOW2:

        |configure.svg|
