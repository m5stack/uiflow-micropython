.. currentmodule:: network
.. _network.WLAN.sta:

WLAN STA -- control built-in WiFi interfaces
==============================================

This class provides a driver for WiFi STA network processors.

.. include:: ../refs/system.wlan.sta.ref

Micropython Example:

    .. literalinclude:: ../../../examples/system/wlan_sta/wlan_sta_cores3_example.py
        :language: python
        :linenos:

UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |wlan_sta_cores3_example.m5f2|

Constructors
------------
.. class:: WLAN(interface_id)
   :noindex:

Create a WLAN network interface object. Supported interfaces are
``network.STA_IF`` (station aka client, connects to upstream WiFi access points)

    UIFLOW2:

        |init.png|

Methods
-------
.. method:: WLAN.status([param])
   :noindex:


    Return the current status of the wireless connection.

    When called with no argument the return value describes the network link status.
    The possible statuses are defined as constants:

        * ``STAT_IDLE`` -- no connection and no activity,
        * ``STAT_CONNECTING`` -- connecting in progress,
        * ``STAT_WRONG_PASSWORD`` -- failed due to incorrect password,
        * ``STAT_NO_AP_FOUND`` -- failed because no access point replied,
        * ``STAT_CONNECT_FAIL`` -- failed due to other problems,
        * ``STAT_GOT_IP`` -- connection successful.

    When called with one argument *param* should be a string naming the status
    parameter to retrieve.  
    
    Supported parameters in WiFI STA mode are: ``'rssi'``.

    UIFLOW2:

        |get_rssi.png|


.. method:: WLAN.isconnected()
   :noindex:


    In case of STA mode, returns ``True`` if connected to a WiFi access
    point and has a valid IP address.

    UIFLOW2:

        |isconnected.png|


.. method:: WLAN.active([is_active])
   :noindex:


    Activate ("up") or deactivate ("down") network interface, if boolean
    argument is passed. Otherwise, query current state if no argument is
    provided. Most other methods require active interface.

        |active.png|


.. method:: WLAN.connect(ssid=None, key=None, *, bssid=None)

    Connect to the specified wireless network, using the specified key.
    If *bssid* is given then the connection will be restricted to the
    access-point with that MAC address (the *ssid* must also be specified
    in this case).

        |connect.png|


.. method:: WLAN.disconnect()
   :noindex:


    Disconnect from the currently connected wireless network.

        |disconnect.png|

.. method:: WLAN.ifconfig([(ip, subnet, gateway, dns)])
   :noindex:

   Get/set IP-level network interface parameters: IP address, subnet mask,
   gateway and DNS server. When called with no arguments, this method returns
   a 4-tuple with the above information. To set the above values, pass a
   4-tuple with the required information. å

        |get_localip.png|

        |get_subnet.png|

        |get_gateway.png|

        |get_dns.png|



.. method:: WLAN.config('param')
            WLAN.config(param=value, ...)
   :noindex:

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

        |set_dhcp_hostname.png|

        |set_reconnects.png|

        |set_txpower.png|

        |get_dhcp_hostname.png|

        |get_reconnects.png|

        |get_txpower.png|

        |get_mac.png|



.. method:: WLAN.scan()

    Scan for the available wireless networks.
    Hidden networks -- where the SSID is not broadcast -- will also be scanned
    if the WLAN interface allows it.

    Scanning is only possible on STA interface. Returns list of tuples with
    the information about WiFi access points:

        (ssid, bssid, channel, RSSI, security, hidden)

    *bssid* is hardware address of an access point, in binary form, returned as
    bytes object. You can use `binascii.hexlify()` to convert it to ASCII form.

    There are five values for security:

        * 0 -- open
        * 1 -- WEP
        * 2 -- WPA-PSK
        * 3 -- WPA2-PSK
        * 4 -- WPA/WPA2-PSK

    and two for hidden:

        * 0 -- visible
        * 1 -- hidden

        |scan.png|

        |scan_get_value.png|