EasyTCPClient
=============

.. include:: ../refs/software.easysocket.tcp.client.ref

EasyTCPClient provides a simple way to create TCP clients in an event-driven manner.

UiFlow2 Example
---------------

simple client
^^^^^^^^^^^^^

Open the |cores3_simple_client_example.m5f2| project in UiFlow2.

This example creates a TCP client that connects to a server and sends data.

UiFlow2 Code Block:

    |cores3_simple_client_example.png|

Example output:

    None

MicroPython Example
-------------------

simple client
^^^^^^^^^^^^^

This example creates a TCP client that connects to a server and sends data.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/softwave/easysocket/tcp_client/cores3_simple_client_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

.. autoclass:: software.easysocket.tcp_client.EasyTCPClient
    :members:
