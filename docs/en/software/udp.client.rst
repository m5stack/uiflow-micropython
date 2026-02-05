EasyUDPClient
=============

.. include:: ../refs/software.easysocket.udp.client.ref

EasyUDPClient provides a simple way to create UDP clients in an event-driven manner.

UiFlow2 Example
---------------

simple client
^^^^^^^^^^^^^

Open the |udp_client_core2_example.m5f2| project in UiFlow2.

This example creates a UDP client that connects to a server and sends data.

UiFlow2 Code Block:

    |udp_client_core2_example.png|

Example output:

    None

MicroPython Example
-------------------

simple client
^^^^^^^^^^^^^

This example creates a UDP client that connects to a server and sends data.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/software/easysocket/udp_client/udp_client_core2_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

.. autoclass:: software.easysocket.udp_client.EasyUDPClient
    :members:
