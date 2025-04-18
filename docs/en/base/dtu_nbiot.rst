Atom DTU NBIoT Base
====================

.. sku: K059

.. include:: ../refs/base.dtu_nbiot.ref

This is the driver library for the ATOM DTU NBIoT Base to accept and send data from the DTU NBIoT.

Support the following products:

    ================== ====================
    |Atom DTU NBIoT|   |Atom DTU NBIoT CN|
    ================== ====================


UiFlow2 Example
---------------

NBIoT HTTP Example
^^^^^^^^^^^^^^^^^^^

Open the |base_nbiot_atoms3_http_example.m5f2| project in UiFlow2.

This example shows how to send HTTP request using the Atom DTU NBIoT Base.

UiFlow2 Code Block:

    |example.png|

Example output:

    Output of received NBIoT message data via serial port.

MicroPython Example
-------------------

NBIoT HTTP Example
^^^^^^^^^^^^^^^^^^^^

This example shows how to send HTTP request using the Atom DTU NBIoT Base.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/dtu_nbiot/base_nbiot_atoms3_http_example.py
        :language: python
        :linenos:

Example output:

    Output of received NBIoT message data via serial port.

MQTT Example
^^^^^^^^^^^^^^

Open the |base_nbiot_atoms3_mqtt_example.m5f2| project in UiFlow2.

This example shows how to send MQTT message using the Atom DTU NBIoT Base.

UiFlow2 Code Block:

    |example.png|

Example output:

    Output of received NBIoT message data via serial port.

MicroPython Example
-------------------

MQTT Example
^^^^^^^^^^^^^^^^^^^^

This example shows how to send MQTT message using the Atom DTU NBIoT Base.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/dtu_nbiot/base_nbiot_atoms3_mqtt_example.py
        :language: python
        :linenos:

Example output:

    Output of received NBIoT message data via serial port.

**API**
-------

AtomDTUNBIoT
^^^^^^^^^^^^

.. autoclass:: base.dtu_nbiot.AtomDTUNBIoT
    :members:

See :ref:`base.AtomDTUNBIoT.Methods <unit.NBIOTUnit.Methods>` for more details.
