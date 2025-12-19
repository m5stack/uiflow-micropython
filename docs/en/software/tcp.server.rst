EasyTCPServer
=============

.. include:: ../refs/software.easysocket.tcp.server.ref

EasyTCPServer and EasyTCPClientSocket provide a simple way to create TCP servers and manage client connections in an event-driven manner.

UiFlow2 Example
---------------

simple server
^^^^^^^^^^^^^

Open the |cores3_simple_server_example.m5f2| project in UiFlow2.

This example creates a TCP server that listens on port 8000 and displays the received data on the screen.

UiFlow2 Code Block:

    |cores3_simple_server_example.png|

Example output:

    None

MicroPython Example
-------------------

simple server
^^^^^^^^^^^^^

This example creates a TCP server that listens on port 8000 and displays the received data on the screen.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/softwave/easysocket/tcp_server/cores3_simple_server_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

.. autoclass:: software.easysocket.tcp_server.EasyTCPServer
    :members:

.. autoclass:: software.easysocket.tcp_server.EasyTCPClientSocket
    :members:
