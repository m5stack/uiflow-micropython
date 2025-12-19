Chain ToF
=========

.. include:: ../refs/chain.tof.ref

ToFChain is the helper class for ToF (Time of Flight) sensor devices on the Chain bus. It provides methods to read distance measurements, configure measurement parameters (time, mode, status), and check measurement completion status.

Support the following products:

    |Chain ToF|

UiFlow2 Example
---------------

Distance measurement display
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |m5core_chain_tof_basic_example.m5f2| project in UiFlow2.

This example demonstrates how to read distance measurements from the Chain ToF sensor and display them on screen. The example configures the sensor for continuous measurement mode and updates the distance value in real-time.

UiFlow2 Code Block:

    |m5core_chain_tof_basic_example.png|

Example output:

    None

MicroPython Example
-------------------

Distance measurement display
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to read distance measurements from the Chain ToF sensor and display them on screen. The example configures the sensor for continuous measurement mode and updates the distance value in real-time.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/chain/tof/m5core_chain_tof_basic_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

ToFChain
^^^^^^^^

.. autoclass:: chain.tof.ToFChain
    :members:
    :member-order: bysource
    :exclude-members:

