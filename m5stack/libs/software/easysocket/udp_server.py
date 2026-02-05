# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import socket
import select
import micropython
import errno
import struct


class EasyUDPServer:
    """Create an EasyUDPServer object.

    :param str host: The host address to bind to.
    :param int port: The port number to bind to.
    :param int mode: The UDP mode (unicast, broadcast, multicast). Default is unicast.
    :param str multicast_group: The multicast group address (required if mode is multicast).
    :param bool verbose: Whether to print verbose output.

    .. note::

        start service automatically when initialized.

    .. note::

        This class is non-blocking and event-driven. You need to call `check_event()` periodically to process events.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from easysocket import EasyUDPServer

            udp_server = EasyUDPServer(host="0.0.0.0", port=8080)
    """

    MODE_UNICAST = 0
    MODE_BROADCAST = 1
    MODE_MULTICAST = 2

    def __init__(
        self, host="0.0.0.0", port=8000, mode=MODE_UNICAST, multicast_group=None, verbose=False
    ):
        self._address = (host, port)
        self._mode = mode
        self._multicast_group = multicast_group

        self._on_data_received = None
        self._started = False
        self.server_sock = None
        self._verbose = verbose

        self._poll = select.poll()
        self.start()

    def start(self):
        """Start the server.

        MicroPython Code Block:

            .. code-block:: python

                udp_server.start()
        """
        if hasattr(self, "_started") and self._started:
            return

        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if self._mode == self.MODE_BROADCAST:
            try:
                self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                if self._verbose:
                    print("Broadcast mode enabled")
            except Exception as e:
                if self._verbose:
                    print(f"Warning: Could not set SO_BROADCAST: {e}")

        elif self._mode == self.MODE_MULTICAST:
            if not self._multicast_group:
                raise ValueError("Multicast mode requires multicast_group parameter")

            if not self._is_multicast_address(self._multicast_group):
                raise ValueError(f"Invalid multicast address: {self._multicast_group}")

            if self._verbose:
                print(f"Multicast mode: joining group {self._multicast_group}")

            self._join_multicast_group(self._multicast_group)

        self.server_sock.bind(self._address)
        self.server_sock.setblocking(False)

        self._poll.register(self.server_sock, select.POLLIN | select.POLLERR)

        self._started = True

        if self._verbose:
            mode_str = ["Unicast", "Broadcast", "Multicast"][self._mode]
            print(f"UDP Server started on {self._address} ({mode_str} mode)")

    @staticmethod
    def _ip_to_bytes(ip_str):
        parts = ip_str.split(".")
        if len(parts) != 4:
            raise ValueError(f"Invalid IP address: {ip_str}")

        try:
            return bytes([int(p) for p in parts])
        except ValueError:
            raise ValueError(f"Invalid IP address: {ip_str}")

    def _is_multicast_address(self, ip):
        try:
            parts = ip.split(".")
            if len(parts) != 4:
                return False
            first_octet = int(parts[0])
            return 224 <= first_octet <= 239
        except:
            return False

    def _join_multicast_group(self, mcast_addr, local_ip="0.0.0.0"):
        try:
            mreq = struct.pack("4s4s", self._ip_to_bytes(mcast_addr), self._ip_to_bytes(local_ip))

            self.server_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

            if self._verbose:
                print(f"Joined multicast group: {mcast_addr}")

        except Exception as e:
            print(f"Failed to join multicast group: {e}")
            raise

    def stop(self):
        """Stop the server.

        MicroPython Code Block:

            .. code-block:: python

                udp_server.stop()
        """

        if hasattr(self, "_started") and self._started:
            self.close()

    def close(self) -> None:
        if self._started:
            self._started = False
            if self.server_sock:
                try:
                    self._poll.unregister(self.server_sock)
                except:
                    pass
                self.server_sock.close()
                self.server_sock = None

            if self._verbose:
                print("UDP Server stopped")

    def on_data_received(self, callback):
        """Set the callback function for data received event.

        :param callback: The callback function.

        UiFlow2 Code Block:

            |received_callback.png|

        MicroPython Code Block:

            .. code-block:: python

                def on_data_received_cb(args):
                    client, address, data = args
                    print("Received:", data, "from", address)

                udp_server.on_data_received(on_data_received_cb)
        """
        self._on_data_received = callback

    def check_event(self, timeout=-1):
        """Check for events.

        :param int timeout: The timeout in milliseconds. Default is -1 (no timeout).

        UiFlow2 Code Block:

            |check_event.png|

        MicroPython Code Block:

            .. code-block:: python

                udp_server.check_event()
        """
        if not self._started:
            return

        events = self._poll.poll(timeout)
        for sock_obj, event in events:
            if event & select.POLLERR:
                if self._verbose:
                    print("Socket error occurred")
                continue

            if event & select.POLLIN:
                try:
                    data, addr = self.server_sock.recvfrom(1024)
                    if data and self._on_data_received:
                        micropython.schedule(self._on_data_received, (self, addr, data))
                except OSError as e:
                    if e.errno != errno.EAGAIN:
                        if self._verbose:
                            print(f"UDP recv error: {e} (errno={e.errno})")

    def sendto(self, data, address):
        """Send data to the remote server.

        :param bytes data: The data to send.
        :param tuple address: The (host, port) tuple to send data to.
        :return: The number of bytes sent.

        UiFlow2 Code Block:

            |sendto.png|

        MicroPython Code Block:

            .. code-block:: python

                udp_server.sendto(b"Hello", ("192.168.1.100", 8080))
        """
        if not self._started:
            if self._verbose:
                print("Server not started")
            return 0

        try:
            sent = self.server_sock.sendto(data, address)
            if self._verbose:
                print(f"→ Sent {sent} bytes to {address}")
            return sent
        except OSError as e:
            if self._verbose:
                print(f"UDP send error: {e}")
            return 0

    def setsockopt(self, *args, **kwargs):
        if self.server_sock:
            self.server_sock.setsockopt(*args, **kwargs)
