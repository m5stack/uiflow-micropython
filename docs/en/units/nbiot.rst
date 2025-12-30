NB-IoT Unit
===========

.. sku: U111 U112

.. include:: ../refs/unit.nbiot.ref

The ``NB-IOT Unit`` is a wireless communication module suitable for global wide Cat-NB frequency band . It has a built-in SIM7020G communication module, uses serial communication (AT instruction set control).


Support the following products:

    ================== ====================
    |Unit NBIoT|       |Unit NBIoT-CN|
    ================== ====================

.. note::

    Please ensure that the device supports the NB-IoT frequency bands in your area before use.

.. note::

    Please ensure that the firmware version of SIM7020 is greater than or equal to **1752B12SIM7020C**.

    |get_version.png| can be used to check the firmware version.


UiFlow2 Example
---------------

NBIoT HTTP Example
^^^^^^^^^^^^^^^^^^

Open the |cores3_unit_nbiot_http_example.m5f2| project in UiFlow2.

This example shows how to send HTTP request using the NBIoT Unit.

click **Send** button to send HTTP request. Response data will be printed in the textarea.

UiFlow2 Code Block:

    |cores3_unit_nbiot_http_example.png|

Example output:

    Output of received NBIoT message data on screen.


MQTT Example
^^^^^^^^^^^^

Open the |cores3_unit_nbiot_mqtt_example.m5f2| project in UiFlow2.

This example shows how to send MQTT message using the NBIoT Unit.

UiFlow2 Code Block:

    |cores3_unit_nbiot_mqtt_example.png|

Example output:

    Output of received NBIoT message data on screen.


MicroPython Example
-------------------

NBIoT HTTP Example
^^^^^^^^^^^^^^^^^^

This example shows how to send HTTP request using the NBIoT Unit.

click **Send** button to send HTTP request. Response data will be printed in the textarea.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/nbiot/cores3_unit_nbiot_http_example.py
        :language: python
        :linenos:

Example output:

    Output of received NBIoT message data on screen.


MQTT Example
^^^^^^^^^^^^

This example shows how to send MQTT message using the NBIoT Unit.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/nbiot/cores3_unit_nbiot_mqtt_example.py
        :language: python
        :linenos:

Example output:

    Output of received NBIoT message data on screen.


**API**
-------

