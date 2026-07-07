# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .chain import ChainBus
from .key import KeyChain
import struct
import warnings


class SwitchChain(KeyChain):
    """Switch Chain class for interacting with switch devices over Chain bus.

    :param ChainBus bus: The Chain bus instance.
    :param int device_id: The device ID of the switch on the Chain bus.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from chain import ChainBus
            from chain import SwitchChain

            bus2 = ChainBus(2, tx=21, rx=22)
            chain_switch_0 = SwitchChain(bus2, 1)
    """

    CMD_GET_12ADC = 0x30
    CMD_GET_8ADC = 0x31
    CMD_SET_SLIP_MODE = 0x32
    CMD_GET_SLIP_MODE = 0x33
    CMD_SET_SWITCH_THRESHOLD = 0x34
    CMD_GET_SWITCH_THRESHOLD = 0x35
    CMD_GET_SWITCH_STATUS = 0x36
    CMD_AUTO_SEND_SWITCH_STATUS = 0xE0
    CMD_SET_TRIGGER = 0xE1  # 设置阈值触发上报模式
    CMD_GET_TRIGGER = 0xE2  # 获取阈值触发上报模式
    SLIP_MODE_DOWNUP_DEC = 0x00  # Slide up decreases, slide down increases
    SLIP_MODE_DOWNUP_INC = 0x01  # Slide up increases, slide down decreases

    STATUS_CLOSE = 0  # Switch closed
    STATUS_OPEN = 1  # Switch open

    def __init__(self, bus: ChainBus, device_id: int):
        super().__init__(bus, device_id)

    def get_adc12(self) -> int:
        """Get the 12-bit ADC value of the switch.

        :return: 12-bit ADC value (0-4095), or None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_adc12.png|

        MicroPython Code Block:

            .. code-block:: python

                value = chain_switch_0.get_adc12()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_12ADC, bytes())
        if state:
            if len(response) >= 2:
                return struct.unpack_from("<H", response, 0)[0]
        return None

    def get_adc8(self) -> int:
        """Get the 8-bit ADC value of the switch.

        :return: 8-bit ADC value (0-255), or None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_adc8.png|

        MicroPython Code Block:

            .. code-block:: python

                value = chain_switch_0.get_adc8()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_8ADC, bytes())
        if state:
            if len(response) >= 1:
                return response[0]
        return None

    def set_slip_mode(self, mode: int, save: bool = False) -> bool:
        """Set the slider change mode.

        :param int mode: Slider change mode. Use :attr:`SwitchChain.SLIP_MODE_DOWNUP_DEC` (0) for decreasing or :attr:`SwitchChain.SLIP_MODE_DOWNUP_INC` (1) for increasing.
        :param bool save: Whether to save the setting to flash. Default: False.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_slip_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_switch_0.set_slip_mode(SwitchChain.SLIP_MODE_DOWNUP_INC, True)
        """
        if mode not in (0, 1):
            mode = 0

        payload = struct.pack("<BB", mode, 1 if save else 0)
        state, response = self.bus.chainll.send(self.device_id, self.CMD_SET_SLIP_MODE, payload)
        if state:
            return response[0] == 1
        return False

    def get_slip_mode(self) -> int:
        """Get the slider change mode.

        :return: Slider change mode. :attr:`SwitchChain.SLIP_MODE_DOWNUP_DEC` (0) for decreasing or :attr:`SwitchChain.SLIP_MODE_DOWNUP_INC` (1) for increasing. Returns None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_slip_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                mode = chain_switch_0.get_slip_mode()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_SLIP_MODE, bytes())
        if state:
            if len(response) >= 1:
                return response[0]
        return None

    def set_switch_thresh(
        self, open_threshold: int, close_threshold: int, save: bool = False
    ) -> bool:
        """Set the switch open and close thresholds.

        :param int open_threshold: Open threshold value (0-4095). Must be greater than close_threshold.
        :param int close_threshold: Close threshold value (0-4095). Must be less than open_threshold.
        :param bool save: Whether to save the threshold to flash. Default: False.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_switch_thresh.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_switch_0.set_switch_thresh(3000, 1000, True)
        """
        # Clamp thresholds to valid range
        if open_threshold < 0:
            open_threshold = 0
        elif open_threshold > 4095:
            open_threshold = 4095

        if close_threshold < 0:
            close_threshold = 0
        elif close_threshold > 4095:
            close_threshold = 4095

        # Validate: open threshold must be greater than close threshold
        if open_threshold <= close_threshold:
            warnings.warn("open_threshold must be greater than close_threshold")
            return False

        # Pack as: open_low, open_high, close_low, close_high, flag
        payload = struct.pack(
            "<BBBBB",
            open_threshold & 0xFF,
            (open_threshold >> 8) & 0xFF,
            close_threshold & 0xFF,
            (close_threshold >> 8) & 0xFF,
            1 if save else 0,
        )
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_SWITCH_THRESHOLD, payload
        )
        if state:
            return response[0] == 1
        return False

    def get_open_thresh(self) -> int:
        """Get the switch open threshold.

        :return: Open threshold value (0-4095), or None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_open_thresh.png|

        MicroPython Code Block:

            .. code-block:: python

                open_th = chain_switch_0.get_open_thresh()
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_SWITCH_THRESHOLD, bytes()
        )
        if state:
            if len(response) >= 2:
                # Response format: [open_low, open_high, close_low, close_high]
                open_threshold = response[0] | (response[1] << 8)
                return open_threshold
        return None

    def get_close_thresh(self) -> int:
        """Get the switch close threshold.

        :return: Close threshold value (0-4095), or None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_close_thresh.png|

        MicroPython Code Block:

            .. code-block:: python

                close_th = chain_switch_0.get_close_thresh()
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_SWITCH_THRESHOLD, bytes()
        )
        if state:
            if len(response) >= 4:
                # Response format: [open_low, open_high, close_low, close_high]
                close_threshold = response[2] | (response[3] << 8)
                return close_threshold
        return None

    def get_switch_status(self) -> int:
        """Get the switch status.

        :return: Switch status. 0 means close, 1 means open. Returns None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_switch_status.png|

        MicroPython Code Block:

            .. code-block:: python

                status = chain_switch_0.get_switch_status()
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_SWITCH_STATUS, bytes()
        )
        if state:
            if len(response) >= 1:
                return response[0]
        return None

    def set_trigger(self, enable: bool) -> bool:
        """Enable or disable status change reporting.

        :param bool enable: True to enable status change reporting, False to disable it.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_trigger.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_switch_0.set_trigger(True)
        """
        payload = struct.pack("<B", 1 if enable else 0)
        state, response = self.bus.chainll.send(self.device_id, self.CMD_SET_TRIGGER, payload)
        if state:
            return response[0] == 1
        return False

    def get_trigger(self) -> bool:
        """Get whether status change reporting is enabled.

        :return: True if status change reporting is enabled, False if disabled. Returns False if failed.
        :rtype: bool

        UiFlow2 Code Block:

            |get_trigger.png|

        MicroPython Code Block:

            .. code-block:: python

                enabled = chain_switch_0.get_trigger()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_TRIGGER, bytes())
        if state:
            if len(response) >= 1:
                return response[0] == 1
        return False

    def set_trigger_callback(self, trigger_type: int, callback) -> None:
        """Set callback for switch status change events.

        :param int trigger_type: Trigger type to listen for. Use :attr:`SwitchChain.STATUS_CLOSE` (0) or :attr:`SwitchChain.STATUS_OPEN` (1).
        :param callback: Callback function that will be called when switch status changes.

        .. note::
            Chain related methods cannot be called in the callback function.

        UiFlow2 Code Block:

            |set_trigger_callback.png|

        MicroPython Code Block:

            .. code-block:: python

                def switch_status_callback():
                    print("Switch opened")

                # Listen for open status only
                chain_switch_0.set_trigger_callback(SwitchChain.STATUS_OPEN, switch_status_callback)

                # Listen for close status only
                chain_switch_0.set_trigger_callback(SwitchChain.STATUS_CLOSE, switch_status_callback)
        """
        if trigger_type == self.STATUS_CLOSE:
            self.bus.register_event(self, self.CMD_AUTO_SEND_SWITCH_STATUS, b"\x00\x04", callback)
        elif trigger_type == self.STATUS_OPEN:
            self.bus.register_event(self, self.CMD_AUTO_SEND_SWITCH_STATUS, b"\x01\x04", callback)
        else:
            raise ValueError("Invalid trigger_type. Use STATUS_CLOSE (0) or STATUS_OPEN (1)")
