
Glass2 Unit
==========

.. include:: ../refs/unit.glass2.ref

Glass2 Unit is a 1.51-inch transparent OLED display unit that adopts the SSD1309 driver solution.

Support the following products:

|Glass2Unit|

Micropython Example::
    from unit import Glass2Unit
    from hardware import *
    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    display = Glass2Unit(i2c).display
    
    display.clear(0xffffff) # Clear screen

.. only:: builder_html

class Glass2Unit
----------------

Constructors
------------

.. class:: Glass2Unit(port, address, freq)

    Initialize the Unit Glass2

    :param tuple port: The port to which the Unit Glass2 is connected. port[0]: scl pin, port[1]: sda pin.
    :param int|list|tuple address: I2C address of the Unit Glass2, default is 0x3D.
    :param int freq: I2C frequency of the Unit Glass2.

    UIFLOW2:

        |init.svg|


Methods
-------





