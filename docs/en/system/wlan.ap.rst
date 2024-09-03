.. currentmodule:: network
.. _network.WLAN:

WLAN AP -- control built-in WiFi interfaces
==============================================

This class provides a driver for WiFi AP network processors.

.. include:: ../refs/system.wlan.ap.ref

Micropython Example:

    .. literalinclude:: ../../../examples/system/wlan_ap/wlan_ap_cores3_example.py
        :language: python
        :linenos:

UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |wlan_ap_cores3_example.m5f2|

Constructors
------------
.. class:: WLAN(interface_id)

Create a WLAN network interface object. Supported interfaces are
``network.AP_IF`` (access point, allows other WiFi clients to connect)

    UIFLOW2:

        |init.png|

Methods
-------
.. method:: WLAN.status([param])

    Return the current status of the wireless connection.

    When called with no argument the return value describes the network link status.

    UIFLOW2:

        |scan.png|

        |scan_get_mac.png|

.. method:: WLAN.isconnected()

    In AP mode returns ``True`` when a
    station is connected. Returns ``False`` otherwise.

        |isconnected.png|

.. method:: WLAN.active([is_active])

    Activate ("up") or deactivate ("down") network interface, if boolean
    argument is passed. Otherwise, query current state if no argument is
    provided. Most other methods require active interface.

        |active.png|


.. method:: WLAN.ifconfig([(ip, subnet, gateway, dns)])

   Get/set IP-level network interface parameters: IP address, subnet mask,
   gateway and DNS server. When called with no arguments, this method returns
   a 4-tuple with the above information. To set the above values, pass a
   4-tuple with the required information.

        |get_local_ip.png|

        |get_subnet.png|

        |get_gateway.png|

        |get_dns.png|



.. method:: WLAN.config('param')
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

        |set_ssid.png|

        |set_password.png|

        |set_hidden_status.png|

        |set_auth_mode.png|

        |set_channel.png|

        |set_dhcp_hostname.png|

        |set_max_clients.png|

        |set_txpower.png|

        |get_ssid.png|

        |get_password.png|

        |get_mac.png|

        |get_hidden_status.png|

        |get_auth_mode.png|

        |get_channel.png|

        |get_dhcp_hostname.png|

        |get_max_clients.png|

        |get_txpower.png|


        
Constants
---------
.. data:: WLAN.AUTH_OPEN
        WLAN.AUTH_WEP
        WLAN.AUTH_WPA_PSK
        WLAN.AUTH_WPA2_PSK
        WLAN.AUTH_WPA_WPA2_PSK
        WLAN.AUTH_WPA2_ENTERPRISE
        WLAN.AUTH_WPA3_PSK
        WLAN.AUTH_WPA2_WPA3_PSK
        WLAN.AUTH_WAPI_PSK


Allowed values for the ``WLAN.config(authmode=...)`` network interface parameter:

        * ``AUTH_OPEN``: 0 -- open
        * ``AUTH_WEP``: 1 -- WEP
        * ``AUTH_WPA_PSK``: 2 -- WPA-PSK
        * ``AUTH_WPA2_PSK``: 3 -- WPA2-PSK
        * ``AUTH_WPA_WPA2_PSK``: 4 -- WPA/WPA2-PSK
        * ``AUTH_WPA2_ENTERPRISE``: 5 -- WPA2-Enterprise
        * ``AUTH_WPA3_PSK``: 6 -- WPA3-PSK
        * ``AUTH_WPA2_WPA3_PSK``: 7 -- WPA2/WPA3-PSK
        * ``AUTH_WAPI_PSK``: 8 -- WAPI-PSK
