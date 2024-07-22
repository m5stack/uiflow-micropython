
MiniOLEDUnit
============

.. include:: ../refs/unit.minioled.ref

MiniOLED UNIT is a 0.42-inch I2C interface OLED screen unit, it's a 72*40, monochrome white display.

Support the following products:

|MiniOLEDUnit|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from unit import MiniOLEDUnit
    oled = MiniOLEDUnit()
    oled.display.fill(0)

.. only:: builder_html

class MiniOLEDUnit
------------------

Constructors
------------

.. class:: MiniOLEDUnit(port, address, freq)

    Initialize the Unit MiniOLED

    :param tuple port: The port to which the Unit MiniOLED is connected. port[0]: scl pin, port[1]: sda pin.
    :param int|list|tuple address: I2C address of the Unit MiniOLED, default is 0x3D.
    :param int freq: I2C frequency of the Unit MiniOLED.

    UIFLOW2:

        |init.svg|


Methods
-------





