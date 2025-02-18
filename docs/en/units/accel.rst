Accel Unit
==========

.. sku: U056

.. include:: ../refs/unit.accel.ref

This is the driver library of Accel Unit, which is used to obtain data from the
acceleration sensor and support motion detection.

Support the following products:

    |ACCEL|


UiFlow2 Example
---------------

get accel value
^^^^^^^^^^^^^^^

Open the |stickcplus2_unit_accel_example.m5f2| project in UiFlow2.

This example gets the acceleration value of the Accel Unit and displays it on the screen.

UiFlow2 Code Block:

    |example.png|

Example output:

    None

MicroPython Example
-------------------

get accel value
^^^^^^^^^^^^^^^

This example gets the acceleration value of the Accel Unit and displays it on the screen.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/accel/stickcplus2_unit_accel_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

AccelUnit
^^^^^^^^^

.. autoclass:: unit.accel.AccelUnit
    :members:

ADXL345
^^^^^^^

.. autoclass:: unit.accel.ADXL345
    :members:
