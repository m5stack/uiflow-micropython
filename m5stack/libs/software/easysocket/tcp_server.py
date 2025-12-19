# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import socket
import select
import micropython
import errno


class EasyTCPClientSocket:
    """Create an EasyTCPClientSocket object.

    .. note::

        this is a wrapper class for the socket object used in EasyTCPServer.

    :param socket sock: The socket object.
    """

    def __init__(self, sock):
        self.sock = sock
        self.poller = select.poll()
        self.poller.register(self.sock, select.POLLOUT)

    def send(self, *args, **kwargs):
        """Send data to the client.

        :param bytes data: The data to send.
        :return: The number of bytes sent.
        :rtype: int

        UiFlow2 Code Block:

            |send.png|

        MicroPython Code Block:

            .. code-block:: python

                client_socket.send(data)
        """
        return self.sock.send(*args, **kwargs)

    def sendall(self, *args, **kwargs):
        """Send all data to the client.

        :param bytes data: The data to send.

        UiFlow2 Code Block:

            |sendall.png|

        MicroPython Code Block:

            .. code-block:: python

                client_socket.sendall(data)
        """
        view = memoryview(args[0])
        total_sent = 0
        total_len = len(args[0])

        while total_sent < total_len:
            try:
                sent = self.sock.send(view[total_sent:])
                if sent is None:
                    sent = 0
                total_sent += sent
            except OSError as e:
                if e.errno == errno.EAGAIN:
                    self.poller.poll()
                else:
                    raise e

    def recv(self, *args, **kwargs):
        return self.sock.recv(*args, **kwargs)

    def close(self, *args, **kwargs):
        """Close the connection.

        UiFlow2 Code Block:

            |close.png|

        MicroPython Code Block:

            .. code-block:: python

                client_socket.close()
        """
        self.sock.close(*args, **kwargs)

    def settimeout(self, *args, **kwargs):
        self.sock.settimeout(*args, **kwargs)

    def setblocking(self, *args, **kwargs):
        self.sock.setblocking(*args, **kwargs)

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
        return self.sock.getsockname(*args, **kwargs)

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
        return self.sock.getpeername(*args, **kwargs)


class EasyTCPServer:
    """Create an EasyTCPServer object.

    :param str host: The host address to bind to. Default is "0.0.0.0".
    :param int port: The port number to bind to. Default is 8000.
    :param int listen: The number of unaccepted connections that the system will allow before refusing new connections. Default is 3.
    :param bool verbose: Whether to print verbose output. Default is False.

    .. note::

        start service automatically when initialized.

    .. note::

        This class is non-blocking and event-driven. You need to call `check_event()` periodically
        to process events.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from easysocket import EasyTCPServer

            server = EasyTCPServer(host="0.0.0.0", port=8080)
    """

    def __init__(self, host="0.0.0.0", port=8000, listen=3, verbose=False):
        self._address = (host, port)
        self._listen = listen

        self._on_client_connect = None
        self._on_client_disconnect = None
        self._on_data_received = None

        self._client_sockets = {}
        self._verbose = verbose

        self._poll = select.poll()
        self.start()

    def start(self):
        """Start the server.

        UiFlow2 Code Block:

            |start.png|

        MicroPython Code Block:

            .. code-block:: python

                server.start()
        """
        if hasattr(self, "_start") and self._start:
            return

        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind(self._address)
        self.server_sock.listen(self._listen)
        self.server_sock.setblocking(False)

        self._poll.register(self.server_sock, select.POLLIN)

        self._start = True

    def stop(self) -> None:
        """Stop the server.

        UiFlow2 Code Block:

            |stop.png|

        MicroPython Code Block:

            .. code-block:: python

                server.stop()
        """
        if hasattr(self, "_start") and self._start:
            self.close()

    def close(self) -> None:
        if self._start:
            self._start = False
            for client_sock in list(self._client_sockets.keys()):
                self._poll.unregister(client_sock)
                client_sock.close()
            self._client_sockets.clear()

            self._poll.unregister(self.server_sock)
            self.server_sock.close()

    def get_sessions(self) -> tuple:
        """Get all connected client sockets.

        :return: A tuple of connected client sockets.
        :rtype: tuple[EasyTCPClientSocket]

        UiFlow2 Code Block:

            |get_sessions.png|

        MicroPython Code Block:

            .. code-block:: python

                sessions = server.get_sessions()
        """
        return tuple(self._client_sockets.values())

    def on_client_connect(self, callback):
        """Set the callback function for client connection event.

        :param callback: The callback function. The callback function must accept a single argument,
                         which is the connected client socket instance of :class:`EasyTCPClientSocket`.

        UiFlow2 Code Block:

            |on_client_connect.png|

        MicroPython Code Block:

            .. code-block:: python

                def on_client_connect_cb(client_socket):
                    print("Client connected")

                server.on_client_connect(on_client_connect_cb)
        """
        self._on_client_connect = callback

    def on_client_disconnect(self, callback):
        """Set the callback function for client disconnection event.

        :param callback: The callback function. The callback function must accept a single argument,
                         which is the disconnected client socket instance of :class:`EasyTCPClientSocket`.

        UiFlow2 Code Block:

            |on_client_disconnect.png|

        MicroPython Code Block:

            .. code-block:: python

                def on_client_disconnect_cb(client_socket):
                    print("Client disconnected")

                server.on_client_disconnect(on_client_disconnect_cb)
        """
        self._on_client_disconnect = callback

    def on_data_received(self, callback):
        """Set the callback function for data received event.

        :param callback: The callback function. The callback function must accept a single argument,
                         which is a tuple containing the client socket instance of :class:`EasyTCPClientSocket` and the received data (bytes).

        UiFlow2 Code Block:

            |on_data_received.png|

        MicroPython Code Block:

            .. code-block:: python

                def on_data_received_cb(args):
                    client_socket, data = args
                    print("Received:", data)

                server.on_data_received(on_data_received_cb)
        """
        self._on_data_received = callback

    def check_event(self, timeout=-1):
        """Check for events.

        :param int timeout: The timeout in milliseconds. Default is -1 (no timeout).

        UiFlow2 Code Block:

            |check_event.png|

        MicroPython Code Block:

            .. code-block:: python

                server.check_event()
        """
        if not self._start:
            return

        events = self._poll.poll(timeout)
        for sock_obj, event in events:
            if sock_obj == self.server_sock:
                """new client connection"""
                if event & select.POLLIN:
                    client_sock, client_addr = self.server_sock.accept()
                    client_sock.setblocking(False)
                    self._poll.register(client_sock, select.POLLIN)

                    client_wrapper = EasyTCPClientSocket(client_sock)
                    self._client_sockets[client_sock] = client_wrapper

                    if self._verbose:
                        print("Accepting new client: ", client_addr)

                    if self._on_client_connect:
                        micropython.schedule(self._on_client_connect, client_wrapper)
            else:
                """existing client socket event"""
                if event & select.POLLIN:
                    try:
                        data = sock_obj.recv(1024)
                        client_wrapper = self._client_sockets.get(sock_obj)
                        if self._verbose:
                            print(
                                "Received data from ",
                                client_wrapper.getpeername(),
                                ": ",
                                data,
                            )
                        if data:
                            if self._on_data_received:
                                micropython.schedule(
                                    self._on_data_received,
                                    (client_wrapper, data),
                                )
                        else:
                            self._handle_client_disconnect(sock_obj)
                    except OSError as e:
                        if e.errno == errno.EAGAIN:
                            pass
                        else:
                            self._handle_client_disconnect(sock_obj)

                if event & (select.POLLERR | select.POLLHUP):
                    self._handle_client_disconnect(sock_obj)

    def _handle_client_disconnect(self, client_sock):
        self._poll.unregister(client_sock)
        client_sock.close()

        client_wrapper = self._client_sockets.pop(client_sock, None)
        if client_wrapper:
            if self._verbose:
                print("Client disconnected: ", client_wrapper.getpeername())
            if self._on_client_disconnect:
                micropython.schedule(self._on_client_disconnect, client_wrapper)

    def setsockopt(self, *args, **kwargs):
        self.server_sock.setsockopt(*args, **kwargs)

    def settimeout(self, *args, **kwargs):
        self.server_sock.settimeout(*args, **kwargs)

    def setblocking(self, *args, **kwargs):
        self.server_sock.setblocking(*args, **kwargs)

    def getsockname(self, *args, **kwargs):
        return self.server_sock.getsockname(*args, **kwargs)

    def getpeername(self, *args, **kwargs):
        return self.server_sock.getpeername(*args, **kwargs)
