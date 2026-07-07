# EasyTCPServer

<!-- .. include:: ../refs/software.easysocket.tcp.server.ref -->

EasyTCPServer and EasyTCPClientSocket provide a simple way to create TCP servers and manage client connections in an event-driven manner.

## UiFlow2 Example

#### simple server

Open the |cores3_simple_server_example.m5f2| project in UiFlow2.

This example creates a TCP server that listens on port 8000 and displays the received data on the screen.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### simple server

This example creates a TCP server that listens on port 8000 and displays the received data on the screen.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from easysocket import EasyTCPServer
import network

page0 = None
button0 = None
label0 = None
textarea0 = None
label1 = None
textarea1 = None
textarea2 = None
label3 = None
wlan_sta = None
tcps_0 = None

client = None
received_data = None
state = None

def tcps_0_connect_event(client_sock):
    global \
        page0, \
        button0, \
        label0, \
        textarea0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcps_0, \
        client, \
        received_data, \
        state
    client = client_sock
    textarea2.add_text(str("new clinet: "))
    textarea2.add_text(str(client.getpeername()[0]))
    textarea2.add_text(str("\n"))

def tcps_0_received_event(args):
    global \
        page0, \
        button0, \
        label0, \
        textarea0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcps_0, \
        client, \
        received_data, \
        state
    client, received_data = args
    textarea2.add_text(str(client.getpeername()[0]))
    textarea2.add_text(str(":"))
    textarea2.add_text(str(received_data))
    textarea2.add_text(str("\n"))

def tcps_0_disconnect_event(client_sock):
    global \
        page0, \
        button0, \
        label0, \
        textarea0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcps_0, \
        client, \
        received_data, \
        state
    client = client_sock
    textarea2.add_text(str(client.getpeername()[0]))
    textarea2.add_text(str(" disconnected\n"))

def button0_short_clicked_event(event_struct):
    global \
        page0, \
        button0, \
        label0, \
        textarea0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcps_0, \
        client, \
        received_data, \
        state
    state = not state
    if state:
        textarea2.set_text("")
        tcps_0.start()
        button0.set_btn_text(str("stop"))
        button0.set_bg_color(0xFF0000, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    else:
        tcps_0.stop()
        button0.set_btn_text(str("start"))
        button0.set_bg_color(0x3366FF, 255, lv.PART.MAIN | lv.STATE.DEFAULT)

def button0_event_handler(event_struct):
    global \
        page0, \
        button0, \
        label0, \
        textarea0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcps_0, \
        client, \
        received_data, \
        state
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button0_short_clicked_event(event_struct)
    return

def setup():
    global \
        page0, \
        button0, \
        label0, \
        textarea0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcps_0, \
        client, \
        received_data, \
        state

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    textarea0 = m5ui.M5TextArea(
        text="textarea0",
        placeholder="Placeholder...",
        x=40,
        y=6,
        w=70,
        h=36,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    textarea1 = m5ui.M5TextArea(
        text="textarea0",
        placeholder="Placeholder...",
        x=178,
        y=6,
        w=56,
        h=36,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    textarea2 = m5ui.M5TextArea(
        text="Text",
        placeholder="Placeholder...",
        x=6,
        y=76,
        w=308,
        h=158,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    button0 = m5ui.M5Button(
        text="stop",
        x=239,
        y=6,
        bg_c=0xF32121,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "IP:",
        x=6,
        y=10,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label1 = m5ui.M5Label(
        "Port:",
        x=116,
        y=10,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label3 = m5ui.M5Label(
        "Log:",
        x=6,
        y=50,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    button0.add_event_cb(button0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    wlan_sta = network.WLAN(network.STA_IF)
    wlan_sta.active(True)
    tcps_0 = EasyTCPServer(host="0.0.0.0", port=8000, listen=0, verbose=True)
    tcps_0.on_client_connect(tcps_0_connect_event)
    tcps_0.on_data_received(tcps_0_received_event)
    tcps_0.on_client_disconnect(tcps_0_disconnect_event)
    button0.set_size(74, 36)
    textarea0.set_one_line(True)
    textarea1.set_one_line(True)
    textarea0.set_text(str(wlan_sta.ifconfig()[0]))
    textarea1.set_text(str("8000"))
    state = True

def loop():
    global \
        page0, \
        button0, \
        label0, \
        textarea0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcps_0, \
        client, \
        received_data, \
        state
    M5.update()
    tcps_0.check_event(timeout=10)

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

```

Example output:

    None

## **API**

## EasyTCPServer
Create an EasyTCPServer object.

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

MicroPython Code Block:

    .. code-block:: python

        from easysocket import EasyTCPServer

        server = EasyTCPServer(host="0.0.0.0", port=8080)

### `start`
Start the server.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        server.start()

### `stop`
Stop the server.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        server.stop()

### `close`

### `get_sessions`
Get all connected client sockets.

:return: A tuple of connected client sockets.
:rtype: tuple[EasyTCPClientSocket]

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        sessions = server.get_sessions()

### `on_client_connect`
Set the callback function for client connection event.

:param callback: The callback function. The callback function must accept a single argument,
                 which is the connected client socket instance of :class:`EasyTCPClientSocket`.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        def on_client_connect_cb(client_socket):
            print("Client connected")

        server.on_client_connect(on_client_connect_cb)

### `on_client_disconnect`
Set the callback function for client disconnection event.

:param callback: The callback function. The callback function must accept a single argument,
                 which is the disconnected client socket instance of :class:`EasyTCPClientSocket`.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        def on_client_disconnect_cb(client_socket):
            print("Client disconnected")

        server.on_client_disconnect(on_client_disconnect_cb)

### `on_data_received`
Set the callback function for data received event.

:param callback: The callback function. The callback function must accept a single argument,
                 which is a tuple containing the client socket instance of :class:`EasyTCPClientSocket` and the received data (bytes).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        def on_data_received_cb(args):
            client_socket, data = args
            print("Received:", data)

        server.on_data_received(on_data_received_cb)

### `check_event`
Check for events.

:param int timeout: The timeout in milliseconds. Default is -1 (no timeout).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        server.check_event()

### `setsockopt`

### `settimeout`

### `setblocking`

### `getsockname`

### `getpeername`

## EasyTCPClientSocket
Create an EasyTCPClientSocket object.

.. note::

    this is a wrapper class for the socket object used in EasyTCPServer.

:param socket sock: The socket object.

### `send`
Send data to the client.

:param bytes data: The data to send.
:return: The number of bytes sent.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        client_socket.send(data)

### `sendall`
Send all data to the client.

:param bytes data: The data to send.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        client_socket.sendall(data)

### `recv`

### `close`
Close the connection.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        client_socket.close()

### `settimeout`

### `setblocking`

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
