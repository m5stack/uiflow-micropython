Ultrasonic Unit
===============

.. include:: ../refs/unit.ultrasonic.ref

Support the following products:

    |Ultrasonic|


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from hardware import *
    from unit import *

    i2c0 = None
    ultrasonic_0 = None

    def setup():
    global i2c0, ultrasonic_0

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    ultrasonic_0 = ULTRASONIC_I2C(i2c0)
    M5.begin()
    Widgets.fillScreen(0x222222)


UIFLOW2 Example:

    |example.svg|


.. only:: builder_html

    |ultrasonic_core_example.m5f2|


class ULTRASONIC_I2C
--------------------

Constructors
--------------

.. class:: ULTRASONIC_I2C(PORT)

    Create a ULTRASONIC I2C object.

    The parameters is:
        - ``PORT`` Define an i2c port.

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: ULTRASONIC_I2C.get_target_distance()

    Acquire transmitting distance

    UIFLOW2:

        |get_target_distance.svg|
