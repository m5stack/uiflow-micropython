<!-- .. currentmodule:: network -->
<!-- .. _network.WLAN: -->

# WLAN AP -- control built-in WiFi interfaces

This class provides a driver for WiFi AP network processors.

<!-- .. include:: ../refs/system.wlan.ap.ref -->

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import network

title0 = None
label0 = None
label1 = None
label2 = None
wlan = None

ap_client = None

def setup():
    global title0, label0, label1, label2, wlan

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("WLAN AP CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("label0", 2, 77, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 2, 111, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 2, 145, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    wlan = network.WLAN(network.AP_IF)
    wlan.config(max_clients=4)
    wlan.config(essid="M5CoreS3AP")
    wlan.active(True)

# Please connect to the AP named M5CoreS3.
def loop():
    global title0, label0, label1, label2, wlan
    M5.update()
    label0.setText(str((str("AP is connected?:") + str((wlan.isconnected())))))
    label1.setText(str((str("SSID:") + str((wlan.config("essid"))))))
    for ap_client in wlan.status("stations"):
        label2.setText(str(ap_client[0]))

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

UIFLOW2 Example:

<!-- .. only:: builder_html -->

    |wlan_ap_cores3_example.m5f2|

## Constructors

<!-- .. class:: WLAN(interface_id) -->

Create a WLAN network interface object. Supported interfaces are
``network.AP_IF`` (access point, allows other WiFi clients to connect)

    UIFLOW2:

## Methods

<!-- .. method:: WLAN.status([param]) -->

    Return the current status of the wireless connection.

    When called with no argument the return value describes the network link status.

    UIFLOW2:

<!-- .. method:: WLAN.isconnected() -->

    In AP mode returns ``True`` when a
    station is connected. Returns ``False`` otherwise.

<!-- .. method:: WLAN.active([is_active]) -->

    Activate ("up") or deactivate ("down") network interface, if boolean
    argument is passed. Otherwise, query current state if no argument is
    provided. Most other methods require active interface.

<!-- .. method:: WLAN.ifconfig([(ip, subnet, gateway, dns)]) -->

   Get/set IP-level network interface parameters: IP address, subnet mask,
   gateway and DNS server. When called with no arguments, this method returns
   a 4-tuple with the above information. To set the above values, pass a
   4-tuple with the required information.

<!-- .. method:: WLAN.config('param') -->
            WLAN.config(param=value, ...)

   Get or set general network interface parameters. These methods allow to work
   with additional parameters beyond standard IP configuration (as dealt with by
   `AbstractNIC.ipconfig()`). These include network-specific and hardware-specific
   parameters. For setting parameters, keyword argument syntax should be used,
   multiple parameters can be set at once. For querying, parameters name should
   be quoted as a string, and only one parameter can be queried at a time:

   Following are commonly supported parameters (availability of a specific parameter
   depends on network technology type, driver, and `MicroPython port`).

   =============  ===========
   Parameter      Description
   =============  ===========
   mac            MAC address (bytes)
   ssid           WiFi access point name (string)
   channel        WiFi channel (integer)
   hidden         Whether SSID is hidden (boolean)
   security       Security protocol supported (enumeration, see module constants)
   key            Access key (string)
   hostname       The hostname that will be sent to DHCP (STA interfaces) and mDNS (if supported, both STA and AP). (Deprecated, use :func:`network.hostname` instead)
   reconnects     Number of reconnect attempts to make (integer, 0=none, -1=unlimited)
   txpower        Maximum transmit power in dBm (integer or float)
   pm             WiFi Power Management setting (see below for allowed values)
   =============  ===========

## Constants

<!-- .. data:: WLAN.AUTH_OPEN -->
        WLAN.AUTH_WEP
        WLAN.AUTH_WPA_PSK
        WLAN.AUTH_WPA2_PSK
        WLAN.AUTH_WPA_WPA2_PSK
        WLAN.AUTH_WPA2_ENTERPRISE
        WLAN.AUTH_WPA3_PSK
        WLAN.AUTH_WPA2_WPA3_PSK
        WLAN.AUTH_WAPI_PSK

Allowed values for the ``WLAN.config(authmode=...)`` network interface parameter:

        - ``AUTH_OPEN``: 0 -- open
        - ``AUTH_WEP``: 1 -- WEP
        - ``AUTH_WPA_PSK``: 2 -- WPA-PSK
        - ``AUTH_WPA2_PSK``: 3 -- WPA2-PSK
        - ``AUTH_WPA_WPA2_PSK``: 4 -- WPA/WPA2-PSK
        - ``AUTH_WPA2_ENTERPRISE``: 5 -- WPA2-Enterprise
        - ``AUTH_WPA3_PSK``: 6 -- WPA3-PSK
        - ``AUTH_WPA2_WPA3_PSK``: 7 -- WPA2/WPA3-PSK
        - ``AUTH_WAPI_PSK``: 8 -- WAPI-PSK
