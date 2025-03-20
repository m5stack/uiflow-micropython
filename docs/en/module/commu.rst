Commu Module
==============

.. sku: M011

.. include:: ../refs/module.commu.ref

This is the driver library for the module Commu for receiving and sending CAN / RS485 / I2C data.

Support the following products:

    |commu|


UiFlow2 Example
---------------

CAN, RS485, I2C communication
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |commu_core2_example.m5f2| project in UiFlow2.

This example shows how to receive and send data using the Commu Module.

UiFlow2 Code Block:

    |example.png|

Example output:

    None

MicroPython Example
-------------------

CAN, RS485, I2C communication
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example shows how to receive and send data using the Commu Module.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/commu/commu_core2_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

CommuModule
^^^^^^^^^^^

.. autoclass:: module.commu.CommuModuleCAN
    :members:

.. autoclass:: module.commu.CommuModuleRS485
    :members:

    The `CommuModuleRS485` class wraps an instance of the `UART` class.

    For more details, see :ref:`hardware.UART <hardware.UART>`.

.. autoclass:: module.commu.CommuModuleI2C
    :members:

    The `CommuModuleI2C` class wraps an instance of the `I2C` class.

    For more details, see :ref:`machine.I2C <machine.I2C>`. -- a two-wire serial protocol.
