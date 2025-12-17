.. py:currentmodule:: umqtt

umqtt.default
=============

.. include:: ../refs/software.umqtt.default.ref

`umqtt.default` rewrites the :py:meth:`subscribe` method and supports ca file.

UiFlow2 Example
---------------

MQTT basic
^^^^^^^^^^

Open the |cores3_mqtt_basic_example.m5f2| project in UiFlow2.

This example demonstrates how to connect to an MQTT broker.

UiFlow2 Code Block:

    |cores3_mqtt_basic_example.png|

Example output:

    None


MQTT over SSL
^^^^^^^^^^^^^

Open the |cores3_mqtt_over_ssl_example.m5f2| project in UiFlow2.

This example demonstrates how to connect to an MQTT broker over SSL.

UiFlow2 Code Block:

    |cores3_mqtt_over_ssl_example.png|

Example output:

    None


MicroPython Example
-------------------

MQTT basic
^^^^^^^^^^

This example demonstrates how to connect to an MQTT broker.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/softwave/mqtt/cores3_mqtt_basic_example.py

Example output:

    None


MQTT over SSL
^^^^^^^^^^^^^

This example demonstrates how to connect to an MQTT broker over SSL.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/softwave/mqtt/cores3_mqtt_over_ssl_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

MQTTClient
^^^^^^^^^^

.. class:: MQTTClient(client_id, server, port=0, user=None, password=None, keepalive=0, ssl=False, ssl_params={})

    Create an MQTTClient object.

    :param str client_id: the unique client id string used when connecting to
                          the broker.
    :param str server: the hostname or IP address of the remote broker.
    :param int port: the network port of the server host to connect to.
    :param user: a username for broker authentication.
    :type user: str or None
    :param password: a password for broker authentication.
    :type password: str or None
    :param int keepalive: maximum period in seconds allowed between
                          communications with the broker. If no other messages
                          are being exchanged, this controls the rate at which
                          the client will send ping messages to the broker.
    :param bool ssl: Whether to use ssl.
    :param dict ssl_params: Some parameters required to initiate an ssl connection.
    :return: MQTTClient object
    :rtype: MQTTClient

    UiFlow2 Code Block:

        |init.png|

        |init_ssl.png|

    MicroPython Code Block:

        .. code-block:: python

            from umqtt import MQTTClient

            mqtt_client = MQTTClient(
                'uf2',
                'y90166f4.ala.cn-hangzhou.emqxsl.cn',
                port=8883,
                user='test',
                password='test',
                keepalive=0,
                ssl=True,
                ssl_params={
                    "server_hostname":'y90166f4.ala.cn-hangzhou.emqxsl.cn',
                    "key": "/flash/certificate/emqxsl-ca.crt", # 私钥文件，双向认证的时候使用
                    "cert": "/flash/certificate/emqxsl-ca.crt", # 客户端证书文件，双向认证的时候使用
                    "cafile": "/flash/certificate/emqxsl-ca.crt", # CA证书，单向认证的时候使用
                }
            )


    .. method:: MQTTClient.connect(clean_session=True) -> bool

        Connect to a server. Returns True if this connection uses persisten
        session stored on a server (this will be always False if clean_session=True
        argument is used (default)).

        UiFlow2 Code Block:

            |connect.png|

        MicroPython Code Block:

            .. code-block:: python

                mqtt_client.connect(clean_session=True)


    .. method:: MQTTClient.disconnect() -> None

        Disconnect from a server, release resources.

        UiFlow2 Code Block:

            |disconnect.png|

        MicroPython Code Block:

            .. code-block:: python

                mqtt_client.disconnect()


    .. method:: MQTTClient.reconnect() -> None

        Disconnect from a server, release resources.

        UiFlow2 Code Block:

            |reconnect.png|

        MicroPython Code Block:

            .. code-block:: python

                mqtt_client.reconnect()


    .. method:: MQTTClient.ping() -> None

        Ping server (response is processed automatically by :py:meth:`wait_msg()`).

        MicroPython Code Block:

            .. code-block:: python

                mqtt_client.ping()


    .. method:: MQTTClient.publish(topic, msg, retain=False, qos=0) -> None

        Publish a message.

        :param topic: the topic that the message should be published on.
        :type topic: str or bytes or bytearray
        :param msg: the message to send as a will.
        :type msg: str or bytes or bytearray
        :param bool retain: if set to True, the will message will be set as
                            the "last will"/retained message for the topic.
        :param int qos: the quality of service level to use

        UiFlow2 Code Block:

            |publish.png|

        MicroPython Code Block:

            .. code-block:: python

                mqtt_client.publish(topic, msg, retain=False, qos=0)


    .. method:: MQTTClient.subscribe(topic, handler, qos=0) -> None

        Subscribe to a topic.

        :param topic: a string specifying the subscription topic to subscribe to.
        :type topic: str or bytes or bytearray
        :param function handler: called when a message has been received on a topic
                                that the client subscribes to and the message does
                                match an existing topic filter callback.
        :param int qos: the desired quality of service level for the subscription.
                        Defaults to 0.

        UiFlow2 Code Block:

            |subscribe.png|

        An handler showing a message has been received::

            def on_sub_cb(data):
                print("topic:", data[0])
                print("msg:", data[1])

        On uiflow2, you can get the **topic** and **message** of the current handler
        through |get_topic.png| and |get_msg.png|.


    .. method:: MQTTClient.unsubscribe(topic) -> None

        Unsubscribe from a topic.

        :param topic: a string specifying the subscription topic to unsubscribe from.
        :type topic: str or bytes or bytearray

        UiFlow2 Code Block:

            |unsubscribe.png|

        MicroPython Code Block:

            .. code-block:: python

                mqtt_client.unsubscribe(topic)


    .. method:: MQTTClient.set_last_will(topic, msg, retain=False, qos=0) -> None

        .. important::

            Should be called before :py:meth:`connect()`.

        Set MQTT "last will" message.

        :param topic: the topic that the will message should be published on.
        :type topic: str or bytes or bytearray
        :param msg: the message to send as a will. If not given, or set to None a
                    zero length message will be used as the will.
        :type msg: str or bytes or bytearray
        :param bool retain: if set to True, the will message will be set as
                            the "last will"/retained message for the topic.
        :param int qos: the quality of service level to use for the will.

        UiFlow2 Code Block:

            |set_last_will.png|

        MicroPython Code Block:

            .. code-block:: python

                mqtt_client.set_last_will()


    .. method:: MQTTClient.wait_msg() -> None

        .. important::

            :py:meth:`wait_msg()` and :py:meth:`check_msg()` are "main loop iteration"
            methods, blocking and non-blocking version. They should be called
            periodically in a loop, :py:meth:`wait_msg()` if you don't have any
            other foreground tasks to perform (i.e. your app just reacts to
            subscribed MQTT messages), :py:meth:`check_msg()` if you process other
            foreground tasks too.

            Note that you don't need to call :py:meth:`wait_msg()` /
            :py:meth:`check_msg()` if you only publish messages, never subscribe
            to them.

        Wait for a server message.

        MicroPython Code Block:

            .. code-block:: python

                mqtt_client.wait_msg()


    .. method:: MQTTClient.check_msg(attempts=2) -> None

        Check if there's pending message from server. If yes, process the same way
        as :py:meth:`wait_msg()`, if not, return immediately.

        UiFlow2 Code Block:

            |wait_msg.png|

        MicroPython Code Block:

            .. code-block:: python

                mqtt_client.check_msg()