.. autoclass:: unit.nbiot.NBIOTUnit
    :members:


    .. py:method:: connect(apn="cmnbiot")

        Connect to the NB-IoT network.

        :param str apn: The APN of the NB-IoT network. Default is "cmnbiot".

        UiFlow2 Code Block:

            |connect.png|

        MicroPython Code Block:

            .. code-block:: python

                nbiot.connect("cmnbiot")


    .. py:method:: isconnected()

        Check if the NB-IoT unit is connected to the network.

        :return: True if connected, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |isconnected.png|

        MicroPython Code Block:

            .. code-block:: python

                if nbiot.isconnected():
                    print("NB-IoT unit is connected")
                else:
                    print("NB-IoT unit is not connected")


    .. py:method:: active(en)

        Activate or deactivate the NB-IoT unit. Deactivating will enter low power consumption mode.

        :param bool en: True to activate, False to deactivate.

        UiFlow2 Code Block:

            |active.png|

        MicroPython Code Block:

            .. code-block:: python

                nbiot.active(True)


    .. py:method:: status([param])

        Get the status of the NB-IoT unit.

        Following are commonly supported parameters.

        ================= =================
        Parameter         Description
        ----------------- -----------------
        rssi              signal strength
        ----------------- -----------------
        pin               SIM Card status
        ----------------- -----------------
        station           station registration status
        ================= =================

        :param str param: Optional parameter to specify the status type.
        :return: Status information.
        :rtype: str | tuple

        UiFlow2 Code Block:

            |get_rssi_status.png|

            |get_sim_status.png|

            |get_station_info.png|

        MicroPython Code Block:

            .. code-block:: python

                # get signal strength
                print(nbiot.status("rssi"))

                # get SIM Card status
                print(nbiot.status("pin"))

                # get station registration status
                print(nbiot.status("station"))


    .. py:method:: ifconfig

        Get IP-level network interface parameters: IP address, subnet mask, gateway and DNS server.

        :return: A tuple with the network interface parameters.
        :rtype: tuple

        UiFlow2 Code Block:

            |get_local_ip.png|

            |get_subnet.png|

            |get_gateway.png|

            |get_dns.png|

        MicroPython Code Block:

            .. code-block:: python

                # Get IP address
                print(nbiot.ifconfig()[0])
                # Get subnet mask
                print(nbiot.ifconfig()[1])
                # Get gateway
                print(nbiot.ifconfig()[2])
                # Get DNS server
                print(nbiot.ifconfig()[3])


    .. py:method:: config('param')
                   config(param=value)

        Get or set the configuration parameters of the NB-IoT unit.

        Following are commonly supported parameters.

        ================= ================= =================
        Parameter         permissions       Description
        ----------------- ----------------- -----------------
        apn               R                 Access Point Name
        ----------------- ----------------- -----------------
        mode              R                 Network mode(only supported NB-IoT)
        ----------------- ----------------- -----------------
        band              R/W               Frequency Band
        ----------------- ----------------- -----------------
        ccid              R                 SIM Card CCID
        ----------------- ----------------- -----------------
        imei              R                 Device IMEI
        ----------------- ----------------- -----------------
        imsi              R                 SIM Card IMSI
        ----------------- ----------------- -----------------
        mfr               R                 Manufacturer
        ----------------- ----------------- -----------------
        model             R                 Module Model
        ----------------- ----------------- -----------------
        version           R                 Firmware Version
        ================= ================= =================

        :param str param: The configuration parameter to get or set.
        :param value: The value to set for the configuration parameter.
        :return: The value of the configuration parameter when getting.
        :rtype: None | str | int | tuple

        UiFlow2 Code Block:

            |get_apn.png|

            |get_mode.png|

            |get_iccid.png|

            |get_imei.png|

            |get_imsi.png|

            |get_mfr.png|

            |get_model.png|

            |get_version.png|

        MicroPython Code Block:

            .. code-block:: python

                # Get apn
                print(nbiot.config('apn'))

                # Get network mode
                nbiot.config('mode')

                # Get Frequency Band
                nbiot.config('band')

                # Set Frequency Band
                nbiot.config(band=(1, 3, 5, 8))

                # Get CCID
                nbiot.config('ccid')

                # Get IMEI
                nbiot.config('imei')

                # Get IMSI
                nbiot.config('imsi')

                # Get Manufacturer
                nbiot.config('mfr')

                # Get Module Model
                nbiot.config('model')

                # Get Firmware Version
                nbiot.config('version')


    .. py:method:: request(method, url, data=None, json=None, headers={}, stream=None, auth=None, timeout=None, parse_headers=True)
                   head(url, **kw)
                   get(url, **kw)
                   post(url, **kw)
                   put(url, **kw)
                   patch(url, **kw)
                   delete(url, **kw)

        Send an HTTP request.

        :param str method: HTTP method to use (e.g. "GET", "POST").
        :param str url: URL to send the request to.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like object to send in the body of the Request.
        :param json: (optional) A JSON serializable Python object to send in the body of the Request.
        :param dict headers: (optional) Dictionary of HTTP Headers to send with the Request.
        :param bool stream: (optional) if False, the response content will be immediately downloaded.
        :param tuple auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
        :param float timeout: (optional) How many seconds to wait for the server to send data before giving up.
        :param bool parse_headers: (optional) Whether to parse response headers.

        :return: A Response object.

        .. note::

            See :mod:`requests2` for more details.

        UiFlow2 Code Block:

            |http_request.png|

        MicroPython Code Block:

            .. code-block:: python

                # GET request
                response = nbiot.get("http://httpbin.org/get")
                print(response.status_code)
                print(response.text)
                response.close()

                # POST request with JSON data
                response = nbiot.post("http://httpbin.org/post", json={"key": "value"})
                print(response.json())
                response.close()


    .. py:method:: MQTTClient(client_id, server, port=0, user=None, password=None, keepalive=0, ssl=False, ssl_params={})

        Create an MQTT client.

        :param str client_id: The unique client ID string.
        :param str server: The hostname or IP address of the remote broker.
        :param int port: Network port of the server host to connect to. Default is 0.
        :param str user: User name for authentication.
        :param str password: Password for authentication.
        :param int keepalive: Maximum period in seconds allowed between communications with the broker. Default is 0.
        :param bool ssl: Whether to use SSL/TLS support. Default is False.
        :param dict ssl_params: SSL/TLS parameters.

        :return: An MQTTClient object.

        .. note::

            See :class:`MQTTClient <umqtt.MQTTClient>` for more details.

        UiFlow2 Code Block:

            |mqtt_client.png|

        MicroPython Code Block:

            .. code-block:: python

                mqtt = nbiot.MQTTClient("client_id", "mqtt.m5stack.com", port=1883, user="user", password="password")
                mqtt.connect()
                mqtt.publish("topic", "message")
                mqtt.subscribe("topic", lambda topic, msg: print(topic, msg))
                mqtt.check_msg()
