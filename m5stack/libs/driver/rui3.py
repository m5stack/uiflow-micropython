# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
import time


class RUI3:
    """
    note:
        en: RUI3 class provides methods to interact with RAK Wireless modules using AT commands. It supports module initialization, configuration, and retrieval of various module parameters.

    details:
        link: https://docs.rakwireless.com/
        image: https://docs.rakwireless.com/assets/images/logo.png
        category:

    example:
        - ../../../examples/module/rui3/rui3_example.py

    m5f2:
        - module/rui3/rui3_example.m5f2
    """

    def __init__(self, id, tx, rx, debug=False):
        """
        note:
            en: Initialize the RUI3 module by setting up UART communication with the specified parameters.

        params:
            id:
                note: The UART ID used for communication.
            tx:
                note: The UART TX pin.
            rx:
                note: The UART RX pin.
            debug:
                note: Enables debug mode to log additional details, default is False.
        """
        self.uart = machine.UART(id, tx=tx, rx=rx, baudrate=115200, bits=8, parity=None, stop=1)
        self.debug = debug
        self.uart.read()
        if self.get_serial_number() is False:
            raise ValueError("The LoRaWAN-X Unit is not responding. Please check the connection.")

    def send_cmd(self, cmd, have_return=False, is_single=False, async_event=False, timeout=100):
        """
        note:
            en: Sends an AT command to the module and optionally reads the response.

        params:
            cmd:
                note: The AT command string to send.
            have_return:
                note: Specifies whether to read a response from the module.
            is_single:
                note: Indicates if the command expects a single-line response.
            async_event:
                note: Specifies whether to handle asynchronous events.
            timeout:
                note: The timeout duration in milliseconds for receiving a response, default is 100ms.

        returns:
            note: The processed response from the module or None if no response is expected.
        """
        self.uart.read()
        self.uart.write(cmd + "\r\n")
        if have_return:
            return self.read_response(cmd.rstrip("?"), is_single, async_event, timeout)

    def read_response(self, cmd, is_single=False, async_event=False, timeout=100):
        """
        note:
            en: Reads and processes the module response to an AT command.

        params:
            cmd:
                note: The AT command sent to the module.
            is_single:
                note: Indicates if a single-line response is expected.
            async_event:
                note: Specifies whether to handle asynchronous events.
            timeout:
                note: The timeout duration in milliseconds for receiving a response.

        returns:
            note:
                - True if the response is valid and matches a single-line expectation.
                - A processed response string when CMD+RESPONSE is received.
                - An event response string if async_event is enabled and an event is detected.
                - False if no valid response is received or an error occurs.
        """
        start_time = time.ticks_ms()
        response = ""
        event_response = None
        ok_received = False

        while time.ticks_diff(time.ticks_ms(), start_time) < timeout:
            line = self.uart.readline()
            if not line:
                continue

            decoded_line = line.decode("utf-8")
            time.sleep_ms(10)
            if decoded_line:
                response += decoded_line

                # 如果接收到 AT_PARAM_ERROR 错误，提前退出
                if "AT_PARAM_ERROR" in response:
                    if self.debug:
                        print("DEBUG: AT_PARAM_ERROR received, returning.")
                    break

                if "OK" in response:
                    ok_received = True
                # 检查事件响应并且+EVT:后跟\r\n，提前退出
                if async_event and "+EVT:" in response:
                    evt_index = response.find("+EVT:")
                    evt_data = response[evt_index:].split(":", 1)
                    if len(evt_data) > 1 and evt_data[1]:
                        event_response = evt_data[1].strip()
                        if line.endswith(b"\r\n"):  # 如果事件响应后紧跟\r\n，立即退出
                            if self.debug:
                                print(f"DEBUG: Raw response:{repr(response)}")
                                print("DEBUG: Event response received with \\r\\n, exiting loop.")
                                print(f"DEBUG: Event response: {repr(event_response)}")
                            return event_response

                if (
                    not async_event
                    and ok_received
                    or ok_received
                    and (not async_event or event_response)
                ):
                    if line.endswith(b"\r\n"):
                        if self.debug:
                            print(
                                "DEBUG: Conditions met and complete data received, exiting loop."
                            )
                        break

        response = response.replace("\r\n", "")

        if self.debug:
            print(f"DEBUG: Final response: {repr(response)}")
        # 用于处理仅返回OK的情况
        if is_single and ok_received:
            return True

            # 用于处理CMD+RESPONSE的情况
        if response.startswith(cmd) and response.endswith("OK"):
            response_parts = response[len(cmd) :].split("=")
            if self.debug:
                print(f"response_parts:{response_parts}")
            return response_parts[0].rstrip("OK")

        if response.find("AT_MODE_NO_SUPPORT") != -1:
            raise ValueError("The current mode does not support this AT command!")
        elif response.find("Current Work Mode: ") != -1:
            return response.split("Current Work Mode: ")[1].strip()

        return False

    def get_commuinication_state(self):
        """
        note:
            en: Checks the communication state by sending the AT command and expecting a response.

        params:
            note:

        returns:
            note: The response from the module indicating the communication state.
        """
        return self.send_cmd("AT", True, True)

    def reset_module(self):
        """
        note:
            en: Resets the module using the ATZ command.

        params:
            note:
        """
        self.send_cmd("ATZ")

    def reset_module_to_default(self):
        """
        note:
            en: Resets the module to its default settings using the ATR command. Waits for the reset process to complete.

        params:
            note:
        """
        self.send_cmd("ATR")
        time.sleep(1.5)

    def get_serial_number(self):
        """
        note:
            en: Retrieves the serial number of the module.

        params:
            note:

        returns:
            note: The serial number as a string.
        """
        return self.send_cmd("AT+SN=?", True)

    def get_fireware_version(self):
        """
        note:
            en: Retrieves the firmware version of the module.

        params:
            note:

        returns:
            note: The firmware version as a string.
        """
        return self.send_cmd("AT+VER=?", True)

    def get_at_version(self):
        """
        note:
            en: Retrieves the AT command version supported by the module.

        params:
            note:

        returns:
            note: The AT command version as a string.
        """
        return self.send_cmd("AT+CLIVER=?", True)

    def get_hardware_version(self):
        """
        note:
            en: Retrieves the hardware version of the module.

        params:
            note:

        returns:
            note: The hardware version as a string.
        """
        return self.send_cmd("AT+HWMODEL=?", True)

    def get_hardware_id(self):
        """
        note:
            en: Retrieves the hardware ID of the module.

        params:
            note:

        returns:
            note: The hardware ID as a string.
        """
        return self.send_cmd("AT+HWID=?", True)

    def get_ble_mac(self):
        """
        note:
            en: Retrieves the Bluetooth MAC address of the module.

        params:
            note:

        returns:
            note: The BLE MAC address as a string.
        """
        return self.send_cmd("AT+BLEMAC=?", True)

    def set_sleep_time(self, time):
        """
        note:
            en: Configures the sleep time for the module. If no time is provided, the module enters sleep mode.

        params:
            time:
                note: The sleep duration in seconds. If None, triggers sleep mode without specifying a duration.

        returns:
            note: True if the command is successfully sent, else False.
        """
        if time:
            return self.send_cmd("AT+SLEEP=" + str(time), True, True, False, 200)
        else:
            self.send_cmd("AT+SLEEP")
            return True

    def get_low_power_mode(self):
        """
        note:
            en: Checks if the module is in low-power mode.

        params:
            note:

        returns:
            note: True if low-power mode is enabled, otherwise False.
        """
        return self.send_cmd("AT+LPM=?", True) == "1"

    def set_low_power_mode(self, mode: bool):
        """
        note:
            en: Sets the module low-power mode.

        params:
            mode:
                note: A boolean value indicating whether to enable (True) or disable (False) low-power mode.

        returns:
            note: True if the command is successfully sent, else False.
        """
        return self.send_cmd("AT+LPM=" + str(int(mode)), True, True)

    def set_baud_rate(self, rate):
        """
        note:
            en: Sets the baud rate for UART communication.

        params:
            rate:
                note: The desired baud rate value.

        returns:
            note: True if the command is successfully sent, else False.
        """
        return self.send_cmd("AT+BAUD=" + str(rate), True, True)

    def get_baud_rate(self):
        """
        note:
            en: Retrieves the current UART baud rate setting.

        params:
            note:

        returns:
            note: The baud rate as an integer.
        """
        return int(self.send_cmd("AT+BAUD=?", True))

    # OTAA Mode
    def get_device_eui(self):
        """
        note:
            en: Retrieves the Device EUI for OTAA (Over-The-Air Activation) mode.

        params:
            note:

        returns:
            note: The Device EUI as a string.
        """
        return self.send_cmd("AT+DEVEUI=?", True)

    def set_device_eui(self, eui: str):
        """
        note:
            en: Configures the Device EUI for OTAA mode.

        params:
            eui:
                note: The Device EUI to set, as a string.

        returns:
            note: True if the command is successfully sent, else False.
        """
        return self.send_cmd("AT+DEVEUI=" + eui, True, True)

    def get_app_eui(self):
        """
        note:
            en: Retrieves the Application EUI for OTAA mode.

        params:
            note:

        returns:
            note: The Application EUI as a string.
        """
        return self.send_cmd("AT+APPEUI=?", True)

    def set_app_eui(self, eui: str):
        """
        note:
            en: Configures the Application EUI for OTAA mode.

        params:
            eui:
                note: The Application EUI to set, as a string.

        returns:
            note: True if the command is successfully sent, else False.
        """
        return self.send_cmd("AT+APPEUI=" + eui, True, True)

    def get_app_key(self):
        """
        note:
            en: Retrieves the Application Key for OTAA mode.

        params:
            note:

        returns:
            note: The Application Key as a string.
        """
        return self.send_cmd("AT+APPKEY=?", True)

    def set_app_key(self, key: str):
        """
        note:
            en: Configures the Application Key for OTAA mode.

        params:
            key:
                note: The Application Key to set, as a string.

        returns:
            note: True if the command is successfully sent, else False.
        """
        return self.send_cmd("AT+APPKEY=" + key, True, True)

    # ABP Mode
    def get_device_address(self):
        """
        note:
            en: Retrieves the device address.

        params:
            note:

        returns:
            note: The device address as a string.
        """
        return self.send_cmd("AT+DEVADDR=?", True)

    def set_device_address(self, address: str):
        """
        note:
            en: Sets the device address.

        params:
            address:
                note: The device address to set, provided as a string.
        """
        return self.send_cmd("AT+DEVADDR=" + address, True, True)

    def get_apps_key(self):
        """
        note:
            en: Retrieves the application session key.

        params:
            note:

        returns:
            note: The application session key as a string.
        """
        return self.send_cmd("AT+APPSKEY=?", True)

    def set_apps_key(self, key: str):
        """
        note:
            en: Sets the application session key. This operation is applicable only in ABP mode.

        params:
            key:
                note: The application session key to set, provided as a string.

        returns:
            note: The result of the AT command execution
        """
        return self.send_cmd("AT+APPSKEY=" + key, True, True)

    def get_networks_key(self):
        """
        note:
            en: Retrieves the network session key.

        params:
            note:

        returns:
            note: The network session key as a string.
        """
        return self.send_cmd("AT+NWKSKEY=?", True)

    def set_networks_key(self, key: str):
        """
        note:
            en: Sets the network session key. This operation is applicable only in ABP mode.

        params:
            key:
                note: The network session key to set, provided as a string.

        returns:
            note: The result of the AT command execution
        """
        return self.send_cmd("AT+NWKSKEY=" + key, True, True)

    def set_network_id(self, id: str):
        """
        note:
            en: Sets the network ID.

        params:
            id:
                note: The network ID to set, provided as a string.

        returns:
            note: The result of the AT command execution
        """
        return self.send_cmd("AT+NETID=" + id, True, True)

    def get_network_id(self):
        """
        note:
            en: Retrieves the network ID.

        params:
            note:

        returns:
            note: The network ID as a string.
        """
        return self.send_cmd("AT+NETID=?", True)

    def get_mc_root_key(self):
        """
        note:
            en: Retrieves the multicast root key.

        params:
            note:

        returns:
            note: The multicast root key as a string.
        """
        return self.send_cmd("AT+MCROOTKEY=?", True)

    def get_confirm_mode(self):
        """
        note:
            en: Retrieves the confirmation mode.

        params:
            note:

        returns:
            note: True if confirmation mode is enabled; otherwise, False.
        """
        return self.send_cmd("AT+CFM=?", True) == "1"

    def set_confirm_mode(self, mode: bool):
        """
        note:
            en: Sets the confirmation mode.

        params:
            mode:
                note: A boolean indicating whether to enable (True) or disable (False) confirmation mode.

        returns:
            note: The result of the AT command execution
        """
        return self.send_cmd("AT+CFM=" + str(int(mode)), True, True)

    def get_confirm_state(self):
        """
        note:
            en: Retrieves the status of the last confirmed uplink.

        params:
            note:

        returns:
            note: True if the last confirmed uplink succeeded; otherwise, False.
        """
        return self.send_cmd("AT+CFS=?", True) == "1"

    def get_join_config(self):
        """
        note:
            en: Retrieves the current join configuration for LoRa.

        params:
            note:

        returns:
            note: A tuple containing state, auto_join, retry_interval, and max_retry as integers, or False if retrieval failed.
        """
        lora_config = self.send_cmd("AT+JOIN=?", True)
        if lora_config:
            return tuple(map(int, lora_config.split(":")[:4]))
        return False

    def set_join_config(
        self,
        state: int,
        auto_join: int,
        retry_interval: int = 8,
        max_retry: int = 0,
        timeout: int = 8000,
    ):
        """
        note:
            en: Configures the join parameters for LoRa. The configuration does not confirm network join success.

        params:
            state:
                note: The join state to configure, as an integer.
            auto_join:
                note: The auto-join flag, as an integer.
            retry_interval:
                note: The interval between join retries, default is 8 seconds.
            max_retry:
                note: The maximum number of retries, default is 0 (no limit).
            timeout:
                note: The timeout duration in milliseconds for the command, default is 8000ms.

        return:
            note: True if the command is successfully set, else False.
        """
        return self.send_cmd(
            f"AT+JOIN={state}:{auto_join}:{retry_interval}:{max_retry}",
            True,
            False,
            True,
            timeout,
        )

    def join_network(self, timeout: int = 8000):
        """
        note:
            en: Joins the LoRa network using predefined join parameters.

        params:
            timeout:
                note: The timeout duration in milliseconds for the join command, default is 8000ms.

        returns:
            note: True if the module successfully joins the network, otherwise False
        """
        buf = self.send_cmd("AT+JOIN=1:0:8:0", True, False, True, timeout)
        if timeout != 0:
            return buf == "JOINED"

    def get_join_mode(self):
        """
        note:
            en: Retrieves the current join mode. 0 indicates ABP mode, 1 indicates OTAA mode.

        params:
            note:

        returns:
            note: The join mode as an integer (0 for ABP, 1 for OTAA).
        """
        return int(self.send_cmd("AT+NJM=?", True))

    def set_join_mode(self, mode: int):
        """
        note:
            en: Sets the join mode for the LoRa module.

        params:
            mode:
                note: The join mode to set, 0 for ABP or 1 for OTAA.

        returns:
            note: True if the command is successfully set, else False.
        """
        return self.send_cmd("AT+NJM=" + str(mode), True, True)

    def get_join_state(self):
        """
        note:
            en: Checks whether the module has successfully joined the network. 1 indicates joined, 0 indicates not joined.

        params:
            note:

        returns:
            note: True if joined, otherwise False.
        """
        return self.send_cmd("AT+NJS=?", True) == "1"

    def get_last_receive(self):
        """
        note:
            en: Retrieves the data from the last received message.

        params:
            note:

        returns:
            note: The received data as a string.
        """
        buf = self.send_cmd("AT+RECV=?", True)
        if isinstance(buf, str):
            if buf.find(":") != -1:
                buf = buf.split(":")
                return (int(buf[0]), bytes.fromhex(buf[1]))
        return False

    def send_data(self, port: int, data: bytes, timeout=600):
        """
        note:
            en: Sends data through a specific port.

        params:
            port:
                note: The port number to send data through.
            data:
                note: The data to send, provided as bytes.
            timeout:
                note: The timeout duration in milliseconds for the send command, default is 600ms.

        returns:
            note: True if the data was sent successfully, otherwise False.
        """
        buf = self.send_cmd(f"AT+SEND={port}:{data}", True, False, True, timeout)
        if timeout != 0:
            return buf in [
                "TX_DONE",
                "SEND_CONFIRMED_OK",
            ]

    def send_long_data(self, port: int, ack: bool, data: bytes, timeout=500):
        """
        note:
            en: Sends long data through a specific port with optional acknowledgment.

        params:
            port:
                note: The port number to send data through.
            ack:
                note: Indicates whether acknowledgment is required (True or False).
            data:
                note: The long data to send, provided as bytes.
            timeout:
                note: The timeout duration in milliseconds for the send command, default is 500ms.

        returns:
            note: True if the data was sent successfully, otherwise False.
        """
        return self.send_cmd(f"AT+SEND={port}:{int(ack)}:{data}", True, False, True, timeout) in [
            "TX_DONE",
            "SEND_CONFIRMED_OK",
        ]

    def set_retry(self, retry: int):
        """
        note:
            en: Configures the retry cycle for transmissions.

        params:
            retry:
                note: The retry cycle value, ranging from 0 to 7, default is 0.

        returns:
            note: True if the command is successfully set, else False.
        """
        return self.send_cmd(f"AT+RETY={retry}", True, True)

    def get_retry(self):
        """
        note:
            en: Retrieves the current retry cycle configuration.

        params:
            note:

        returns:
            note: The retry cycle value as an integer.
        """
        return int(self.send_cmd("AT+RETY=?", True))

    def get_adaptive_rate_state(self):
        """
        note:
            en: Checks whether adaptive data rate (ADR) is enabled. 1 indicates enabled, 0 indicates disabled.

        params:
            note:

        returns:
            note: True if ADR is enabled, otherwise False.
        """
        return self.send_cmd("AT+ADR=?", True) == "1"

    def set_adaptive_rate_state(self, state: bool):
        """
        note:
            en: Configures the adaptive data rate (ADR) state.

        params:
            state:
                note: A boolean indicating whether to enable (True) or disable (False) ADR.

        returns:
            note: True if the command is successfully set, else False.
        """
        return self.send_cmd("AT+ADR=" + str(int(state)), True, True)

    def get_lorawan_node_class(self):
        """
        note:
            en: Retrieves the current LoRaWAN node class.

        params:
            note:

        returns:
            note: The LoRaWAN node class as a string.
        """
        return self.send_cmd("AT+CLASS=?", True)

    def set_lorawan_node_class(self, node_class: str):
        """
        note:
            en: Sets the LoRaWAN node class.

        params:
            node_class:
                note: The node class to set, provided as a string (e.g., "A", "B", or "C").

        returns:
            note: True if the command is successfully set, else False.
        """
        return self.send_cmd("AT+CLASS=" + node_class, True, True)

    def get_duty_cycle_state(self):
        """
        note:
            en: Checks whether the ETSI duty cycle is enabled. 1 indicates enabled, 0 indicates disabled.

        params:
            note:

        returns:
            note: True if the duty cycle is enabled, otherwise False.
        """
        return self.send_cmd("AT+DCS=?", True) == "1"

    def set_duty_cycle_state(self, state: bool):
        """
        note:
            en: Sets the ETSI duty cycle state, which can be enabled or disabled depending on the region.

        params:
            state:
                note: A boolean indicating whether to enable (True) or disable (False) the duty cycle.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd("AT+DCS=" + str(int(state)), True, True)

    def get_data_rate(self):
        """
        note:
            en: Retrieves the current data rate configuration.

        params:
            note:

        returns:
            note: The data rate as an integer.
        """
        return int(self.send_cmd("AT+DR=?", True))

    def set_data_rate(self, rate: int):
        """
        note:
            en: Sets the data rate for communication.

        params:
            rate:
                note: The data rate to set, provided as an integer.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd("AT+DR=" + str(rate), True, True)

    def get_join_delay_on_window1(self):
        """
        note:
            en: Retrieves the delay for the join procedure on window 1.

        params:
            note:

        returns:
            note: The join delay for window 1 as an integer.
        """
        return int(self.send_cmd("AT+JN1DL=?", True))

    def set_join_delay_on_window1(self, delay: int):
        """
        note:
            en: Sets the join delay for window 1.

        params:
            delay:
                note: The join delay to set for window 1 as an integer.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd("AT+JN1DL=" + str(delay), True, True)

    def get_join_delay_on_window2(self):
        """
        note:
            en: Retrieves the delay for the join procedure on window 2.

        params:
            note:

        returns:
            note: The join delay for window 2 as an integer.
        """
        return int(self.send_cmd("AT+JN2DL=?", True))

    def set_join_delay_on_window2(self, delay: int):
        """
        note:
            en: Sets the join delay for window 2.

        params:
            delay:
                note: The join delay to set for window 2 as an integer.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd("AT+JN2DL=" + str(delay), True, True)

    def get_public_network_mode(self):
        """
        note:
            en: Retrieves the public network mode (enabled or disabled).

        params:
            note:

        returns:
            note: True if public network mode is enabled, False otherwise.
        """
        return self.send_cmd("AT+PNM=?", True) == "1"

    def set_public_network_mode(self, mode: bool):
        """
        note:
            en: Sets the public network mode to enabled or disabled.

        params:
            mode:
                note: A boolean indicating whether to enable (True) or disable (False) the public network mode.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd(f"AT+PNM={int(mode)}", True, True)

    def get_rx_delay_on_window1(self):
        """
        note:
            en: Retrieves the receive window 1 delay.

        params:
            note:

        returns:
            note: The receive window 1 delay as an integer.
        """
        return int(self.send_cmd("AT+RX1DL=?", True))

    def set_rx_delay_on_window1(self, delay: int):
        """
        note:
            en: Sets the receive delay for window 1.

        params:
            delay:
                note: The delay to set for receive window 1 as an integer.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd("AT+RX1DL=" + str(delay), True, True)

    def get_rx_delay_on_window2(self):
        """
        note:
            en: Retrieves the receive window 2 delay.

        params:
            note:

        returns:
            note: The receive window 2 delay as an integer.
        """
        return int(self.send_cmd("AT+RX2DL=?", True))

    def set_rx_delay_on_window2(self, delay: int):
        """
        note:
            en: Sets the receive delay for window 2.

        params:
            delay:
                note: The delay to set for receive window 2, with a range of 2 to 16.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd("AT+RX2DL=" + str(delay), True, True)

    def get_rx_data_rate_on_windows2(self):
        """
        note:
            en: Retrieves the receive data rate for window 2.

        params:
            note:

        returns:
            note: The receive data rate for window 2 as an integer.
        """
        return int(self.send_cmd("AT+RX2DR=?", True))

    def set_rx_data_rate_on_windows2(self, rate: int):
        """
        note:
            en: Sets the receive data rate for window 2.

        params:
            rate:
                note: The data rate to set for window 2.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd(f"AT+RX2DR={rate}", True, True)

    def get_rx_frequency_on_windows2(self):
        """
        note:
            en: Retrieves the receive frequency for window 2, based on regional frequency settings.

        params:
            note:

        returns:
            note: The receive frequency for window 2 as an integer.
        """
        return int(self.send_cmd("AT+RX2FQ=?", True))

    def get_tx_power(self):
        """
        note:
            en: Retrieves the current transmit power setting.

        params:
            note:

        returns:
            note: The transmit power setting as an integer.
        """
        return int(self.send_cmd("AT+TXP=?", True))

    def set_tx_power(self, power: int):
        """
        note:
            en: Sets the transmit power.

        params:
            power:
                note: The transmit power to set.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd("AT+TXP=" + str(power), True, True)

    def get_network_link_state(self):
        """
        note:
            en: Retrieves the network link state.

        params:
            note:

        returns:
            note: The network link state as a string.
        """
        return self.send_cmd("AT+LINKCHECK=?", True)

    def set_network_link_state(self, state: int):
        """
        note:
            en: Sets the network link state for the device.

        params:
            state:
                note: The state to set for network link:
                    0 - Disable Link Check
                    1 - Execute Link Check once on the next payload uplink
                    2 - Automatically execute Link Check after every payload uplink

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd("AT+LINKCHECK=" + str(state), True, True)

    def get_listen_before_talk(self):
        """
        note:
            en: Retrieves the Listen Before Talk (LBT) state.

        params:
            note:

        returns:
            note: True if LBT is enabled, False if not.
        """
        return self.send_cmd("AT+LBT=?", True) == "1"

    def set_listen_before_talk(self, state: bool):
        """
        note:
            en: Sets the Listen Before Talk (LBT) state.

        params:
            state:
                note: The state to set for LBT (True for enabled, False for disabled).

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd(f"AT+LBT={int(state)}", True, True)

    def set_listen_before_talk_rssi(self, rssi: int):
        """
        note:
            en: Sets the RSSI threshold for Listen Before Talk (LBT).

        params:
            rssi:
                note: The RSSI threshold to set for LBT.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd("AT+LBTRSSI=" + str(rssi), True, True)

    def get_listen_before_talk_rssi(self):
        """
        note:
            en: Retrieves the RSSI threshold for Listen Before Talk (LBT).

        params:
            note:

        returns:
            note: The RSSI threshold as an integer.
        """
        return int(self.send_cmd("AT+LBTRSSI=?", True))

    def get_listen_before_talk_scan_time(self):
        """
        note:
            en: Retrieves the scan time for Listen Before Talk (LBT).

        params:
            note:

        returns:
            note: The scan time for LBT as an integer.
        """
        return int(self.send_cmd("AT+LBTSCANTIME=?", True))

    def set_listen_before_talk_scan_time(self, time: int):
        """
        note:
            en: Sets the scan time for Listen Before Talk (LBT).

        params:
            time:
                note: The scan time to set for LBT.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd("AT+LBTSCANTIME=" + str(time), True, True)

    def get_time_request(self):
        """
        note:
            en: Retrieves the time request state.

        params:
            note:

        returns:
            note: The time request state as an integer.
        """
        return int(self.send_cmd("AT+TIMEREQ=?", True))

    def set_time_request(self, state: bool):
        """
        note:
            en: Sets the time request state.

        params:
            state:
                note: The state to set for time request (True to enable, False to disable).

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd(f"AT+TIMEREQ={int(state)}", True, True)

    def get_location_time(self):
        """
        note:
            en: Retrieves the location time in UTC+0.

        params:
            note:

        returns:
            note: The location time in UTC+0 as a string.
        """
        return self.send_cmd("AT+LTIME=?", True)

    def get_unicast_ping_interval(self):
        """
        note:
            en: Retrieves the unicast ping interval in Class B mode.

        params:
            note:

        returns:
            note: The unicast ping interval as an integer.
        """
        return int(self.send_cmd("AT+PGSLOT=?", True))

    def set_unicast_ping_interval(self, interval: int):
        """
        note:
            en: Sets the unicast ping interval for the device.

        params:
            interval:
                note: The interval to set for the unicast ping (0 to 7). 0 means approximately every second during the beacon window, and 7 means every 128 seconds (maximum ping period).

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd("AT+PGSLOT=" + str(interval), True, True)

    def get_beacon_frequency(self):
        """
        note:
            en: Retrieves the beacon frequency.

        params:
            note:

        returns:
            note: The beacon frequency as an integer.
        """
        return int(self.send_cmd("AT+BFREQ=?", True))

    def get_beacon_time(self):
        """
        note:
            en: Retrieves the beacon time.

        params:
            note:

        returns:
            note: The beacon time as an integer.
        """
        return int(self.send_cmd("AT+BTIME=?", True))

    def get_beacon_gateway_gps(self):
        """
        note:
            en: Retrieves the beacon gateway GPS location.

        params:
            note:

        returns:
            note: The beacon gateway GPS information as a string.
        """
        return self.send_cmd("AT+BGW=?", True)

    def get_rssi(self):
        """
        note:
            en: Retrieves the Received Signal Strength Indicator (RSSI).

        params:
            note:

        returns:
            note: The RSSI value as a string.
        """
        return self.send_cmd("AT+RSSI=?", True)

    def get_all_rssi(self):
        """
        note:
            en: Retrieves the RSSI values from all channels.

        params:
            note:

        returns:
            note: The RSSI values for all channels as a string.
        """
        return self.send_cmd("AT+ARSSI=?", True)

    def get_signal_noise_ratio(self):
        """
        note:
            en: Retrieves the Signal-to-Noise Ratio (SNR).

        params:
            note:

        returns:
            note: The SNR value as a string.
        """
        return self.send_cmd("AT+SNR=?", True)

    def get_channel_mask(self):
        """
        note:
            en: Retrieves the channel mask (only for US915, AU915, CN470).

        params:
            note:

        returns:
            note: The channel mask as a string.
        """
        return self.send_cmd("AT+MASK=?", True)

    def set_channel_mask(self, mask: str):
        """
        note:
            en: Sets the channel mask to open or close specific channels (only for US915, AU915, CN470).

        params:
            mask:
                note: The channel mask as a 4-length hexadecimal string.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd("AT+MASK=" + mask, True, True)

    def get_eight_channel_mode_state(self):
        """
        note:
            en: Retrieves the state of the eight-channel mode.

        params:
            note:

        returns:
            note: The state of the eight-channel mode as a string.
        """
        return self.send_cmd("AT+CHE=?", True)

    def set_eight_channel_mode_state(self, max_group: int) -> bool:
        """
        note:
            en: Sets the state of the eight-channel mode, with a group number between 1 and 12.

        params:
            max_group:
                note: The maximum group number (1 to 12).

        returns:
            note: True if the AT command execution is successful, False otherwise.
        """
        if not (1 <= max_group <= 12):
            raise ValueError("Channel group must be between 1 and 12.")

        state_str = ":".join(map(str, range(1, max_group + 1)))
        return self.send_cmd(f"AT+CHE={state_str}", True, True)

    def get_single_channel_mode(self):
        """
        note:
            en: Retrieves the single channel mode.

        params:
            note:

        returns:
            note: The single channel mode as a string.
        """
        return self.send_cmd("AT+CHS=?", True)

    def set_single_channel_mode(self):
        """
        note:
            en: Sets the single channel mode.

        params:
            note:

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd("AT+CHS", True, True)

    def get_active_region(self):
        """
        note:
            en: Retrieves the active region for the device.

        params:
            note:

        returns:
            note: The active region as a string.
        """
        return self.send_cmd("AT+BAND=?", True)

    def set_active_region(self, region: int):
        """
        note:
            en: Sets the active region for the device.

        params:
            region:
                note: The region to set for the device (0-12):
                    0 = EU433, 1 = CN470, 2 = RU864, 3 = IN865, 4 = EU868, 5 = US915,
                    6 = AU915, 7 = KR920, 8 = AS923-1, 9 = AS923-2, 10 = AS923-3,
                    11 = AS923-4, 12 = LA915.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd("AT+BAND=" + str(region), True, True)

    def add_multicast_group(
        self, Class: str, DevAddr, NwkSKey, AppSKey, Frequency, Datarate, Periodicit
    ):
        """
        note:
            en: Adds a multicast group to the device.

        params:
            Class:
                note: The class of the multicast group.
            DevAddr:
                note: The device address.
            NwkSKey:
                note: The network session key.
            AppSKey:
                note: The application session key.
            Frequency:
                note: The frequency for the multicast group.
            Datarate:
                note: The datarate for the multicast group.
            Periodicit:
                note: The periodicity for the multicast group.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd(
            f"AT+ADDMULC={Class}:{DevAddr}:{NwkSKey}:{AppSKey}:{Frequency}:{Datarate}:{Periodicit}",
            True,
            True,
        )

    def remove_multicast_group(self, DevAddr):
        """
        note:
            en: Removes a multicast group by the given device address.

        params:
            DevAddr:
                note: The device address of the multicast group to remove.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd(f"AT+RMVMULC={DevAddr}", True, True)

    def get_multicast_list(self):
        """
        note:
            en: Retrieves the list of multicast groups.

        params:
            note:

        returns:
            note: The list of multicast groups as a string.
        """
        return self.send_cmd("AT+LSTMULC=?", True)

    def get_network_mode(self):
        """
        note:
            en: Retrieves the current network mode.

        params:
            note:

        returns:
            note: The current network mode as an integer: 0 = P2P_LORA, 1 = LoRaWAN, 2 = P2P_FSK.
        """
        return self.send_cmd("AT+NWM=?", True)

    def set_network_mode(self, mode: int):
        """
        note:
            en: Sets the network mode for the device.

        params:
            mode:
                note: The mode to set for the network: 0 = P2P_LORA, 1 = LoRaWAN, 2 = P2P_FSK.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd("AT+NWM=" + str(mode), True, False, True, 500)

    def get_p2p_frequency(self):
        """
        note:
            en: Retrieves the current P2P frequency.

        params:
            note:

        returns:
            note: The current P2P frequency as an integer.
        """
        return int(self.send_cmd("AT+PFREQ=?", True))

    def set_p2p_frequency(self, frequency: int):
        """
        note:
            en: Sets the P2P frequency for the device.

        params:
            frequency:
                note: The frequency to set for P2P communication. Low-frequency range: 150000000-525000000, High-frequency range: 525000000-960000000.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd("AT+PFREQ=" + str(frequency), True, True)

    def get_p2p_spreading_factor(self):
        """
        note:
            en: Retrieves the current P2P spreading factor.

        params:
            note:

        returns:
            note: The current P2P spreading factor as an integer.
        """
        return int(self.send_cmd("AT+PSF=?", True))

    def set_p2p_spreading_factor(self, spreading_factor: int):
        """
        note:
            en: Sets the P2P spreading factor.

        params:
            spreading_factor:
                note: The spreading factor to set for P2P communication. The default value is 7, and the range is 5 to 12.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd("AT+PSF=" + str(spreading_factor), True, True)

    def get_p2p_bandwidth(self):
        """
        note:
            en: Retrieves the current P2P bandwidth.

        params:
            note:

        returns:
            note: The current P2P bandwidth as an integer.
        """
        return int(self.send_cmd("AT+PBW=?", True))

    def set_p2p_bandwidth(self, bandwidth: int):
        """
        note:
            en: Sets the P2P bandwidth.

        params:
            bandwidth:
                note: The bandwidth to set for P2P communication. Default is 0.
                    For LoRa: 0 = 125, 1 = 250, 2 = 500, 3 = 7.8, 4 = 10.4, 5 = 15.63, 6 = 20.83, 7 = 31.25, 8 = 41.67, 9 = 62.5.
                    For FSK: 4800-467000.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd("AT+PBW=" + str(bandwidth), True, True)

    def get_p2p_code_rate(self):
        """
        note:
            en: Retrieves the current P2P code rate.

        params:
            note:

        returns:
            note: The current P2P code rate as an integer.
        """
        return int(self.send_cmd("AT+PCR=?", True))

    def set_p2p_code_rate(self, code_rate: int):
        """
        note:
            en: Sets the P2P code rate.

        params:
            code_rate:
                note: The code rate to set for P2P communication. Default is 0, range is 0 to 3, 0 = 4/5, 1 = 4/6, 2 = 4/7, 3 = 4/8.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd("AT+PCR=" + str(code_rate), True, True)

    def get_p2p_preamble_length(self):
        """
        note:
            en: Retrieves the current P2P preamble length.

        params:
            note:

        returns:
            note: The current P2P preamble length as an integer.
        """
        return int(self.send_cmd("AT+PPL=?", True))

    def set_p2p_preamble_length(self, length: int):
        """
        note:
            en: Sets the P2P preamble length.

        params:
            length:
                note: The preamble length to set for P2P communication. Default is 8, range is 5 to 65535.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd("AT+PPL=" + str(length), True, True)

    def get_p2p_tx_power(self):
        """
        note:
            en: Retrieves the current P2P transmission power.

        params:
            note:

        returns:
            note: The current P2P transmission power as an integer.
        """
        return int(self.send_cmd("AT+PTP=?", True))

    def set_p2p_tx_power(self, power: int):
        """
        note:
            en: Sets the P2P transmission power.

        params:
            power:
                note: The transmission power to set for P2P communication. Default is 14 dBm, range is 5 to 22 dBm.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd("AT+PTP=" + str(power), True, True)

    def get_p2p_fsk_bitrate(self):
        """
        note:
            en: Retrieves the current P2P FSK bitrate.

        params:
            note:

        returns:
            note: The current P2P FSK bitrate as an integer.
        """
        return int(self.send_cmd("AT+PBR=?", True))

    def set_p2p_fsk_bitrate(self, bitrate: int):
        """
        note:
            en: Sets the P2P FSK bitrate.

        params:
            bitrate:
                note: The bitrate to set for P2P FSK communication. The range is 600 to 300000 b/s.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd("AT+PBR=" + str(bitrate), True, True)

    def get_p2p_fsk_frequency_deviation(self):
        """
        note:
            en: Retrieves the current P2P FSK frequency deviation.

        params:
            note:

        returns:
            note: The current P2P FSK frequency deviation as an integer.
        """
        return int(self.send_cmd("AT+PFDEV=?", True))

    def set_p2p_fsk_frequency_deviation(self, deviation: int):
        """
        note:
            en: Sets the P2P FSK frequency deviation.

        params:
            deviation:
                note: The frequency deviation to set for P2P FSK communication. The range is 600 to 200000 Hz.

        returns:
            note: The result of the AT command execution.
        """
        return self.send_cmd("AT+PFDEV=" + str(deviation), True, True)

    def send_p2p_data(self, payload: str, timeout=1000, to_hex=False):
        """
        note:
            en: Sends P2P data with a given payload.

        params:
            payload:
                note: The payload to send, 2 to 500 characters in length, must be an even number of characters composed of 0-9, a-f, A-F, representing 1 to 256 hexadecimal values.
            timeout:
                note: The timeout for the data transmission, default is 1000 ms.
            to_hex:
                note: A boolean indicating whether to convert the payload to hexadecimal format.

        returns:
            note: True if the data was sent successfully ("TXFSK DONE" or "TXP2P DONE"), False otherwise.
        """
        if to_hex:
            payload = payload.encode("utf-8").hex()
        buf = self.send_cmd(f"AT+PSEND={payload}", True, False, True, timeout)
        if timeout != 0:
            return buf in [
                "TXFSK DONE",
                "TXP2P DONE",
            ]

    def get_p2p_channel_activity(self):
        """
        note:
            en: Get the current channel activity status in P2P mode.

        params:
            note:

        returns:
            note: The channel activity status as an integer (0 or 1).
        """
        return int(self.send_cmd("AT+CAD=?", True))

    def set_p2p_channel_activity(self, state: bool):
        """
        note:
            en: Enable or disable channel activity in P2P mode.

        params:
            state:
                note: 0 to disable, 1 to enable channel activity.

        returns:
            note: The response from the command execution.
        """
        return self.send_cmd(f"AT+CAD={int(state)}", True, True)

    def get_p2p_receive_data(self, timeout=500, to_str=False):
        """
        note:
            en: Receive data in P2P mode, including RSSI, SNR, and payload.

        params:
            timeout:
                note: Timeout for listening to P2P LoRa data packets.
                Valid values are 1~65535, with special cases for continuous listening and no timeout.
            to_str:
                note: A boolean indicating whether to convert the payload to a string.

        returns:
            note: A tuple (RSSI, SNR, Payload) if data is received; False if no data is received.
        """
        self.send_cmd("AT+PRECV=0", True, False, True, 0)
        buf = self.send_cmd(f"AT+PRECV={timeout}", True, False, True, timeout)
        if isinstance(buf, str):
            if buf.find("RXP2P:") != -1:
                buf = buf.split(":")
                return (
                    int(buf[1]),
                    int(buf[2]),
                    bytes.fromhex(buf[3]).decode() if to_str else buf[3],
                )
        return False

    def get_p2p_encryption_state(self):
        """
        note:
            en: Get the current encryption state in P2P mode.

        params:
            note:

        returns:
            note: The encryption state as an integer (0 or 1).
        """
        return int(self.send_cmd("AT+ENCRY=?", True))

    def set_p2p_encryption_state(self, state: bool):
        """
        note:
            en: Enable or disable encryption in P2P mode.

        params:
            state:
                note: 0 to disable, 1 to enable encryption.

        returns:
            note: The response from the command execution.
        """
        return self.send_cmd(f"AT+ENCRY={int(state)}", True, True)

    def get_p2p_encryption_key(self):
        """
        note:
            en: Get the current encryption key in P2P mode.

        params:
            note:

        returns:
            note: The encryption key as a string.
        """
        return self.send_cmd("AT+ENCKEY=?", True)

    def set_p2p_encryption_key(self, key: str):
        """
        note:
            en: Set the encryption key in P2P mode.

        params:
            key:
                note: The encryption key, represented as a 16-character hexadecimal string.

        returns:
            note: The response from the command execution.
        """
        return self.send_cmd(f"AT+ENCKEY={key}", True, True)

    def get_p2p_crypt_state(self):
        """
        note:
            en: Get the current cryptographic state in P2P mode (not supported on RAK3172).

        params:
            note:

        returns:
            note: The cryptographic state as an integer (0 or 1).
        """
        # RAK3172 not support
        return int(self.send_cmd("AT+PCRYPT=?", True))

    def set_p2p_crypt_state(self, state: bool):
        """
        note:
            en: Enable or disable cryptographic state in P2P mode (not supported on RAK3172).

        params:
            state:
                note: 0 to disable, 1 to enable cryptographic state.

        returns:
            note: The response from the command execution.
        """
        # RAK3172 not support
        return self.send_cmd(f"AT+PCRYPT={int(state)}", True, True)

    def get_p2p_crypt_key(self):
        """
        note:
            en: Get the cryptographic key in P2P mode (not supported on RAK3172).

        params:
            note:

        returns:
            note: The cryptographic key as a string.
        """
        # RAK3172 not support
        return self.send_cmd("AT+PKEY=?", True)

    def set_p2p_crypt_key(self, key):
        """
        note:
            en: Set the cryptographic key in P2P mode (not supported on RAK3172).

        params:
            key:
                note: The cryptographic key, represented as an 8-character hexadecimal string.

        returns:
            note: The response from the command execution.
        """
        # RAK3172 not support
        # key:8 hex string
        return self.send_cmd(f"AT+PKEY={key}", True, True)

    def get_p2p_encryption_iv(self):
        """
        note:
            en: Get the encryption IV in P2P mode.

        params:
            note:

        returns:
            note: The encryption IV as a string.
        """
        return self.send_cmd("AT+CRYPIV=?", True)

    def set_p2p_encryption_iv(self, iv: str):
        """
        note:
            en: Set the encryption IV in P2P mode.

        params:
            iv:
                note: The encryption IV, represented as an 8-character hexadecimal string.

        returns:
            note: The response from the command execution.
        """
        return self.send_cmd(f"AT+CRYPIV={iv}", True, True)

    def get_p2p_parameters(self):
        """
        note:
            en: Get the current P2P parameters.

        params:
            note:

        returns:
            note: The current P2P parameters as a string.
        """
        return self.send_cmd("AT+P2P=?", True)

    def set_p2p_parameters(
        self,
        frequency: int = 868000000,
        spreading_factor: int = 7,
        bandwidth: int = 125,
        code_rate: int = 0,
        preamble_length: int = 8,
        tx_power: int = 14,
    ):
        """
        note:
            en: Set P2P LoRa parameters, including frequency, spreading factor, bandwidth, code rate, preamble length, and transmit power.

        params:
            frequency:
                note: The frequency to use for communication, range 150000000-960000000.
            spreading_factor:
                note: The spreading factor, which can be {6, 7, 8, 9, 10, 11, 12}.
            bandwidth:
                note: The bandwidth, which can be {125, 250, 500}.
            code_rate:
                note: The code rate, where possible values are {4/5=0, 4/6=1, 4/7=2, 4/8=3}.
            preamble_length:
                note: The length of the preamble, which can be from 2 to 65535.
            tx_power:
                note: The transmit power, which can be in the range {5-22}.

        returns:
            note: The response from the command execution.
        """
        return self.send_cmd(
            f"AT+P2P={frequency}:{spreading_factor}:{bandwidth}:{code_rate}:{preamble_length}:{tx_power}",
            True,
            True,
        )

    def get_p2p_iq_inversion(self):
        """
        note:
            en: Get the current IQ inversion state in P2P mode.

        params:
            note:

        returns:
            note: The IQ inversion state as an integer (0 or 1).
        """
        return int(self.send_cmd("AT+IQINVER=?", True))

    def set_p2p_iq_inversion(self, state: bool):
        """
        note:
            en: Enable or disable IQ inversion in P2P mode.

        params:
            state:
                note: 0 to disable, 1 to enable IQ inversion.

        returns:
            note: The response from the command execution.
        """
        return self.send_cmd(f"AT+IQINVER={int(state)}", True, True)

    def get_p2p_sync_word(self):
        """
        note:
            en: Get the current sync word in P2P mode.

        params:
            note:

        returns:
            note: The sync word as a string.
        """
        return self.send_cmd("AT+SYNCWORD=?", True)

    def set_p2p_sync_word(self, sync_word: int):
        """
        note:
            en: Set the sync word in P2P mode.

        params:
            sync_word:
                note: The sync word value, which should be in the range of 0x0000 to 0xFFFF.

        returns:
            note: The response from the command execution.
        """
        sync_word_str = f"{sync_word:04X}"
        return self.send_cmd(f"AT+SYNCWORD={sync_word_str}", True, True)

    def get_p2p_symbol_timeout(self):
        """
        note:
            en: Get the current symbol timeout in P2P mode.

        params:
            note:

        returns:
            note: The symbol timeout as an integer.
        """
        return int(self.send_cmd("AT+SYMBOLTIMEOUT=?", True))

    def set_p2p_symbol_timeout(self, timeout):
        """
        note:
            en: Set the symbol timeout in P2P mode.

        params:
            timeout:
                note: The timeout value, which should be in the range of 0-248.

        returns:
            note: The response from the command execution.
        """
        return self.send_cmd(f"AT+SYMBOLTIMEOUT={int(timeout)}", True, True)

    def get_p2p_fix_length_payload_state(self):
        """
        note:
            en: Get the current fixed length payload state in P2P mode.

        params:
            note:

        returns:
            note: The fixed length payload state as an integer (0 or 1).
        """
        return int(self.send_cmd("AT+FIXLENGTHPAYLOAD=?", True))

    def set_p2p_fix_length_payload_state(self, state: bool):
        """
        note:
            en: Enable or disable fixed length payload in P2P mode.

        params:
            state:
                note: 0 to disable, 1 to enable fixed length payload.

        returns:
            note: The response from the command execution.
        """
        return self.send_cmd(f"AT+FIXLENGTHPAYLOAD={int(state)}", True, True)


# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import sys

if sys.platform != "esp32":
    from typing import Literal


class LoRaWANUnit_RUI3(RUI3):
    def __init__(self, id: Literal[0, 1, 2] = 1, port: list | tuple = None, debug=False):
        super().__init__(id, port[1], port[0], debug)

    def set_abp_config(self, dev_addr: str, apps_key: str, nwks_key: str):
        """
        note:
            en: Configure the device for ABP (Activation By Personalization) mode using the provided device address, application session key, and network session key.

        params:
            dev_addr:
                note: The device address for ABP configuration.
            apps_key:
                note: The application session key for encryption.
            nwks_key:
                note: The network session key for communication.
        """
        self.set_join_mode(0)
        self.set_device_address(dev_addr)
        self.set_apps_key(apps_key)
        self.set_networks_key(nwks_key)

    def get_abp_config(self) -> tuple[str | bool | None, str | bool | None, str | bool | None]:
        """
        note:
            en: Retrieve the current ABP configuration, including the device address, application session key, and network session key.

        params:
            note:

        returns:
            note: A tuple containing the device address, application session key, and network session key. Returns None or False for missing or invalid configurations.
        """
        return (self.get_device_address(), self.get_apps_key(), self.get_networks_key())

    def set_otaa_config(self, device_eui, app_eui, app_key):
        """
        note:
            en: Configure the device for OTAA (Over-The-Air Activation) mode using the provided device EUI, application EUI, and application key.

        params:
            device_eui:
                note: The device EUI for OTAA configuration.
            app_eui:
                note: The application EUI for OTAA configuration.
            app_key:
                note: The application key for encryption.
        """
        self.set_join_mode(1)
        self.set_device_eui(device_eui)
        self.set_app_eui(app_eui)
        self.set_app_key(app_key)

    def get_otaa_config(self):
        """
        note:
            en: Retrieve the current OTAA configuration, including the device EUI, application key, and application EUI.

        params:
            note:

        returns:
            note: A tuple containing the device EUI, application key, and application EUI.
        """
        return (self.get_device_eui(), self.get_app_key(), self.get_app_eui())
