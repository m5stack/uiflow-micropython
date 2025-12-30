NB-IoT Module
=============

.. include:: ../refs/module.nbiot.ref

The ``NB-IoT Module`` is a wireless communication module suitable for global Cat-NB frequency bands. It features an integrated SIM7020G communication module and communicates via serial port (AT commands).

Support the following products:

    |NB-IoT Module|

.. note::

    Please ensure that the device supports the NB-IoT frequency bands in your area before use.

.. note::

    Please ensure that the firmware version of SIM7020 is greater than or equal to **1752B12SIM7020C**.

    |get_version.png| can be used to check the firmware version.


UiFlow2 Example
---------------

NBIoT HTTP Example
^^^^^^^^^^^^^^^^^^

Open the |cores3_module_nbiot_http_example.m5f2| project in UiFlow2.

This example shows how to send HTTP request using the NBIoT Module.

UiFlow2 Code Block:

    |cores3_module_nbiot_http_example.png|

Example output:

    Output of received NBIoT message data on screen.


MQTT Example
^^^^^^^^^^^^

Open the |cores3_module_nbiot_mqtt_example.m5f2| project in UiFlow2.

This example shows how to send MQTT message using the NBIoT Module.

UiFlow2 Code Block:

    |cores3_module_nbiot_mqtt_example.png|

Example output:

    Output of received NBIoT message data on screen.



MicroPython Example
-------------------

NBIoT HTTP Example
^^^^^^^^^^^^^^^^^^

This example shows how to send HTTP request using the NBIoT Module.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/nbiot/cores3_module_nbiot_http_example.py
        :language: python
        :linenos:

Example output:

    Output of received NBIoT message data on screen.


MQTT Example
^^^^^^^^^^^^

This example shows how to send MQTT message using the NBIoT Module.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/nbiot/cores3_module_nbiot_mqtt_example.py
        :language: python
        :linenos:

Example output:

    Output of received NBIoT message data on screen.


**API**
-------

.. autoclass:: module.nbiot.NBIOTModule
    :members:

    .. note::

        See :class:`NBIOTUnit <unit.nbiot.NBIOTUnit>` for more details.
