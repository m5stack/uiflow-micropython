addon DisplayOut
=================

.. py:currentmodule:: addon.display_out

.. include:: ../refs/addon.display_out.ref

``DisplayOut`` enables HDMI display output on Unit PoE-P4 by registering the
PoE-P4 HDMI interface as an M5 display. Use it when an external HDMI monitor is
connected to the Unit PoE-P4 display output.

Support the following products:

    |UNIT_POEP4|

UiFlow2 Example
---------------

HDMI output
^^^^^^^^^^^^

Open the |display_out_poep4_example.m5f2| project in UiFlow2.

This example initializes the HDMI output at ``1280x720@60Hz`` and draws basic widgets on the external display.

UiFlow2 Code Block:

    |init.png|

Example output:

    |example.png|

MicroPython Example
-------------------

HDMI output
^^^^^^^^^^^^^

This example initializes the HDMI output and draws basic widgets on the external display.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/addon/display_out/display_out_poep4_example.py
        :language: python
        :linenos:

Example output:

    |example.png|


**API**
-------

DisplayOut
^^^^^^^^^^

.. autoclass:: addon.display_out.DisplayOut
    :members:
    :member-order: bysource
