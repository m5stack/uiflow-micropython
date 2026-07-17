
# LoRaWAN-X Unit

Unit LoRaWAN-X is a LoRaWAN communication module based on LoRa technology, specifically designed for those frequency band. The module adopts the STM32WLE5 solution, supporting long-range communication with low power consumption and high sensitivity characteristics. The module integrates the LoRaWAN protocol stack and supports three operating modes: Class A, Class B, and Class C. It also supports point-to-point (P2P) communication mode and uses a UART communication interface (controlled by the AT command set) for flexible configuration.

Support the following products:

LoRaWAN-CN470         LoRaWAN-AS923

LoRaWAN-EU868         LoRaWAN-US915

Micropython LoRaWAN-CN470 LoRaWAN OTAA Mode Example:

```python
import os, sys, io
import M5
from M5 import *
from unit import LoRaWANUnit_RUI3
import time

title0 = None
label2 = None
label0 = None
label1 = None
lorawancn470_0 = None

def setup():
    global title0, label2, label0, label1, lorawancn470_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "LoRaWAN OTAA CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label2 = Widgets.Label(
        "LoRa Message Rec:", 1, 172, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label(
        "LoRa Network Join status:", 1, 68, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "LoRa Message Send status:", 1, 121, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    lorawancn470_0 = LoRaWANUnit_RUI3(2, port=(1, 2))
    lorawancn470_0.set_network_mode(1)
    lorawancn470_0.set_otaa_config("xxxxx", "xxxxx", "xxxxx")
    lorawancn470_0.set_channel_mask("0400")
    lorawancn470_0.set_rx_delay_on_window1(1)
    lorawancn470_0.set_rx_delay_on_window2(2)
    lorawancn470_0.set_rx_data_rate_on_windows2(0)
    lorawancn470_0.set_lorawan_node_class("C")
    lorawancn470_0.join_network(0)

def loop():
    global title0, label2, label0, label1, lorawancn470_0
    M5.update()
    label0.setText(
        str((str("LoRa Network Join status:") + str((lorawancn470_0.get_join_state()))))
    )
    if lorawancn470_0.get_join_state():
        label1.setText(
            str(
                (
                    str("LoRa Message Send status:")
                    + str((lorawancn470_0.send_data(1, "aabbcc", 6000)))
                )
            )
        )
        label2.setText(str((str("LoRa Message Rec:") + str((lorawancn470_0.get_last_receive())))))
    time.sleep(6)

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

Micropython LoRaWAN-CN470 P2P Mode TX Example:

```python
import os, sys, io
import M5
from M5 import *
from unit import LoRaWANUnit_RUI3
import time

title0 = None
label0 = None
lorawancn470_0 = None

def setup():
    global title0, label0, lorawancn470_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "LoRaWAN P2P Send CoreS3 e.g.", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label(
        "P2P Message Send State:", 3, 115, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    lorawancn470_0 = LoRaWANUnit_RUI3(2, port=(1, 2))
    lorawancn470_0.set_network_mode(0)
    lorawancn470_0.set_p2p_frequency(470000000)
    lorawancn470_0.set_p2p_spreading_factor(7)
    lorawancn470_0.set_p2p_bandwidth(0)
    lorawancn470_0.set_p2p_tx_power(14)
    lorawancn470_0.set_p2p_code_rate(0)
    lorawancn470_0.set_p2p_preamble_length(8)
    lorawancn470_0.set_p2p_sync_word(0xFFFF)

def loop():
    global title0, label0, lorawancn470_0
    M5.update()
    label0.setText(
        str(
            (
                str("P2P Message Send State:")
                + str((lorawancn470_0.send_p2p_data("M5", timeout=1000, to_hex=True)))
            )
        )
    )
    time.sleep(3.5)

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

Micropython LoRaWAN-CN470 P2P Mode RX Example:

```python
import os, sys, io
import M5
from M5 import *
from unit import LoRaWANUnit_RUI3
import time

title0 = None
label0 = None
lorawancn470_0 = None

def setup():
    global title0, label0, lorawancn470_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "LoRaWAN P2P Rec CoreS3 e.g.", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label(
        "P2P Message Rec:", 3, 115, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    lorawancn470_0 = LoRaWANUnit_RUI3(2, port=(1, 2))
    lorawancn470_0.set_network_mode(0)
    lorawancn470_0.set_p2p_frequency(470000000)
    lorawancn470_0.set_p2p_spreading_factor(7)
    lorawancn470_0.set_p2p_bandwidth(0)
    lorawancn470_0.set_p2p_tx_power(14)
    lorawancn470_0.set_p2p_code_rate(0)
    lorawancn470_0.set_p2p_preamble_length(8)
    lorawancn470_0.set_p2p_sync_word(0xFFFF)

def loop():
    global title0, label0, lorawancn470_0
    M5.update()
    label0.setText(
        str((str("P2P Message Rec:") + str((lorawancn470_0.get_p2p_receive_data(3000, True)))))
    )
    time.sleep(3.5)

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

## class LoRaWAN_X

## Constructors

### `class LoRaWAN_X(id, tx, rx, debug)`

    Initialize the LoRaWAN_X module by setting up UART communication with the specified parameters.

    - Parameter `id`: The UART ID used for communication.
    - Parameter `tx`: The UART TX pin.
    - Parameter `rx`: The UART RX pin.
    - Parameter `debug` (`bool`): Enables debug mode to log additional details, default is False.

## Methods

### `LoRaWAN_X.set_abp_config(dev_addr, apps_key, nwks_key)`

    Configure the device for ABP (Activation By Personalization) mode using the provided device address, application session key, and network session key.

    - Parameter `dev_addr` (`str`): The device address for ABP configuration.
    - Parameter `apps_key` (`str`): The application session key for encryption.
    - Parameter `nwks_key` (`str`): The network session key for communication.

### `LoRaWAN_X.get_abp_config()`

    Retrieve the current ABP configuration, including the device address, application session key, and network session key.

    - Returns: A tuple containing the device address, application session key, and network session key. Returns None or False for missing or invalid configurations.

### `LoRaWAN_X.set_otaa_config(device_eui, app_eui, app_key)`

    Configure the device for OTAA (Over-The-Air Activation) mode using the provided device EUI, application EUI, and application key.

    - Parameter `device_eui`: The device EUI for OTAA configuration.
    - Parameter `app_eui`: The application EUI for OTAA configuration.
    - Parameter `app_key`: The application key for encryption.

### `LoRaWAN_X.get_otaa_config()`

    Retrieve the current OTAA configuration, including the device EUI, application key, and application EUI.

    - Returns: A tuple containing the device EUI, application key, and application EUI.

### `LoRaWAN_X.send_cmd(cmd, have_return, is_single, async_event, timeout)`

    Sends an AT command to the module and optionally reads the response.

    - Parameter `cmd`: The AT command string to send.
    - Parameter `have_return` (`bool`): Specifies whether to read a response from the module.
    - Parameter `is_single` (`bool`): Indicates if the command expects a single-line response.
    - Parameter `async_event` (`bool`): Specifies whether to handle asynchronous events.
    - Parameter `timeout` (`int`): The timeout duration in milliseconds for receiving a response, default is 100ms.

    - Returns: The processed response from the module or None if no response is expected.

### `LoRaWAN_X.read_response(cmd, is_single, async_event, timeout)`

    Reads and processes the module response to an AT command.

    - Parameter `cmd`: The AT command sent to the module.
    - Parameter `is_single` (`bool`): Indicates if a single-line response is expected.
    - Parameter `async_event` (`bool`): Specifies whether to handle asynchronous events.
    - Parameter `timeout` (`int`): The timeout duration in milliseconds for receiving a response.

    - Returns:
        - True if the response is valid and matches a single-line expectation.
        - A processed response string when CMD+RESPONSE is received.
        - An event response string if async_event is enabled and an event is detected.
        - False if no valid response is received or an error occurs.

### `LoRaWAN_X.get_commuinication_state()`

    Checks the communication state by sending the AT command and expecting a response.

    - Returns: The response from the module indicating the communication state.

### `LoRaWAN_X.reset_module()`

    Resets the module using the ATZ command.

### `LoRaWAN_X.reset_module_to_default()`

    Resets the module to its default settings using the ATR command. Waits for the reset process to complete.

### `LoRaWAN_X.get_serial_number()`

    Retrieves the serial number of the module.

    - Returns: The serial number as a string.

### `LoRaWAN_X.get_fireware_version()`

    Retrieves the firmware version of the module.

    - Returns: The firmware version as a string.

### `LoRaWAN_X.get_at_version()`

    Retrieves the AT command version supported by the module.

    - Returns: The AT command version as a string.

### `LoRaWAN_X.get_hardware_version()`

    Retrieves the hardware version of the module.

    - Returns: The hardware version as a string.

### `LoRaWAN_X.get_hardware_id()`

    Retrieves the hardware ID of the module.

    - Returns: The hardware ID as a string.

### `LoRaWAN_X.get_ble_mac()`

    Retrieves the Bluetooth MAC address of the module.

    - Returns: The BLE MAC address as a string.

### `LoRaWAN_X.set_sleep_time(time)`

    Configures the sleep time for the module. If no time is provided, the module enters sleep mode.

    - Parameter `time`: The sleep duration in seconds. If None, triggers sleep mode without specifying a duration.

    - Returns: True if the command is successfully sent, else False.

### `LoRaWAN_X.get_low_power_mode()`

    Checks if the module is in low-power mode.

    - Returns: True if low-power mode is enabled, otherwise False.

### `LoRaWAN_X.set_low_power_mode(mode)`

    Sets the module low-power mode.

    - Parameter `mode` (`bool`): A boolean value indicating whether to enable (True) or disable (False) low-power mode.

    - Returns: True if the command is successfully sent, else False.

### `LoRaWAN_X.set_baud_rate(rate)`

    Sets the baud rate for UART communication.

    - Parameter `rate`: The desired baud rate value.

    - Returns: True if the command is successfully sent, else False.

### `LoRaWAN_X.get_baud_rate()`

    Retrieves the current UART baud rate setting.

    - Returns: The baud rate as an integer.

### `LoRaWAN_X.get_device_eui()`

    Retrieves the Device EUI for OTAA (Over-The-Air Activation) mode.

    - Returns: The Device EUI as a string.

### `LoRaWAN_X.set_device_eui(eui)`

    Configures the Device EUI for OTAA mode.

    - Parameter `eui` (`str`): The Device EUI to set, as a string.

    - Returns: True if the command is successfully sent, else False.

### `LoRaWAN_X.get_app_eui()`

    Retrieves the Application EUI for OTAA mode.

    - Returns: The Application EUI as a string.

### `LoRaWAN_X.set_app_eui(eui)`

    Configures the Application EUI for OTAA mode.

    - Parameter `eui` (`str`): The Application EUI to set, as a string.

    - Returns: True if the command is successfully sent, else False.

### `LoRaWAN_X.get_app_key()`

    Retrieves the Application Key for OTAA mode.

    - Returns: The Application Key as a string.

### `LoRaWAN_X.set_app_key(key)`

    Configures the Application Key for OTAA mode.

    - Parameter `key` (`str`): The Application Key to set, as a string.

    - Returns: True if the command is successfully sent, else False.

### `LoRaWAN_X.get_device_address()`

    Retrieves the device address.

    - Returns: The device address as a string.

### `LoRaWAN_X.set_device_address(address)`

    Sets the device address.

    - Parameter `address` (`str`): The device address to set, provided as a string.

    - Returns: The application session key as a string.

### `LoRaWAN_X.get_apps_key()`

    Retrieves the application session key.

    - Returns: The result of the AT command execution
### `LoRaWAN_X.set_apps_key(key)`

    Sets the application session key. This operation is applicable only in ABP mode.

    - Parameter `key` (`str`): The application session key to set, provided as a string.

    - Returns: The network session key as a string.

### `LoRaWAN_X.get_networks_key()`

    Retrieves the network session key.

    - Returns: The result of the AT command execution

### `LoRaWAN_X.set_networks_key(key)`

    Sets the network session key. This operation is applicable only in ABP mode.

    - Parameter `key` (`str`): The network session key to set, provided as a string.

    - Returns: The result of the AT command execution

### `LoRaWAN_X.set_network_id(id)`

    Sets the network ID.

    - Parameter `id` (`str`): The network ID to set, provided as a string.

    - Returns: The network ID as a string.

### `LoRaWAN_X.get_network_id()`

    Retrieves the network ID.

    - Returns: The multicast root key as a string.

### `LoRaWAN_X.get_mc_root_key()`

    Retrieves the multicast root key.

    - Returns: True if confirmation mode is enabled; otherwise, False.

### `LoRaWAN_X.get_confirm_mode()`

    Retrieves the confirmation mode.

    - Returns: The result of the AT command execution

### `LoRaWAN_X.set_confirm_mode(mode)`

    Sets the confirmation mode.

    - Parameter `mode` (`bool`): A boolean indicating whether to enable (True) or disable (False) confirmation mode.

    - Returns: True if the last confirmed uplink succeeded; otherwise, False.

### `LoRaWAN_X.get_confirm_state()`

    Retrieves the status of the last confirmed uplink.

    - Returns: A tuple containing state, auto_join, retry_interval, and max_retry as integers, or False if retrieval failed.

### `LoRaWAN_X.get_join_config()`

    Retrieves the current join configuration for LoRa.

    - Returns: True if the module successfully joins the network, otherwise False

### `LoRaWAN_X.set_join_config(state, auto_join, retry_interval, max_retry, timeout)`

    Configures the join parameters for LoRa. The configuration does not confirm network join success.

    - Returns: True if the command is successfully set, else False.
    - Parameter `state` (`int`): The join state to configure, as an integer.
    - Parameter `auto_join` (`int`): The auto-join flag, as an integer.
    - Parameter `retry_interval` (`int`): The interval between join retries, default is 8 seconds.
    - Parameter `max_retry` (`int`): The maximum number of retries, default is 0 (no limit).
    - Parameter `timeout` (`int`): The timeout duration in milliseconds for the command, default is 8000ms.

    - Returns: The join mode as an integer (0 for ABP, 1 for OTAA).

### `LoRaWAN_X.join_network(timeout)`

    Joins the LoRa network using predefined join parameters.

    - Parameter `timeout` (`int`): The timeout duration in milliseconds for the join command, default is 8000ms.

    - Returns: True if the command is successfully set, else False.

### `LoRaWAN_X.get_join_mode()`

    Retrieves the current join mode. 0 indicates ABP mode, 1 indicates OTAA mode.

    - Returns: True if joined, otherwise False.

### `LoRaWAN_X.set_join_mode(mode)`

    Sets the join mode for the LoRa module.

    - Parameter `mode` (`int`): The join mode to set, 0 for ABP or 1 for OTAA.

    - Returns: The received data as a string.

### `LoRaWAN_X.get_join_state()`

    Checks whether the module has successfully joined the network. 1 indicates joined, 0 indicates not joined.

    - Returns: True if the data was sent successfully, otherwise False.

### `LoRaWAN_X.get_last_receive()`

    Retrieves the data from the last received message.

    - Returns: True if the data was sent successfully, otherwise False.

### `LoRaWAN_X.send_data(port, data, timeout)`

    Sends data through a specific port.

    - Parameter `port` (`int`): The port number to send data through.
    - Parameter `data` (`bytes`): The data to send, provided as bytes.
    - Parameter `timeout` (`int`): The timeout duration in milliseconds for the send command, default is 600ms.

    - Returns: True if the command is successfully set, else False.

### `LoRaWAN_X.send_long_data(port, ack, data, timeout)`

    Sends long data through a specific port with optional acknowledgment.

    - Parameter `port` (`int`): The port number to send data through.
    - Parameter `ack` (`bool`): Indicates whether acknowledgment is required (True or False).
    - Parameter `data` (`bytes`): The long data to send, provided as bytes.
    - Parameter `timeout` (`int`): The timeout duration in milliseconds for the send command, default is 500ms.

    - Returns: The retry cycle value as an integer.

### `LoRaWAN_X.set_retry(retry)`

    Configures the retry cycle for transmissions.

    - Parameter `retry` (`int`): The retry cycle value, ranging from 0 to 7, default is 0.

    - Returns: True if the command is successfully set, else False.

### `LoRaWAN_X.get_retry()`

    Retrieves the current retry cycle configuration.

    - Returns: The retry cycle value as an integer.

### `LoRaWAN_X.get_adaptive_rate_state()`

    Checks whether adaptive data rate (ADR) is enabled. 1 indicates enabled, 0 indicates disabled.

    - Returns: True if ADR is enabled, otherwise False.

### `LoRaWAN_X.set_adaptive_rate_state(state)`

    Configures the adaptive data rate (ADR) state.

    - Parameter `state` (`bool`): A boolean indicating whether to enable (True) or disable (False) ADR.

    - Returns: True if the command is successfully set, else False.

### `LoRaWAN_X.get_lorawan_node_class()`

    Retrieves the current LoRaWAN node class.

    - Returns: The LoRaWAN node class as a string.

### `LoRaWAN_X.set_lorawan_node_class(node_class)`

    Sets the LoRaWAN node class.

    - Parameter `node_class` (`str`): The node class to set, provided as a string

    - Returns: True if the command is successfully set, else False.

### `LoRaWAN_X.get_duty_cycle_state()`

    Checks whether the ETSI duty cycle is enabled. 1 indicates enabled, 0 indicates disabled.

    - Returns: True if the duty cycle is enabled, otherwise False.

### `LoRaWAN_X.set_duty_cycle_state(state)`

    Sets the ETSI duty cycle state, which can be enabled or disabled depending on the region.

    - Parameter `state` (`bool`): A boolean indicating whether to enable (True) or disable (False) the duty cycle.

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_data_rate()`

    Retrieves the current data rate configuration.

    - Returns: The data rate as an integer.

### `LoRaWAN_X.set_data_rate(rate)`

    Sets the data rate for communication.

    - Parameter `rate` (`int`): The data rate to set, provided as an integer.

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_join_delay_on_window1()`

    Retrieves the delay for the join procedure on window 1.

    - Returns: The join delay for window 1 as an integer.

### `LoRaWAN_X.set_join_delay_on_window1(delay)`

    Sets the join delay for window 1.

    - Parameter `delay` (`int`): The join delay to set for window 1 as an integer.

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_join_delay_on_window2()`

    Retrieves the delay for the join procedure on window 2.

    - Returns: The join delay for window 2 as an integer.

### `LoRaWAN_X.set_join_delay_on_window2(delay)`

    Sets the join delay for window 2.

    - Parameter `delay` (`int`): The join delay to set for window 2 as an integer.

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_public_network_mode()`

    Retrieves the public network mode (enabled or disabled).

    - Returns: True if public network mode is enabled, False otherwise.

### `LoRaWAN_X.set_public_network_mode(mode)`

    Sets the public network mode to enabled or disabled.

    - Parameter `mode` (`bool`): A boolean indicating whether to enable (True) or disable (False) the public network mode.

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_rx_delay_on_window1()`

    Retrieves the receive window 1 delay.

    - Returns: The receive window 1 delay as an integer.

### `LoRaWAN_X.set_rx_delay_on_window1(delay)`

    Sets the receive delay for window 1.

    - Parameter `delay` (`int`): The delay to set for receive window 1 as an integer.

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_rx_delay_on_window2()`

    Retrieves the receive window 2 delay.

    - Returns: The receive window 2 delay as an integer.

### `LoRaWAN_X.set_rx_delay_on_window2(delay)`

    Sets the receive delay for window 2.

    - Parameter `delay` (`int`): The delay to set for receive window 2, with a range of 2 to 16.

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_rx_data_rate_on_windows2()`

    Retrieves the receive data rate for window 2.

    - Returns: The receive data rate for window 2 as an integer.

### `LoRaWAN_X.set_rx_data_rate_on_windows2(rate)`

    Sets the receive data rate for window 2.

    - Parameter `rate` (`int`): The data rate to set for window 2.

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_rx_frequency_on_windows2()`

    Retrieves the receive frequency for window 2, based on regional frequency settings.

    - Returns: The receive frequency for window 2 as an integer.

### `LoRaWAN_X.get_tx_power()`

    Retrieves the current transmit power setting.

    - Returns: The transmit power setting as an integer.

### `LoRaWAN_X.set_tx_power(power)`

    Sets the transmit power.

    - Parameter `power` (`int`): The transmit power to set.

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_network_link_state()`

    Retrieves the network link state.

    - Returns: The network link state as a string.

### `LoRaWAN_X.set_network_link_state(state)`

    - Parameter `state` (`int`): Sets the network link state for the device.
            0 - Disable Link Check
            1 - Execute Link Check once on the next payload uplink
            2 - Automatically execute Link Check after every payload uplink

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_listen_before_talk()`

    Retrieves the Listen Before Talk (LBT) state.

    - Returns: True if LBT is enabled, False if not.

### `LoRaWAN_X.set_listen_before_talk(state)`

    Sets the Listen Before Talk (LBT) state.

    - Parameter `state` (`bool`): The state to set for LBT (True for enabled, False for disabled).

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.set_listen_before_talk_rssi(rssi)`

    Sets the RSSI threshold for Listen Before Talk (LBT).

    - Parameter `rssi` (`int`): The RSSI threshold to set for LBT.

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_listen_before_talk_rssi()`

    Retrieves the RSSI threshold for Listen Before Talk (LBT).

    - Returns: The RSSI threshold as an integer.

### `LoRaWAN_X.get_listen_before_talk_scan_time()`

    Retrieves the scan time for Listen Before Talk (LBT).

    - Returns: The scan time for LBT as an integer.

### `LoRaWAN_X.set_listen_before_talk_scan_time(time)`

    Sets the scan time for Listen Before Talk (LBT).

    - Parameter `time` (`int`): The scan time to set for LBT.

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_time_request()`

    Retrieves the time request state.

    - Returns: The time request state as an integer.

### `LoRaWAN_X.set_time_request(state)`

    Sets the time request state.

    - Parameter `state` (`bool`): The state to set for time request (True to enable, False to disable).

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_location_time()`

    Retrieves the location time in UTC+0.

    - Returns: The location time in UTC+0 as a string.

### `LoRaWAN_X.get_unicast_ping_interval()`

    Retrieves the unicast ping interval in Class B mode.

    - Returns: The unicast ping interval as an integer.

### `LoRaWAN_X.set_unicast_ping_interval(interval)`

    Sets the unicast ping interval for the device.

    - Parameter `interval` (`int`): The interval to set for the unicast ping (0 to 7). 0 means approximately every second during the beacon window, and 7 means every 128 seconds (maximum ping period).

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_beacon_frequency()`

    Retrieves the beacon frequency.

    - Returns: The beacon frequency as an integer.

### `LoRaWAN_X.get_beacon_time()`

    Retrieves the beacon time.

    - Returns: The beacon time as an integer.

### `LoRaWAN_X.get_beacon_gateway_gps()`

    Retrieves the beacon gateway GPS location.

    - Returns: The beacon gateway GPS information as a string.

### `LoRaWAN_X.get_rssi()`

    Retrieves the Received Signal Strength Indicator (RSSI).

    - Returns: The RSSI value as a string.

### `LoRaWAN_X.get_all_rssi()`

    Retrieves the RSSI values from all channels.

    - Returns: The RSSI values for all channels as a string.

### `LoRaWAN_X.get_signal_noise_ratio()`

    Retrieves the Signal-to-Noise Ratio (SNR).

    - Returns: The SNR value as a string.

### `LoRaWAN_X.get_channel_mask()`

    Retrieves the channel mask (only for US915, AU915, CN470).

    - Returns: The channel mask as a string.

### `LoRaWAN_X.set_channel_mask(mask)`

    Sets the channel mask to open or close specific channels (only for US915, AU915, CN470).

    - Parameter `mask` (`str`): The channel mask as a 4-length hexadecimal string.

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_eight_channel_mode_state()`

    Retrieves the state of the eight-channel mode.

    - Returns: The state of the eight-channel mode as a string.

### `LoRaWAN_X.set_eight_channel_mode_state(max_group)`

    Sets the state of the eight-channel mode, with a group number between 1 and 12.

    - Parameter `max_group` (`int`): The maximum group number (1 to 12).

    - Returns: True if the AT command execution is successful, False otherwise.

### `LoRaWAN_X.get_single_channel_mode()`

    Retrieves the single channel mode.

    - Returns: The single channel mode as a string.

### `LoRaWAN_X.set_single_channel_mode()`

    Sets the single channel mode.

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_active_region()`

    Retrieves the active region for the device.

    - Returns: The active region as a string.

### `LoRaWAN_X.set_active_region(region)`

    - Parameter `region` (`int`): Sets the active region for the device.

    - Returns: The result of the AT command execution.

            - `EU433`: 0
            - `CN470`: 1
            - `RU864`: 2
            - `IN865`: 3
            - `EU868`: 4
            - `US915`: 5
            - `AU915,`: 6
            - `KR920,`: 7
            - `AS923-1`: 8
            - `AS923-2`: 9
            - `AS923-3`: 10
            - `AS923-4`: 11
            - `LA915`: 12

### `LoRaWAN_X.add_multicast_group(Class, DevAddr, NwkSKey, AppSKey, Frequency, Datarate, Periodicit)`

    Adds a multicast group to the device.

    - Parameter `Class` (`str`): The class of the multicast group.
    - Parameter `DevAddr`: The device address.
    - Parameter `NwkSKey`: The network session key.
    - Parameter `AppSKey`: The application session key.
    - Parameter `Frequency`: The frequency for the multicast group.
    - Parameter `Datarate`: The datarate for the multicast group.
    - Parameter `Periodicit`: The periodicity for the multicast group.

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.remove_multicast_group(DevAddr)`

    Removes a multicast group by the given device address.

    - Parameter `DevAddr`: The device address of the multicast group to remove.

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_multicast_list()`

    Retrieves the list of multicast groups.

    - Returns: The list of multicast groups as a string.

### `LoRaWAN_X.get_network_mode()`

    Retrieves the current network mode.

    - Returns: The current network mode as an integer

            - `P2P_LORA`: 0
            - `LoRaWAN`: 1
            - `P2P_FSK`: 2

### `LoRaWAN_X.set_network_mode(mode)`

    Sets the network mode for the device.

    - Parameter `mode` (`int`): The mode to set for the get_network_id.

            - `P2P_LORA`: 0
            - `LoRaWAN`: 1
            - `P2P_FSK`: 2

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_p2p_frequency()`

    Retrieves the current P2P frequency.

    - Returns: The current P2P frequency as an integer.

### `LoRaWAN_X.set_p2p_frequency(frequency)`

    Sets the P2P frequency for the device.

    - Parameter `frequency` (`int`): The frequency to set for P2P communication.

        - `Low-frequency` : 150000000-525000000
        - `High-frequency` : 525000000-960000000

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_p2p_spreading_factor()`

    Retrieves the current P2P spreading factor.

    - Returns: The current P2P spreading factor as an integer.

### `LoRaWAN_X.set_p2p_spreading_factor(spreading_factor)`

    Sets the P2P spreading factor.

    - Parameter `spreading_factor` (`int`): The spreading factor to set for P2P communication. The default value is 7, and the range is 5 to 12.

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_p2p_bandwidth()`

    Retrieves the current P2P bandwidth.

    - Returns: The current P2P bandwidth as an integer.

### `LoRaWAN_X.set_p2p_bandwidth(bandwidth)`

    - Parameter `bandwidth` (`int`):

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_p2p_code_rate()`

    Retrieves the current P2P code rate.

    - Returns: The current P2P code rate as an integer.

### `LoRaWAN_X.set_p2p_code_rate(code_rate)`

    Sets the P2P code rate.

    - Parameter `code_rate` (`int`): The code rate to set for P2P communication. Default is 0, range is 0 to 3. 0 = 4/5, 1 = 4/6, 2 = 4/7, 3 = 4/8.

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_p2p_preamble_length()`

    Retrieves the current P2P preamble length.

    - Returns: The current P2P preamble length as an integer.

### `LoRaWAN_X.set_p2p_preamble_length(length)`

    Sets the P2P preamble length.

    - Parameter `length` (`int`): The preamble length to set for P2P communication. Default is 8, range is 5 to 65535.

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_p2p_tx_power()`

    Retrieves the current P2P transmission power.

    - Returns: The current P2P transmission power as an integer.

### `LoRaWAN_X.set_p2p_tx_power(power)`

    Sets the P2P transmission power.

    - Parameter `power` (`int`): The transmission power to set for P2P communication. Default is 14 dBm, range is 5 to 22 dBm.

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_p2p_fsk_bitrate()`

    Retrieves the current P2P FSK bitrate.

    - Returns: The current P2P FSK bitrate as an integer.

### `LoRaWAN_X.set_p2p_fsk_bitrate(bitrate)`

    Sets the P2P FSK bitrate.

    - Parameter `bitrate` (`int`): The bitrate to set for P2P FSK communication. The range is 600 to 300000 b/s.

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.get_p2p_fsk_frequency_deviation()`

    Retrieves the current P2P FSK frequency deviation.

    - Returns: The current P2P FSK frequency deviation as an integer.

### `LoRaWAN_X.set_p2p_fsk_frequency_deviation(deviation)`

    Sets the P2P FSK frequency deviation.

    - Parameter `deviation` (`int`): The frequency deviation to set for P2P FSK communication. The range is 600 to 200000 Hz.

    - Returns: The result of the AT command execution.

### `LoRaWAN_X.send_p2p_data(payload, timeout, to_hex=False)`

    Sends P2P data with a given payload.

    - Parameter `payload` (`str`): The payload to send, 2 to 500 characters in length, must be an even number of characters composed of 0-9, a-f, A-F, representing 1 to 256 hexadecimal values.
    - Parameter `timeout` (`int`): The timeout for the data transmission, default is 1000 ms.
    - Parameter `to_hex` (`bool`): A boolean indicating whether to convert the payload to hexadecimal format.

    - Returns: True if the data was sent successfully ("TXFSK DONE" or "TXP2P DONE"), False otherwise.

### `LoRaWAN_X.get_p2p_channel_activity()`

    Get the current channel activity status in P2P mode.

    - Returns: The channel activity status as an integer (0 or 1).

### `LoRaWAN_X.set_p2p_channel_activity(state)`

    Enable or disable channel activity in P2P mode.

    - Parameter `state` (`bool`): 0 to disable, 1 to enable channel activity.

    - Returns: The response from the command execution.

### `LoRaWAN_X.get_p2p_receive_data(timeout=500, to_str=False)`

    - Parameter `timeout` (`int`): Timeout for listening to P2P LoRa data packets.
                Valid values are 1~65535, with special cases for continuous listening and no timeout.
    - Parameter `to_str` (`bool`): A boolean indicating whether to convert the payload to a string.

    - Returns: A tuple (RSSI, SNR, Payload) if data is received; False if no data is received.

### `LoRaWAN_X.get_p2p_encryption_state()`

    Get the current encryption state in P2P mode.

    - Returns: The encryption state as an integer (0 or 1).

### `LoRaWAN_X.set_p2p_encryption_state(state)`

    Enable or disable encryption in P2P mode.

    - Parameter `state` (`bool`): 0 to disable, 1 to enable encryption.

    - Returns: The response from the command execution.

### `LoRaWAN_X.get_p2p_encryption_key()`

    Get the current encryption key in P2P mode.

    - Returns: The encryption key as a string.

### `LoRaWAN_X.set_p2p_encryption_key(key)`

    Set the encryption key in P2P mode.

    - Parameter `key` (`str`): The encryption key, represented as a 16-character hexadecimal string.

    - Returns: The response from the command execution.

### `LoRaWAN_X.get_p2p_crypt_state()`

    Get the current cryptographic state in P2P mode (not supported on RAK3172).

    - Returns: The cryptographic state as an integer (0 or 1).

### `LoRaWAN_X.set_p2p_crypt_state(state)`

    Enable or disable cryptographic state in P2P mode (not supported on RAK3172).

    - Parameter `state` (`bool`): 0 to disable, 1 to enable cryptographic state.

    - Returns: The response from the command execution.

### `LoRaWAN_X.get_p2p_crypt_key()`

    Get the cryptographic key in P2P mode (not supported on RAK3172).

    - Returns: The cryptographic key as a string.

### `LoRaWAN_X.set_p2p_crypt_key(key)`

    Set the cryptographic key in P2P mode (not supported on RAK3172).

    - Parameter `key`: The cryptographic key, represented as an 8-character hexadecimal string.

    - Returns: The response from the command execution.

### `LoRaWAN_X.get_p2p_encryption_iv()`

    Get the encryption IV in P2P mode.

    - Returns: The encryption IV as a string.

### `LoRaWAN_X.set_p2p_encryption_iv(iv)`

    Set the encryption IV in P2P mode.

    - Parameter `iv` (`str`): The encryption IV, represented as an 8-character hexadecimal string.

    - Returns: The response from the command execution.

### `LoRaWAN_X.get_p2p_parameters()`

    Get the current P2P parameters.

    - Returns: The current P2P parameters as a string.

### `LoRaWAN_X.set_p2p_parameters(frequency, spreading_factor, bandwidth, code_rate, preamble_length, tx_power)`

    Set P2P LoRa parameters, including frequency, spreading factor, bandwidth, code rate, preamble length, and transmit power.

    - Parameter `frequency` (`int`): The frequency to use for communication, range 150000000-960000000.
    - Parameter `spreading_factor` (`int`): The spreading factor, which can be {6, 7, 8, 9, 10, 11, 12}.
    - Parameter `bandwidth` (`int`): The bandwidth, which can be {125, 250, 500}.
    - Parameter `code_rate` (`int`): The code rate, where possible values are {4/5=0, 4/6=1, 4/7=2, 4/8=3}.
    - Parameter `preamble_length` (`int`): The length of the preamble, which can be from 2 to 65535.
    - Parameter `tx_power` (`int`): The transmit power, which can be in the range {5-22}.

    - Returns: The response from the command execution.

### `LoRaWAN_X.get_p2p_iq_inversion()`

    Get the current IQ inversion state in P2P mode.

    - Returns: The IQ inversion state as an integer (0 or 1).

### `LoRaWAN_X.set_p2p_iq_inversion(state)`

    Enable or disable IQ inversion in P2P mode.

    - Parameter `state` (`bool`): 0 to disable, 1 to enable IQ inversion.

    - Returns: The response from the command execution.

### `LoRaWAN_X.get_p2p_sync_word()`

    Get the current sync word in P2P mode.

    - Returns: The sync word as a string.

### `LoRaWAN_X.set_p2p_sync_word(sync_word)`

    Set the sync word in P2P mode.

    - Parameter `sync_word` (`int`): The sync word value, which should be in the range of 0x0000 to 0xFFFF.

    - Returns: The response from the command execution.

### `LoRaWAN_X.get_p2p_symbol_timeout()`

    Get the current symbol timeout in P2P mode.

    - Returns: The symbol timeout as an integer.

### `LoRaWAN_X.set_p2p_symbol_timeout(timeout)`

    Set the symbol timeout in P2P mode.

    - Parameter `timeout` (`bool`): The timeout value, which should be in the range of 0-248.

    - Returns: The response from the command execution.

### `LoRaWAN_X.get_p2p_fix_length_payload_state()`

    Get the current fixed length payload state in P2P mode.

    - Returns: The fixed length payload state as an integer (0 or 1).

### `LoRaWAN_X.set_p2p_fix_length_payload_state(state)`

    Enable or disable fixed length payload in P2P mode.

    - Parameter `state` (`bool`): 0 to disable, 1 to enable fixed length payload.

    - Returns: The response from the command execution.
