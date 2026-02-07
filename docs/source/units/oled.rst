
OLED Unit
==========

.. sku: u119

.. include:: ../refs/unit.oled.ref

Unit OLED is a 1.3-inch OLED expansion screen unit. Driveing by SH1107, and the resolution is 128*64, monochrome display.

Support the following products:

    |OLEDUnit|


UiFlow2 Example
---------------

Draw Text
^^^^^^^^^

Open the |cores3_oled_example.m5f2| project in UiFlow2.

This example displays the text "OLED" on the screen.

UiFlow2 Code Block:

    |example.png|

Example output:

    None


MicroPython Example
-------------------

Draw Text
^^^^^^^^^

This example displays the text "OLED" on the screen.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/oled/cores3_oled_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

class OLEDUnit
^^^^^^^^^^^^^^

.. autoclass:: unit.oled.OLEDUnit
    :members:

    OLEDUnit class inherits Display class, See :ref:`hardware.Display <hardware.Display>` for more details.
