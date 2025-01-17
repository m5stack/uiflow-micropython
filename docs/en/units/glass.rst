
Glass Unit
===========

.. include:: ../refs/unit.glass.ref

Unit Glass is a 1.51-inch transparent OLED expansion screen unit. It adopts STM32+SSD1309 driver scheme,resolution is 128*64, monochrome display, transparent area is 128*56.

Support the following products:

|GlassUnit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/glass/cores3_glass_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |cores3_glass_example.m5f2|


class GlassUnit
---------------

Constructors
------------

.. class:: GlassUnit(i2c, address: int = 0x3d, freq: int = 400000)

    Initialize the Unit Glass

    :param I2C i2c: the I2C object.
    :param int address: I2C address of the Unit Glass, default is 0x3D.
    :param int freq: I2C frequency of the Unit Glass.

    UIFLOW2:

        |init.png|

