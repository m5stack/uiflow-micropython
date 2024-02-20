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

    |tx_example.svg|

UIFLOW2 RX Example:

    |rx_example.svg|

.. only:: builder_html

|lora_e220_tx_core2.m5f2|

|lora_e220_rx_dial.m5f2|

工作模式
--------

.. table:: 工作模式表
    :name: working-mode

    ===================== === === =========
    Mode (0-3)            M1  M0  功能描述
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

    创建一个 LoRaE220JPUnit 对象.

    The parameters is:
        - ``port`` uart的引脚元组，其中包含: ``(tx_pin, rx_pin)``。
        - ``port_id`` uart端口ID。

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: LoRaE220JPUnit.setup(own_address=0, own_channel=0, encryption_key=0x2333, air_data_rate=LoRaE220JPUnit.BW500K_SF5, subpacket_size=LoRaE220JPUnit.SUBPACKET_200_BYTE, rssi_ambient_noise_flag=LoRaE220JPUnit.RSSI_AMBIENT_NOISE_DISABLE, transmitting_power=LoRaE220JPUnit.TX_POWER_13dBm, rssi_byte_flag=LoRaE220JPUnit.RSSI_BYTE_DISABLE, transmission_method_type=LoRaE220JPUnit.UART_TT_MODE, wor_cycle=LoRaE220JPUnit.WOR_2000MS) -> bool

    .. NOTE:: 当 LoRaE220JPUnit 的工作模式为 3 时可用。工作模式请参考 :ref:`工作模式表 <working-mode>` 。

    设置模块的参数。

    The parameters is:
        - ``own_address``: 本机地址。
        - ``own_channel``: 本机通道。
        - ``encryption_key``: 加密密钥。
        - ``air_data_rate``: 速率。
        - ``subpacket_size``: 数据包最大长度。
        - ``rssi_ambient_noise_flag``: RSSI。
        - ``transmitting_power``: 发射功率。
        - ``rssi_byte_flag``: RSSI。
        - ``transmission_method_type``: 传输模式。
        - ``lbt_flag``: LBT Flag。
        - ``wor_cycle``: WOR。

    UIFLOW2:

        |setup.svg|


.. method:: LoRaE220JPUnit.receiveNoneBlock(receive_callback: function) -> None

    .. deprecated:: 2.0.2

        这个方法已被弃用，并将在 2.0.2 版本中移除。

    .. NOTE:: 当 LoRaE220JPUnit 的工作模式为 0 / 1 / 2 时可用。工作模式请参考 :ref:`工作模式表 <working-mode>` 。

    使用非阻塞模式接收数据。 ``receive_callback`` 传入的回调函数，当接收到数据时会被调用。

    receive_callback 的格式为::

        def receive_callback(data: bytes, rssi: int)

    UIFLOW2:

        |receiveNoneBlock.svg|


.. method:: LoRaE220JPUnit.receive_none_block(receive_callback: function) -> None

    .. versionadded:: 2.0.2

        这个方法将在 2.0.2 版本中添加。

    .. NOTE:: 当 LoRaE220JPUnit 的工作模式为 0 / 1 / 2 时可用。工作模式请参考 :ref:`工作模式表 <working-mode>` 。

    使用非阻塞模式接收数据。 ``receive_callback`` 传入的回调函数，当接收到数据时会被调用。

    receive_callback 的格式为::

        def receive_callback(data: bytes, rssi: int)

    UIFLOW2:

        |receiveNoneBlock.svg|
        |receive_callback1.svg|
        |receive_callback2.svg|

.. method:: LoRaE220JPUnit.stopReceive() -> None

    .. deprecated:: 2.0.2

        这个方法已被弃用，并将在 2.0.2 版本中移除。

    .. NOTE:: 当 LoRaE220JPUnit 的工作模式为 0 / 1 / 2 时可用。工作模式请参考 :ref:`工作模式表 <working-mode>` 。

   停止非阻塞模式接收数据。

    UIFLOW2:

        |stopReceive.svg|


.. method:: LoRaE220JPUnit.stop_receive() -> None

    .. versionadded:: 2.0.2

        这个方法将在 2.0.2 版本中添加。

    .. NOTE:: 当 LoRaE220JPUnit 的工作模式为 0 / 1 / 2 时可用。工作模式请参考 :ref:`工作模式表 <working-mode>` 。

   停止非阻塞模式接收数据。

    UIFLOW2:

        |stopReceive.svg|


.. method:: LoRaE220JPUnit.receive(timeout=1000) -> tuple[bytes, int]

    .. NOTE:: 当 LoRaE220JPUnit 的工作模式为 0 / 1 / 2 时可用。工作模式请参考 :ref:`工作模式表 <working-mode>` 。

    使用阻塞的方式接收数据。 ``timeout`` 用于设置接收超时时间，单位是 ms。

    UIFLOW2:

        |receive.svg|


.. method:: LoRaE220JPUnit.send(target_address: int, target_channel: int, send_data: bytes | str) -> bool

    .. NOTE:: 当 LoRaE220JPUnit 的工作模式为 0 或者 1 时可用。工作模式请参考 :ref:`工作模式表 <working-mode>` 。

    向指定的目标地址和信道发送数据。

    The parameters is:

        - ``target_address`` 目标地址，地址范围是 0x0000 - 0xFFFF ，其中 0xFFFF 是广播地址。
        - ``target_channel`` 目标信道，有效的信道范围是 0 - 30。
        - ``send_data`` 需要发送的数据。

    UIFLOW2:

        |send1.svg|
        |send2.svg|
        |send3.svg|


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

    波特率。

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

    速率。

.. data:: LoRaE220JPUnit.SUBPACKET_200_BYTE
          LoRaE220JPUnit.SUBPACKET_128_BYTE
          LoRaE220JPUnit.SUBPACKET_64_BYTE
          LoRaE220JPUnit.SUBPACKET_32_BYTE
    :type: int

    数据包最大长度。

.. data:: LoRaE220JPUnit.RSSI_AMBIENT_NOISE_ENABLE
          LoRaE220JPUnit.RSSI_AMBIENT_NOISE_DISABLE
    :type: int

    RSSI 环境噪声。

.. data:: LoRaE220JPUnit.TX_POWER_13dBm
          LoRaE220JPUnit.TX_POWER_12dBm
          LoRaE220JPUnit.TX_POWER_7dBm
          LoRaE220JPUnit.TX_POWER_0dBm
    :type: int

    发射功率。

.. data:: LoRaE220JPUnit.RSSI_BYTE_ENABLE
          LoRaE220JPUnit.RSSI_BYTE_DISABLE
    :type: int

    RSSI 字节。使能后，模块会在每次接收到数据后，会在数据后面追加一个字节的 RSSI 值。

.. data:: LoRaE220JPUnit.UART_TT_MODE
          LoRaE220JPUnit.UART_P2P_MODE
    :type: int

    传输模式。

.. data:: LoRaE220JPUnit.WOR_500MS
          LoRaE220JPUnit.WOR_1000MS
          LoRaE220JPUnit.WOR_1500MS
          LoRaE220JPUnit.WOR_2000MS
          LoRaE220JPUnit.WOR_2500MS
          LoRaE220JPUnit.WOR_3000MS
    :type: int

    无线唤醒时间。
