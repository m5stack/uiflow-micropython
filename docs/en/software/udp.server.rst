EasyUDPServer
=============

.. include:: ../refs/software.easysocket.udp.server.ref

EasyUDPServer and EasyUDPClientSocket provide a simple way to create UDP servers and manage client connections in an event-driven manner.

UiFlow2 Example
---------------

simple server
^^^^^^^^^^^^^

Open the |udp_server_core2_example.m5f2| project in UiFlow2.

This example creates a UDP server that listens on port 8000 and displays the received data on the screen.

UiFlow2 Code Block:

    |udp_server_core2_example.png|

Example output:

    None

MicroPython Example
-------------------

simple server
^^^^^^^^^^^^^

This example creates a UDP server that listens on port 8000 and displays the received data on the screen.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/software/easysocket/udp_server/udp_server_core2_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

.. autoclass:: software.easysocket.udp_server.EasyUDPServer
    :members:
