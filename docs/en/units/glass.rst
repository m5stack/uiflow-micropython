
GlassUnit
=========

.. include:: ../refs/unit.glass.ref

Unit Glass is a 1.51-inch transparent OLED expansion screen unit. It adopts STM32+SSD1309 driver scheme,resolution is 128*64, monochrome display, transparent area is 128*56.

Support the following products:

|GlassUnit|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from unit import GlassUnit
    glass = GlassUnit()
    glass.display.fill(0)


UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

class GlassUnit
---------------

Constructors
------------

.. class:: GlassUnit(port, address, freq)

    Initialize the Unit Glass

    :param tuple port: The port to which the Unit Glass is connected. port[0]: scl pin, port[1]: sda pin.
    :param int|list|tuple address: I2C address of the Unit Glass, default is 0x3D.
    :param int freq: I2C frequency of the Unit Glass.

    UIFLOW2:

        |init.svg|


Methods
-------





