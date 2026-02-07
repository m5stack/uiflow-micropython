GatewayH2 Module
================

.. sku: M141

.. include:: ../refs/module.gateway_h2.ref

This library is the driver for Module Gateway H2, and the module communicates via UART.

Support the following products:

    |Module Gateway H2|

.. note:: When using this module, you need to flash the NCP firmware to the module. For details, refer to the `ESP Zigbee NCP <https://docs.m5stack.com/en/esp_idf/zigbee/module_gateway_h2/zigbee_ncp>`_ documentation.

UiFlow2 Example
---------------

Switch Control
^^^^^^^^^^^^^^

.. note:: To use this example, you need to flash this program onto an ESP32C6 or similar module as a light node device. For details, refer to `HA_on_off_light <https://github.com/espressif/esp-zigbee-sdk/tree/main/examples/esp_zigbee_HA_sample/HA_on_off_light>`_

Open the |cores3_switch_endpoint_example.m5f2| project in UiFlow2.

The example demonstrates group control and targeted device operation for light nodes through SwitchEndpoint of Gateway H2 module.

UiFlow2 Code Block:

    |cores3_switch_endpoint_example.png|

Example output:

    None
 
MicroPython Example
-------------------

Switch Control
^^^^^^^^^^^^^^

The example demonstrates group control and targeted device operation for light nodes through SwitchEndpoint of Gateway H2 module.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/gateway_h2/cores3_switch_endpoint_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

GatewayH2Module
^^^^^^^^^^^^^^^

.. class:: module.gateway_h2.GatewayH2Module

    Create an GatewayH2Module object.

    :param int id: UART id.
    :param int tx: the UART TX pin.
    :param int rx: the UART RX pin.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from module import GatewayH2Module

            module_gateway_h2 = GatewayH2Module(id = 1, tx = 10, rx = 17)

    .. method:: create_switch_endpoint()

        Create Switch Endpoint. 

        :returns SwitchEndpoint: zigbee switch endpoint object.
        :return type: SwitchEndpoint

        UiFlow2 Code Block:

            |init.png|

        MicroPython Code Block:

            .. code-block:: python

                h2_switch_endpoint = module_gateway_h2.create_switch_endpoint()

.. _switchendpoint:

SwitchEndpoint
^^^^^^^^^^^^^^

.. class:: SwitchEndpoint

    Return by GatewayH2Module.create_switch_endpoint() or GatewayH2Unit.create_switch_endpoint()

    .. method:: on([addr])

        Turn on the light.

        :param addr: The device address (optional).
        
        - If called as ``on()``, turn on all devices.
        - If called as ``on(addr)``, turn on special address devices.

        UiFlow2 Code Block:

            |on.png|
            |all_on.png|

        MicroPython Code Block:

            .. code-block:: python

                h2_switch_endpoint.on(addr)
                h2_switch_endpoint.on()

    .. method:: off([addr])

        Turn off the light.

        :param addr: The device address (optional).

        - If called as ``off()``, turn off all devices.
        - If called as ``off(addr)``, turn off special address devices.

        UiFlow2 Code Block:

            |off.png|
            |all_off.png|

        MicroPython Code Block:

            .. code-block:: python

                h2_switch_endpoint.off(addr)
                h2_switch_endpoint.off()

    .. method:: toggle([addr])

        Toggle the light state.

        :param addr: The device address (optional).

        - If called as ``toggle()``, toggle all devices.
        - If called as ``toggle(addr)``, toggle special address devices.

        UiFlow2 Code Block:

            |toggle.png|
            |all_toggle.png|

        MicroPython Code Block:

            .. code-block:: python
                
                h2_switch_endpoint.toggle(addr)
                h2_switch_endpoint.toggle()
