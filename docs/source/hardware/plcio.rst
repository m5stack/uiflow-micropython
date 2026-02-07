PLC I/O
=======

.. include:: ../refs/hardware.plcio.ref

PLC I/O is used to control the Input/Output (I/O) Capabilities of host devices.

The following are the host's support for PLC I/O functions:

.. table::
    :widths: auto
    :align: center

    +-----------------+----------------+---------+
    |Controller       | Digital Input  | Relay   |
    +=================+================+=========+
    | StampPLC        | |S|            | |S|     |
    +-----------------+----------------+---------+


.. |S| unicode:: U+2714


UiFlow2 Example
---------------

Digital input control relay
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |stamplc_plcio_example.m5f2| project in UiFlow2.

This example shows how to control a relay using a digital input.

UiFlow2 Code Block:

    |stamplc_plcio_example.png|

Example output:

    None


MicroPython Example
-------------------

Digital input control relay
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example shows how to control a relay using a digital input.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/hardware/plcio/stamplc_plcio_example.py
        :language: python
        :linenos:

Example output:

    None


API
---

.. toctree::
    :maxdepth: 1

    plcio.digitalinput.rst
    plcio.relay.rst
