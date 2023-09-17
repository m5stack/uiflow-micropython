:py:mod:`umqtt` -- a simple MQTT client
=======================================

.. py:module:: umqtt
    :synopsis: a simple MQTT client

.. include:: ../refs/software.umqtt.ref

umqtt is a simple MQTT client for MicroPython. (Note that it uses some
MicroPython shortcuts and doesn't work with CPython).

Supported MQTT features
-----------------------

QoS 0 and 1 are supported for both publish and subscribe. QoS2 isn't
supported to keep code size small. Besides ClientID, only "clean
session" parameter is supported for connect as of now.

Design requirements
-------------------

* Memory efficiency.
* Avoid infamous design anti-patterns like "callback hell".
* Support for both publishing and subscription via a single client
  object (another alternative would be to have separate client classes
  for publishing and subscription).

MQTT client with automatic reconnect
------------------------------------

There's a separate `umqtt.robust`_ module which builds on `umqtt.simple`_
and adds automatic reconnect support in case of network errors.
Please see its |umqtt.robust|_ for further details.

MQTT client with SSL file
-------------------------

There is a separate `umqtt.default`_ module that builds on top of `umqtt.robust`_
and supports SSL certificates passed in as files and callback delivery for each
subscribed topic.
Please see its |umqtt.default|_ for further details.

API design
----------

Based on the requirements above, there are following API traits:

* All data related to MQTT messages is encoded as bytes. This includes
  both message content AND topic names (even though MQTT spec states
  that topic name is UTF-8 encoded). The reason for this is simple:
  what is received over network socket is binary data (bytes) and
  it would require extra step to convert that to a string, spending
  memory on that. Note that this applies only to topic names (because
  they can be both sent and received). Other parameters specified by
  MQTT as UTF-8 encoded (e.g. ClientID) are accepted as strings.
* Subscribed messages are delivered via a callback. This is to avoid
  using a queue for subscribed messages, as otherwise they may be
  received at any time (including when client expects other type
  of server response, so there're 2 choices: either deliver them
  immediately via a callback or queue up until an "expected" response
  arrives). Note that lack of need for a queue is delusive: the
  runtime call stack forms an implicit queue in this case. And unlike
  explicit queue, it's much harder to control. This design was chosen
  because in a common case of processing subscribed messages it's
  the most efficient. However, if in subscription callback, new
  messages of QoS>0 are published, this may lead to deep, or
  infinite recursion (the latter means an application will terminate
  with ``RuntimeException``).

Usage Model::

    # uiflow2 uses this class by default
    from umqtt import MQTTClient

    # If you want to use the `umqtt.default` module, go this way.
    from umqtt.simple import MQTTClient

    # If you want to use the `umqtt.robust` module, go this way.
    from umqtt.robust import MQTTClient

Classes
-------

.. toctree::
    :maxdepth: 1

    umqtt.default.rst
