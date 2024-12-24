LCD Unit
========

.. include:: ../refs/unit.lcd.ref


Unit LCD is a 1.14 inch color LCD expansion screen unit. It adopts ST7789V2
drive scheme, the resolution is 135*240, and it supports
RGB666 display (262,144 colors). The internal integration of ESP32-PICO control
core (built-in firmware, display development is more convenient), support
through I2C (addr: 0x3E) communication interface for control and firmware
upgrades. The back of the screen is integrated with a magnetic design,
which can easily adsorb the metal surface for fixing. The LCD screen extension
is suitable for embedding in various instruments or control devices that need
to display simple content as a display panel.


Support the following products:

    |LCDUnit|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/lcd/cores3_lcd_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |cores3_lcd_example.m5f2|


class LCDUnit
-------------

Constructors
------------

.. class:: LCDUnit(i2c, address: int = 0x3e, freq: int = 400000)

    Initialize the Unit LCD

    :param I2C i2c: the I2C object.
    :param int address: I2C address of the Unit LCDUnit, default is 0x3e.
    :param int freq: I2C frequency of the Unit LCDUnit.

    UIFLOW2:

        |init.png|
