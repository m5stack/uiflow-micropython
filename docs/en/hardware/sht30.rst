SHT30
=====

.. include:: ../refs/hardware.sht30.ref

SHT30 is a sensor that can be used to measure temperature and humidity.

UiFlow2 Example
---------------

get temperature and humidity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |paper_sht30_example.m5f2| project in UiFlow2.

This example reads the temperature and humidity from the SHT30 sensor.

UiFlow2 Code Block:

    |example.png|

Example output:

    None


MicroPython Example
-------------------

get temperature and humidity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example reads the temperature and humidity from the SHT30 sensor.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/hardware/sht30/paper_sht30_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

SHT30
^^^^^^^^

.. autoclass:: hardware.sht30.SHT30
    :members:
    :member-order: bysource

.. autoclass:: driver.sht30.SHT30
    :members:
    :member-order: bysource