Cat1CN Unit
====================

.. sku: U204

.. include:: ../refs/unit.cat1cn.ref

This is the driver library for the Cat1CN Unit to accept and send data.

Support the following products:

|Cat1CNUnit|

UiFlow2 Example
---------------
HTTP Example
^^^^^^^^^^^^^^^^^^^

Open the |cat1cn_core2_http_example.m5f2| project in UiFlow2.

This example shows how to send HTTP request.

UiFlow2 Code Block:

    |http_example.png|

Example output:

    None

MicroPython Example
-------------------
HTTP Example
^^^^^^^^^^^^^^^^^^^^

This example shows how to send HTTP request.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/cat1cn/cat1cn_core2_http_example.py
        :language: python
        :linenos:

Example output:

    None

MQTT Example
^^^^^^^^^^^^^^

Open the |cat1cn_core2_mqtt_example.m5f2| project in UiFlow2.

This example shows how to send MQTT message.

UiFlow2 Code Block:

    |mqtt_example.png|

Example output:

    None

MicroPython Example
-------------------

MQTT Example
^^^^^^^^^^^^^^^^^^^^

This example shows how to send MQTT message.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/cat1cn/cat1cn_core2_mqtt_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

Cat1Unit
^^^^^^^^^^^^

.. autoclass:: unit.cat1.Cat1Unit
    :members:

See :class:`NBIOTUnit <unit.nbiot.NBIOTUnit>` for more details.
