Atom DTU NBIoT2 V11
===================

.. sku: K059-B

.. include:: ../refs/base.dtu_nbiot2v11.ref

This is the driver library for the ATOM DTU NBIoT2 V11 to accept and send data from the DTU NBIoT.

Support the following products:

    |Atom DTU NBIoT2|

.. note::

    Please ensure that the device supports the NB-IoT frequency bands in your area before use.

.. note::

    Please ensure that the firmware version of SIM7028 is greater than or equal to **2110B07SIM7028**.

    |nbiot_get_version.png| can be used to check the firmware version.

UiFlow2 Example
---------------

NBIoT HTTP Example
^^^^^^^^^^^^^^^^^^^

Open the |atoms3_base_nbiot2v11_http_example.m5f2| project in UiFlow2.

This example shows how to send HTTP request using the Atom DTU NBIoT2 V11.

UiFlow2 Code Block:

    |atoms3_base_nbiot2v11_http_example.png|

Example output:

    Output of received NBIoT message data via serial port.


MQTT Example
^^^^^^^^^^^^^^

Open the |atoms3_base_nbiot2v11_mqtt_example.m5f2| project in UiFlow2.

This example shows how to send MQTT message using the Atom DTU NBIoT2 V11.

UiFlow2 Code Block:

    |atoms3_base_nbiot2v11_mqtt_example.png|

Example output:

    Output of received NBIoT message data on screen.


MicroPython Example
-------------------

NBIoT HTTP Example
^^^^^^^^^^^^^^^^^^

This example shows how to send HTTP request using the Atom DTU NBIoT2 V11.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/dtu_nbiot2v11/atoms3_base_nbiot2v11_http_example.py
        :language: python
        :linenos:

Example output:

    Output of received NBIoT message data via serial port.


MQTT Example
^^^^^^^^^^^^

This example shows how to send MQTT message using the Atom DTU NBIoT2 V11.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/dtu_nbiot2v11/atoms3_base_nbiot2v11_mqtt_example.py
        :language: python
        :linenos:

Example output:

    Output of received NBIoT message data on screen.


**API**
-------

AtomDTUNBIoT2V11
^^^^^^^^^^^^^^^^

.. autoclass:: base.dtu_nbiot2_v11.AtomDTUNBIoT2V11
    :members:

    .. note::

        See :class:`NBIOT2Unit <unit.nbiot2.NBIOT2Unit>` for more details.

AtomRS485
^^^^^^^^^

.. note::

    See :class:`AtomRS485 <base.rs232.AtomRS232>` for more details.
