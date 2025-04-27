# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
import _thread
import time


class RUI3:
    _instance = None
    _recv_thread_running = False

    def __init__(self, id, tx, rx, debug=False):
        if RUI3._instance is not None:
            try:
                RUI3._instance.close()
            except Exception as e:
                print("clean rui3 instance error:", e)

        self.uart = machine.UART(id, tx=tx, rx=rx, baudrate=115200, bits=8, parity=None, stop=1)
        self.debug = debug
        self.lock = _thread.allocate_lock()
        self.buffer = []
        self.running = True
        self.uart.read()

        RUI3._instance = self
        RUI3._recv_thread_running = True

        _thread.start_new_thread(self._recv_loop, ())

        if self.get_serial_number() is False:
            self.close()
            raise ValueError("The LoRaWAN-X Unit is not responding. Please check the connection.")

    def close(self):
        self.running = False
        RUI3._recv_thread_running = False
        time.sleep_ms(100)
        try:
            self.uart.deinit()
        except:
            pass
        RUI3._instance = None
        if self.debug:
            print("RUI3 已关闭。")

    def _recv_loop(self):
        while self.running:
            if not self.lock.locked():
                self.lock.acquire()
                try:
                    line = self.uart.readline()
                    if line:
                        if self.debug:
                            print(f"DEBUG: RAW DATA: {line}")
                        if line.startswith(b"+EVT:RX_"):
                            parts = line.decode("utf-8").strip().split(":")
                            decoded = (int(parts[-2]), parts[-1])
                            self.buffer.append(decoded)
                finally:
                    self.lock.release()
            time.sleep_ms(100)

    def get_received_data(self):
        """Retrieve the data from the last received message.

        :returns: A tuple containing the port number (int) and the received data (bytes), or False if no data was received.
        :rtype: tuple[int, bytes] | bool

        MicroPython Code Block:

            .. code-block:: python

                data = lorawan_rui3.get_received_data()
                if data:
                    print(f"Received data: {data}")
                else:
                    print("No data received.")
        """
        data = self.buffer[:]
        self.buffer.clear()
        return data

    def get_received_data_string(self) -> str:
        """Retrieve the received data as a string.

        :returns: The received data as a string, or an empty string if no data was received.
        :rtype: str

        MicroPython Code Block:

            .. code-block:: python

                data = lorawan_rui3.get_received_data_string()
                if data:
                    print(f"Received data: {data}")
                else:
                    print("No data received.")
        """
        return ",".join([str(item[1]) for item in self.get_received_data()])

    def get_received_data_count(self):
        """Retrieve the number of received data.

        :returns: The number of received data.
        :rtype: int

        MicroPython Code Block:

            .. code-block:: python

                count = lorawan_rui3.get_received_data_count()
                print(f"Received data count: {count}")
        """
        return len(self.buffer)

    def send_cmd(
        self,
        cmd: str,
        have_return: bool = False,
        is_single: bool = False,
        async_event: bool = False,
        timeout: int = 100,
    ) -> str | bool:
        self.lock.acquire()
        try:
            self.uart.read()
            self.uart.write(cmd + "\r\n")
            if have_return:
                return self.read_response(cmd.rstrip("?"), is_single, async_event, timeout)
        finally:
            self.lock.release()

    def read_response(self, cmd, is_single=False, async_event=False, timeout=100):
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
        return self.send_cmd("AT", True, True)

    def reset_module(self):
        self.send_cmd("ATZ")

    def reset_module_to_default(self):
        """Reset the module to its factory default settings.

        MicroPython Code Block:

            .. code-block:: python

                rui3.reset_module_to_default()
        """
        self.send_cmd("ATR")
        time.sleep(1.5)

    def get_serial_number(self) -> str | bool:
        return self.send_cmd("AT+SN=?", True)

    def get_fireware_version(self):
        return self.send_cmd("AT+VER=?", True)

    def get_at_version(self):
        return self.send_cmd("AT+CLIVER=?", True)

    def get_hardware_version(self):
        return self.send_cmd("AT+HWMODEL=?", True)

    def get_hardware_id(self):
        return self.send_cmd("AT+HWID=?", True)

    def get_ble_mac(self):
        return self.send_cmd("AT+BLEMAC=?", True)

    def set_sleep_time(self, time):
        if time:
            return self.send_cmd("AT+SLEEP=" + str(time), True, True, False, 200)
        else:
            self.send_cmd("AT+SLEEP")
            return True

    def get_low_power_mode(self):
        return self.send_cmd("AT+LPM=?", True) == "1"

    def set_low_power_mode(self, mode: bool):
        return self.send_cmd("AT+LPM=" + str(int(mode)), True, True)

    def set_baud_rate(self, rate):
        return self.send_cmd("AT+BAUD=" + str(rate), True, True)

    def get_baud_rate(self):
        return int(self.send_cmd("AT+BAUD=?", True))

    # OTAA Mode
    def get_device_eui(self):
        """Get the device EUI.

        :returns: The device EUI.
        :rtype: str

        MicroPython Code Block:

            .. code-block:: python

                lorawan_rui3.get_device_eui()

        """
        return self.send_cmd("AT+DEVEUI=?", True)

    def set_device_eui(self, eui: str):
        return self.send_cmd("AT+DEVEUI=" + eui, True, True)

    def get_app_eui(self):
        return self.send_cmd("AT+APPEUI=?", True)

    def set_app_eui(self, eui: str):
        return self.send_cmd("AT+APPEUI=" + eui, True, True)

    def get_app_key(self):
        return self.send_cmd("AT+APPKEY=?", True)

    def set_app_key(self, key: str):
        return self.send_cmd("AT+APPKEY=" + key, True, True)

    # ABP Mode
    def get_device_address(self):
        return self.send_cmd("AT+DEVADDR=?", True)

    def set_device_address(self, address: str):
        return self.send_cmd("AT+DEVADDR=" + address, True, True)

    def get_apps_key(self):
        return self.send_cmd("AT+APPSKEY=?", True)

    def set_apps_key(self, key: str):
        return self.send_cmd("AT+APPSKEY=" + key, True, True)

    def get_networks_key(self):
        return self.send_cmd("AT+NWKSKEY=?", True)

    def set_networks_key(self, key: str):
        return self.send_cmd("AT+NWKSKEY=" + key, True, True)

    def set_network_id(self, id: str):
        return self.send_cmd("AT+NETID=" + id, True, True)

    def get_network_id(self):
        return self.send_cmd("AT+NETID=?", True)

    def get_mc_root_key(self):
        return self.send_cmd("AT+MCROOTKEY=?", True)

    def get_confirm_mode(self):
        return self.send_cmd("AT+CFM=?", True) == "1"

    def set_confirm_mode(self, mode: bool):
        return self.send_cmd("AT+CFM=" + str(int(mode)), True, True)

    def get_confirm_state(self):
        return self.send_cmd("AT+CFS=?", True) == "1"

    def get_join_config(self):
        lora_config = self.send_cmd("AT+JOIN=?", True)
        if lora_config:
            return tuple(map(int, lora_config.split(":")[:4]))
        return False

    def set_join_config(
        self,
        state: int,
        auto_join: int,
        reattempt_interval: int = 8,
        max_attempts: int = 0,
        timeout: int = 8000,
    ):
        """Configure the join parameters for LoRaWAN.

        The configuration does not confirm network join success.

        :param int state: The join state to configure, as an integer.
        :param int auto_join: The auto-join flag, as an integer.
        :param int reattempt_interval: The interval between join retries, in seconds. Default is 8.
        :param int max_attempts: The maximum number of retries. Default is 0 (no limit).
        :param int timeout: The timeout duration in milliseconds for the command. Default is 8000ms.

        :returns: True if the command is successfully set, else False.
        :rtype: bool

        MicroPython Code Block:

            .. code-block:: python

                lorawan_rui3.set_join_config(
                    state=1,
                    auto_join=1,
                    reattempt_interval=10,
                    max_attempts=5,
                    timeout=10000
                )
        """
        return self.send_cmd(
            f"AT+JOIN={state}:{auto_join}:{reattempt_interval}:{max_attempts}",
            True,
            False,
            True,
            timeout,
        )

    def join_network(self, timeout: int = 8000):
        """Join the LoRa network using predefined join parameters.

        :param int timeout: The timeout duration in milliseconds for the join command. Default is 8000ms.

        :returns: True if the command is successfully set, else False.
        :rtype: bool

            |join_network_return.png|


        MicroPython Code Block:

            .. code-block:: python

                if lorawan_rui3.join_network(timeout=10000):
                    print("Network joined successfully!")
                else:
                    print("Failed to join network.")
        """
        buf = self.send_cmd("AT+JOIN=1:0:8:0", True, False, True, timeout)
        if timeout != 0:
            return buf == "JOINED"

    def get_join_mode(self):
        return int(self.send_cmd("AT+NJM=?", True))

    def set_join_mode(self, mode: int):
        """Set the join mode for the LoRa module.

        :param int mode: The join mode to set, 0 for ABP or 1 for OTAA.

        :returns: True if the command is successfully set, else False.
        :rtype: bool

        MicroPython Code Block:

            .. code-block:: python

                lorawan_rui3.set_join_mode(1)  # Set to OTAA mode

        """
        return self.send_cmd("AT+NJM=" + str(mode), True, True)

    def get_join_state(self):
        """Check whether the module has successfully joined the network.

        :returns: True if joined, otherwise False.
        :rtype: bool

        MicroPython Code Block:

            .. code-block:: python

                if lorawan_rui3.get_join_state():
                    print("Module is joined to the network.")
                else:
                    print("Module is not joined to the network.")
        """
        return self.send_cmd("AT+NJS=?", True) == "1"

    def get_last_receive(self):
        """Retrieve the data from the last received message.

        :returns: A tuple containing the port number (int) and the received data (bytes), or False if no data was received.
        :rtype: tuple[int, bytes] | bool

        MicroPython Code Block:

            .. code-block:: python

                last_data = lorawan_rui3.get_last_receive()
                if last_data:
                    port, data = last_data
                    print(f"Received data on port {port}: {data}")
                else:
                    print("No data received.")
        """
        buf = self.send_cmd("AT+RECV=?", True)
        if isinstance(buf, str):
            if buf.find(":") != -1:
                buf = buf.split(":")
                return (int(buf[0]), buf[1])
        return False

    def send_data(self, port: int, data: bytes | str, timeout: int = 600):
        """Send data through a specific port.

        :param int port: The port number to send data through.
        :param data: The data to send, provided as bytes or string(if data is bytes, it will be converted to string).
        :type data: bytes | str
        :param int timeout: The timeout duration in milliseconds for the send command. Default is 600ms.

        :returns: True if the data was sent successfully, otherwise False.
        :rtype: bool

            |send_data_return.png|

        MicroPython Code Block:

            .. code-block:: python

                success = lorawan_rui3.send_data(port=1, data=b"HelloLoRa", timeout=800)
                if success:
                    print("Data sent successfully!")
                else:
                    print("Failed to send data.")

        """
        if isinstance(data, str):
            pass
        elif isinstance(data, bytes):
            data = data.decode()
        else:
            raise ValueError("Invalid data type.")
        print(f"AT+SEND={port}:{data}")
        buf = self.send_cmd(f"AT+SEND={port}:{data}", True, False, True, timeout)
        if timeout != 0:
            return buf in [
                "TX_DONE",
                "SEND_CONFIRMED_OK",
            ]

    def send_long_data(self, port: int, ack: bool, data: bytes, timeout: int = 500):
        return self.send_cmd(f"AT+SEND={port}:{int(ack)}:{data}", True, False, True, timeout) in [
            "TX_DONE",
            "SEND_CONFIRMED_OK",
        ]

    def set_retry(self, retry: int):
        return self.send_cmd(f"AT+RETY={retry}", True, True)

    def get_retry(self):
        return int(self.send_cmd("AT+RETY=?", True))

    def get_adaptive_rate_state(self):
        return self.send_cmd("AT+ADR=?", True) == "1"

    def set_adaptive_rate_state(self, state: bool):
        return self.send_cmd("AT+ADR=" + str(int(state)), True, True)

    def get_lorawan_node_class(self):
        return self.send_cmd("AT+CLASS=?", True)

    def set_lorawan_node_class(self, node_class: str):
        return self.send_cmd("AT+CLASS=" + node_class, True, True)

    def get_duty_cycle_state(self):
        return self.send_cmd("AT+DCS=?", True) == "1"

    def set_duty_cycle_state(self, state: bool):
        return self.send_cmd("AT+DCS=" + str(int(state)), True, True)

    def get_data_rate(self):
        return int(self.send_cmd("AT+DR=?", True))

    def set_data_rate(self, rate: int):
        return self.send_cmd("AT+DR=" + str(rate), True, True)

    def get_join_delay_on_window1(self):
        return int(self.send_cmd("AT+JN1DL=?", True))

    def set_join_delay_on_window1(self, delay: int):
        return self.send_cmd("AT+JN1DL=" + str(delay), True, True)

    def get_join_delay_on_window2(self):
        return int(self.send_cmd("AT+JN2DL=?", True))

    def set_join_delay_on_window2(self, delay: int):
        return self.send_cmd("AT+JN2DL=" + str(delay), True, True)

    def get_public_network_mode(self):
        return self.send_cmd("AT+PNM=?", True) == "1"

    def set_public_network_mode(self, mode: bool):
        return self.send_cmd(f"AT+PNM={int(mode)}", True, True)

    def get_rx_delay_on_window1(self):
        return int(self.send_cmd("AT+RX1DL=?", True))

    def set_rx_delay_on_window1(self, delay: int):
        return self.send_cmd("AT+RX1DL=" + str(delay), True, True)

    def get_rx_delay_on_window2(self):
        return int(self.send_cmd("AT+RX2DL=?", True))

    def set_rx_delay_on_window2(self, delay: int):
        return self.send_cmd("AT+RX2DL=" + str(delay), True, True)

    def get_rx_data_rate_on_windows2(self):
        return int(self.send_cmd("AT+RX2DR=?", True))

    def set_rx_data_rate_on_windows2(self, rate: int):
        return self.send_cmd(f"AT+RX2DR={rate}", True, True)

    def get_rx_frequency_on_windows2(self):
        return int(self.send_cmd("AT+RX2FQ=?", True))

    def get_tx_power(self):
        return int(self.send_cmd("AT+TXP=?", True))

    def set_tx_power(self, power: int):
        return self.send_cmd("AT+TXP=" + str(power), True, True)

    def get_network_link_state(self):
        return self.send_cmd("AT+LINKCHECK=?", True)

    def set_network_link_state(self, state: int):
        return self.send_cmd("AT+LINKCHECK=" + str(state), True, True)

    def get_listen_before_talk(self):
        return self.send_cmd("AT+LBT=?", True) == "1"

    def set_listen_before_talk(self, state: bool):
        return self.send_cmd(f"AT+LBT={int(state)}", True, True)

    def set_listen_before_talk_rssi(self, rssi: int):
        return self.send_cmd("AT+LBTRSSI=" + str(rssi), True, True)

    def get_listen_before_talk_rssi(self):
        return int(self.send_cmd("AT+LBTRSSI=?", True))

    def get_listen_before_talk_scan_time(self):
        return int(self.send_cmd("AT+LBTSCANTIME=?", True))

    def set_listen_before_talk_scan_time(self, time: int):
        return self.send_cmd("AT+LBTSCANTIME=" + str(time), True, True)

    def get_time_request(self):
        return int(self.send_cmd("AT+TIMEREQ=?", True))

    def set_time_request(self, state: bool):
        return self.send_cmd(f"AT+TIMEREQ={int(state)}", True, True)

    def get_location_time(self):
        return self.send_cmd("AT+LTIME=?", True)

    def get_unicast_ping_interval(self):
        return int(self.send_cmd("AT+PGSLOT=?", True))

    def set_unicast_ping_interval(self, interval: int):
        return self.send_cmd("AT+PGSLOT=" + str(interval), True, True)

    def get_beacon_frequency(self):
        return int(self.send_cmd("AT+BFREQ=?", True))

    def get_beacon_time(self):
        return int(self.send_cmd("AT+BTIME=?", True))

    def get_beacon_gateway_gps(self):
        return self.send_cmd("AT+BGW=?", True)

    def get_rssi(self):
        return self.send_cmd("AT+RSSI=?", True)

    def get_all_rssi(self):
        return self.send_cmd("AT+ARSSI=?", True)

    def get_signal_noise_ratio(self):
        return self.send_cmd("AT+SNR=?", True)

    def get_channel_mask(self):
        return self.send_cmd("AT+MASK=?", True)

    def set_channel_mask(self, mask: str):
        return self.send_cmd("AT+MASK=" + mask, True, True)

    def get_eight_channel_mode_state(self):
        return self.send_cmd("AT+CHE=?", True)

    def set_eight_channel_mode_state(self, max_group: int) -> bool:
        if not (1 <= max_group <= 12):
            raise ValueError("Channel group must be between 1 and 12.")

        state_str = ":".join(map(str, range(1, max_group + 1)))
        return self.send_cmd(f"AT+CHE={state_str}", True, True)

    def get_single_channel_mode(self):
        return self.send_cmd("AT+CHS=?", True)

    def set_single_channel_mode(self, freq: int):
        return self.send_cmd("AT+CHS=" + str(freq), True, True)

    def get_active_region(self):
        return self.send_cmd("AT+BAND=?", True)

    def set_active_region(self, region: int):
        return self.send_cmd("AT+BAND=" + str(region), True, True)

    def add_multicast_group(
        self, Class: str, DevAddr, NwkSKey, AppSKey, Frequency, Datarate, Periodicit
    ):
        return self.send_cmd(
            f"AT+ADDMULC={Class}:{DevAddr}:{NwkSKey}:{AppSKey}:{Frequency}:{Datarate}:{Periodicit}",
            True,
            True,
        )

    def remove_multicast_group(self, DevAddr):
        return self.send_cmd(f"AT+RMVMULC={DevAddr}", True, True)

    def get_multicast_list(self):
        return self.send_cmd("AT+LSTMULC=?", True)

    def get_network_mode(self):
        return self.send_cmd("AT+NWM=?", True)

    def set_network_mode(self, mode: int):
        """Set the network mode for the device.

        :returns: The result of the AT command execution.
        :rtype: bool

        :param int mode: The mode to set for the network:

            - 0 = P2P_LORA
            - 1 = LoRaWAN
            - 2 = P2P_FSK

        MicroPython Code Block:

            .. code-block:: python

                lorawan_rui3.set_network_mode(0)  # Set to P2P_LORA mode
        """
        return self.send_cmd("AT+NWM=" + str(mode), True, False, True, 500)

    def get_p2p_frequency(self):
        """Retrieve the current P2P frequency.

        :returns: The current P2P frequency as an integer.
        :rtype: int

        MicroPython Code Block:

            .. code-block:: python

                frequency = lorawan_rui3.get_p2p_frequency()
                print(f"Current P2P frequency: {frequency} Hz")
        """
        return int(self.send_cmd("AT+PFREQ=?", True))

    def set_p2p_frequency(self, frequency: int):
        """Set the P2P frequency for the device.

        :returns: The result of the AT command execution.
        :rtype: bool

        :param int frequency: The frequency to set for P2P communication.

            - Low-frequency range: 150000000-600000000
            - High-frequency range: 600000000-960000000

        MicroPython Code Block:

            .. code-block:: python

                success = lorawan_rui3.set_p2p_frequency(433000000)
                if success:
                    print("P2P frequency set successfully!")
                else:
                    print("Failed to set P2P frequency.")
        """
        return self.send_cmd("AT+PFREQ=" + str(frequency), True, True)

    def get_p2p_spreading_factor(self):
        """Retrieve the current P2P spreading factor.

        :returns: The current P2P spreading factor as an integer.
        :rtype: int

        MicroPython Code Block:

            .. code-block:: python

                sf = lorawan_rui3.get_p2p_spreading_factor()
                print(f"Current P2P spreading factor: {sf}")
        """
        return int(self.send_cmd("AT+PSF=?", True))

    def set_p2p_spreading_factor(self, spreading_factor: int):
        """Set the P2P spreading factor.

        :param int spreading_factor: The spreading factor to set for P2P communication.

            - Range is 5 to 12.

        :returns: The result of the AT command execution.
        :rtype: bool

        MicroPython Code Block:

            .. code-block:: python

                success = lorawan_rui3.set_p2p_spreading_factor(10)
                if success:
                    print("P2P spreading factor set successfully!")
                else:
                    print("Failed to set P2P spreading factor.")
        """
        return self.send_cmd("AT+PSF=" + str(spreading_factor), True, True)

    def get_p2p_bandwidth(self):
        """Retrieve the current P2P bandwidth.

        :returns: The current P2P bandwidth as an integer.
        :rtype: int

        MicroPython Code Block:

            .. code-block:: python

                bw = lorawan_rui3.get_p2p_bandwidth()
                print(f"Current P2P bandwidth: {bw}")

        """
        return int(self.send_cmd("AT+PBW=?", True))

    def set_p2p_bandwidth(self, bandwidth: int):
        """Set the P2P bandwidth.

        :param int bandwidth: The bandwidth to set for P2P communication.

            - For LoRa:
                - 0 = 125 kHz
                - 1 = 250 kHz
                - 2 = 500 kHz
                - 3 = 7.8 kHz
                - 4 = 10.4 kHz
                - 5 = 15.63 kHz
                - 6 = 20.83 kHz
                - 7 = 31.25 kHz
                - 8 = 41.67 kHz
                - 9 = 62.5 kHz

            - For FSK:
                Range: 4800-467000 Hz

        :returns: The result of the AT command execution.
        :rtype: bool
            |set_p2p_fsk_bandwidth.png|

            |set_p2p_lora_bandwidth.png|

        MicroPython Code Block:

            .. code-block:: python

                success = lorawan_rui3.set_p2p_bandwidth(1)  # Set to 250 kHz
                if success:
                    print("P2P bandwidth set successfully!")
                else:
                    print("Failed to set P2P bandwidth.")
        """
        return self.send_cmd("AT+PBW=" + str(bandwidth), True, True)

    def get_p2p_code_rate(self):
        """Retrieve the current P2P code rate.

        :returns: The current P2P code rate as an integer.
        :rtype: int

        MicroPython Code Block:

            .. code-block:: python

                code_rate = lorawan_rui3.get_p2p_code_rate()
                print(f"Current P2P code rate: {code_rate}")
        """
        return int(self.send_cmd("AT+PCR=?", True))

    def set_p2p_code_rate(self, code_rate: int):
        """Set the P2P code rate.

        :param int code_rate: The code rate to set for P2P communication.

                - 0 = 4/5
                - 1 = 4/6
                - 2 = 4/7
                - 3 = 4/8

        :returns: The result of the AT command execution.
        :rtype: bool

        MicroPython Code Block:

            .. code-block:: python

                success = lorawan_rui3.set_p2p_code_rate(1)  # Set to 4/6
                if success:
                    print("P2P code rate set successfully!")
                else:
                    print("Failed to set P2P code rate.")
        """
        return self.send_cmd("AT+PCR=" + str(code_rate), True, True)

    def get_p2p_preamble_length(self):
        """Retrieve the current P2P preamble length.

        :returns: The current P2P preamble length as an integer.
        :rtype: int

        MicroPython Code Block:

            .. code-block:: python

                preamble_length = lorawan_rui3.get_p2p_preamble_length()
                print(f"Current P2P preamble length: {preamble_length}")
        """
        return int(self.send_cmd("AT+PPL=?", True))

    def set_p2p_preamble_length(self, length: int):
        """Set the P2P preamble length.

        :returns: The result of the AT command execution.
        :rtype: bool

        :param int length: The preamble length to set for P2P communication.

            - Range is 5 to 65535.

        MicroPython Code Block:

            .. code-block:: python

                success = lorawan_rui3.set_p2p_preamble_length(16)
                if success:
                    print("P2P preamble length set successfully!")
                else:
                    print("Failed to set P2P preamble length.")
        """
        return self.send_cmd("AT+PPL=" + str(length), True, True)

    def get_p2p_tx_power(self):
        """Retrieve the current P2P transmission power.

        :returns: The current P2P transmission power as an integer.
        :rtype: int

        MicroPython Code Block:

            .. code-block:: python

                tx_power = lorawan_rui3.get_p2p_tx_power()
                print(f"Current P2P transmission power: {tx_power} dBm")
        """
        return int(self.send_cmd("AT+PTP=?", True))

    def set_p2p_tx_power(self, power: int):
        """Set the P2P transmission power.

        :param int power: The transmission power to set for P2P communication.

            - Range is 5 to 22 dBm.

        :returns: The result of the AT command execution.
        :rtype: bool

        MicroPython Code Block:

            .. code-block:: python

                success = lorawan_rui3.set_p2p_tx_power(20)  # Set to 20 dBm
                if success:
                    print("P2P transmission power set successfully!")
                else:
                    print("Failed to set P2P transmission power.")
        """
        return self.send_cmd("AT+PTP=" + str(power), True, True)

    def get_p2p_fsk_bitrate(self):
        """Retrieve the current P2P FSK bitrate.

        :returns: The result of the AT command execution.
        :rtype: bool

        MicroPython Code Block:

            .. code-block:: python

                fsk_bitrate = lorawan_rui3.get_p2p_fsk_bitrate()
                print(f"Current P2P FSK bitrate: {fsk_bitrate} b/s")
        """
        return int(self.send_cmd("AT+PBR=?", True))

    def set_p2p_fsk_bitrate(self, bitrate: int):
        """Set the P2P FSK bitrate.

        :param int bitrate: The bitrate to set for P2P FSK communication.

            - Range is 600 to 300000 b/s.

        :returns: The result of the AT command execution.
        :rtype: bool

        MicroPython Code Block:

            .. code-block:: python

                success = lorawan_rui3.set_p2p_fsk_bitrate(9600)  # Set to 9600 b/s
                if success:
                    print("P2P FSK bitrate set successfully!")
                else:
                    print("Failed to set P2P FSK bitrate.")

        """
        return self.send_cmd("AT+PBR=" + str(bitrate), True, True)

    def get_p2p_fsk_frequency_deviation(self):
        return int(self.send_cmd("AT+PFDEV=?", True))

    def set_p2p_fsk_frequency_deviation(self, deviation: int):
        return self.send_cmd("AT+PFDEV=" + str(deviation), True, True)

    def send_p2p_data(self, payload: str, timeout: int = 1000, to_hex: bool = False):
        """Send P2P data with a given payload.

        :param str payload: The payload to send.

            - Length must be between 2 and 500 characters.
            - Must consist of an even number of characters composed of 0-9, a-f, A-F, representing 1 to 256 hexadecimal values.
        :param int timeout: The timeout for the data transmission, in milliseconds. Default is 1000 ms.
        :param bool to_hex: Indicates whether to convert the payload to hexadecimal format. Default is False.

        :returns: True if the data was sent successfully ("TXFSK DONE" or "TXP2P DONE"), False otherwise.
        :rtype: bool

            |send_p2p_data_return.png|

        MicroPython Code Block:

            .. code-block:: python

                success = lorawan_rui3.send_p2p_data("abcdef", timeout=2000, to_hex=True)
                if success:
                    print("P2P data sent successfully!")
                else:
                    print("Failed to send P2P data.")

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
        return int(self.send_cmd("AT+CAD=?", True))

    def set_p2p_channel_activity(self, state: bool):
        return self.send_cmd(f"AT+CAD={int(state)}", True, True)

    def get_p2p_receive_data(self, timeout: int = 500, to_str: bool = False):
        """Receive data in P2P mode, including RSSI, SNR, and payload.

        :param int timeout: Timeout for listening to P2P LoRa data packets, in milliseconds.

                - Valid values are 1 to 65535.
                    - 0: Continuous listening.
                    - 65535: No timeout.

        :param bool to_str: Indicates whether to convert the payload to a string. Default is False.
        :returns: A tuple (RSSI, SNR, Payload) if data is received; False if no data is received.
        :rtype: tuple[int, int, str] | bool

        MicroPython Code Block:

            .. code-block:: python

                result = lorawan_rui3.get_p2p_receive_data(timeout=1000, to_str=True)
                if result:
                    rssi, snr, payload = result
                    print(f"Received data - RSSI: {rssi}, SNR: {snr}, Payload: {payload}")
                else:
                    print("No data received.")

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
        return int(self.send_cmd("AT+ENCRY=?", True))

    def set_p2p_encryption_state(self, state: bool):
        return self.send_cmd(f"AT+ENCRY={int(state)}", True, True)

    def get_p2p_encryption_key(self):
        return self.send_cmd("AT+ENCKEY=?", True)

    def set_p2p_encryption_key(self, key: str):
        return self.send_cmd(f"AT+ENCKEY={key}", True, True)

    def get_p2p_crypt_state(self):
        # RAK3172 not support
        return int(self.send_cmd("AT+PCRYPT=?", True))

    def set_p2p_crypt_state(self, state: bool):
        # RAK3172 not support
        return self.send_cmd(f"AT+PCRYPT={int(state)}", True, True)

    def get_p2p_crypt_key(self):
        # RAK3172 not support
        return self.send_cmd("AT+PKEY=?", True)

    def set_p2p_crypt_key(self, key):
        # RAK3172 not support
        # key:8 hex string
        return self.send_cmd(f"AT+PKEY={key}", True, True)

    def get_p2p_encryption_iv(self):
        return self.send_cmd("AT+CRYPIV=?", True)

    def set_p2p_encryption_iv(self, iv: str):
        return self.send_cmd(f"AT+CRYPIV={iv}", True, True)

    def get_p2p_parameters(self):
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
        return self.send_cmd(
            f"AT+P2P={frequency}:{spreading_factor}:{bandwidth}:{code_rate}:{preamble_length}:{tx_power}",
            True,
            True,
        )

    def get_p2p_iq_inversion(self):
        return int(self.send_cmd("AT+IQINVER=?", True))

    def set_p2p_iq_inversion(self, state: bool):
        return self.send_cmd(f"AT+IQINVER={int(state)}", True, True)

    def get_p2p_sync_word(self):
        """Get the current sync word in P2P mode.

        :returns: The sync word as a string.
        :rtype: str

        MicroPython Code Block:

            .. code-block:: python

                sync_word = lorawan_rui3.get_p2p_sync_word()
                print(f"Current P2P sync word: {sync_word}")

        """
        return self.send_cmd("AT+SYNCWORD=?", True)

    def set_p2p_sync_word(self, sync_word: int):
        """Set the sync word in P2P mode.

        :param int sync_word: The sync word value.

            - Must be in the range of 0x0000 to 0xFFFF.

        :returns: The response from the command execution.
        :rtype: bool

        MicroPython Code Block:

            .. code-block:: python

                success = lorawan_rui3.set_p2p_sync_word(0x1234)
                if success:
                    print("P2P sync word set successfully!")
                else:
                    print("Failed to set P2P sync word.")

        """
        sync_word_str = f"{sync_word:04X}"
        return self.send_cmd(f"AT+SYNCWORD={sync_word_str}", True, True)

    def get_p2p_symbol_timeout(self):
        return int(self.send_cmd("AT+SYMBOLTIMEOUT=?", True))

    def set_p2p_symbol_timeout(self, timeout):
        return self.send_cmd(f"AT+SYMBOLTIMEOUT={int(timeout)}", True, True)

    def get_p2p_fix_length_payload_state(self):
        return int(self.send_cmd("AT+FIXLENGTHPAYLOAD=?", True))

    def set_p2p_fix_length_payload_state(self, state: bool):
        return self.send_cmd(f"AT+FIXLENGTHPAYLOAD={int(state)}", True, True)
