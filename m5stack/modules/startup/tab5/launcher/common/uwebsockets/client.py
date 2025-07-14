"""
Websockets client for micropython

Based very heavily off
https://github.com/aaugustin/websockets/blob/master/websockets/client.py
"""

import socket
import binascii
import random
import ssl

from .protocol import Websocket, urlparse


class WebsocketClient(Websocket):
    is_client = True


def connect(uri):
    """
    Connect a websocket.
    """

    uri = urlparse(uri)
    assert uri

    sock = socket.socket()
    addr = socket.getaddrinfo(uri.hostname, uri.port)
    sock.connect(addr[0][4])
    if uri.protocol == "wss":
        sock = ssl.wrap_socket(sock, server_hostname=uri.hostname)

    def send_header(header, *args):
        sock.write(header % args + "\r\n")

    # Sec-WebSocket-Key is 16 bytes of random base64 encoded
    key = binascii.b2a_base64(bytes(random.getrandbits(8) for _ in range(16)))[:-1]

    send_header(b"GET %s HTTP/1.1", uri.path or "/")
    send_header(b"Host: %s:%s", uri.hostname, uri.port)
    send_header(b"Connection: Upgrade")
    send_header(b"Upgrade: websocket")
    send_header(b"Sec-WebSocket-Key: %s", key)
    send_header(b"Sec-WebSocket-Version: 13")
    send_header(b"Origin: http://{hostname}:{port}".format(hostname=uri.hostname, port=uri.port))
    send_header(b"")

    header = sock.readline()[:-2]
    assert header.startswith(b"HTTP/1.1 101 "), header

    # We don't (currently) need these headers
    # FIXME: should we check the return key?
    while header:
        header = sock.readline()[:-2]

    return WebsocketClient(sock)
