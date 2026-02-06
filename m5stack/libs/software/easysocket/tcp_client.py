# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import socket
import select
import micropython
import warnings
import errno


class EasyTCPClient:
    """Create an EasyTCPClient object.

    :param str remote_host: The remote host address.
    :param int remote_port: The remote port number.
    :param int timeout: The timeout in seconds. Default is 10.

    .. note::

        connection is initiated in the background when the object is created.

    .. note::

        This class is non-blocking and event-driven. You need to call `check_event()` periodically
        to process events.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from easysocket.tcp_client import EasyTCPClient

            client = EasyTCPClient("192.168.1.100", 8080)
    """

    _STATE_DISCONNECTED = 0
    _STATE_CONNECTING = 1
    _STATE_CONNECTED = 2

    def __init__(self, remote_host, remote_port, timeout=10):
        self._client_sock = None
        (self._remote_host, self._remote_port) = socket.getaddrinfo(
            remote_host, remote_port, 0, socket.SOCK_STREAM
        )[0][-1]

        self._on_connect = None
        self._on_data_received = None
        self._on_disconnect = None
        self._con_state = self._STATE_DISCONNECTED

        self._poll = select.poll()
        self.connect()

    def connect(self):
        """Connect to the remote server.

        UiFlow2 Code Block:

            |connect.png|

        MicroPython Code Block:

            .. code-block:: python

                client.connect()
        """
        if self._con_state in (self._STATE_CONNECTED, self._STATE_CONNECTING):
            return

        if self._client_sock:
            self._client_sock.close()

        self._client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client_sock.setblocking(False)

        try:
            self._client_sock.connect((self._remote_host, self._remote_port))
            self._con_state = self._STATE_CONNECTING
        except OSError as e:
            if e.args[0] != 119:  # EINPROGRESS
                self._client_sock.close()
                raise e
            self._con_state = self._STATE_CONNECTING

        self._poll.register(self._client_sock, select.POLLOUT | select.POLLERR | select.POLLHUP)

    def on_connect(self, callback):
        """Set the callback function for connection event.

        :param callback: The callback function.

        UiFlow2 Code Block:

            |on_connect.png|

        MicroPython Code Block:

            .. code-block:: python

                def on_connect_cb(client):
                    print("Connected")

                client.on_connect(on_connect_cb)
        """
        self._on_connect = callback

    def on_data_received(self, callback):
        """Set the callback function for data received event.

        :param callback: The callback function.

        UiFlow2 Code Block:

            |on_data_received.png|

        MicroPython Code Block:

            .. code-block:: python

                def on_data_received_cb(client, data):
                    print("Received:", data)

                client.on_data_received(on_data_received_cb)
        """
        self._on_data_received = callback

    def on_disconnect(self, callback):
        """Set the callback function for disconnection event.

        :param callback: The callback function.

        UiFlow2 Code Block:

            |on_disconnect.png|

        MicroPython Code Block:

            .. code-block:: python

                def on_disconnect_cb(client):
                    print("Disconnected")

                client.on_disconnect(on_disconnect_cb)
        """
        self._on_disconnect = callback

    def check_event(self, timeout=-1):
        """Check for events.

        :param int timeout: The timeout in milliseconds. Default is -1 (no timeout).

        UiFlow2 Code Block:

            |check_event.png|

        MicroPython Code Block:

            .. code-block:: python

                client.check_event()
        """
        if self._con_state not in (self._STATE_CONNECTED, self._STATE_CONNECTING):
            return

        events = self._poll.poll(timeout)
        for sock, event in events:
            if event & (select.POLLERR | select.POLLHUP):
                self._handle_disconnect()
                continue

            if self._con_state == self._STATE_CONNECTING:
                if event & select.POLLOUT:
                    self._con_state = self._STATE_CONNECTED
                    self._poll.modify(
                        self._client_sock, select.POLLIN | select.POLLERR | select.POLLHUP
                    )
                    if self._on_connect:
                        micropython.schedule(self._on_connect, self)

            if self._con_state == self._STATE_CONNECTED:
                if event & select.POLLIN:
                    try:
                        data = self._client_sock.recv(1024)
                        if data:
                            if self._on_data_received:
                                micropython.schedule(self._on_data_received, (self, data))
                        else:
                            self._handle_disconnect()
                    except OSError as e:
                        if e.errno == errno.EAGAIN:
                            pass
                        else:
                            self._handle_disconnect()

    def _handle_disconnect(self):
        if self._con_state not in (self._STATE_CONNECTED, self._STATE_CONNECTING):
            return

        self._con_state = self._STATE_DISCONNECTED
        self._poll.unregister(self._client_sock)
        self._client_sock.close()

        if self._on_disconnect:
            micropython.schedule(self._on_disconnect, self)

    def send(self, *args, **kwargs):
        """Send data to the remote server.

        :param bytes data: The data to send.
        :return: The number of bytes sent.

        UiFlow2 Code Block:

            |send.png|

        MicroPython Code Block:

            .. code-block:: python

                client.send(b"Hello")
        """
        if self._con_state != self._STATE_CONNECTED:
            warnings.warn("Socket is not connected. Call connect() first.")
            return 0
        return self._client_sock.send(*args, **kwargs)

    def sendall(self, *args, **kwargs):
        """Send all data to the remote server.

        :param bytes data: The data to send.

        UiFlow2 Code Block:

            |sendall.png|

        MicroPython Code Block:

            .. code-block:: python

                client.sendall(b"Hello")
        """
        if self._con_state != self._STATE_CONNECTED:
            warnings.warn("Socket is not connected. Call connect() first.")
            return 0
        return self._client_sock.sendall(*args, **kwargs)

    def recv(self, *args, **kwargs):
        if self._con_state != self._STATE_CONNECTED:
            warnings.warn("Socket is not connected. Call connect() first.")
            return b""
        return self._client_sock.recv(*args, **kwargs)

    def close(self, *args, **kwargs):
        """Close the connection.

        UiFlow2 Code Block:

            |close.png|

        MicroPython Code Block:

            .. code-block:: python

                client.close()
        """
        self._con_state = self._STATE_DISCONNECTED
        self._poll.unregister(self._client_sock)
        self._client_sock.close(*args, **kwargs)

    def setsockopt(self, *args, **kwargs):
        self._client_sock.setsockopt(*args, **kwargs)

    def settimeout(self, timeout):
        self._client_sock.settimeout(timeout)

    def setblocking(self, flag):
        self._client_sock.setblocking(flag)

    def getsockname(self, *args, **kwargs):
        """Return the socket's own address.

        :return: The socket's own address. the format is (host, port).
        :rtype: tuple

        UiFlow2 Code Block:

            |getsockname.png|

        MicroPython Code Block:

            .. code-block:: python

                # get local ip address
                client_socket.getsockname()[0]
        """
        return self._client_sock.getsockname(*args, **kwargs)

    def getpeername(self, *args, **kwargs):
        """Return the remote address to which the socket is connected.

        :return: The remote address. the format is (host, port).
        :rtype: tuple

        UiFlow2 Code Block:

            |getpeername.png|

        MicroPython Code Block:

            .. code-block:: python

                # get remote ip address
                client_socket.getpeername()[0]
        """
        return self._client_sock.getpeername(*args, **kwargs)
