
MiniOLED Unit
==============

.. include:: ../refs/unit.minioled.ref

MiniOLED UNIT is a 0.42-inch I2C interface OLED screen unit, it's a 72*40, monochrome white display.

Support the following products:

|MiniOLEDUnit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/minioled/cores3_minioled_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |cores3_minioled_example.m5f2|


class MiniOLEDUnit
------------------

Constructors
------------

.. class:: MiniOLEDUnit(i2c, address: int = 0x3c, freq: int = 400000)

    Initialize the Unit MiniOLED

    :param I2C i2c: the I2C object.
    :param int|list|tuple address: I2C address of the Unit MiniOLED, default is 0x3c.
    :param int freq: I2C frequency of the Unit MiniOLED.

    UIFLOW2:

        |init.png|


Methods
-------





