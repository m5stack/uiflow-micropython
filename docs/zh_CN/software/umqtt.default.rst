.. py:currentmodule:: umqtt

umqtt.default
=============

.. include:: ../refs/software.umqtt.default.ref

`umqtt.default` 重写了 :py:meth:`subscribe` 方法并支持 ca 文件。

Micropython Example::

    import umqtt

    c = umqtt.MQTTClient(
        "umqtt_client",
        "emqxsl.cn",
        port=8883, user='test', password='test', keepalive=60,
        ssl=True,
        ssl_params={"cert": "/flash/certificate/emqxsl-ca.crt", "server_hostname": "emqxsl.cn"}
    )

    def on_sub_cb(data):
        print("topic:", data[0])
        print("msg:", data[1])

    if not c.connect(clean_session=True):
        print("New session being set up")
        c.subscribe(b"testtopic", on_sub_cb)

    while True:
        c.wait_msg()

UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

    :download:`example.m5f2 <../../_static/software/umqtt/example.m5f2>`

Constructors
------------

.. py:class:: umqtt.MQTTClient(client_id, server, port=0, user=None, password=None, keepalive=0, ssl=False, ssl_params={}) -> None

    创建 MQTTClient 对象。

    :param str client_id: 连接到MQTT broker时使用的唯一客户端 ID 字符串。
    :param str server: 远程MQTT broker的主机名或 IP 地址。
    :param int port: 要连接的服务器主机的网络端口。
    :param user: 用于MQTT broker身份验证的用户名。
    :type user: str or None
    :param password: 用于MQTT broker身份验证的密码。
    :type password: str or None
    :param int keepalive: 与代理通信之间允许的最长时间（以秒为单位）。如果没有交换其
                          他消息，这将控制客户端向代理发送 ping 消息的速率。
    :param bool ssl: 是否使用ssl。
    :param dict ssl_params: 启动 ssl 连接所需的一些参数。
    :return: MQTTClient 对象
    :rtype: MQTTClient

    UIFLOW2:

        |init.svg|
        |init1.svg|

Methods
-------

.. method:: MQTTClient.connect(clean_session=True) -> bool

    连接到服务器。如果此连接使用存储在服务器上的持久会话，则返回 True （如果使用
    clean_session=True 参数（默认），则始终为 False ）。

    UIFLOW2:

        |connect.svg|

.. method:: MQTTClient.disconnect() -> None

    断开与服务器的连接，释放资源。

    UIFLOW2:

        |disconnect.svg|

.. method:: MQTTClient.reconnect() -> None

    断开与服务器的连接，释放资源。

    UIFLOW2:

        |reconnect.svg|

.. method:: MQTTClient.ping() -> None

    Ping 服务器（响应由 :py:meth:`wait_msg()` 自动处理）。

    UIFLOW2:

        None

.. method:: MQTTClient.publish(topic, msg, retain=False, qos=0) -> None

    发布消息。

    :param topic: 应发布消息的主题。
    :type topic: str or bytes or bytearray
    :param msg: 实际要发送的消息。
    :type msg: str or bytes or bytearray
    :param bool retain: 如果设置为 True ，则遗嘱消息将被设置为该主题的“最后遗嘱”/保留消息。
    :param int qos: 使用的服务质量级别

    UIFLOW2:

        |publish.svg|

.. method:: MQTTClient.subscribe(topic, handler, qos=0) -> None

    订阅主题。

    :param topic: 指定要订阅的订阅主题的字符串。
    :type topic: str or bytes or bytearray
    :param function handler: 当收到有关客户端订阅的主题的消息并且该消息与现有主题过滤器回调匹配时调用。
    :param int qos: 订阅所需的服务质量级别。 默认为 0。

    UIFLOW2:

        |subscribe.svg|

    显示已收到消息的处理程序::

        def on_sub_cb(data):
            print("topic:", data[0])
            print("msg:", data[1])

    在 uiflow2 上，可以通过 |get_topic.svg| 和 |get_msg.svg| 获取当前 handler 的
    **topic** 和 **message** 。

.. method:: MQTTClient.set_last_will(topic, msg, retain=False, qos=0) -> None

    .. important::

        应该在 :py:meth:`connect()` 之前调用。

    设置 MQTT 遗嘱消息。

    :param topic: 应发布遗嘱消息的主题。
    :type topic: str or bytes or bytearray
    :param msg: 作为遗嘱发送的消息。如果未给出或设置为 None ，则将使用零长度消息作为遗嘱。
    :type msg: str or bytes or bytearray
    :param bool retain: 如果设置为 True ，则遗嘱消息将被设置为该主题的“最后遗嘱”/保留消息。
    :param int qos: 用于意愿的服务质量水平。

    UIFLOW2:

        |subscribe.svg|

.. method:: MQTTClient.wait_msg() -> None

    .. important::

        :py:meth:`wait_msg()` 和 :py:meth:`check_msg()` 是主循环迭代方法，有阻
        塞和非阻塞版本。 如果您没有任何其他前台任务要执行（即您的应用程序仅对订阅的
        MQTT 消息做出反应），则应在循环中定期调用 :py:meth:`wait_msg()` ，如果您还
        处理其他前台任务，则使用 :py:meth:`check_msg ()` 。

        请注意，如果您只发布消息，从不订阅消息，则不需要调用
        :py:meth:`wait_msg()` / :py:meth:`check_msg()` 。

    等待服务器消息。

    UIFLOW2:

        |wait_msg.svg|

.. method:: MQTTClient.check_msg(attempts=2) -> None

    检查是否有来自服务器的待处理消息。如果是， 则与 :py:meth:`wait_msg()` 处理方式相
    同，如果不是，则立即返回。

    UIFLOW2:

        None
