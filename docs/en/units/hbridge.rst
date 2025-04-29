Hbridge Unit
============================

.. sku: U160

.. sku: U160-V11

.. include:: ../refs/unit.hbridge.ref

This library is the driver for Unit HBridge. Only version v1.1 supports current measurement.

Support the following products:

    =================== ====================
    |Unit HBridge|      |Unit HBridge v1.1|
    =================== ====================


UiFlow2 Example
---------------

Motor speed and rotate direction control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |cores3_hbridge_motor_control.m5f2| project in UiFlow2.

This example demonstrates how to control the motor's speed and switch its rotation direction.

UiFlow2 Code Block:

    |cores3_hbridge_motor_control.png|

Example output:

    None


MicroPython Example
-------------------

Motor speed and rotate direction control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to control the motor's speed and switch its rotation direction.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/hbridge/cores3_hbridge_motor_control.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

HbridgeRUnit
^^^^^^^^^^^^

.. autoclass:: unit.hbridge.HbridgeUnit
    :members:
