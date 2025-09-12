Step16 Unit 
===========

.. sku: U198

.. include:: ../refs/unit.step16.ref

This library is the driver for Unit Step16.

Support the following products:

    |Unit Step16|

UiFlow2 Example
---------------

Read Encoder
^^^^^^^^^^^^

Open the |cores3_step16_unit_example.m5f2| project in UiFlow2.

This example shows how to read and display encoder readings.
 
UiFlow2 Code Block:

    |cores3_step16_unit_example.png|

Example output:

    None
 
MicroPython Example
-------------------


Read Encoder
^^^^^^^^^^^^

This example shows how to read and display encoder readings.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/step16/cores3_step16_unit_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

Step16Unit
^^^^^^^^^^

.. autoclass:: unit.step16.Step16Unit
    :members:

