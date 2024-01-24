:py:mod:`umqtt` -- a simple MQTT client
=======================================

.. py:module:: umqtt
    :synopsis: a simple MQTT client

.. include:: ../refs/software.umqtt.ref

umqtt 是 MicroPython 的简单 MQTT 客户端。（请注意，它使用了一些
MicroPython 快捷方式，不适用于 CPython ）。

支持的 MQTT 功能
----------------

发布和订阅均支持 QoS 0 和 1。 不支持 QoS2 以保持较小的代码大小。 除了 ClientID 之外，
目前仅支持“clean session”参数进行连接。

设计要求
--------

* 内存效率。
* 避免臭名昭著的设计反模式，例如“回调地狱”。
* 通过单个客户端对象支持发布和订阅（另一种选择是使用单独的客户端类来进行发布和订阅）。

具有自动重新连接功能的 MQTT 客户端
----------------------------------

有一个单独的 `umqtt.robust`_ 模块，它构建在 `umqtt.simple`_ 之上，并在出现网络错误
时添加自动重新连接支持。
请参阅其 |umqtt.robust|_ 了解更多详细信息。

带有 SSL 文件的 MQTT 客户端
----------------------------

有一个单独的 `umqtt.default`_ 模块，它构建在 `umqtt.robust`_ 之上，并且支持 SSL 证
书以文件方式传入并为每一个订阅主题设置回调传递。
请参阅其 |umqtt.default|_ 了解更多详细信息。

API设计
--------

基于上述需求， API 具有以下特征：

* 所有与 MQTT 消息相关的数据都编码为字节。这包括消息内容和主题名称（即使 MQTT 规范声
  明主题名称是 UTF-8 编码的）。原因很简单：通过网络套接字接收到的是二进制数据（字节），
  需要额外的步骤将其转换为字符串，从而消耗内存。请注意，这仅适用于主题名称（因为它们
  既可以发送也可以接收）。 MQTT 指定为 UTF-8 编码的其他参数（例如 ClientID ）被接受为
  字符串。
* 订阅的消息通过回调传递。这是为了避免对订阅的消息使用队列，否则它们可能会随时收到（包
  括当客户端期望其他类型的服务器响应时），因此有两种选择：要么通过回调立即传递它们，要
  么排队直到“预期”响应到达）。请注意，不需要队列是错误的：在这种情况下，运行时调用堆栈
  形成隐式队列。 与显式队列不同，它更难控制。选择这种设计是因为在处理订阅消息的常见情
  况下，它是最有效的。然而，如果在订阅回调中，发布了 QoS > 0 的新消息，这可能会导致
  深度或无限递归（后者意味着应用程序将因 “RuntimeException” 而终止）。

Usage Model::

    # uiflow2默认使用这个类
    from umqtt import MQTTClient

    # 如果想要使用 `umqtt.default` module ，请通过这种方式。
    from umqtt.simple import MQTTClient

    # 如果想要使用 `umqtt.robust` module ，请通过这种方式。
    from umqtt.robust import MQTTClient

Classes
-------

.. toctree::
    :maxdepth: 1

    umqtt.default.rst
