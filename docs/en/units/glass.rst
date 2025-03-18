Glass Unit
===========

.. include:: ../refs/unit.glass.ref

Unit Glass is a 1.51-inch transparent OLED expansion screen unit. It adopts STM32+SSD1309 driver scheme,resolution is 128*64, monochrome display, transparent area is 128*56.

Support the following products:

    |GlassUnit|


UiFlow2 Example
---------------

Draw Text
^^^^^^^^^

Open the |cores3_glass_example.m5f2| project in UiFlow2.

This example displays the text "GLASS" on the screen.

UiFlow2 Code Block:

    |example.png|

Example output:

    None


MicroPython Example
-------------------

Draw Text
^^^^^^^^^

This example displays the text "GLASS" on the screen.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/glass/cores3_glass_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

class GlassUnit
^^^^^^^^^^^^^^^

.. autoclass:: unit.glass.GlassUnit
    :members:

    GlassUnit class inherits Display class, See :ref:`hardware.Display <hardware.Display>` for more details.
