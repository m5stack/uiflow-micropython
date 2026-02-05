# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import socket
import select
import micropython
import warnings
import errno


class EasyUDPClient:
    """Create an EasyUDPClient object.

    :param str remote_host: The remote host address.
    :param int remote_port: The remote port number.
    :param int mode: The UDP mode (unicast, broadcast, multicast). Default is unicast.

    .. note::

        connection is initiated in the background when the object is created.

    .. note::

        This class is non-blocking and event-driven. You need to call `check_event()` periodically to process events.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from easysocket import EasyUDPClient

            udp_client = EasyUDPClient("192.168.1.100", 8080, mode=EasyUDPClient.MODE_UNICAST)
    """

    _STATE_CLOSED = 0
    _STATE_READY = 1

    MODE_UNICAST = 0
    MODE_BROADCAST = 1
    MODE_MULTICAST = 2

    def __init__(self, remote_host, remote_port, mode=MODE_UNICAST):
        self._mode = mode
        self._client_sock = None
        (self._remote_host, self._remote_port) = socket.getaddrinfo(
            remote_host, remote_port, 0, socket.SOCK_DGRAM
        )[0][-1]

        self._on_data_received = None
        self._con_state = self._STATE_CLOSED
        self._poll = select.poll()
        self.connect()

    def connect(self):
        """Connect to the remote server.

        MicroPython Code Block:

            .. code-block:: python

                udp_client.connect()
        """
        if self._con_state == self._STATE_READY:
            return

        if self._client_sock:
            try:
                self._poll.unregister(self._client_sock)
            except:
                pass
            self._client_sock.close()

        self._client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._client_sock.setblocking(False)

        self._client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if self._mode == self.MODE_BROADCAST:
            self._client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self._client_sock.bind(("", self._remote_port))

        elif self._mode == self.MODE_MULTICAST:
            self._client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._client_sock.bind(("", self._remote_port))

        else:
            try:
                self._client_sock.connect((self._remote_host, self._remote_port))
            except:
                self._client_sock.bind(("", 0))

        self._con_state = self._STATE_READY
        self._poll.register(self._client_sock, select.POLLIN | select.POLLERR)

    @staticmethod
    def _ip_to_bytes(ip_str):
        parts = ip_str.split(".")
        if len(parts) != 4:
            raise ValueError(f"Invalid IP address: {ip_str}")

        try:
            return bytes([int(p) for p in parts])
        except ValueError:
            raise ValueError(f"Invalid IP address: {ip_str}")

    def on_data_received(self, callback):
        """Set the callback function for data received event.

        :param callback: The callback function.

        UiFlow2 Code Block:

            |received_callback.png|

        MicroPython Code Block:

            .. code-block:: python

                def on_data_received_cb(client, data):
                    print("Received:", data)

                udp_client.on_data_received(on_data_received_cb)
        """
        self._on_data_received = callback

    def check_event(self, timeout=-1):
        """Check for events.

        :param int timeout: The timeout in milliseconds. Default is -1 (no timeout).

        UiFlow2 Code Block:

            |check_event.png|

        MicroPython Code Block:

            .. code-block:: python

                udp_client.check_event()
        """
        if self._con_state != self._STATE_READY:
            return

        events = self._poll.poll(timeout)
        for sock, event in events:
            if event & select.POLLERR:
                pass

            if event & select.POLLIN:
                try:
                    data, addr = self._client_sock.recvfrom(1024)
                    if data and self._on_data_received:
                        micropython.schedule(self._on_data_received, (self, addr, data))
                except OSError as e:
                    if e.errno != errno.EAGAIN:
                        warnings.warn(f"UDP recv error:{e} (errno={e.errno}).")

    def send(self, data):
        """Send data to the remote server.

        :param bytes data: The data to send.
        :return: The number of bytes sent.

        UiFlow2 Code Block:

            |send.png|

        MicroPython Code Block:

            .. code-block:: python

                udp_client.send(b"Hello")
        """
        if self._con_state != self._STATE_READY:
            warnings.warn("Socket is not connected. Call connect() first.")
            return 0

        if self._mode in (self.MODE_BROADCAST, self.MODE_MULTICAST):
            return self.sendto(data, (self._remote_host, self._remote_port))

        return self._client_sock.send(data)

    def sendto(self, data, address=None):
        """Send data to the remote server.

        :param bytes data: The data to send.
        :param tuple address: The (host, port) tuple to send data to.
        :return: The number of bytes sent.

        UiFlow2 Code Block:

            |sendto.png|

            |sendto2.png|

        MicroPython Code Block:

            .. code-block:: python

                udp_client.sendto(b"Hello", ("192.168.1.100", 8080))
        """
        if address is None:
            address = (self._remote_host, self._remote_port)

        return self._client_sock.sendto(data, address)

    def recv(self, *args, **kwargs):
        if self._con_state != self._STATE_READY:
            warnings.warn("Socket is not connected. Call connect() first.")
            return b""
        return self._client_sock.recv(*args, **kwargs)

    def recvfrom(self, bufsize=1024):
        if self._con_state != self._STATE_READY:
            warnings.warn("Socket is not ready. Call connect() first.")
            return (b"", None)

        try:
            return self._client_sock.recvfrom(bufsize)
        except OSError as e:
            if e.errno == errno.EAGAIN:
                return (b"", None)
            warnings.warn(f"UDP recvfrom error:{e} (errno={e.errno}).")
            return (b"", None)

    def close(self):
        """Close the socket.

        UiFlow2 Code Block:

            |close.png|

        MicroPython Code Block:

            .. code-block:: python

                udp_client.close()
        """
        if self._client_sock:
            try:
                self._poll.unregister(self._client_sock)
            except:
                pass
            self._client_sock.close()
            self._client_sock = None
        self._con_state = self._STATE_CLOSED

    def setsockopt(self, *args, **kwargs):
        if self._client_sock:
            self._client_sock.setsockopt(*args, **kwargs)

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
        return self._client_sock.getsockname(*args, **kwargs) if self._client_sock else None

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
        if self._mode != self.MODE_UNICAST:
            return None
        return self._client_sock.getpeername(*args, **kwargs) if self._client_sock else None
