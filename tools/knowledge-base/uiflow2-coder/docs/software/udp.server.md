# EasyUDPServer

EasyUDPServer and EasyUDPClientSocket provide a simple way to create UDP servers and manage client connections in an event-driven manner.

## MicroPython Example

#### simple server

This example creates a UDP server that listens on port 8000 and displays the received data on the screen.

```python
import os, sys, io
import M5
from M5 import *
from easysocket import EasyUDPServer
import network
import time

title0 = None
label2 = None
label0 = None
label1 = None
wlan_sta = None
udps_0 = None

received_data = None
client_address_port = None

def udps_0_received_event(args):
    global title0, label2, label0, label1, wlan_sta, udps_0, received_data, client_address_port
    server, client_address_port, received_data = args
    label1.setText(str("Receive Msg:"))
    label2.setText(str((str(received_data) + str(client_address_port))))
    print((str(received_data) + str(client_address_port)))
    udps_0.sendto(received_data, client_address_port)

def setup():
    global title0, label2, label0, label1, wlan_sta, udps_0, received_data, client_address_port

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "UDPServer Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label2 = Widgets.Label("", 1, 146, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("Local IP:", 2, 68, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Receive Msg:", 2, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    wlan_sta = network.WLAN(network.STA_IF)
    print("wait network connecting")
    while not (wlan_sta.isconnected()):
        print(".")
        time.sleep(1)
    print("connect success")
    print(wlan_sta.ifconfig()[0])
    label0.setText(str((str("Local IP:") + str((wlan_sta.ifconfig()[0])))))
    udps_0 = EasyUDPServer(
        host="0.0.0.0",
        port=8000,
        mode=EasyUDPServer.MODE_UNICAST,
        multicast_group=None,
        verbose=False,
    )
    udps_0.on_data_received(udps_0_received_event)

def loop():
    global title0, label2, label0, label1, wlan_sta, udps_0, received_data, client_address_port
    M5.update()
    udps_0.check_event(timeout=-1)

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

## **API**

## `EasyUDPServer`
Create an EasyUDPServer object.

- Parameter `host` (`str`): The host address to bind to.
- Parameter `port` (`int`): The port number to bind to.
- Parameter `mode` (`int`): The UDP mode (unicast, broadcast, multicast). Default is unicast.
- Parameter `multicast_group` (`str`): The multicast group address (required if mode is multicast).
- Parameter `verbose` (`bool`): Whether to print verbose output.

> Note: start service automatically when initialized.
> Note: This class is non-blocking and event-driven. You need to call `check_event()` periodically to process events.

```python
from easysocket import EasyUDPServer

udp_server = EasyUDPServer(host="0.0.0.0", port=8080)
```

### `start`
Start the server.

```python
udp_server.start()
```

### `stop`
Stop the server.

```python
udp_server.stop()
```

### `close`

### `on_data_received`
Set the callback function for data received event.

- Parameter `callback`: The callback function.

```python
def on_data_received_cb(args):
    client, address, data = args
    print("Received:", data, "from", address)

udp_server.on_data_received(on_data_received_cb)
```

### `check_event`
Check for events.

- Parameter `timeout` (`int`): The timeout in milliseconds. Default is -1 (no timeout).

```python
udp_server.check_event()
```

### `sendto`
Send data to the remote server.

- Parameter `data` (`bytes`): The data to send.
- Parameter `address` (`tuple`): The (host, port) tuple to send data to.
- Returns: The number of bytes sent.

```python
udp_server.sendto(b"Hello", ("192.168.1.100", 8080))
```

### `setsockopt`
