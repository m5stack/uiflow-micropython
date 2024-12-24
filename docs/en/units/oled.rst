
OLED Unit
==========

.. include:: ../refs/unit.oled.ref

Unit OLED is a 1.3-inch OLED expansion screen unit. Driveing by SH1107, and the resolution is 128*64, monochrome display.

Support the following products:

|OLEDUnit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/oled/cores3_oled_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |cores3_oled_example.m5f2|

class OLEDUnit
--------------

Constructors
------------

.. class:: OLEDUnit(i2c, address: int = 0x3c, freq: int = 400000)

    Initialize the Unit OLED

    :param I2C i2c: the I2C object.
    :param int address: I2C address of the Unit OLED, default is 0x3c.
    :param int freq: I2C frequency of the Unit OLED.

    UIFLOW2:

        |init.png|
