NCIR Unit
=========

.. include:: ../refs/unit.ncir.ref

Support the following products:

    |NCIR|


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from hardware import *
    from unit import *

    i2c0 = None
    ncir_0 = None

    def setup():
    global i2c0, ncir_0

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    ncir_0 = NCIRUnit(i2c0)
    M5.begin()
    Widgets.fillScreen(0x222222)

    print(ncir_0.get_ambient_temperature())
    print(ncir_0.get_object_temperature())


UIFLOW2 Example:

    |example.svg|


.. only:: builder_html

    |ncir_core_example.m5f2|


class NCIRUnit
--------------

Constructors
------------

.. class:: NCIRUnit(i2c)

    Create an NCIRUnit object.

    The parameters is:
        - ``i2c`` Define the i2c pin.

    UIFLOW2:

        |init.svg|


.. _unit.NCIRUnit.Methods:

Methods
-------

.. method:: ncir.get_ambient_temperature()

    Obtain the ambient temperature.

    UIFLOW2:

        |get_ambient_temperature.svg|


.. method:: ncir.get_object_temperature()

   Get the temperature of the measured object.

    UIFLOW2:

        |get_object_temperature.svg|
