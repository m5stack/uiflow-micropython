LoRaE220 Unit
=============

.. include:: ../refs/unit.lora_e220.ref

Support the following products:

    |LoRaE220|


Micropython TX Example::

    import os, sys, io
    import M5
    from M5 import *
    from unit import LoRaE220JPUnit
    import time

    lorae220_0 = LoRaE220JPUnit((33, 32))

    while True:
        lorae220_0.send(0xFFFF, 0, bytes([0x68, 0x65, 0x6C, 0x6C, 0x6F]))
        time.sleep(1)


Micropython RX Example::

    import os, sys, io
    from unit import LoRaE220JPUnit

    def lorae220_0_receive_event(received_data, rssi):
        print(received_data)

    lorae220_0 = LoRaE220JPUnit((15, 13))
    lorae220_0.receiveNoneBlock(lorae220_0_receive_event)


UIFLOW2 TX Example:

    |tx_example.png|


UIFLOW2 RX Example:

    |rx_example.png|


.. only:: builder_html

    |lora_e220_tx_core2.m5f2|

    |lora_e220_rx_dial.m5f2|


Working Mode
------------

.. table:: Working mode table
    :name: working-mode
        :noindex:

    ===================== === === =========
    Mode (0-3)            M1  M0  Function description
    --------------------- --- --- ---------
    0:Transmission Mode   0   0   SEND: Users can enter data through the serial port, and the module will start wireless transmission.

                                  RECEIVE: The wireless receiving function of the module is enabled, and the wireless data will be output through the TXD pin of the serial port after receiving it.
    --------------------- --- --- ---------
    1:WOR Sending Mode    0   1   SEND: Wirelessly sending data on

                                  RECEIVE: Wireless receiving data on

                                  NOTE: Support Air Wake Up
    --------------------- --- --- ---------
    2:WOR Receiving Mode  1   0   SEND: Wirelessly sending data off

                                  RECEIVE: Wireless receiving data on

                                  NOTE: Support Air Wake Up
    --------------------- --- --- ---------
    3:Configuration Mode  1   1   SEND: Wirelessly sending data off

                                  RECEIVE: Wireless receiving data off

                                  CONFIGURATION: Users can access registers to configure module status
    ===================== === === =========

|working mode.jpg|


class LoRaE220JPUnit
--------------------

Constructors
------------

.. class:: LoRaE220JPUnit(port, port_id=1)

    Create a LoRaE220JPUnit object.

    The parameters is:
        - ``port`` uart pin tuple, which contains: ``(tx_pin, rx_pin)``.
        - ``port_id`` uart port ID.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: LoRaE220JPUnit.setup(own_address=0, own_channel=0, encryption_key=0x2333, air_data_rate=LoRaE220JPUnit.BW500K_SF5, subpacket_size=LoRaE220JPUnit.SUBPACKET_200_BYTE, rssi_ambient_noise_flag=LoRaE220JPUnit.RSSI_AMBIENT_NOISE_DISABLE, transmitting_power=LoRaE220JPUnit.TX_POWER_13dBm, rssi_byte_flag=LoRaE220JPUnit.RSSI_BYTE_DISABLE, transmission_method_type=LoRaE220JPUnit.UART_TT_MODE, wor_cycle=LoRaE220JPUnit.WOR_2000MS) -> bool

    .. NOTE:: Available when LoRaE220JPUnit working mode is 3. Please refer to :ref:`working mode table <working-mode>` for the working mode.

    Set module parameters.

    The parameters is:
        - ``own_address``: Local address.
        - ``own_channel``: Native channel.
        - ``encryption_key``: Encryption key.
        - ``air_data_rate``: rate.
        - ``subpacket_size``: Maximum packet length.
        - ``rssi_ambient_noise_flag``: RSSI Ambient Noise.
        - ``transmitting_power``: Transmit power.
        - ``rssi_byte_flag``: Output RSSI strength bytes.
        - ``transmission_method_type``: transmission mode.
        - ``lbt_flag``: Parameter no longer used.
        - ``wor_cycle``: Wireless wake-up time.

    UIFLOW2:

        |setup.png|


.. method:: LoRaE220JPUnit.receiveNoneBlock(receive_callback: function) -> None

    .. deprecated:: 2.0.2

        This method is deprecated and will be removed in version 2.0.2.

    .. NOTE:: Available when the working mode of LoRaE220JPUnit is 0 / 1 / 2. Please refer to :ref:`working mode table <working-mode>` for the working mode.

    Use non-blocking mode to receive data. ``receive_callback`` The callback function passed in will be called when data is received.

    The format of receive_callback is::

        def receive_callback(data: bytes, rssi: int)

    UIFLOW2:

        |receiveNoneBlock.png|


.. method:: LoRaE220JPUnit.receive_none_block(receive_callback: function) -> None

    .. versionadded:: 2.0.2

        This method will be added in version 2.0.2.

    .. NOTE:: Available when the working mode of LoRaE220JPUnit is 0 / 1 / 2. Please refer to :ref:`working mode table <working-mode>` for the working mode.

    Use non-blocking mode to receive data. ``receive_callback`` The callback function passed in will be called when data is received.

    The format of receive_callback is::

        def receive_callback(data: bytes, rssi: int)

    UIFLOW2:

        |receiveNoneBlock.png|
        |receive_callback1.png|
        |receive_callback2.png|

