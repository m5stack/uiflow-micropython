# EasyUDPClient

<!-- .. include:: ../refs/software.easysocket.udp.client.ref -->

EasyUDPClient provides a simple way to create UDP clients in an event-driven manner.

## UiFlow2 Example

#### simple client

Open the |udp_client_core2_example.m5f2| project in UiFlow2.

This example creates a UDP client that connects to a server and sends data.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### simple client

This example creates a UDP client that connects to a server and sends data.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from easysocket import EasyUDPClient
import network
import time

title0 = None
label2 = None
label0 = None
label1 = None
wlan_sta = None
udpc_0 = None

import random

received_data = None
client_address_port = None

def udpc_0_received_event(args):
    global title0, label2, label0, label1, wlan_sta, udpc_0, received_data, client_address_port
    client, client_address_port, received_data = args
    label1.setText(str("Receive Msg:"))
    label2.setText(str((str(received_data) + str(client_address_port))))

def setup():
    global title0, label2, label0, label1, wlan_sta, udpc_0, received_data, client_address_port

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "UDPClient Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label2 = Widgets.Label("", 2, 156, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("Local IP:", 2, 77, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Receive Msg:", 1, 122, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    wlan_sta = network.WLAN(network.STA_IF)
    wlan_sta.active(True)
    print("wait network connecting")
    while not (wlan_sta.isconnected()):
        print(".")
        time.sleep(1)
    print("connect success")
    print(wlan_sta.ifconfig()[0])
    label0.setText(str((str("Local IP:") + str((wlan_sta.ifconfig()[0])))))
    udpc_0 = EasyUDPClient(
        "Please enter the UDP server IP address.", 8000, EasyUDPClient.MODE_UNICAST
    )
    udpc_0.on_data_received(udpc_0_received_event)

def loop():
    global title0, label2, label0, label1, wlan_sta, udpc_0, received_data, client_address_port
    M5.update()
    udpc_0.check_event(timeout=1)
    if BtnA.wasPressed():
        udpc_0.send(str((random.randint(1, 100))))

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

```

Example output:

    None

## **API**

## EasyUDPClient
Create an EasyUDPClient object.

:param str remote_host: The remote host address.
:param int remote_port: The remote port number.
:param int mode: The UDP mode (unicast, broadcast, multicast). Default is unicast.

.. note::

    connection is initiated in the background when the object is created.

.. note::

    This class is non-blocking and event-driven. You need to call `check_event()` periodically to process events.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from easysocket import EasyUDPClient

        udp_client = EasyUDPClient("192.168.1.100", 8080, mode=EasyUDPClient.MODE_UNICAST)

### `connect`
Connect to the remote server.

MicroPython Code Block:

    .. code-block:: python

        udp_client.connect()

### `on_data_received`
Set the callback function for data received event.

:param callback: The callback function.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        def on_data_received_cb(client, data):
            print("Received:", data)

        udp_client.on_data_received(on_data_received_cb)

### `check_event`
Check for events.

:param int timeout: The timeout in milliseconds. Default is -1 (no timeout).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        udp_client.check_event()

### `send`
Send data to the remote server.

:param bytes data: The data to send.
:return: The number of bytes sent.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        udp_client.send(b"Hello")

### `sendto`
Send data to the remote server.

:param bytes data: The data to send.
:param tuple address: The (host, port) tuple to send data to.
:return: The number of bytes sent.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        udp_client.sendto(b"Hello", ("192.168.1.100", 8080))

### `recv`

### `recvfrom`

### `close`
Close the socket.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        udp_client.close()

### `setsockopt`

### `getsockname`
Return the socket's own address.

:return: The socket's own address. the format is (host, port).
:rtype: tuple

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        # get local ip address
        client_socket.getsockname()[0]

### `getpeername`
Return the remote address to which the socket is connected.

:return: The remote address. the format is (host, port).
:rtype: tuple

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        # get remote ip address
        client_socket.getpeername()[0]
