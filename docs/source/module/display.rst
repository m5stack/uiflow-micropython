
Display Module
==============

.. sku: M126

.. include:: ../refs/module.display.ref

Display Module 13.2 is an expansion module for HD audio and video, using GAOYUN GW1NR series FPGA chip to output display signals, and employing the LT8618S chip for signal output conditioning.

Support the following products:

    |DisplayModule|


UiFlow2 Example
---------------

Draw Text
^^^^^^^^^

Open the |cores3_display_example.m5f2| project in UiFlow2.

This example displays the text "Display" on the screen.

UiFlow2 Code Block:

    |example.png|

Example output:

    None


MicroPython Example
-------------------

This example displays the text "Display" on the screen.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/display/cores3_display_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

Class DisplayModule
^^^^^^^^^^^^^^^^^^^

.. autoclass:: module.display.DisplayModule
    :members:

    DisplayModule class inherits Display class, See :ref:`hardware.Display <hardware.Display>` for more details.
