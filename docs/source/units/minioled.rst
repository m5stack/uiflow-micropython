
MiniOLED Unit
==============

.. include:: ../refs/unit.minioled.ref

MiniOLED UNIT is a 0.42-inch I2C interface OLED screen unit, it's a 72*40, monochrome white display.

Support the following products:

    |MiniOLEDUnit|


UiFlow2 Example
---------------

Draw Text
^^^^^^^^^

Open the |cores3_minioled_example.m5f2| project in UiFlow2.

This example displays the text "Mini" on the screen.

UiFlow2 Code Block:

    |example.png|

Example output:

    None


MicroPython Example
-------------------

Draw Text
^^^^^^^^^

This example displays the text "Mini" on the screen.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/minioled/cores3_minioled_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

class MiniOLEDUnit
^^^^^^^^^^^^^^^^^^

.. autoclass:: unit.minioled.MiniOLEDUnit
    :members:

    MiniOLEDUnit class inherits Display class, See :ref:`hardware.Display <hardware.Display>` for more details.
