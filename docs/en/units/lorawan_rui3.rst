
LoRaWAN-X Unit
==============
.. sku:U184-CN470,U184-AS923,U184-EU868,U184-US915
.. include:: ../refs/unit.lorawan_rui3.ref

Unit LoRaWAN-X is a LoRaWAN communication module based on LoRa technology, specifically designed for those frequency band. The module adopts the STM32WLE5 solution, supporting long-range communication with low power consumption and high sensitivity characteristics. The module integrates the LoRaWAN protocol stack and supports three operating modes: Class A, Class B, and Class C. It also supports point-to-point (P2P) communication mode and uses a UART communication interface (controlled by the AT command set) for flexible configuration.

Support the following products:

================== ==================
|LoRaWAN-CN470|         |LoRaWAN-AS923|
================== ==================

================== ==================
|LoRaWAN-EU868|         |LoRaWAN-US915|
================== ==================

Micropython LoRaWAN-CN470 LoRaWAN OTAA Mode Example:

    .. literalinclude:: ../../../examples/unit/lorawan_rui3/lorawan_otaa_cores3_example.py
        :language: python
        :linenos:

Micropython LoRaWAN-CN470 P2P Mode TX Example:

    .. literalinclude:: ../../../examples/unit/lorawan_rui3/lorawan_p2p_cores3_example.py
        :language: python
        :linenos:

Micropython LoRaWAN-CN470 P2P Mode RX Example:

    .. literalinclude:: ../../../examples/unit/lorawan_rui3/lorawan_p2p_rec_cores3_example.py
        :language: python
        :linenos:

UIFLOW2 LoRaWAN-CN470 LoRaWAN OTAA Mode Example:

    |lorawan_otaa_cores3_example.png|

    |lorawan_otaa_cores3_example.m5f2|

UIFLOW2 LoRaWAN-CN470 P2P Mode TX Example:

    |lorawan_p2p_cores3_example.png|

    |lorawan_p2p_cores3_example.m5f2|

UIFLOW2 LoRaWAN-CN470 P2P Mode RX Example:

    |lorawan_p2p_rec_cores3_example.png|

    |lorawan_p2p_rec_cores3_example.m5f2|

class LoRaWAN_X
---------------

Constructors
------------

.. class:: LoRaWAN_X(id, tx, rx, debug)

    Initialize the LoRaWAN_X module by setting up UART communication with the specified parameters.

    :param  id: The UART ID used for communication.
    :param  tx: The UART TX pin.
    :param  rx: The UART RX pin.
    :param bool debug: Enables debug mode to log additional details, default is False.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: LoRaWAN_X.set_abp_config(dev_addr, apps_key, nwks_key)

    Configure the device for ABP (Activation By Personalization) mode using the provided device address, application session key, and network session key.

    :param str dev_addr: The device address for ABP configuration.
    :param str apps_key: The application session key for encryption.
    :param str nwks_key: The network session key for communication.

    UIFLOW2:

        |set_abp_config.png|

.. method:: LoRaWAN_X.get_abp_config()

    Retrieve the current ABP configuration, including the device address, application session key, and network session key.

    :return: A tuple containing the device address, application session key, and network session key. Returns None or False for missing or invalid configurations.

    UIFLOW2:

        |get_abp_config.png|

.. method:: LoRaWAN_X.set_otaa_config(device_eui, app_eui, app_key)

    Configure the device for OTAA (Over-The-Air Activation) mode using the provided device EUI, application EUI, and application key.

    :param  device_eui: The device EUI for OTAA configuration.
    :param  app_eui: The application EUI for OTAA configuration.
    :param  app_key: The application key for encryption.

    UIFLOW2:

        |set_otaa_config.png|

.. method:: LoRaWAN_X.get_otaa_config()

    Retrieve the current OTAA configuration, including the device EUI, application key, and application EUI.

    :return: A tuple containing the device EUI, application key, and application EUI.

    UIFLOW2:

        |get_otaa_config.png|

.. method:: LoRaWAN_X.send_cmd(cmd, have_return, is_single, async_event, timeout)

    Sends an AT command to the module and optionally reads the response.

    :param  cmd: The AT command string to send.
    :param bool have_return: Specifies whether to read a response from the module.
    :param bool is_single: Indicates if the command expects a single-line response.
    :param bool async_event: Specifies whether to handle asynchronous events.
    :param int timeout: The timeout duration in milliseconds for receiving a response, default is 100ms.

    :returns: The processed response from the module or None if no response is expected.

