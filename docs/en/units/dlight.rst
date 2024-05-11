DLight Unit
===========

.. include:: ../refs/unit.dlight.ref

Support the following products:

    |Dlight|


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from hardware import *
    from unit import *

    i2c0 = None
    dlight_0 = None

    def setup():
    global i2c0, dlight_0

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    dlight_0 = DLight(i2c0)
    print(dlight_0.get_lux())
    M5.begin()
    Widgets.fillScreen(0x222222)


UIFLOW2 Example:

    |example.svg|


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
