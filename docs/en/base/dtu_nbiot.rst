Atom DTU NBIoT
==============

.. sku: K059 K060

.. include:: ../refs/base.dtu_nbiot.ref

This is the driver library for the ATOM DTU NBIoT to accept and send data from the DTU NBIoT.

Support the following products:

    ================== ====================
    |Atom DTU NBIoT|   |Atom DTU NBIoT CN|
    ================== ====================

.. note::

    Please ensure that the device supports the NB-IoT frequency bands in your area before use.

.. note::

    Please ensure that the firmware version of SIM7020 is greater than or equal to **1752B12SIM7020C**.

    |nbiot_get_version.png| can be used to check the firmware version.

UiFlow2 Example
---------------

NBIoT HTTP Example
^^^^^^^^^^^^^^^^^^

Open the |atoms3_base_nbiot_http_example.m5f2| project in UiFlow2.

This example shows how to send HTTP request using the Atom DTU NBIoT.

UiFlow2 Code Block:

    |atoms3_base_nbiot_http_example.png|

Example output:

    Output of received NBIoT message data via serial port.


MQTT Example
^^^^^^^^^^^^^^

Open the |atoms3_base_nbiot_mqtt_example.m5f2| project in UiFlow2.

This example shows how to send MQTT message using the Atom DTU NBIoT.

UiFlow2 Code Block:

    |atoms3_base_nbiot_mqtt_example.png|

Example output:

    Output of received NBIoT message data on screen.


MicroPython Example
-------------------

NBIoT HTTP Example
^^^^^^^^^^^^^^^^^^^^

This example shows how to send HTTP request using the Atom DTU NBIoT.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/dtu_nbiot/atoms3_base_nbiot_http_example.py
        :language: python
        :linenos:

Example output:

    Output of received NBIoT message data via serial port.


MQTT Example
^^^^^^^^^^^^

This example shows how to send MQTT message using the Atom DTU NBIoT.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/dtu_nbiot/atoms3_base_nbiot_mqtt_example.py
        :language: python
        :linenos:

Example output:

    Output of received NBIoT message data on screen.


**API**
-------

AtomDTUNBIoT
^^^^^^^^^^^^

.. autoclass:: base.dtu_nbiot.AtomDTUNBIoT
    :members:

    .. note::

        See :class:`NBIOTUnit <unit.nbiot.NBIOTUnit>` for more details.

AtomRS485
^^^^^^^^^

.. note::

    See :class:`AtomRS485 <base.rs232.AtomRS232>` for more details.
