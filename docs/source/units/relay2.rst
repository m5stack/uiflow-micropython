Relay2 Unit
==================

.. sku: U131

.. include:: ../refs/unit.relay2.ref

This is the driver library of Relay2 Unit, which is used to control the relay.

Support the following products:

    |RELAY2|


UiFlow2 Example
---------------

control relay
^^^^^^^^^^^^^^^

Open the |relay2_core2_example.m5f2| project in UiFlow2.

This example controls the relay of the Relay2 Unit and displays it on the screen.

UiFlow2 Code Block:

    |example.png|

Example output:

    None

MicroPython Example
-------------------

control relay
^^^^^^^^^^^^^^^

This example controls the relay of the Relay2 Unit and displays it on the screen.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/relay2/relay2_core2_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

Relay2Unit
^^^^^^^^^^

.. autoclass:: unit.relay2.Relay2Unit
    :members:
