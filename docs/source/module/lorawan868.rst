
LoRaWAN868 Module
=================

.. include:: ../refs/module.lorawan868.ref

COM.LoRaWAN is a LoRaWAN communication module in the M5Stack stackable module series, supporting node-to-node or LoRaWAN communication.

Support the following products:

|LoRaWAN868Module|

Micropython TX Example:

    .. literalinclude:: ../../../examples/module/lorawan868/lorawan868_example_tx.py
        :language: python
        :linenos:

Micropython RX Example:

    .. literalinclude:: ../../../examples/module/lorawan868/lorawan868_example_rx.py
        :language: python
        :linenos:

UIFLOW2 TX Example:

    |tx_example.png|

UIFLOW2 RX Example:

    |rx_example.png|

.. only:: builder_html

    |lorawan868_example_tx.m5f2|

    |lorawan868_example_rx.m5f2|

class LoRaWAN868Module
----------------------

Constructors
------------

.. class:: LoRaWAN868Module(id, port, band)

    Initialize the LoRaWANModule.

    :param int id: The UART ID to use for communication.
    :param  port: The UART port to use for communication, specified as a tuple of (rx, tx) pins.
    :param  band: The frequency to use for LoRa communication

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: LoRaWAN868Module.set_mode(mode)

    Set the mode of the LoRaWAN module.

    :param  mode: The mode to set.

    UIFLOW2:

        |set_mode.png|

.. method:: LoRaWAN868Module.set_parameters(freq, power, sf, bw, cr, preamble, crc, iq_inv, save)

    Set the parameters of the LoRaWAN module.

    :param  freq: Set LoRa listening/sending frequency in Hz.
    :param  power: LoRa signal output power in dBm;
    :param  sf: Spreading factor, from 5~12
    :param  bw: Bandwidth 0 – 125K, 1 – 250K, 2 – 500K;
    :param  cr: 1 – 4/5, 2 – 4/6, 3 – 4/7, 4 – 4/8;
    :param  preamble: Preamble Length from 8~65535 bit;
    :param  crc: 0 – disable CRC check, 1 – enable CRC check;
    :param  iq_inv: 0 -- not inverted, 1 – inverted;
    :param  save: Save parameters to FLASH, 0 – not save, 1 – save.

    UIFLOW2:

        |set_parameters.png|

.. method:: LoRaWAN868Module.wake_up()

    Wake up the device through a serial port interrupt. After resetting, the device is in sleep state. In theory, sending any data through the serial port can trigger the interrupt and wake up the device.


    UIFLOW2:

        |wake_up.png|

.. method:: LoRaWAN868Module.sleep()

    Put the device into low-power mode.


    UIFLOW2:

        |sleep.png|

.. method:: LoRaWAN868Module.reset()

    Reset the device.


    UIFLOW2:

        |reset.png|

.. method:: LoRaWAN868Module.restore_factory_settings()

    Restore the device to factory settings. The parameters will reset and the device will enter sleep mode after response ends.


    UIFLOW2:

        |restore_factory_settings.png|

.. method:: LoRaWAN868Module.set_copyright(enable)

    Enable or disable copyright information print when boot loader mode begins. Default is enable.

    :param bool enable: Set True to enable, False to disable.

    UIFLOW2:

        |set_copyright.png|

.. method:: LoRaWAN868Module.set_auto_low_power(enable)

    Enable or disable automatic low-power mode. Default is enable.

    :param bool enable: Set True to enable, False to disable.

    UIFLOW2:

        |set_auto_low_power.png|

.. method:: LoRaWAN868Module.query_chip_id()

    Query the unique ID of the chip, which can be used to query the corresponding serial number.


    UIFLOW2:

        |query_chip_id.png|

.. method:: LoRaWAN868Module.enable_rx(timeout)

    Enable the LoRaWAN module to receive data.

    :param int timeout: The timeout for the receive operation.

    UIFLOW2:

        |enable_rx.png|

.. method:: LoRaWAN868Module.set_deveui(deveui)

    Set or query the DevEui. DevEui must be 16 hex characters (0-9, A-F).

    :param  deveui: The DevEui to set. If None, query the current DevEui.

    UIFLOW2:

        |set_deveui.png|

.. method:: LoRaWAN868Module.set_appeui(appeui)

    Set or query the AppEui. AppEui must be 16 hex characters (0-9, A-F).

    :param  appeui: The AppEui to set. If None, query the current AppEui.

    UIFLOW2:

        |set_appeui.png|

.. method:: LoRaWAN868Module.set_appkey(appkey)

    Set or query the AppKey. AppKey must be 32 hex characters (0-9, A-F).

    :param  appkey: The AppKey to set. If None, query the current AppKey.

    UIFLOW2:

        |set_appkey.png|

.. method:: LoRaWAN868Module.set_nwkskey(nwkskey)

    Set or query the NwkSKey. NwkSKey must be 32 hex characters (0-9, A-F).

    :param  nwkskey: The NwkSKey to set. If None, query the current NwkSKey.

    UIFLOW2:

        |set_nwkskey.png|

