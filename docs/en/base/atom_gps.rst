ATOM GPS Base
==============

.. sku: A134/K043

.. include:: ../refs/base.gps.ref

This is the driver library of ATOM GPS Base, which is used to obtain data from the
GPS module.

Support the following products:

    ================== ==================
    |ATOM GPS|         |ATOM GPS Base|
    ================== ==================


UiFlow2 Example
---------------

get gps data
^^^^^^^^^^^^^

Open the |atoms3_gps_example.m5f2| project in UiFlow2.

This example gets the GPS data of the ATOM GPS Base and displays it on the serial monitor.

UiFlow2 Code Block:

    |example.png|

Example output:

    None

MicroPython Example
-------------------

get gps data
^^^^^^^^^^^^^^^

This example gets the GPS data of the ATOM GPS Base and displays it on the serial monitor.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/gps/atoms3_gps_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

ATOMGPSBase
^^^^^^^^^^^

.. autoclass:: base.atom_gps.ATOMGPSBase
    :members:
