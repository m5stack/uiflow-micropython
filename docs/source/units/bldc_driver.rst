BLDCDriver Unit
===============

.. sku: U181

.. include:: ../refs/unit.bldc_driver.ref

This library is the driver for Unit BLDCDriver.

Support the following products:

    |Unit BLDCDriver|

UiFlow2 Example
---------------

Motor speed control
^^^^^^^^^^^^^^^^^^^

Open the |cores3_bldc_driver_example.m5f2| project in UiFlow2.

The example program gradually increases the motor speed and then stops the motor.

UiFlow2 Code Block:

    |cores3_bldc_driver_example.png|

Example output:

    None

MicroPython Example
-------------------

Motor speed control
^^^^^^^^^^^^^^^^^^^

The example program gradually increases the motor speed and then stops the motor.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/bldc_driver/cores3_bldc_driver_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

BLDCDriverUnit
^^^^^^^^^^^^^^

.. autoclass:: unit.bldc_driver.BLDCDriverUnit
    :members:
