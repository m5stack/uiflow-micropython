StamPLC PoE
============

.. include:: ../refs/stamplc.poe.ref

Supported Products:

    |StamPLC PoE|

UiFlow2 Example
---------------

Get the weather
^^^^^^^^^^^^^^^

This example connects to the network using the StamPLC PoE and sends an HTTP request to query the geographical location of the current public IP address.

UiFlow2 Code Block:

    |stamplc_poe_example.png|

Example output:

    None

MicroPython Example
-------------------

Get the weather
^^^^^^^^^^^^^^^

This example connects to the network using the StamPLC PoE and sends an HTTP request to query the geographical location of the current public IP address.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/stamplc/poe/poe_stamplc_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

StamPLC PoE
^^^^^^^^^^^^

.. autoclass:: stamplc.poe.PoEStamPLC
    :members:

See :ref:`module.LAN.Methods <module.LAN.Methods>` for more APIs details.
