GatewayH2 Unit
==============

.. sku: U195

.. include:: ../refs/unit.gateway_h2.ref

This library is the driver for Unit Gateway H2, and the unit communicates via UART.

Support the following products:

    |Unit Gateway H2|

.. note:: When using this unit, you need to flash the NCP firmware to the unit. For details, refer to the `ESP Zigbee NCP <https://docs.m5stack.com/zh_CN/guide/zigbee/unit_gateway_h2/zigbee_ncp>`_ documentation.

UiFlow2 Example
---------------

Switch Control
^^^^^^^^^^^^^^

.. note:: To use this example, you need to flash this program onto an ESP32C6 or similar unit as a light node device. For details, refer to `HA_on_off_light <https://github.com/espressif/esp-zigbee-sdk/tree/main/examples/esp_zigbee_HA_sample/HA_on_off_light>`_

Open the |cores3_switch_endpoint_example.m5f2| project in UiFlow2.

The example demonstrates group control and targeted device operation for light nodes through SwitchEndpoint of Gateway H2 unit.

UiFlow2 Code Block:

    |cores3_switch_endpoint_example.png|

Example output:

    None
 
MicroPython Example
-------------------

Switch Control
^^^^^^^^^^^^^^

The example demonstrates group control and targeted device operation for light nodes through SwitchEndpoint of Gateway H2 unit.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/gateway_h2/cores3_switch_endpoint_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

GatewayH2Unit
^^^^^^^^^^^^^

.. class:: unit.gateway_h2.GatewayH2Unit

    Create an GatewayH2Unit object.

    :param int id: The UART ID for communication with the GatewayH2 Unit. It can be 1, 2.
    :param port: A list or tuple containing the TX and RX pins for UART communication.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import GatewayH2Unit

            gateway_h2_unit = GatewayH2Unit(2, port=(1, 2))

    .. method:: create_switch_endpoint()

        Create Switch Endpoint.

        :returns SwitchEndpoint: zigbee switch endpoint object.
        :return type: SwitchEndpoint

        UiFlow2 Code Block:

            |init.png|

        MicroPython Code Block:

            .. code-block:: python

                h2_switch_endpoint = gateway_h2_unit.create_switch_endpoint()

Refer to :ref:`switchendpoint` for more details about SwitchEndpoint.