.. method:: LoRaWAN_X.read_response(cmd, is_single, async_event, timeout)

    Reads and processes the module response to an AT command.

    :param  cmd: The AT command sent to the module.
    :param bool is_single: Indicates if a single-line response is expected.
    :param bool async_event: Specifies whether to handle asynchronous events.
    :param int timeout: The timeout duration in milliseconds for receiving a response.

    :returns:
        - True if the response is valid and matches a single-line expectation.
        - A processed response string when CMD+RESPONSE is received.
        - An event response string if async_event is enabled and an event is detected.
        - False if no valid response is received or an error occurs.

.. method:: LoRaWAN_X.get_commuinication_state()

    Checks the communication state by sending the AT command and expecting a response.


    :returns: The response from the module indicating the communication state.

.. method:: LoRaWAN_X.reset_module()

    Resets the module using the ATZ command.

.. method:: LoRaWAN_X.reset_module_to_default()

    Resets the module to its default settings using the ATR command. Waits for the reset process to complete.


    UIFLOW2:

        |reset_module_to_default.png|

.. method:: LoRaWAN_X.get_serial_number()

    Retrieves the serial number of the module.

    :returns: The serial number as a string.

.. method:: LoRaWAN_X.get_fireware_version()

    Retrieves the firmware version of the module.

    :returns: The firmware version as a string.

.. method:: LoRaWAN_X.get_at_version()

    Retrieves the AT command version supported by the module.

    :returns: The AT command version as a string.

.. method:: LoRaWAN_X.get_hardware_version()

    Retrieves the hardware version of the module.

    :returns: The hardware version as a string.

.. method:: LoRaWAN_X.get_hardware_id()

    Retrieves the hardware ID of the module.

    :returns: The hardware ID as a string.

.. method:: LoRaWAN_X.get_ble_mac()

    Retrieves the Bluetooth MAC address of the module.

    :returns: The BLE MAC address as a string.

.. method:: LoRaWAN_X.set_sleep_time(time)

    Configures the sleep time for the module. If no time is provided, the module enters sleep mode.

    :param  time: The sleep duration in seconds. If None, triggers sleep mode without specifying a duration.

    :returns: True if the command is successfully sent, else False.

.. method:: LoRaWAN_X.get_low_power_mode()

    Checks if the module is in low-power mode.

    :returns: True if low-power mode is enabled, otherwise False.

.. method:: LoRaWAN_X.set_low_power_mode(mode)

    Sets the module low-power mode.

    :param bool mode: A boolean value indicating whether to enable (True) or disable (False) low-power mode.

    :returns: True if the command is successfully sent, else False.

.. method:: LoRaWAN_X.set_baud_rate(rate)

    Sets the baud rate for UART communication.

    :param  rate: The desired baud rate value.

    :returns: True if the command is successfully sent, else False.

.. method:: LoRaWAN_X.get_baud_rate()

    Retrieves the current UART baud rate setting.

    :returns: The baud rate as an integer.

.. method:: LoRaWAN_X.get_device_eui()

    Retrieves the Device EUI for OTAA (Over-The-Air Activation) mode.

    :returns: The Device EUI as a string.

.. method:: LoRaWAN_X.set_device_eui(eui)

    Configures the Device EUI for OTAA mode.

    :param str eui: The Device EUI to set, as a string.

    :returns: True if the command is successfully sent, else False.

.. method:: LoRaWAN_X.get_app_eui()

    Retrieves the Application EUI for OTAA mode.

    :returns: The Application EUI as a string.

.. method:: LoRaWAN_X.set_app_eui(eui)

    Configures the Application EUI for OTAA mode.

    :param str eui: The Application EUI to set, as a string.

    :returns: True if the command is successfully sent, else False.

.. method:: LoRaWAN_X.get_app_key()

    Retrieves the Application Key for OTAA mode.

    :returns: The Application Key as a string.

.. method:: LoRaWAN_X.set_app_key(key)

    Configures the Application Key for OTAA mode.

    :param str key: The Application Key to set, as a string.

    :returns: True if the command is successfully sent, else False.

.. method:: LoRaWAN_X.get_device_address()

    Retrieves the device address.

    :returns: The device address as a string.

.. method:: LoRaWAN_X.set_device_address(address)

    Sets the device address.

    :param str address: The device address to set, provided as a string.
    
    :returns: The application session key as a string.

.. method:: LoRaWAN_X.get_apps_key()

    Retrieves the application session key.

    :returns: The result of the AT command execution
.. method:: LoRaWAN_X.set_apps_key(key)

    Sets the application session key. This operation is applicable only in ABP mode.

    :param str key: The application session key to set, provided as a string.

    :returns: The network session key as a string.

.. method:: LoRaWAN_X.get_networks_key()

    Retrieves the network session key.

    :returns: The result of the AT command execution

.. method:: LoRaWAN_X.set_networks_key(key)

    Sets the network session key. This operation is applicable only in ABP mode.

    :param str key: The network session key to set, provided as a string.

    :returns: The result of the AT command execution

.. method:: LoRaWAN_X.set_network_id(id)

    Sets the network ID.

    :param str id: The network ID to set, provided as a string.

    :returns: The network ID as a string.

.. method:: LoRaWAN_X.get_network_id()

    Retrieves the network ID.

    :returns: The multicast root key as a string.

.. method:: LoRaWAN_X.get_mc_root_key()

    Retrieves the multicast root key.

    :returns: True if confirmation mode is enabled; otherwise, False.

.. method:: LoRaWAN_X.get_confirm_mode()

    Retrieves the confirmation mode.

    :returns: The result of the AT command execution

.. method:: LoRaWAN_X.set_confirm_mode(mode)

    Sets the confirmation mode.

    :param bool mode: A boolean indicating whether to enable (True) or disable (False) confirmation mode.

    :returns: True if the last confirmed uplink succeeded; otherwise, False.

.. method:: LoRaWAN_X.get_confirm_state()

    Retrieves the status of the last confirmed uplink.

    :returns: A tuple containing state, auto_join, retry_interval, and max_retry as integers, or False if retrieval failed.

.. method:: LoRaWAN_X.get_join_config()

    Retrieves the current join configuration for LoRa.

    :returns: True if the module successfully joins the network, otherwise False

.. method:: LoRaWAN_X.set_join_config(state, auto_join, retry_interval, max_retry, timeout)

    Configures the join parameters for LoRa. The configuration does not confirm network join success.

    :return: True if the command is successfully set, else False.
    :param int state: The join state to configure, as an integer.
    :param int auto_join: The auto-join flag, as an integer.
    :param int retry_interval: The interval between join retries, default is 8 seconds.
    :param int max_retry: The maximum number of retries, default is 0 (no limit).
    :param int timeout: The timeout duration in milliseconds for the command, default is 8000ms.

    :returns: The join mode as an integer (0 for ABP, 1 for OTAA).
    
    UIFLOW2:

        |set_join_config.png|

.. method:: LoRaWAN_X.join_network(timeout)

    Joins the LoRa network using predefined join parameters.

    :param int timeout: The timeout duration in milliseconds for the join command, default is 8000ms.

    :returns: True if the command is successfully set, else False.
    
    UIFLOW2:

        |join_network.png|

        |join_network_return.png|

.. method:: LoRaWAN_X.get_join_mode()

    Retrieves the current join mode. 0 indicates ABP mode, 1 indicates OTAA mode.

    :returns: True if joined, otherwise False.

.. method:: LoRaWAN_X.set_join_mode(mode)

    Sets the join mode for the LoRa module.

    :param int mode: The join mode to set, 0 for ABP or 1 for OTAA.

    :returns: The received data as a string.
    
    UIFLOW2:

        |set_join_mode.png|

.. method:: LoRaWAN_X.get_join_state()

    Checks whether the module has successfully joined the network. 1 indicates joined, 0 indicates not joined.

    :returns: True if the data was sent successfully, otherwise False.
    
    UIFLOW2:

        |get_join_state.png|

.. method:: LoRaWAN_X.get_last_receive()

    Retrieves the data from the last received message.

    :returns: True if the data was sent successfully, otherwise False.
    
    UIFLOW2:

        |get_last_receive.png|

.. method:: LoRaWAN_X.send_data(port, data, timeout)

    Sends data through a specific port.

    :param int port: The port number to send data through.
    :param bytes data: The data to send, provided as bytes.
    :param int timeout: The timeout duration in milliseconds for the send command, default is 600ms.
    
    :returns: True if the command is successfully set, else False.
    
    UIFLOW2:

        |send_data.png|

        |send_data_return.png|

.. method:: LoRaWAN_X.send_long_data(port, ack, data, timeout)

    Sends long data through a specific port with optional acknowledgment.

    :param int port: The port number to send data through.
    :param bool ack: Indicates whether acknowledgment is required (True or False).
    :param bytes data: The long data to send, provided as bytes.
    :param int timeout: The timeout duration in milliseconds for the send command, default is 500ms.

    :returns: The retry cycle value as an integer.

.. method:: LoRaWAN_X.set_retry(retry)

    Configures the retry cycle for transmissions.

    :param int retry: The retry cycle value, ranging from 0 to 7, default is 0.

    :returns: True if the command is successfully set, else False.

.. method:: LoRaWAN_X.get_retry()

    Retrieves the current retry cycle configuration.

    :returns: The retry cycle value as an integer.

.. method:: LoRaWAN_X.get_adaptive_rate_state()

    Checks whether adaptive data rate (ADR) is enabled. 1 indicates enabled, 0 indicates disabled.

    :returns: True if ADR is enabled, otherwise False.

.. method:: LoRaWAN_X.set_adaptive_rate_state(state)

    Configures the adaptive data rate (ADR) state.

    :param bool state: A boolean indicating whether to enable (True) or disable (False) ADR.

    :returns: True if the command is successfully set, else False.

.. method:: LoRaWAN_X.get_lorawan_node_class()

    Retrieves the current LoRaWAN node class.

    :returns: The LoRaWAN node class as a string.

.. method:: LoRaWAN_X.set_lorawan_node_class(node_class)

    Sets the LoRaWAN node class.

    :param str node_class: The node class to set, provided as a string

    :returns: True if the command is successfully set, else False.

.. method:: LoRaWAN_X.get_duty_cycle_state()

    Checks whether the ETSI duty cycle is enabled. 1 indicates enabled, 0 indicates disabled.

    :returns: True if the duty cycle is enabled, otherwise False.

.. method:: LoRaWAN_X.set_duty_cycle_state(state)

    Sets the ETSI duty cycle state, which can be enabled or disabled depending on the region.

    :param bool state: A boolean indicating whether to enable (True) or disable (False) the duty cycle.

    :returns: The result of the AT command execution.

.. method:: LoRaWAN_X.get_data_rate()

    Retrieves the current data rate configuration.

    :returns: The data rate as an integer.

.. method:: LoRaWAN_X.set_data_rate(rate)

    Sets the data rate for communication.

    :param int rate: The data rate to set, provided as an integer.

    :returns: The result of the AT command execution.

.. method:: LoRaWAN_X.get_join_delay_on_window1()

    Retrieves the delay for the join procedure on window 1.

    :returns: The join delay for window 1 as an integer.

.. method:: LoRaWAN_X.set_join_delay_on_window1(delay)

    Sets the join delay for window 1.

    :param int delay: The join delay to set for window 1 as an integer.

    :returns: The result of the AT command execution.

.. method:: LoRaWAN_X.get_join_delay_on_window2()

    Retrieves the delay for the join procedure on window 2.

    :returns: The join delay for window 2 as an integer.

.. method:: LoRaWAN_X.set_join_delay_on_window2(delay)

    Sets the join delay for window 2.

    :param int delay: The join delay to set for window 2 as an integer.

    :returns: The result of the AT command execution.

.. method:: LoRaWAN_X.get_public_network_mode()

    Retrieves the public network mode (enabled or disabled).

    :returns: True if public network mode is enabled, False otherwise.

.. method:: LoRaWAN_X.set_public_network_mode(mode)

    Sets the public network mode to enabled or disabled.

    :param bool mode: A boolean indicating whether to enable (True) or disable (False) the public network mode.

    :returns: The result of the AT command execution.

.. method:: LoRaWAN_X.get_rx_delay_on_window1()

    Retrieves the receive window 1 delay.

    :returns: The receive window 1 delay as an integer.

.. method:: LoRaWAN_X.set_rx_delay_on_window1(delay)

    Sets the receive delay for window 1.

    :param int delay: The delay to set for receive window 1 as an integer.

    :returns: The result of the AT command execution.

.. method:: LoRaWAN_X.get_rx_delay_on_window2()

    Retrieves the receive window 2 delay.

    :returns: The receive window 2 delay as an integer.

.. method:: LoRaWAN_X.set_rx_delay_on_window2(delay)

    Sets the receive delay for window 2.

    :param int delay: The delay to set for receive window 2, with a range of 2 to 16.

    :returns: The result of the AT command execution.

.. method:: LoRaWAN_X.get_rx_data_rate_on_windows2()

    Retrieves the receive data rate for window 2.

    :returns: The receive data rate for window 2 as an integer.

.. method:: LoRaWAN_X.set_rx_data_rate_on_windows2(rate)

    Sets the receive data rate for window 2.

    :param int rate: The data rate to set for window 2.

    :returns: The result of the AT command execution.

