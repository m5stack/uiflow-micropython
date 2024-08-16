
MiniOLEDUnit
============

.. include:: ../refs/unit.minioled.ref

MiniOLED UNIT is a 0.42-inch I2C interface OLED screen unit, it's a 72*40, monochrome white display.

Support the following products:

|MiniOLEDUnit|

Micropython Example::
    from unit import MiniOLEDUnit
    from hardware import *
    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    display = MiniOLEDUnit(i2c).display
    
    display.clear(0xffffff) # Clear screen

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





