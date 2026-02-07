Zigbee Module
=============

.. include:: ../refs/module.zigbee.ref

Zigbee is a self-organizing network communication module launched by M5Stack.
The module adopts the CC2630F128 solution, integrates the Zigbee protocol stack
internally, and provides an open serial communication interface. It features an
external antenna, with a stable single-node communication distance of up to 1 km
and supports up to 200 levels of router depth. Through MESH networking, it can
significantly extend the range of your IoT applications, offering both ultra-low
power consumption and high sensitivity. The Zigbee network can support hundreds
of nodes and has enhanced security features, providing a complete and
interoperable IoT solution for home and building automation.


Support the following products:

    |ZigbeeModule|


Micropython TX Example:

    .. literalinclude:: ../../../examples/module/zigbee/cores3_zigbee_tx_example.py
        :language: python
        :linenos:


Micropython RX Example:

    .. literalinclude:: ../../../examples/module/zigbee/core2_zigbee_rx_example.py
        :language: python
        :linenos:


UIFLOW2 TX Example:

    |tx_example.png|


UIFLOW2 RX Example:

    |rx_example.png|


.. only:: builder_html

    |cores3_zigbee_tx_example.m5f2|

    |stickc_plus2_zigbee_rx_example.m5f2|


class ZigbeeModule
------------------

Constructors
------------

.. class:: ZigbeeModule(id: Literal[0, 1, 2], port: list | tuple, verbose: bool=True)

    Create a Zigbee unit.

    :param id: The ID of the unit.
    :param port: The port that the unit is connected to.
    :param verbose: Print the log information. Default is True.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: ZigbeeModule.set_module_param(device_type: int, pan_id: int, channel: int, transfer_mode: int, custom_address: int, ant_type: int, encryption_enable=ENCRYPTION_ENABLE, encryption_key=b'\x11\x12\x13\x14', node_type=DEVICE_TYPE_ROUTER, node_ant_type=ANT_TYPRE_ON_BOARD, node_transfer_mode=TRANSFER_MODE_PASS_THROUGH, node_custom_address=0x0066,)

    :param int device_type: The device type of the Zigbee module.
    :param int pan_id: The PAN ID of the Zigbee module. The PAN ID is a 16-bit value that is used to identify the network.
    :param int channel: The channel of the Zigbee module. The channel range is from 11 to 26
    :param int transfer_mode: The transfer mode of the Zigbee module.
    :param int custom_address: The custom address of the Zigbee module.
    :param int ant_type: The antenna type of the Zigbee module.
    :param int encryption_enable: The encryption status of the Zigbee module.
    :param bytes encryption_key: The encryption key of the Zigbee module.
    :param int node_type: The node type of the Zigbee module.
    :param int node_ant_type: The antenna type of the Zigbee node.
    :param int node_transfer_mode: The transfer mode of the Zigbee node.
    :param int node_custom_address: The custom address of the Zigbee node.

    Set the parameters of the Zigbee module.

    UIFLOW2:

        |set_module_param.png|

        |set_module_param1.png|

        |set_module_param2.png|


.. method:: ZigbeeModule.set_device_type(device_type: int)

    :param int device_type: The device type of the Zigbee module.

    Set the device type of the Zigbee module.

    UIFLOW2:

        |set_device_type.png|


.. method:: ZigbeeModule.set_pan_id(pan_id: int)

    :param int pan_id: The PAN ID of the Zigbee module.

    Set the PAN ID of the Zigbee module.

    UIFLOW2:

        |set_pan_id.png|


.. method:: ZigbeeModule.set_channel(channel: int)

    :param int channel: The channel of the Zigbee module.

    Set the channel of the Zigbee module.

    UIFLOW2:

        |set_channel.png|


.. method:: ZigbeeModule.set_transfer_mode(transfer_mode: int)

    :param int transfer_mode: The transfer mode of the Zigbee module.

    Set the transfer mode of the Zigbee module.

    UIFLOW2:

        |set_transfer_mode.png|


.. method:: ZigbeeModule.get_custom_address() -> int

    Get the custom address of the Zigbee module.

    :return: The custom address of the Zigbee module.

    UIFLOW2:

        |get_custom_address.png|


.. method:: ZigbeeModule.set_custom_address(custom_address: int)

    :param int custom_address: The custom address of the Zigbee module.

    Set the custom address of the Zigbee module.

    UIFLOW2:

        |set_custom_address.png|


.. method:: ZigbeeModule.set_ant_type(ant_type: int)

    :param int ant_type: The antenna type of the Zigbee module.

    Set the antenna type of the Zigbee module.

    UIFLOW2:

        |set_ant_type.png|


.. method:: ZigbeeModule.get_short_address() -> int

    Get the short address of the Zigbee module.

    :return: The short address of the Zigbee module.

    UIFLOW2:

        |get_short_address.png|


.. method:: ZigbeeModule.isconnected() -> bool

    Check whether the Zigbee module is connected to the Zigbee network.

    :return: True if the Zigbee module is connected to the Zigbee network, False otherwise.

    UIFLOW2:

        |isconnected.png|


.. method:: ZigbeeModule.receive_none_block(receive_callback)

    :param receive_callback: The callback function that is called when the Zigbee module receives data.

    Receive data from the Zigbee module.

    UIFLOW2:

        |receive_none_block.png|

        |receive_data_str_event.png|

        |receive_data_event.png|


.. method:: ZigbeeModule.stop_receive()

    Stop receiving data from the Zigbee module.

    UIFLOW2:

        |stop_receive.png|


.. method:: ZigbeeModule.p2p_transmission(address: int, data: bytes)

    :param int address: The custom address of the Zigbee module that the data is sent to.
    :param bytes data: The data that is sent to the Zigbee module.

    Send data to the Zigbee module.

    UIFLOW2:

        |p2p_transmission.png|

.. method:: ZigbeeModule.broadcast(data: bytes)

    :param bytes data: The data that is sent to the Zigbee module.

    Broadcast data to all Zigbee modules.

    UIFLOW2:

        |broadcast.png|
