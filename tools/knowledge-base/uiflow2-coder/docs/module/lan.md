# LAN Module

Supported Products:

     LAN Module

## MicroPython Example

#### Get the weather

This example connects to the network using the LAN module and sends an HTTP request to query the geographical location of the current public IP address.

```python
import os, sys, io
import M5
from M5 import *
import network
from module import LANModule
import time
import requests2

label_status = None
title0 = None
label_info = None
wlan = None
lan_0 = None
http_req = None

def setup():
    global label_status, title0, label_info, wlan, lan_0, http_req
    M5.begin()
    Widgets.fillScreen(0x222222)
    label_status = Widgets.Label(
        "Waiting for network connection", 5, 50, 1.0, 0xFF0000, 0x222222, Widgets.FONTS.DejaVu18
    )
    title0 = Widgets.Title("LANModule Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_info = Widgets.Label("Get info", 5, 90, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    lan_0 = LANModule(cs=1, rst=0, int=10)
    lan_0.active(True)
    while not (lan_0.isconnected()):
        time.sleep(1)
        print(".")
    print("local network is connected")
    label_status.setText(str("Network connected!"))
    label_status.setColor(0x00FF00, 0x222222)
    http_req = requests2.get(
        "https://wttr.in/?format=%22%C,%20%t%22", headers={"Content-Type": "application/json"}
    )
    print(http_req.text)
    label_info.setText(str(http_req.text))

def loop():
    global label_status, title0, label_info, wlan, lan_0, http_req
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            lan_0.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

## **API**

## class LANModule

### `class module.lan.LANModule(cs=-1, rst=-1, int=-1)`

    Create a LANModule object.

    - Parameter `cs`: chip select pin
    - Parameter `rst`: reset pin
    - Parameter `int`: interrupt pin

```python
from module import LANModule

lan_0 = LANModule(cs=1, rst=0, int=10)
```
### `LANModule.deinit()`

        Deinitialize the LAN module.

```python
lan_0.deinit()
```
### `LANModule.isconnected()`

        Check whether the physical Ethernet link is active.

        - Returns: `True` if the Ethernet cable is connected and the link is up, `False` otherwise.
        - Return type: bool

```python
lan_0.isconnected()
```
### `LANModule.status()`

        Get the LAN connect status.

        - Returns: LAN status code, possible values:

            - network.ETH_INITIALIZED(0): Ethernet interface initialized
            - network.ETH_STARTED(1): Ethernet driver started
            - network.ETH_STOPPED(2): Ethernet driver stopped
            - network.ETH_CONNECTED(3): Physical link established (cable connected)
            - network.ETH_DISCONNECTED(4): Physical link lost (cable disconnected)
            - network.ETH_GOT_IP(5): IP address obtained, network ready

        - Return type: int

```python
lan_0.status()
```
### `LANModule.ifconfig()[0]`

        Get the local IP address.

        - Returns: Local IP address as a string, e.g. "192.168.1.100"
        - Return type: str

```python
lan_0.ifconfig()[0]
```
### `LANModule.ifconfig()[1]`

            Get the subnet mask.

            - Returns: Subnet mask as a string, e.g. "255.255.255.0"
            - Return type: str

```python
lan_0.ifconfig()[1]
```
### `LANModule.ifconfig()[2]`

        Get the gateway address.

        - Returns: Gateway IP as a string, e.g. "192.168.1.1"
        - Return type: str

```python
lan_0.ifconfig()[2]
```
### `LANModule.ifconfig()[3]`

        Get the DNS server address.

        - Returns: DNS server IP as a string, e.g. "8.8.8.8"
        - Return type: str

```python
lan_0.ifconfig()[3]
```
### `LANModule.config('mac')`

            Get the MAC address of the LAN module.

            - Parameter `param`: Configuration parameter name, must be 'mac'
            - Type of `param`: str

            - Returns: MAC address as a string or bytes, e.g. "00:11:22:33:44:55"
            - Return type: str or bytes

```python
mac_address = lan_0.config('mac')
```
### `LANModule.active([state])`

        Enable or disable the LAN interface.

        - Parameter `| None state` (`bool`): Optional boolean value. If `True`, activates the LAN interface; if `False`, deactivates it.
        - Returns: Current active state of the interface if no parameter is given.
        - Return type: bool

```python
lan_0.active([state])
```
### `LANModule.config(mac=bytearray)`

        Set the MAC address of the LAN module.

        - Parameter `mac`: MAC address to set, as a bytearray of 6 bytes
        - Type of `mac`: bytearray

        - Returns: None

```python
lan_0.config(mac=bytearray([0x02, 0x00, 0x00, 0x12, 0x34, 0x56]))
```
### `LANModule.set_default_netif()`

        Sets the default network interface.

```python
lan_0.set_default_netif()
```
### `LANModule.ifconfig([(ip, subnet, gateway, dns)])`

        Get or set the IP address, subnet mask, gateway, and DNS server for the LAN interface.

        - Parameter `ip` (`str`): Static IP address to assign to the LAN interface.
        - Parameter `subnet` (`str`): Subnet mask (usually '255.255.255.0').
        - Parameter `gateway` (`str`): IP address of the network gateway/router.
        - Parameter `dns` (`str`): DNS server IP address.

```python
lan_0.ifconfig([(ip, subnet, gateway, dns)])
```
### `LANModule.ifconfig([(ip, subnet, gateway, dns)])`

        Get or set the IP address, subnet mask, gateway, and DNS server for the LAN interface.

        - Parameter `ip` (`str`): Static IP address to assign to the LAN interface.
        - Parameter `subnet` (`int`): Subnet mask as a CIDR prefix length (e.g. `24` means `255.255.255.0`).
        - Parameter `gateway` (`str`): IP address of the network gateway/router.
        - Parameter `dns` (`str`): DNS server IP address.

```python
lan_0.ifconfig([(ip, subnet, gateway, dns)])
```
