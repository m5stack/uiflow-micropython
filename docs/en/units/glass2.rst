
Glass2 Unit
===========

.. include:: ../refs/unit.glass2.ref

Glass2 Unit is a 1.51-inch transparent OLED display unit that adopts the SSD1309 driver solution.

Support the following products:

|Glass2Unit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/glass2/cores3_glass2_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |cores3_glass2_example.m5f2|

class Glass2Unit
----------------

Constructors
------------

.. class:: Glass2Unit(i2c, address: int = 0x3c, freq: int = 400000)

    Initialize the Unit Glass2

    :param I2C i2c: the I2C object.
    :param int address: I2C address of the Unit Glass2, default is 0x3c.
    :param int freq: I2C frequency of the Unit Glass2.

    UIFLOW2:

        |init.png|
