NB-IoT2 Unit
============

.. sku: U111-B

.. include:: ../refs/unit.nbiot2.ref

The ``NB-IOT2 Unit`` is a wireless communication module suitable for global Cat-NB frequency bands. It features an integrated SIM7028 communication module, utilizing serial communication (controlled via AT commands).

Support the following products:

    |NB-IOT2Unit|

.. note::

    Please ensure that the device supports the NB-IoT frequency bands in your area before use.

.. note::

    Please ensure that the firmware version of SIM7028 is greater than or equal to **2110B07SIM7028**.

    |get_version.png| can be used to check the firmware version.

UiFlow2 Example
---------------

NBIoT HTTP Example
^^^^^^^^^^^^^^^^^^

Open the |cores3_unit_nbiot2_http_example.m5f2| project in UiFlow2.

This example shows how to send HTTP request using the NBIoT2 Unit.

click **Send** button to send HTTP request. Response data will be printed in the textarea.

UiFlow2 Code Block:

    |cores3_unit_nbiot2_http_example.png|

Example output:

    Output of received NBIoT message data on screen.


MQTT Example
^^^^^^^^^^^^^^

Open the |cores3_unit_nbiot2_mqtt_example.m5f2| project in UiFlow2.

This example shows how to send MQTT message using the NBIoT2 Unit.

UiFlow2 Code Block:

    |cores3_unit_nbiot2_mqtt_example.png|

Example output:

    Output of received NBIoT message data on screen.


MicroPython Example
-------------------

NBIoT HTTP Example
^^^^^^^^^^^^^^^^^^

This example shows how to send HTTP request using the NBIoT2 Unit.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/nbiot2/cores3_unit_nbiot2_http_example.py
        :language: python
        :linenos:

Example output:

    Output of received NBIoT message data on screen.


MQTT Example
^^^^^^^^^^^^

This example shows how to send MQTT message using the NBIoT2 Unit.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/nbiot2/cores3_unit_nbiot2_mqtt_example.py
        :language: python
        :linenos:

Example output:

    Output of received NBIoT message data on screen.


**API**
-------

NBIOT2Unit
^^^^^^^^^^

.. autoclass:: unit.nbiot2.NBIOT2Unit
    :members:

    .. note::

        See :class:`NBIOTUnit <unit.nbiot.NBIOTUnit>` for more details.
