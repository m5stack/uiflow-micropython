
Glass Unit
===========

.. include:: ../refs/unit.glass.ref

Unit Glass is a 1.51-inch transparent OLED expansion screen unit. It adopts STM32+SSD1309 driver scheme,resolution is 128*64, monochrome display, transparent area is 128*56.

Support the following products:

|GlassUnit|

Micropython Example::
    from unit import GlassUnit
    from hardware import *
    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    display = GlassUnit(i2c).display
    
    display.clear(0xffffff) # Clear screen

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





