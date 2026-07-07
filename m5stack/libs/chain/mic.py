# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .chain import ChainBus
from .key import KeyChain
import struct


class MicChain(KeyChain):
    """Mic Chain class for interacting with microphone devices over Chain bus.

    :param ChainBus bus: The Chain bus instance.
    :param int device_id: The device ID of the microphone on the Chain bus.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from chain import ChainBus
            from chain import MicChain

            bus2 = ChainBus(2, tx=21, rx=22)
            chain_mic_0 = MicChain(bus2, 1)
    """

    CMD_GET_12ADC = 0x30
    CMD_GET_8ADC = 0x31
    CMD_SET_THRESHOLD_VALUE = 0x32  # 设置触发阈值
    CMD_GET_THRESHOLD_VALUE = 0x33  # 获取触发阈值
    CMD_TRIGGER = 0xE0  # 触发
    CMD_SET_MODE = 0xE1  # 设置阈值触发上报模式
    CMD_GET_MODE = 0xE2  # 获取阈值触发上报模式
    CMD_SET_TRIGGER_INTERVAL = 0xE3  # 设置触发间隔
    CMD_GET_TRIGGER_INTERVAL = 0xE4  # 获取触发间隔

    TRIGGER_LOW_TO_HIGH = 0  # ADC value crosses threshold from low to high
    TRIGGER_HIGH_TO_LOW = 1  # ADC value crosses threshold from high to low

    def __init__(self, bus: ChainBus, device_id: int):
        super().__init__(bus, device_id)

    def get_adc8(self) -> int:
        """Get the 8-bit ADC value of the microphone.

        :return: 8-bit ADC value (0-255), or None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_adc8.png|

        MicroPython Code Block:

            .. code-block:: python

                value = chain_mic_0.get_adc8()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_8ADC, bytes())
        if state:
            if len(response) >= 1:
                return response[0]
        return None

    def get_adc12(self) -> int:
        """Get the 12-bit ADC value of the microphone.

        :return: 12-bit ADC value (0-4095), or None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_adc12.png|

        MicroPython Code Block:

            .. code-block:: python

                value = chain_mic_0.get_adc12()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_12ADC, bytes())
        if state:
            if len(response) >= 2:
                return struct.unpack_from("<H", response, 0)[0]
        return None

    def set_trigger(self, enable: bool) -> bool:
        """Enable or disable threshold-triggered reporting.

        :param bool enable: True to enable threshold-triggered reporting, False to disable it.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_trigger.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_mic_0.set_trigger(True)
        """
        payload = struct.pack("<B", 1 if enable else 0)
        state, response = self.bus.chainll.send(self.device_id, self.CMD_SET_MODE, payload)
        if state:
            return response[0] == 1
        return False

    def get_trigger(self) -> bool:
        """Get whether threshold-triggered reporting is enabled.

        :return: True if threshold-triggered reporting is enabled, False if disabled. Returns False if failed.
        :rtype: bool

        UiFlow2 Code Block:

            |get_trigger.png|

        MicroPython Code Block:

            .. code-block:: python

                enabled = chain_mic_0.get_trigger()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_MODE, bytes())
        if state:
            if len(response) >= 1:
                return response[0] == 1
        return False

    def set_trigger_thresh(self, threshold: int, save: bool = False) -> bool:
        """Set the microphone trigger threshold.

        :param int threshold: Threshold value (0-4095).
        :param bool save: Whether to save the threshold to flash. Default: False.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_trigger_thresh.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_mic_0.set_trigger_thresh(2000, True)
        """
        # Clamp threshold to valid range
        if threshold < 0:
            threshold = 0
        elif threshold > 4095:
            threshold = 4095

        payload = struct.pack("<HB", threshold & 0xFFFF, 1 if save else 0)
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_THRESHOLD_VALUE, payload
        )
        if state:
            return response[0] == 1
        return False

    def get_trigger_thresh(self) -> int:
        """Get the microphone trigger threshold.

        :return: Threshold value (0-4095), or None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_trigger_thresh.png|

        MicroPython Code Block:

            .. code-block:: python

                threshold = chain_mic_0.get_trigger_thresh()
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_THRESHOLD_VALUE, bytes()
        )
        if state:
            if len(response) >= 2:
                return struct.unpack_from("<H", response, 0)[0]
        return None

    def set_trigger_interval(self, interval_ms: int) -> bool:
        """Set the minimum trigger interval (debounce time).

        :param int interval_ms: Minimum time interval between triggers in milliseconds. Range: 300-1000.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_trigger_interval.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_mic_0.set_trigger_interval(500)  # Set 500ms minimum interval between triggers
        """
        # Clamp interval_ms to valid range
        if interval_ms < 300:
            interval_ms = 300
        elif interval_ms > 1000:
            interval_ms = 1000

        payload = struct.pack("<H", interval_ms & 0xFFFF)
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_TRIGGER_INTERVAL, payload
        )
        if state:
            return response[0] == 1
        return False

    def get_trigger_interval(self) -> int:
        """Get the minimum trigger interval (debounce time).

        :return: Minimum trigger interval in milliseconds, or None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_trigger_interval.png|

        MicroPython Code Block:

            .. code-block:: python

                interval = chain_mic_0.get_trigger_interval()
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_TRIGGER_INTERVAL, bytes()
        )
        if state:
            if len(response) >= 2:
                return struct.unpack_from("<H", response, 0)[0]
        return None

    def set_trigger_callback(self, trigger_type: int, callback) -> None:
        """Set callback for microphone trigger events.

        :param int trigger_type: Trigger type to listen for. Use :attr:`MicChain.TRIGGER_LOW_TO_HIGH` (0) or :attr:`MicChain.TRIGGER_HIGH_TO_LOW` (1).
        :param callback: Callback function that will be called when microphone triggers.

        .. note::
            Chain related methods cannot be called in the callback function.

        UiFlow2 Code Block:

            |set_trigger_callback.png|

        MicroPython Code Block:

            .. code-block:: python

                def mic_trigger_callback():
                    print("Sound detected")

                # Listen for low-to-high trigger only
                chain_mic_0.set_trigger_callback(MicChain.TRIGGER_LOW_TO_HIGH, mic_trigger_callback)

                # Listen for high-to-low trigger only
                chain_mic_0.set_trigger_callback(MicChain.TRIGGER_HIGH_TO_LOW, mic_trigger_callback)
        """
        if trigger_type == self.TRIGGER_LOW_TO_HIGH:
            self.bus.register_event(self, self.CMD_TRIGGER, b"\x00\x03", callback)
        elif trigger_type == self.TRIGGER_HIGH_TO_LOW:
            self.bus.register_event(self, self.CMD_TRIGGER, b"\x01\x03", callback)
        else:
            raise ValueError(
                "Invalid trigger_type. Use TRIGGER_LOW_TO_HIGH (0) or TRIGGER_HIGH_TO_LOW (1)"
            )
