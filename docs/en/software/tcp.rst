TCP
===

TCP is a connection-oriented protocol, meaning that a connection must be
established before data can be sent. It uses a three-way handshake to establish
a connection, which involves the exchange of SYN (synchronize) and ACK
(acknowledge) packets between the client and server. Once the connection is
established, data can be sent in both directions until either party decides to
close the connection.


API
---

.. toctree::
    :maxdepth: 1

    tcp.client.rst
    tcp.server.rst