.. method:: LoRaWAN_X.get_rx_frequency_on_windows2()

    Retrieves the receive frequency for window 2, based on regional frequency settings.

    :returns: The receive frequency for window 2 as an integer.

.. method:: LoRaWAN_X.get_tx_power()

    Retrieves the current transmit power setting.

    :returns: The transmit power setting as an integer.

.. method:: LoRaWAN_X.set_tx_power(power)

    Sets the transmit power.

    :param int power: The transmit power to set.

    :returns: The result of the AT command execution.

.. method:: LoRaWAN_X.get_network_link_state()

    Retrieves the network link state.

    :returns: The network link state as a string.

.. method:: LoRaWAN_X.set_network_link_state(state)

    :param int state: Sets the network link state for the device.
            0 - Disable Link Check
            1 - Execute Link Check once on the next payload uplink
            2 - Automatically execute Link Check after every payload uplink

    :returns: The result of the AT command execution.

.. method:: LoRaWAN_X.get_listen_before_talk()

    Retrieves the Listen Before Talk (LBT) state.

    :returns: True if LBT is enabled, False if not.

.. method:: LoRaWAN_X.set_listen_before_talk(state)

    Sets the Listen Before Talk (LBT) state.

    :param bool state: The state to set for LBT (True for enabled, False for disabled).

    :returns: The result of the AT command execution.

.. method:: LoRaWAN_X.set_listen_before_talk_rssi(rssi)

    Sets the RSSI threshold for Listen Before Talk (LBT).

    :param int rssi: The RSSI threshold to set for LBT.

    :returns: The result of the AT command execution.

.. method:: LoRaWAN_X.get_listen_before_talk_rssi()

    Retrieves the RSSI threshold for Listen Before Talk (LBT).

    :returns: The RSSI threshold as an integer.

.. method:: LoRaWAN_X.get_listen_before_talk_scan_time()

    Retrieves the scan time for Listen Before Talk (LBT).

    :returns: The scan time for LBT as an integer.

.. method:: LoRaWAN_X.set_listen_before_talk_scan_time(time)

    Sets the scan time for Listen Before Talk (LBT).

    :param int time: The scan time to set for LBT.

    :returns: The result of the AT command execution.

.. method:: LoRaWAN_X.get_time_request()

    Retrieves the time request state.

    :returns: The time request state as an integer.

.. method:: LoRaWAN_X.set_time_request(state)

    Sets the time request state.

    :param bool state: The state to set for time request (True to enable, False to disable).

    :returns: The result of the AT command execution.

.. method:: LoRaWAN_X.get_location_time()

    Retrieves the location time in UTC+0.

    :returns: The location time in UTC+0 as a string.

.. method:: LoRaWAN_X.get_unicast_ping_interval()

    Retrieves the unicast ping interval in Class B mode.

    :returns: The unicast ping interval as an integer.

.. method:: LoRaWAN_X.set_unicast_ping_interval(interval)

    Sets the unicast ping interval for the device.

    :param int interval: The interval to set for the unicast ping (0 to 7). 0 means approximately every second during the beacon window, and 7 means every 128 seconds (maximum ping period).

    :returns: The result of the AT command execution.

.. method:: LoRaWAN_X.get_beacon_frequency()

    Retrieves the beacon frequency.

    :returns: The beacon frequency as an integer.

.. method:: LoRaWAN_X.get_beacon_time()

    Retrieves the beacon time.

    :returns: The beacon time as an integer.

.. method:: LoRaWAN_X.get_beacon_gateway_gps()

    Retrieves the beacon gateway GPS location.

    :returns: The beacon gateway GPS information as a string.

.. method:: LoRaWAN_X.get_rssi()

    Retrieves the Received Signal Strength Indicator (RSSI).

    :returns: The RSSI value as a string.

.. method:: LoRaWAN_X.get_all_rssi()

    Retrieves the RSSI values from all channels.

    :returns: The RSSI values for all channels as a string.

.. method:: LoRaWAN_X.get_signal_noise_ratio()

    Retrieves the Signal-to-Noise Ratio (SNR).

    :returns: The SNR value as a string.

.. method:: LoRaWAN_X.get_channel_mask()

    Retrieves the channel mask (only for US915, AU915, CN470).

    :returns: The channel mask as a string.

.. method:: LoRaWAN_X.set_channel_mask(mask)

    Sets the channel mask to open or close specific channels (only for US915, AU915, CN470).

    :param str mask: The channel mask as a 4-length hexadecimal string.

    :returns: The result of the AT command execution.

.. method:: LoRaWAN_X.get_eight_channel_mode_state()

    Retrieves the state of the eight-channel mode.

    :returns: The state of the eight-channel mode as a string.

.. method:: LoRaWAN_X.set_eight_channel_mode_state(max_group)

    Sets the state of the eight-channel mode, with a group number between 1 and 12.

    :param int max_group: The maximum group number (1 to 12).

    :returns: True if the AT command execution is successful, False otherwise.

.. method:: LoRaWAN_X.get_single_channel_mode()

    Retrieves the single channel mode.

    :returns: The single channel mode as a string.

.. method:: LoRaWAN_X.set_single_channel_mode()

    Sets the single channel mode.

    :returns: The result of the AT command execution.

.. method:: LoRaWAN_X.get_active_region()

    Retrieves the active region for the device.

    :returns: The active region as a string.

.. method:: LoRaWAN_X.set_active_region(region)

    :param int region: Sets the active region for the device.

    :returns: The result of the AT command execution.

            - ``EU433``: 0
            - ``CN470``: 1
            - ``RU864``: 2
            - ``IN865``: 3
            - ``EU868``: 4
            - ``US915``: 5
            - ``AU915,``: 6
            - ``KR920,``: 7
            - ``AS923-1``: 8
            - ``AS923-2``: 9
            - ``AS923-3``: 10
            - ``AS923-4``: 11
            - ``LA915``: 12

.. method:: LoRaWAN_X.add_multicast_group(Class, DevAddr, NwkSKey, AppSKey, Frequency, Datarate, Periodicit)

    Adds a multicast group to the device.

    :param str Class: The class of the multicast group.
    :param  DevAddr: The device address.
    :param  NwkSKey: The network session key.
    :param  AppSKey: The application session key.
    :param  Frequency: The frequency for the multicast group.
    :param  Datarate: The datarate for the multicast group.
    :param  Periodicit: The periodicity for the multicast group.

    :returns: The result of the AT command execution.

.. method:: LoRaWAN_X.remove_multicast_group(DevAddr)

    Removes a multicast group by the given device address.

    :param  DevAddr: The device address of the multicast group to remove.

    :returns: The result of the AT command execution.

.. method:: LoRaWAN_X.get_multicast_list()

    Retrieves the list of multicast groups.

    :returns: The list of multicast groups as a string.

.. method:: LoRaWAN_X.get_network_mode()

    Retrieves the current network mode.

    :returns: The current network mode as an integer

            - ``P2P_LORA``: 0
            - ``LoRaWAN``: 1
            - ``P2P_FSK``: 2

.. method:: LoRaWAN_X.set_network_mode(mode)

    Sets the network mode for the device.

    :param int mode: The mode to set for the get_network_id.

            - ``P2P_LORA``: 0
            - ``LoRaWAN``: 1
            - ``P2P_FSK``: 2

    :returns: The result of the AT command execution.

    UIFLOW2:

        |set_network_mode.png|

.. method:: LoRaWAN_X.get_p2p_frequency()

    Retrieves the current P2P frequency.

    :returns: The current P2P frequency as an integer.

    UIFLOW2:

        |get_p2p_frequency.png|

.. method:: LoRaWAN_X.set_p2p_frequency(frequency)

    Sets the P2P frequency for the device.

    :param int frequency: The frequency to set for P2P communication.

        - ``Low-frequency`` : 150000000-525000000
        - ``High-frequency`` : 525000000-960000000

    :returns: The result of the AT command execution.

    UIFLOW2:

        |set_p2p_frequency.png|

.. method:: LoRaWAN_X.get_p2p_spreading_factor()

    Retrieves the current P2P spreading factor.

    :returns: The current P2P spreading factor as an integer.

    UIFLOW2:

        |get_p2p_spreading_factor.png|

.. method:: LoRaWAN_X.set_p2p_spreading_factor(spreading_factor)

    Sets the P2P spreading factor.

    :param int spreading_factor: The spreading factor to set for P2P communication. The default value is 7, and the range is 5 to 12.

    :returns: The result of the AT command execution.

    UIFLOW2:

        |set_p2p_spreading_factor.png|

.. method:: LoRaWAN_X.get_p2p_bandwidth()

    Retrieves the current P2P bandwidth.


    :returns: The current P2P bandwidth as an integer.

    UIFLOW2:

        |get_p2p_bandwidth.png|

.. method:: LoRaWAN_X.set_p2p_bandwidth(bandwidth)


    :param int bandwidth: 

    :returns: The result of the AT command execution.

    UIFLOW2:

        |set_p2p_fsk_bandwidth.png|

        |set_p2p_lora_bandwidth.png|

.. method:: LoRaWAN_X.get_p2p_code_rate()

    Retrieves the current P2P code rate.


    :returns: The current P2P code rate as an integer.

    UIFLOW2:

        |get_p2p_code_rate.png|

.. method:: LoRaWAN_X.set_p2p_code_rate(code_rate)

    Sets the P2P code rate.

    :param int code_rate: The code rate to set for P2P communication. Default is 0, range is 0 to 3. 0 = 4/5, 1 = 4/6, 2 = 4/7, 3 = 4/8.

    :returns: The result of the AT command execution.

    UIFLOW2:

        |set_p2p_code_rate.png|

.. method:: LoRaWAN_X.get_p2p_preamble_length()

    Retrieves the current P2P preamble length.


    :returns: The current P2P preamble length as an integer.

    UIFLOW2:

        |get_p2p_preamble_length.png|

.. method:: LoRaWAN_X.set_p2p_preamble_length(length)

    Sets the P2P preamble length.

    :param int length: The preamble length to set for P2P communication. Default is 8, range is 5 to 65535.

    :returns: The result of the AT command execution.

    UIFLOW2:

        |set_p2p_preamble_length.png|

.. method:: LoRaWAN_X.get_p2p_tx_power()

    Retrieves the current P2P transmission power.


    :returns: The current P2P transmission power as an integer.

    UIFLOW2:

        |get_p2p_tx_power.png|

.. method:: LoRaWAN_X.set_p2p_tx_power(power)

    Sets the P2P transmission power.

    :param int power: The transmission power to set for P2P communication. Default is 14 dBm, range is 5 to 22 dBm.

    :returns: The result of the AT command execution.

    UIFLOW2:

        |set_p2p_tx_power.png|

.. method:: LoRaWAN_X.get_p2p_fsk_bitrate()

    Retrieves the current P2P FSK bitrate.


    :returns: The current P2P FSK bitrate as an integer.

    UIFLOW2:

        |get_p2p_fsk_bitrate.png|

.. method:: LoRaWAN_X.set_p2p_fsk_bitrate(bitrate)

    Sets the P2P FSK bitrate.

    :param int bitrate: The bitrate to set for P2P FSK communication. The range is 600 to 300000 b/s.

    :returns: The result of the AT command execution.

    UIFLOW2:

        |set_p2p_fsk_bitrate.png|

.. method:: LoRaWAN_X.get_p2p_fsk_frequency_deviation()

    Retrieves the current P2P FSK frequency deviation.


    :returns: The current P2P FSK frequency deviation as an integer.

.. method:: LoRaWAN_X.set_p2p_fsk_frequency_deviation(deviation)

    Sets the P2P FSK frequency deviation.

    :param int deviation: The frequency deviation to set for P2P FSK communication. The range is 600 to 200000 Hz.

    :returns: The result of the AT command execution.

.. method:: LoRaWAN_X.send_p2p_data(payload, timeout)

    Sends P2P data with a given payload.

    :param str payload: The payload to send, 2 to 500 characters in length, must be an even number of characters composed of 0-9, a-f, A-F, representing 1 to 256 hexadecimal values.
    :param int timeout: The timeout for the data transmission, default is 1000 ms.

    :returns: True if the data was sent successfully ("TXFSK DONE" or "TXP2P DONE"), False otherwise.

    UIFLOW2:

        |send_p2p_data.png|

        |send_p2p_data_return.png|

.. method:: LoRaWAN_X.get_p2p_channel_activity()

    Get the current channel activity status in P2P mode.

    :returns: The channel activity status as an integer (0 or 1).

.. method:: LoRaWAN_X.set_p2p_channel_activity(state)

    Enable or disable channel activity in P2P mode.

    :param bool state: 0 to disable, 1 to enable channel activity.

    :returns: The response from the command execution.

.. method:: LoRaWAN_X.get_p2p_receive_data(timeout)


    :param int timeout: Timeout for listening to P2P LoRa data packets.
                Valid values are 1~65535, with special cases for continuous listening and no timeout.

    :returns: A tuple (RSSI, SNR, Payload) if data is received; False if no data is received.

    UIFLOW2:

        |get_p2p_receive_data.png|

.. method:: LoRaWAN_X.get_p2p_encryption_state()

    Get the current encryption state in P2P mode.


    :returns: The encryption state as an integer (0 or 1).

.. method:: LoRaWAN_X.set_p2p_encryption_state(state)

    Enable or disable encryption in P2P mode.

    :param bool state: 0 to disable, 1 to enable encryption.

    :returns: The response from the command execution.

.. method:: LoRaWAN_X.get_p2p_encryption_key()

    Get the current encryption key in P2P mode.

    :returns: The encryption key as a string.

.. method:: LoRaWAN_X.set_p2p_encryption_key(key)

    Set the encryption key in P2P mode.

    :param str key: The encryption key, represented as a 16-character hexadecimal string.

    :returns: The response from the command execution.

.. method:: LoRaWAN_X.get_p2p_crypt_state()

    Get the current cryptographic state in P2P mode (not supported on RAK3172).

    :returns: The cryptographic state as an integer (0 or 1).

.. method:: LoRaWAN_X.set_p2p_crypt_state(state)

    Enable or disable cryptographic state in P2P mode (not supported on RAK3172).

    :param bool state: 0 to disable, 1 to enable cryptographic state.

    :returns: The response from the command execution.

.. method:: LoRaWAN_X.get_p2p_crypt_key()

    Get the cryptographic key in P2P mode (not supported on RAK3172).

    :returns: The cryptographic key as a string.

.. method:: LoRaWAN_X.set_p2p_crypt_key(key)

    Set the cryptographic key in P2P mode (not supported on RAK3172).

    :param  key: The cryptographic key, represented as an 8-character hexadecimal string.

    :returns: The response from the command execution.

.. method:: LoRaWAN_X.get_p2p_encryption_iv()

    Get the encryption IV in P2P mode.

    :returns: The encryption IV as a string.

.. method:: LoRaWAN_X.set_p2p_encryption_iv(iv)

    Set the encryption IV in P2P mode.

    :param str iv: The encryption IV, represented as an 8-character hexadecimal string.

    :returns: The response from the command execution.

.. method:: LoRaWAN_X.get_p2p_parameters()

    Get the current P2P parameters.

    :returns: The current P2P parameters as a string.

.. method:: LoRaWAN_X.set_p2p_parameters(frequency, spreading_factor, bandwidth, code_rate, preamble_length, tx_power)

    Set P2P LoRa parameters, including frequency, spreading factor, bandwidth, code rate, preamble length, and transmit power.

    :param int frequency: The frequency to use for communication, range 150000000-960000000.
    :param int spreading_factor: The spreading factor, which can be {6, 7, 8, 9, 10, 11, 12}.
    :param int bandwidth: The bandwidth, which can be {125, 250, 500}.
    :param int code_rate: The code rate, where possible values are {4/5=0, 4/6=1, 4/7=2, 4/8=3}.
    :param int preamble_length: The length of the preamble, which can be from 2 to 65535.
    :param int tx_power: The transmit power, which can be in the range {5-22}.

    :returns: The response from the command execution.

.. method:: LoRaWAN_X.get_p2p_iq_inversion()

    Get the current IQ inversion state in P2P mode.

    :returns: The IQ inversion state as an integer (0 or 1).

.. method:: LoRaWAN_X.set_p2p_iq_inversion(state)

    Enable or disable IQ inversion in P2P mode.

    :param bool state: 0 to disable, 1 to enable IQ inversion.

    :returns: The response from the command execution.

.. method:: LoRaWAN_X.get_p2p_sync_word()

    Get the current sync word in P2P mode.

    :returns: The sync word as a string.

    UIFLOW2:

        |get_p2p_sync_word.png|

.. method:: LoRaWAN_X.set_p2p_sync_word(sync_word)

    Set the sync word in P2P mode.

    :param int sync_word: The sync word value, which should be in the range of 0x0000 to 0xFFFF.

    :returns: The response from the command execution.

    UIFLOW2:

        |set_p2p_sync_word.png|

.. method:: LoRaWAN_X.get_p2p_symbol_timeout()

    Get the current symbol timeout in P2P mode.

    :returns: The symbol timeout as an integer.

.. method:: LoRaWAN_X.set_p2p_symbol_timeout(timeout)

    Set the symbol timeout in P2P mode.

    :param bool timeout: The timeout value, which should be in the range of 0-248.

    :returns: The response from the command execution.

.. method:: LoRaWAN_X.get_p2p_fix_length_payload_state()

    Get the current fixed length payload state in P2P mode.

    :returns: The fixed length payload state as an integer (0 or 1).

.. method:: LoRaWAN_X.set_p2p_fix_length_payload_state(state)

    Enable or disable fixed length payload in P2P mode.

    :param bool state: 0 to disable, 1 to enable fixed length payload.

    :returns: The response from the command execution.