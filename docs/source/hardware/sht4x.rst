SHT4X
=====

.. py:currentmodule:: hardware.sht4x
.. include:: ../refs/hardware.sht4x.ref

SHT4X measures temperature and relative humidity.

Supported controllers:

.. table::
    :widths: auto
    :align: center

    +-------------------+-----------------+
    | Controller        | SHT4X           |
    +===================+=================+
    | M5PaperColor      | |S|             |
    +-------------------+-----------------+

.. |S| unicode:: U+2714


UiFlow2 Example
---------------

get temperature and humidity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example initializes the onboard SHT4X sensor and reads the temperature and
relative humidity.

Open the |sht4x_papercolor_example.m5f2| project in UiFlow2.

UiFlow2 Code Block:

    |example.png|

Example output:

    None


MicroPython Example
-------------------

get temperature and humidity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example reads temperature and relative humidity from the onboard SHT4X
sensor on M5PaperColor.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/hardware/sht4x/sht4x_papercolor_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

SHT4X
^^^^^

.. autoclass:: hardware.sht4x.SHT4X
    :members:
    :member-order: bysource

.. autoclass:: driver.sht4x.SHT4x
    :members:
    :member-order: bysource
