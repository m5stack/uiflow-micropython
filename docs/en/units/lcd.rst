LCD Unit
========

.. sku: U120

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


UiFlow2 Example
---------------

Draw Text
^^^^^^^^^

Open the |cores3_lcd_example.m5f2| project in UiFlow2.

This example displays the text "LCD" on the screen.

UiFlow2 Code Block:

    |example.png|

Example output:

    None


MicroPython Example
-------------------

Draw Text
^^^^^^^^^

This example displays the text "LCD" on the screen.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/lcd/cores3_lcd_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

class LCDUnit
^^^^^^^^^^^^^

.. autoclass:: unit.lcd.LCDUnit
    :members:

    LCDUnit class inherits Display class, See :ref:`hardware.Display <hardware.Display>` for more details.
