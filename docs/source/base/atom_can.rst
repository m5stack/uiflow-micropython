Atomic CAN Base
================

.. sku: A103/KO57

.. include:: ../refs/base.can.ref

This is the driver library for the ATOM CAN Base to accept and send data from the CAN module.

Support the following products:

    ================== ==================
    |Atom CAN|         |Atomic CAN Base|
    ================== ==================


UiFlow2 Example
---------------

CAN communication
^^^^^^^^^^^^^^^^^

Open the |atoms3_can_example.m5f2| project in UiFlow2.

This example shows how to receive and send data using the Atom CAN Base.

UiFlow2 Code Block:

    |example.png|

Example output:

    Output of received CAN message data via serial port.

MicroPython Example
-------------------

CAN communication
^^^^^^^^^^^^^^^^^^

This example shows how to receive and send data using the Atom CAN Base.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/can/atoms3_can_example.py
        :language: python
        :linenos:

Example output:

    Output of received CAN message data via serial port.

**API**
-------

ATOMCANBase
^^^^^^^^^^^

.. autoclass:: base.atom_can.ATOMCANBase
    :members:

    ATOMCANBase class inherits CAN class, See :class:`hardware.CAN <hardware.CAN>` for more details.
