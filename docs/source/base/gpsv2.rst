Atomic GPS Base v2.0
======================

.. sku: A134-V2

.. include:: ../refs/base.gpsv2.ref

This is the driver library for the Atomic GPS Base v2.0, which is used to get the GPS data.

Support the following products:

    |Atom GPS Base v2.0|

UiFlow2 Example
---------------

get GPS data
^^^^^^^^^^^^^^^^^

Open the |base_gpsv2_atom_example.m5f2| project in UiFlow2.

This example demonstrates how to get the GPS data using Atomic GPS Base v2.0.

UiFlow2 Code Block:

    |example.png|

Example output:

    None


MicroPython Example
-------------------

get GPS data
^^^^^^^^^^^^^^^^^^

This example demonstrates how to get the GPS data using Atomic GPS Base v2.0.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/gpsv2/base_gpsv2_atom_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

AtomicGPSV2Base
^^^^^^^^^^^^^^^

.. autoclass:: base.gpsv2.AtomicGPSV2Base
    :members:
    :member-order: bysource

.. autoclass:: driver.atgm336h.ATGM336H
    :members:
    :member-order: bysource
