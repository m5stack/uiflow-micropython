
Glass2Unit
==========

.. include:: ../refs/unit.glass2.ref

Glass2 Unit is a 1.51-inch transparent OLED display unit that adopts the SSD1309 driver solution.

Support the following products:

|Glass2Unit|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from unit import Glass2Unit
    glass = Glass2Unit()
    glass.display.fill(0)


UIFLOW2 Example:

    |example.svg|

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





