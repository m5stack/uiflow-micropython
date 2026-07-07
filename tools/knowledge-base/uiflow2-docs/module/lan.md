# LAN Module

<!-- .. include:: ../refs/module.lan.ref -->

Supported Products:
######

###### | |LAN Module|            |

## UiFlow2 Example

#### Get the weather

This example connects to the network using the LAN module and sends an HTTP request to query the geographical location of the current public IP address.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Get the weather

This example connects to the network using the LAN module and sends an HTTP request to query the geographical location of the current public IP address.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

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

Example output:

    None

## **API**

<!-- .. _module.LAN.Methods: -->

## class LANModule

<!-- .. class:: module.lan.LANModule(cs=-1, rst=-1, int=-1) -->

    Create a LANModule object.

    :param cs: chip select pin
    :param rst: reset pin
    :param int: interrupt pin

    UiFlow2 Code Block:

    MicroPython Code Block:

<!-- .. code-block:: python -->

            from module import LANModule

            lan_0 = LANModule(cs=1, rst=0, int=10)

<!-- .. method:: LANModule.deinit() -->

        Deinitialize the LAN module.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                lan_0.deinit()

<!-- .. method:: LANModule.isconnected() -->

        Check whether the physical Ethernet link is active.

        :return: `True` if the Ethernet cable is connected and the link is up, `False` otherwise.
        :rtype: bool

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                lan_0.isconnected()

<!-- .. method:: LANModule.status() -->

        Get the LAN connect status.

        :return: LAN status code, possible values:

            - network.ETH_INITIALIZED(0): Ethernet interface initialized
            - network.ETH_STARTED(1): Ethernet driver started
            - network.ETH_STOPPED(2): Ethernet driver stopped
            - network.ETH_CONNECTED(3): Physical link established (cable connected)
            - network.ETH_DISCONNECTED(4): Physical link lost (cable disconnected)
            - network.ETH_GOT_IP(5): IP address obtained, network ready

        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                lan_0.status()

<!-- .. method:: LANModule.ifconfig()[0] -->

        Get the local IP address.

        :return: Local IP address as a string, e.g. "192.168.1.100"
        :rtype: str

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                lan_0.ifconfig()[0]

<!-- .. method:: LANModule.ifconfig()[1] -->

            Get the subnet mask.

            :return: Subnet mask as a string, e.g. "255.255.255.0"
            :rtype: str

            UiFlow2 Code Block:

            MicroPython Code Block:

<!-- .. code-block:: python -->

                    lan_0.ifconfig()[1]

<!-- .. method:: LANModule.ifconfig()[2] -->

        Get the gateway address.

        :return: Gateway IP as a string, e.g. "192.168.1.1"
        :rtype: str

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                lan_0.ifconfig()[2]

<!-- .. method:: LANModule.ifconfig()[3] -->

        Get the DNS server address.

        :return: DNS server IP as a string, e.g. "8.8.8.8"
        :rtype: str

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                lan_0.ifconfig()[3]

<!-- .. method:: LANModule.config('mac') -->

            Get the MAC address of the LAN module.

            :param param: Configuration parameter name, must be 'mac'
            :type param: str

            :return: MAC address as a string or bytes, e.g. "00:11:22:33:44:55"
            :rtype: str or bytes

            UiFlow2 Code Block:

            MicroPython Code Block:

<!-- .. code-block:: python -->

                    mac_address = lan_0.config('mac')

<!-- .. method:: LANModule.active([state]) -->

        Enable or disable the LAN interface.

        :param bool | None state: Optional boolean value. If `True`, activates the LAN interface; if `False`, deactivates it.
        :return: Current active state of the interface if no parameter is given.
        :rtype: bool

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                lan_0.active([state])

<!-- .. method:: LANModule.config(mac=bytearray) -->
        :no-index:

        Set the MAC address of the LAN module.

        :param mac: MAC address to set, as a bytearray of 6 bytes
        :type mac: bytearray

        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                lan_0.config(mac=bytearray([0x02, 0x00, 0x00, 0x12, 0x34, 0x56]))

<!-- .. method:: LANModule.set_default_netif() -->

        Sets the default network interface.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                lan_0.set_default_netif()

<!-- .. method:: LANModule.ifconfig([(ip, subnet, gateway, dns)]) -->

        Get or set the IP address, subnet mask, gateway, and DNS server for the LAN interface.

        :param str ip: Static IP address to assign to the LAN interface.
        :param str subnet: Subnet mask (usually '255.255.255.0').
        :param str gateway: IP address of the network gateway/router.
        :param str dns: DNS server IP address.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                lan_0.ifconfig([(ip, subnet, gateway, dns)])

<!-- .. method:: LANModule.ifconfig([(ip, subnet, gateway, dns)]) -->
        :no-index:

        Get or set the IP address, subnet mask, gateway, and DNS server for the LAN interface.

        :param str ip: Static IP address to assign to the LAN interface.
        :param int subnet: Subnet mask as a CIDR prefix length (e.g. `24` means `255.255.255.0`).
        :param str gateway: IP address of the network gateway/router.
        :param str dns: DNS server IP address.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                lan_0.ifconfig([(ip, subnet, gateway, dns)])
