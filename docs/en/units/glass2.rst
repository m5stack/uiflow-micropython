Glass2 Unit
===========

.. include:: ../refs/unit.glass2.ref

Glass2 Unit is a 1.51-inch transparent OLED display unit that adopts the SSD1309 driver solution.

Support the following products:

    |Glass2Unit|


UiFlow2 Example
---------------

Draw Text
^^^^^^^^^

Open the |cores3_glass2_example.m5f2| project in UiFlow2.

This example displays the text "GLASS2" on the screen.

UiFlow2 Code Block:

    |example.png|

Example output:

    None


MicroPython Example
-------------------

Draw Text
^^^^^^^^^

This example displays the text "GLASS2" on the screen.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/glass2/cores3_glass2_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

class Glass2Unit
----------------

.. autoclass:: unit.glass2.Glass2Unit
    :members:

    Glass2Unit class inherits Display class, See :ref:`hardware.Display <hardware.Display>` for more details.
