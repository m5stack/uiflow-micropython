Tube Pressure Unit
==================

.. sku: U131

.. include:: ../refs/unit.tube_pressure.ref

This is the driver library of Tube Pressure Unit, which is used to control the pressure sensor.

Support the following products:

    |Tube Pressure|


UiFlow2 Example
---------------

get pressure value
^^^^^^^^^^^^^^^^^^

Open the |tube_pressure_core2_example.m5f2| project in UiFlow2.

The example shows the pressure value of the tube pressure unit.

UiFlow2 Code Block:

    |example.png|

Example output:

    None

MicroPython Example
-------------------

get pressure value
^^^^^^^^^^^^^^^^^^

The example shows the pressure value of the tube pressure unit.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/tube_pressure/tube_pressure_core2_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

TubePressureUnit
^^^^^^^^^^^^^^^^

.. autoclass:: unit.tube_pressure.TubePressureUnit
    :members:
