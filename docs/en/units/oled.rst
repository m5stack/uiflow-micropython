
OLEDUnit
========

.. include:: ../refs/unit.oled.ref

Unit OLED is a 1.3-inch OLED expansion screen unit. Driveing by SH1107, and the resolution is 128*64, monochrome display.

Support the following products:

|OLEDUnit|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from unit import OLEDUnit
    oled = OLEDUnit()
    oled.display.fill(0)

.. only:: builder_html

class OLEDUnit
--------------

Constructors
------------

.. class:: OLEDUnit(port, address, freq)

    Initialize the Unit OLED

    :param tuple port: The port to which the Unit OLED is connected. port[0]: scl pin, port[1]: sda pin.
    :param int|list|tuple address: I2C address of the Unit OLED, default is 0x3D.
    :param int freq: I2C frequency of the Unit OLED.

    UIFLOW2:

        |init.svg|


Methods
-------