.. method:: LoRaWAN868Module.set_appskey(appskey)

    Set or query the AppSKey. AppSKey must be 32 hex characters (0-9, A-F).

    :param  appskey: The AppSKey to set. If None, query the current AppSKey.

    UIFLOW2:

        |set_appskey.png|

.. method:: LoRaWAN868Module.set_devaddr(devaddr)

    Set or query the DevAddr. DevAddr must be 8 hex characters (0-9, A-F).

    :param  devaddr: The DevAddr to set. If None, query the current DevAddr.

    UIFLOW2:

        |set_devaddr.png|

.. method:: LoRaWAN868Module.set_otaa_mode(enable)

    Set or query the OTAA mode. 1 for OTAA mode, 0 for ABP mode.

    :param bool enable: Set True for OTAA mode, False for ABP mode.

    UIFLOW2:

        |set_otaa_mode.png|

.. method:: LoRaWAN868Module.set_adr(enable)

    Enable or disable the ADR (Adaptive Data Rate) function. Default is enabled.

    :param bool enable: Set True to enable ADR, False to disable.

    UIFLOW2:

        |set_adr.png|

.. method:: LoRaWAN868Module.set_channel_mask(mask)

    Set or query the LoRaWAN working channel mask.

    :param  mask: The channel mask in hexadecimal format, e.g., 0000000000000000000000FF for channels 0~7.

    UIFLOW2:

        |set_channel_mask.png|

.. method:: LoRaWAN868Module.join_network()

    Join the network using OTAA (Over-The-Air Activation). This command triggers the join process.


    UIFLOW2:

        |join_network.png|

.. method:: LoRaWAN868Module.set_duty_cycle(cycle)

    Set or query the communication cycle in milliseconds. For example, 60000 means communication every 60 seconds.

    :param  cycle: The communication cycle in milliseconds.

    UIFLOW2:

        |set_duty_cycle.png|

.. method:: LoRaWAN868Module.set_class_mode(mode)

    Set or query the device&#x27;s communication mode. Only Class A or Class C are valid.

    :param  mode: Set &quot;A&quot; for Class A or &quot;C&quot; for Class C.

    UIFLOW2:

        |set_class_mode.png|

.. method:: LoRaWAN868Module.set_ack(enable)

    Enable or disable the ACK receipt function. If enabled, the device waits for acknowledgment from the gateway.

    :param bool enable: Set True to enable ACK, False to disable.

    UIFLOW2:

        |set_ack.png|

.. method:: LoRaWAN868Module.set_app_port(port)

    Set or query the application port (fport) for upstream data. Valid range is 0~255.

    :param  port: The application port to set.

    UIFLOW2:

        |set_app_port.png|

.. method:: LoRaWAN868Module.set_retransmission_count(count)

    Set or query the number of retransmissions if communication fails. The valid range is 3~8.

    :param  count: The number of retransmissions to set. If None, query the current setting.

    UIFLOW2:

        |set_retransmission_count.png|

.. method:: LoRaWAN868Module.send_hex(hex_data)

    Send hex data in LoRaWAN or LoRa mode. Hex characters must be in pairs (e.g., &quot;AABB&quot;).

    :param  hex_data: The hex data to send, up to 64 bytes.

    UIFLOW2:

        |send_hex.png|

.. method:: LoRaWAN868Module.send_string(string_data)

    Send string data in LoRaWAN or LoRa mode. The string must consist of ASCII characters.

    :param  string_data: The string data to send, up to 64 bytes.

    UIFLOW2:

        |send_string.png|

.. method:: LoRaWAN868Module.query_lorawan_mode()

    Query if the device is in LoRaWAN or normal LoRa mode.


    UIFLOW2:

        |query_lorawan_mode.png|

.. method:: LoRaWAN868Module.save_parameters_to_flash()

    Save the current LoRa parameters to FLASH memory.


    UIFLOW2:

        |save_parameters_to_flash.png|

.. method:: LoRaWAN868Module.at_cmd(cmd, data)

    Send an AT command to the LoRaWAN module.

    :param  cmd: The AT command to send.
    :param  data: The data to send with the AT command.

    UIFLOW2:

        |at_cmd.png|

.. method:: LoRaWAN868Module.at_query(cmd)

    Query the current settings of the LoRaWAN module.

    :param  cmd: The AT command to query.

    UIFLOW2:

        |at_query.png|

.. method:: LoRaWAN868Module.at_receive()

    Receive a response from the LoRaWAN module.


    UIFLOW2:

        |at_receive.png|

.. method:: LoRaWAN868Module.flush()

    Clear the UART buffer.


    UIFLOW2:

        |flush.png|

.. method:: LoRaWAN868Module.any()

    Check if there is any data in the UART buffer.


    UIFLOW2:

        |any.png|

.. method:: LoRaWAN868Module.receive_data()

    Receive data from the LoRaWAN module.


    UIFLOW2:

        |receive_data.png|



Constants
---------

    .. data:: LoRaWAN868Module.BAND_470
    .. data:: LoRaWAN868Module.BAND_868
    .. data:: LoRaWAN868Module.BAND_915

    LoRa band frequency

    .. data:: LoRaWAN868Module.MODE_LORA
    .. data:: LoRaWAN868Module.MODE_LORAWAN

    LoRa Mode

