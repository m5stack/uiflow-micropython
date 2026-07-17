# EasyUDPClient

EasyUDPClient provides a simple way to create UDP clients in an event-driven manner.

## MicroPython Example

#### simple client

This example creates a UDP client that connects to a server and sends data.

```python
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

## **API**

## `EasyUDPClient`
Create an EasyUDPClient object.

- Parameter `remote_host` (`str`): The remote host address.
- Parameter `remote_port` (`int`): The remote port number.
- Parameter `mode` (`int`): The UDP mode (unicast, broadcast, multicast). Default is unicast.

> Note: connection is initiated in the background when the object is created.
> Note: This class is non-blocking and event-driven. You need to call `check_event()` periodically to process events.

```python
from easysocket import EasyUDPClient

udp_client = EasyUDPClient("192.168.1.100", 8080, mode=EasyUDPClient.MODE_UNICAST)
```

### `connect`
Connect to the remote server.

```python
udp_client.connect()
```

### `on_data_received`
Set the callback function for data received event.

- Parameter `callback`: The callback function.

```python
def on_data_received_cb(client, data):
    print("Received:", data)

udp_client.on_data_received(on_data_received_cb)
```

### `check_event`
Check for events.

- Parameter `timeout` (`int`): The timeout in milliseconds. Default is -1 (no timeout).

```python
udp_client.check_event()
```

### `send`
Send data to the remote server.

- Parameter `data` (`bytes`): The data to send.
- Returns: The number of bytes sent.

```python
udp_client.send(b"Hello")
```

### `sendto`
Send data to the remote server.

- Parameter `data` (`bytes`): The data to send.
- Parameter `address` (`tuple`): The (host, port) tuple to send data to.
- Returns: The number of bytes sent.

```python
udp_client.sendto(b"Hello", ("192.168.1.100", 8080))
```

### `recv`

### `recvfrom`

### `close`
Close the socket.

```python
udp_client.close()
```

### `setsockopt`

### `getsockname`
Return the socket's own address.

- Returns: The socket's own address. the format is (host, port).
- Return type: tuple

```python
# get local ip address
client_socket.getsockname()[0]
```

### `getpeername`
Return the remote address to which the socket is connected.

- Returns: The remote address. the format is (host, port).
- Return type: tuple

```python
# get remote ip address
client_socket.getpeername()[0]
```