.. method:: LoRaE220JPUnit.stopReceive() -> None

    .. deprecated:: 2.0.2

        This method is deprecated and will be removed in version 2.0.2.

    .. NOTE:: Available when the working mode of LoRaE220JPUnit is 0 / 1 / 2. Please refer to :ref:`working mode table <working-mode>` for the working mode.

    Stop receiving data in non-blocking mode.

    UIFLOW2:

        |stopReceive.png|


.. method:: LoRaE220JPUnit.stop_receive() -> None

    .. versionadded:: 2.0.2

        This method will be added in version 2.0.2.

    .. NOTE:: Available when the working mode of LoRaE220JPUnit is 0 / 1 / 2. Please refer to :ref:`working mode table <working-mode>` for the working mode.

    Stop receiving data in non-blocking mode.

    UIFLOW2:

        |stopReceive.png|


.. method:: LoRaE220JPUnit.receive(timeout=1000) -> tuple[bytes, int]

    .. NOTE:: Available when the working mode of LoRaE220JPUnit is 0 / 1 / 2. Please refer to :ref:`working mode table <working-mode>` for the working mode.

    Use blocking method to receive data. ``timeout`` is used to set the reception timeout, the unit is ms.

    UIFLOW2:

        |receive.png|


.. method:: LoRaE220JPUnit.send(target_address: int, target_channel: int, send_data: bytes | str) -> bool

    .. NOTE:: Available when the working mode of LoRaE220JPUnit is 0 or 1. Please refer to :ref:`working mode table <working-mode>` for the working mode.

    Send data to the specified destination address and channel.

    The parameters is:

        - ``target_address`` Target address, the address range is 0x0000 - 0xFFFF, where 0xFFFF is the broadcast address.
        - ``target_channel`` Target channel, valid channel range is 0 - 30.
        - ``send_data`` The data needs to be sent.

    UIFLOW2:

        |send1.png|
        |send2.png|
        |send3.png|


Constants
---------

.. data:: LoRaE220JPUnit.BAUD_1200
          LoRaE220JPUnit.BAUD_2400
          LoRaE220JPUnit.BAUD_4800
          LoRaE220JPUnit.BAUD_9600
          LoRaE220JPUnit.BAUD_19200
          LoRaE220JPUnit.BAUD_38400
          LoRaE220JPUnit.BAUD_57600
          LoRaE220JPUnit.BAUD_115200
    :type: int

    baud rate.

.. data:: LoRaE220JPUnit.BW125K_SF5
          LoRaE220JPUnit.BW125K_SF6
          LoRaE220JPUnit.BW125K_SF7
          LoRaE220JPUnit.BW125K_SF8
          LoRaE220JPUnit.BW125K_SF9
          LoRaE220JPUnit.BW250K_SF5
          LoRaE220JPUnit.BW250K_SF6
          LoRaE220JPUnit.BW250K_SF7
          LoRaE220JPUnit.BW250K_SF8
          LoRaE220JPUnit.BW250K_SF9
          LoRaE220JPUnit.BW250K_SF10
          LoRaE220JPUnit.BW500K_SF5
          LoRaE220JPUnit.BW500K_SF6
          LoRaE220JPUnit.BW500K_SF7
          LoRaE220JPUnit.BW500K_SF8
          LoRaE220JPUnit.BW500K_SF9
          LoRaE220JPUnit.BW500K_SF10
          LoRaE220JPUnit.BW500K_SF11
    :type: int

    rate.

.. data:: LoRaE220JPUnit.SUBPACKET_200_BYTE
          LoRaE220JPUnit.SUBPACKET_128_BYTE
          LoRaE220JPUnit.SUBPACKET_64_BYTE
          LoRaE220JPUnit.SUBPACKET_32_BYTE
    :type: int

    Maximum packet length.

.. data:: LoRaE220JPUnit.RSSI_AMBIENT_NOISE_ENABLE
          LoRaE220JPUnit.RSSI_AMBIENT_NOISE_DISABLE
    :type: int

    RSSI ambient noise.

.. data:: LoRaE220JPUnit.TX_POWER_13dBm
          LoRaE220JPUnit.TX_POWER_12dBm
          LoRaE220JPUnit.TX_POWER_7dBm
          LoRaE220JPUnit.TX_POWER_0dBm
    :type: int

    Transmit power.

.. data:: LoRaE220JPUnit.RSSI_BYTE_ENABLE
          LoRaE220JPUnit.RSSI_BYTE_DISABLE
    :type: int

    RSSI bytes. When enabled, the module will append a byte of RSSI value after the data each time it receives data.

.. data:: LoRaE220JPUnit.UART_TT_MODE
          LoRaE220JPUnit.UART_P2P_MODE
    :type: int

    transmission mode.

.. data:: LoRaE220JPUnit.WOR_500MS
          LoRaE220JPUnit.WOR_1000MS
          LoRaE220JPUnit.WOR_1500MS
          LoRaE220JPUnit.WOR_2000MS
          LoRaE220JPUnit.WOR_2500MS
          LoRaE220JPUnit.WOR_3000MS
    :type: int

    Wireless wake-up time.
