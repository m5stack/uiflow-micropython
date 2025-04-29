ToF4M Unit
==========

.. sku: U056

.. include:: ../refs/unit.tof4m.ref

This is the driver library of ToF4M Unit, which is used to obtain distance data from the
VL53L1CXV0FY sensor.

Support the following products:

    |ToF4M|


UiFlow2 Example
---------------

get distance value
^^^^^^^^^^^^^^^^^^^

Open the |tof4m_core_example.m5f2| project in UiFlow2.

This example gets the distance value of the ToF4M Unit and displays it on the screen.

UiFlow2 Code Block:

    |example.png|

Example output:

    None

MicroPython Example
-------------------

get distance value
^^^^^^^^^^^^^^^^^^^

This example gets the distance value of the ToF4M Unit and displays it on the screen.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/tof4m/tof4m_core_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

TOF4MUnit
^^^^^^^^^

.. autoclass:: unit.tof4m.TOF4MUnit
    :members:

VL53L1CXV0FY
^^^^^^^^^^^^^

.. autoclass:: driver.vl53l1x.VL53L1X
    :members:
