Mini ToF-90° Unit
===================

.. sku: U196

.. include:: ../refs/unit.tof90.ref

This is the driver library of Mini ToF-90° Unit, which is used to obtain data from the distance sensor.

Support the following products:

    |ToF90Unit|


UiFlow2 Example
---------------

get distance value
^^^^^^^^^^^^^^^^^^^

Open the |tof90_core2_example.m5f2| project in UiFlow2.

This example gets the distance value of the Mini ToF-90° Unit and displays it on the screen.

UiFlow2 Code Block:

    |example.png|

Example output:

    None

MicroPython Example
-------------------

get distance value
^^^^^^^^^^^^^^^^^^^

This example gets the distance value of the Mini ToF-90° Unit and displays it on the screen.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/tof90/tof90_core2_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

ToF90Unit
^^^^^^^^^

.. autoclass:: unit.tof.ToF90Unit
    :members:

VL53L0X
^^^^^^^

.. autoclass:: driver.vl53l0x.VL53L0X
    :members:
    :member-order: bysource
    :exclude-members: read_range, do_range_measurement, continuous_mode
