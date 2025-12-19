:py:mod:`easysocket` -- a lightweight network library
=====================================================

easysocket is a lightweight, non-blocking, event-driven network library designed for MicroPython. It encapsulates the complexity of raw socket operations and ``select.poll`` mechanisms, providing a simple callback-based API. Currently, it supports TCP (Transmission Control Protocol) for building robust clients and servers, with UDP (User Datagram Protocol) support planned for future releases.

Features
--------

- **Non-blocking & Event-driven**:
  Based on the ``select.poll()`` mechanism, all socket operations are non-blocking. Events are dispatched via periodic ``check_event()`` calls, preventing network I/O from blocking the main thread—ideal for MicroPython.

- **Callback-based**:
  Simple event hooks for clients (``on_connect``, ``on_data_received``, ``on_disconnect``) and servers (``on_client_connect``, ``on_data_received``, ``on_client_disconnect``). Callbacks are safely scheduled using ``micropython.schedule``.

- **High Abstraction**:
  Automatic connection/listening upon initialization. Server-side client connections are wrapped in ``EasyTCPClientSocket`` objects for easy management.

- **Concurrency**:
  ``EasyTCPServer`` handles multiple client connections simultaneously, managing the lifecycle of each session.

- **Robustness**:
  Handles non-blocking errors (like ``EAGAIN``) and ensures proper resource cleanup (socket closing, poll unregistering) on disconnection.

Classes
-------

.. toctree::
    :maxdepth: 1

    tcp.client.rst
    tcp.server.rst
