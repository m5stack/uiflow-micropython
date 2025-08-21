# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import m5espnow
import time
import sys
import micropython

if sys.platform != "esp32":
    from typing import Literal


class SwitchC6Event:
    EVENT_ONOFF = 0
    EVENT_STATUS = 1
    EVENT_VERSION = 2

    def __init__(
        self,
        source_mac=None,
        target_mac=None,
        onoff=False,
        voltage=0.0,
        event_mac: bytes = None,
        event_data: bytes = None,
        event_type=EVENT_ONOFF,
        is_wait: bool = False,
    ):
        if event_mac is not None and event_data is not None:
            self.unpack(event_mac, event_data)
        else:
            self.source_mac = source_mac
            self.target_mac = target_mac
            self.onoff = onoff
            self.voltage = voltage
            self.is_wait = is_wait
            self.event_type = event_type
            self.version = ""

    def unpack(self, event_mac: bytes, event_data: bytes):
        self.source_mac = self.convert_mac(event_mac)
        print(f"Unpacking event from MAC: {self.source_mac}")

        event_data = event_data.decode("utf-8")
        if event_data.endswith("V"):
            # b"1122-AABB-CCGG;0;3.30V"
            print("Unpacking ON/OFF event")
            parts = event_data.split(";")
            self.target_mac = parts[0]
            self.onoff = int(parts[1]) == 1
            voltage_str = parts[2].rstrip("V")
            self.voltage = float(voltage_str)
            self.event_type = self.EVENT_ONOFF
        else:
            # b"1122-AABB-CCGG;1.0.0"
            print("Unpacking VERSION event")
            parts = event_data.split(";")
            self.target_mac = parts[0]
            self.version = parts[1]
            self.event_type = self.EVENT_VERSION
        self.is_wait = False

    @staticmethod
    def convert_mac(mac: bytes) -> str:
        hex_str = mac.hex().upper()
        formatted = "-".join(hex_str[i : i + 4] for i in range(0, len(hex_str), 4))
        return formatted

    @staticmethod
    def _is_valid_data_format(event_data: bytes) -> bool:
        """验证数据是否以"XXXX-XXXX-XXXX"格式的MAC地址开始"""
        try:
            # 解码为字符串
            data_str = event_data.decode("utf-8")

            # 检查数据长度是否足够包含MAC地址（至少14个字符）
            if len(data_str) < 14:
                return False

            # 提取前14个字符作为MAC地址部分
            mac_part = data_str[:14]

            # 使用已有的MAC验证方法
            return SwitchC6Event._validate_single_mac(mac_part)

        except (UnicodeDecodeError, ValueError, IndexError):
            return False

    @staticmethod
    def _validate_mac_list(mac_list: list) -> bool:
        """验证MAC地址列表中的每个MAC是否符合'XXXX-XXXX-XXXX'格式"""
        if not isinstance(mac_list, list):
            print("target_mac must be a list")
            return False

        if len(mac_list) == 0:
            print("target_mac list cannot be empty")
            return False

        for i, mac in enumerate(mac_list):
            if not isinstance(mac, str):
                print(f"MAC address at index {i} must be a string, got {type(mac)}")
                return False

            # 验证MAC地址格式：XXXX-XXXX-XXXX
            if not SwitchC6Event._validate_single_mac(mac):
                print(
                    f"Invalid MAC address format at index {i}: '{mac}'. Expected format: 'XXXX-XXXX-XXXX'"
                )
                return False

        print(f"All {len(mac_list)} MAC addresses are valid")
        return True

    @staticmethod
    def _validate_single_mac(mac: str) -> bool:
        """验证单个MAC地址是否符合'XXXX-XXXX-XXXX'格式"""
        # 检查长度
        if len(mac) != 14:
            return False

        # 检查连字符位置
        if mac[4] != "-" or mac[9] != "-":
            return False

        # 检查每个十六进制段
        segments = [mac[0:4], mac[5:9], mac[10:14]]

        for segment in segments:
            if len(segment) != 4:
                return False

            # 检查每个字符是否为十六进制
            for char in segment:
                if not (
                    (char >= "0" and char <= "9")
                    or (char >= "A" and char <= "F")
                    or (char >= "a" and char <= "f")
                ):
                    return False

        return True

    def __str__(self):
        if self.event_type in [SwitchC6Event.EVENT_ONOFF, SwitchC6Event.EVENT_STATUS]:
            return f"SwitchC6Event(source_mac={self.source_mac}, target_mac={self.target_mac}, onoff={self.onoff}, voltage={self.voltage})"
        elif self.event_type == SwitchC6Event.EVENT_VERSION:
            return f"SwitchC6Event(source_mac={self.source_mac}, target_mac={self.target_mac}, version={self.version})"
        else:
            return f"SwitchC6Event(source_mac={self.source_mac}, target_mac={self.target_mac})"


class SwitchC6Controller:

    """Create a SwitchC6Controller instance to control M5Stack SwitchC6 devices.

    :param target_mac: List of target MAC addresses in "XXXX-XXXX-XXXX" format.
    :param wifi_channel: WiFi channel to use for communication (default is 0, which uses the current channel).
    :param verbose: If True, print debug information (default is False).
    :raises ValueError: If any MAC address in target_mac is not in the "XXXX-XXXX-XXXX" format.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            import switchc6

            controller = switchc6.SwitchC6Controller(
                target_mac=["1122-AABB-CCDD", "2233-BBEE-DDEE"],
                wifi_channel=0,
                verbose=True
            )
    """

    OFF = 0
    ON = 1
    MAX = 2

    def __init__(self, target_mac: list, wifi_channel: int = 0, verbose: bool = False):
        # 验证target_mac列表中的MAC地址是否符合"XXXX-XXXX-XXXX"格式
        if not SwitchC6Event._validate_mac_list(target_mac):
            raise ValueError(
                "Invalid MAC address format in target_mac list. Expected format: 'XXXX-XXXX-XXXX'"
            )

        self.espnow = m5espnow.M5ESPNow(wifi_ch=wifi_channel)
        self.wifi_channel = self.espnow.wlan_sta.config("channel")
        self.target_mac = target_mac
        self.espnow.set_irq_callback(self.espnow_recv_callback)
        self.queue = SwitchC6Event(
            source_mac=SwitchC6Event.convert_mac(self.espnow.get_mac()),
            target_mac=SwitchC6Event.convert_mac(self.espnow.get_mac()),
            onoff=False,
            event_type=SwitchC6Event.EVENT_ONOFF,
            is_wait=True,
        )
        self._verbose = verbose
        self._callback = None

    def espnow_recv_callback(self, espnow_obj):
        event_mac, event_data = espnow_obj.recv_data()
        micropython.schedule(self._data_handler, (event_mac, event_data))

    def _data_handler(self, args):
        event_mac, event_data = args
        # 验证数据格式是否符合"1122-AABB-CCDD;0;3.30V"
        if not event_mac or not event_data or not SwitchC6Event._is_valid_data_format(event_data):
            # self._verbose and print(f"Invalid data format received: {event_data}")
            return

        self._verbose and print(f"Received data from MAC: {event_mac}, Data: {event_data}")

        event = SwitchC6Event(event_mac=event_mac, event_data=event_data)
        self._verbose and print(f"Received event: {event}")

        if event_mac == b"\xff\xff\xff\xff\xff\xff":
            return

        wait_queue = self.queue
        self._verbose and print(f"Waiting for event: {wait_queue}")
        if wait_queue.event_type == SwitchC6Event.EVENT_ONOFF:
            if (
                event.target_mac == wait_queue.source_mac
                and event.source_mac == wait_queue.target_mac
                and event.onoff == wait_queue.onoff
            ):
                wait_queue.onoff = event.onoff
                wait_queue.voltage = event.voltage
                wait_queue.is_wait = False
                return
        elif wait_queue.event_type == SwitchC6Event.EVENT_STATUS:
            if (
                event.target_mac == wait_queue.source_mac
                and event.source_mac == wait_queue.target_mac
            ):
                wait_queue.onoff = event.onoff
                wait_queue.voltage = event.voltage
                wait_queue.is_wait = False
                return
        elif wait_queue.event_type == SwitchC6Event.EVENT_VERSION:
            if (
                event.target_mac == wait_queue.source_mac
                and event.source_mac == wait_queue.target_mac
            ):
                wait_queue.version = event.version
                wait_queue.is_wait = False
                return

        if event.target_mac == "FFFF-FFFF-FFFF":
            if self._callback:
                micropython.schedule(
                    self._callback,
                    (self, event.source_mac, event.onoff, event.voltage),
                )

    def _communicate(self, payload, wait_queue, timeout: int = 5000) -> None:
        self._verbose and print("set_switch:", payload)
        self._verbose and print("set_switch:", wait_queue)
        self.espnow.set_irq_callback(None)

        # send broadcast message
        self.espnow.broadcast_data("".join(payload).encode("utf-8"))
        self._verbose and print("payload:", "".join(payload).encode("utf-8"))

        cur_time = time.ticks_ms()
        # last_send_time = cur_time
        # resend_interval = 10  # milliseconds
        while time.ticks_diff(time.ticks_ms(), cur_time) < timeout:
            # wait for response
            event_mac, event_data = self.espnow.recv_data()
            if event_mac and event_data:
                self._data_handler((event_mac, event_data))
            if not wait_queue.is_wait:
                break

            # resend if no response received
            # if time.ticks_diff(time.ticks_ms(), last_send_time) > resend_interval:
            #     self._verbose and print("resend")
            #     self.espnow.broadcast_data("".join(payload).encode("utf-8"))
            #     last_send_time = time.ticks_ms()
            self.espnow.broadcast_data("".join(payload).encode("utf-8"))
            # time.sleep_ms(10)
        if wait_queue.is_wait:
            self._verbose and print("Timeout waiting for response")
        self.espnow.set_irq_callback(self.espnow_recv_callback)

    def set_switch(self, target_mac: str, onoff: bool, timeout: int = 5000):
        """Set the switch state of the target device.

        :param target_mac: Target MAC address in "XXXX-XXXX-XXXX" format.
        :param onoff: True to turn on, False to turn off.
        :param timeout: Timeout in milliseconds for waiting for a response (default is 5000).

        UiFlow2 Code Block:

            |set_switch.png|

        MicroPython Code Block:

            .. code-block:: python

                switchc6.set_switch("1122-AABB-CCDD", True, timeout=5000)
        """
        payload = [
            target_mac.upper(),
            "=1" if onoff else "=0",
            ";",
            f"ch={self.wifi_channel}",
            ";",
        ]

        self.queue.target_mac = target_mac.upper()
        self.queue.onoff = onoff
        self.queue.event_type = SwitchC6Event.EVENT_ONOFF
        self.queue.is_wait = True

        self._communicate(payload, self.queue, timeout=timeout)

    def toggle_switch(self, target_mac: str, timeout: int = 5000):
        """Toggle the switch status of the target device.

        :param target_mac: Target MAC address in "XXXX-XXXX-XXXX" format.
        :param timeout: Timeout in milliseconds for waiting for a response (default is 5000).

        UiFlow2 Code Block:

            |toggle_switch.png|

        MicroPython Code Block:

            .. code-block:: python

                switchc6.toggle_switch("1122-AABB-CCDD", timeout=5000)
        """
        current_state = self.get_switch_status(target_mac, timeout=timeout)
        self.set_switch(target_mac, not current_state, timeout=timeout)

    def get_capacitor_voltage(self, target_mac: str, timeout: int = 5000) -> float:
        """Get the capacitor voltage of the target device.

        :param target_mac: Target MAC address in "XXXX-XXXX-XXXX" format.
        :param timeout: Timeout in milliseconds for waiting for a response (default is 5000).
        :returns: The capacitor voltage as a float.
        :rtype: float

        UiFlow2 Code Block:

            |get_capacitor_voltage.png|

        MicroPython Code Block:

            .. code-block:: python

                switchc6.get_capacitor_voltage("1122-AABB-CCDD", timeout=5000)
        """
        payload = [target_mac.upper(), "=?", ";", f"ch={self.wifi_channel}", ";"]

        self.queue.target_mac = target_mac.upper()
        self.queue.event_type = SwitchC6Event.EVENT_STATUS
        self.queue.is_wait = True

        self._communicate(payload, self.queue, timeout=timeout)
        return self.queue.voltage

    def get_switch_status(self, target_mac: str, timeout: int = 5000) -> bool:
        """Get the switch status of the target device.

        :param target_mac: Target MAC address in "XXXX-XXXX-XXXX" format.
        :param timeout: Timeout in milliseconds for waiting for a response (default is 5000).
        :returns: True if the switch is ON, False if it is OFF.
        :rtype: bool

        UiFlow2 Code Block:

            |get_switch_status.png|

        MicroPython Code Block:

            .. code-block:: python

                switchc6.get_switch_status("1122-AABB-CCDD", timeout=5000)
        """
        payload = [target_mac.upper(), "=?", ";", f"ch={self.wifi_channel}", ";"]
        self.queue.target_mac = target_mac.upper()
        self.queue.event_type = SwitchC6Event.EVENT_STATUS
        self.queue.is_wait = True
        self._communicate(payload, self.queue, timeout=timeout)
        return self.queue.onoff

    def set_callback(self, handler) -> None:
        """Set a callback function for the specified trigger.

        :param handler: The callback function to be called when the trigger occurs.
        :param trigger: The trigger type (0 for OFF, 1 for ON).

        UiFlow2 Code Block:

            |event.png|

        MicroPython Code Block:

            .. code-block:: python

                switchc6.set_callback(handler, trigger)
        """
        self._callback = handler

    def get_firmware_version(self, target_mac: str, timeout: int = 5000) -> str:
        """Get the firmware version of the target device.

        :param target_mac: Target MAC address in "XXXX-XXXX-XXXX" format.
        :param timeout: Timeout in milliseconds for waiting for a response (default is 5000).

        :returns: The firmware version as a string.
        :rtype: str

        UiFlow2 Code Block:

            |get_firmware_version.png|

        MicroPython Code Block:

            .. code-block:: python

                switchc6.get_firmware_version("1122-AABB-CCDD", timeout=5000)
        """
        payload = [target_mac.upper(), "=V", ";", f"ch={self.wifi_channel}", ";"]
        self.queue.target_mac = target_mac.upper()
        self.queue.event_type = SwitchC6Event.EVENT_VERSION
        self.queue.is_wait = True
        self._communicate(payload, self.queue, timeout=timeout)
        return self.queue.version
