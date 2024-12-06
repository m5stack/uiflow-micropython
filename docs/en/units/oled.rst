
OLED Unit
========

.. include:: ../refs/unit.oled.ref

Unit OLED is a 1.3-inch OLED expansion screen unit. Driveing by SH1107, and the resolution is 128*64, monochrome display.

Support the following products:

|OLEDUnit|

Micropython Example::
    from unit import OLEDUnit
    from hardware import *
    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    display = OLEDUnit(i2c).display
    
    display.clear(0xffffff) # Clear screen

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





