.. py:currentmodule:: umqtt

umqtt.default
=============

.. include:: ../refs/software.umqtt.default.ref

`umqtt.default` rewrites the :py:meth:`subscribe` method and supports ca file.


Micropython Example:

    .. literalinclude:: ../../../examples/softwave/mqtt/mqtts_cores3_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |mqtts_cores3_example.m5f2|


Constructors
------------

.. py:class:: umqtt.MQTTClient(client_id, server, port=0, user=None, password=None, keepalive=0, ssl=False, ssl_params={}) -> None

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

    UIFLOW2:

        |init.png|

        |init_ssl.png|


Methods
-------

.. method:: MQTTClient.connect(clean_session=True) -> bool

    Connect to a server. Returns True if this connection uses persisten
    session stored on a server (this will be always False if clean_session=True
    argument is used (default)).

    UIFLOW2:

        |connect.png|


.. method:: MQTTClient.disconnect() -> None

    Disconnect from a server, release resources.

    UIFLOW2:

        |disconnect.png|


.. method:: MQTTClient.reconnect() -> None

    Disconnect from a server, release resources.

    UIFLOW2:

        |reconnect.png|


.. method:: MQTTClient.ping() -> None

    Ping server (response is processed automatically by :py:meth:`wait_msg()`).

    UIFLOW2:

        None


.. method:: MQTTClient.publish(topic, msg, retain=False, qos=0) -> None

    Publish a message.

    :param topic: the topic that the message should be published on.
    :type topic: str or bytes or bytearray
    :param msg: the message to send as a will.
    :type msg: str or bytes or bytearray
    :param bool retain: if set to True, the will message will be set as
                        the "last will"/retained message for the topic.
    :param int qos: the quality of service level to use

    UIFLOW2:

        |publish.png|


.. method:: MQTTClient.subscribe(topic, handler, qos=0) -> None

    Subscribe to a topic.

    :param topic: a string specifying the subscription topic to subscribe to.
    :type topic: str or bytes or bytearray
    :param function handler: called when a message has been received on a topic
                             that the client subscribes to and the message does
                             match an existing topic filter callback.
    :param int qos: the desired quality of service level for the subscription.
                    Defaults to 0.

    UIFLOW2:

        |subscribe.png|

    An handler showing a message has been received::

        def on_sub_cb(data):
            print("topic:", data[0])
            print("msg:", data[1])

    On uiflow2, you can get the **topic** and **message** of the current handler
    through |get_topic.png| and |get_msg.png|.


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

    UIFLOW2:

        |subscribe.png|


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

    UIFLOW2:

        None


.. method:: MQTTClient.check_msg(attempts=2) -> None

    Check if there's pending message from server. If yes, process the same way
    as :py:meth:`wait_msg()`, if not, return immediately.

    UIFLOW2:

        |wait_msg.png|
