# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .chain import ChainBus
from .key import KeyChain
import struct


class PIRChain(KeyChain):
    """PIR Chain class for interacting with PIR (Passive Infrared) sensor devices over Chain bus.

    :param ChainBus bus: The Chain bus instance.
    :param int device_id: The device ID of the PIR sensor on the Chain bus.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from chain import ChainBus
            from chain import PIRChain

            bus2 = ChainBus(2, tx=21, rx=22)
            chain_pir_0 = PIRChain(bus2, 1)
    """

    CMD_GET_IR = 0x37
    CMD_AUTO_SEND_IR = 0xE0
    CMD_SET_TRIGGER = 0xE1
    CMD_GET_TRIGGER = 0xE2
    CMD_SET_TRIGGER_DELAY = 0xE3
    CMD_GET_TRIGGER_DELAY = 0xE4

    TRIGGER_MOTION_DETECTED = 1  # Motion detected
    TRIGGER_MOTION_ENDED = 0  # Motion ended

    def __init__(self, bus: ChainBus, device_id: int):
        super().__init__(bus, device_id)

    def get_detect_status(self) -> bool:
        """Get the motion detection status.

        :return: Motion detection status. True means motion detected, False means motion ended. Returns False if failed.
        :rtype: bool

        UiFlow2 Code Block:

            |get_detect_status.png|

        MicroPython Code Block:

            .. code-block:: python

                status = chain_pir_0.get_detect_status()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_IR, bytes())
        if state:
            if len(response) >= 1:
                return response[0] == 1
        return False

    def set_trigger(self, enable: bool) -> bool:
        """Enable or disable PIR detection reporting.

        :param bool enable: True to enable PIR detection reporting, False to disable it.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_trigger.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_pir_0.set_trigger(True)
        """
        payload = struct.pack("<B", 1 if enable else 0)
        state, response = self.bus.chainll.send(self.device_id, self.CMD_SET_TRIGGER, payload)
        if state:
            return response[0] == 1
        return False

    def get_trigger(self) -> bool:
        """Get whether PIR detection reporting is enabled.

        :return: True if PIR detection reporting is enabled, False if disabled. Returns False if failed.
        :rtype: bool

        UiFlow2 Code Block:

            |get_trigger.png|

        MicroPython Code Block:

            .. code-block:: python

                enabled = chain_pir_0.get_trigger()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_TRIGGER, bytes())
        if state:
            if len(response) >= 1:
                return response[0] == 1
        return False

    def set_trigger_hold_time(self, seconds: int, save: bool = False) -> bool:
        """Set the hold time before triggering motion ended status.

        :param int seconds: Hold time in seconds. Range: 0-255.
        :param bool save: Whether to save the setting to flash. Default: False.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_trigger_hold_time.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_pir_0.set_trigger_hold_time(5, False)
        """
        if seconds < 0:
            seconds = 0
        elif seconds > 255:
            seconds = 255

        payload = struct.pack("<BB", seconds, 1 if save else 0)
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_TRIGGER_DELAY, payload
        )
        if state:
            return response[0] == 1
        return False

    def get_trigger_hold_time(self) -> int:
        """Get the hold time before triggering motion ended status.

        :return: Hold time in seconds, or None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_trigger_hold_time.png|

        MicroPython Code Block:

            .. code-block:: python

                hold_time = chain_pir_0.get_trigger_hold_time()
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_TRIGGER_DELAY, bytes()
        )
        if state:
            if len(response) >= 1:
                return response[0]
        return None

    def set_trigger_callback(self, trigger_type: int, callback) -> None:
        """Set callback for PIR motion detection events.

        :param int trigger_type: Trigger type to listen for. Use :attr:`PIRChain.TRIGGER_MOTION_DETECTED` (1) for motion detected or :attr:`PIRChain.TRIGGER_MOTION_ENDED` (0) for motion ended.
        :param callback: Callback function that will be called when PIR motion detection changes.

        .. note::
            Chain related methods cannot be called in the callback function.

        UiFlow2 Code Block:

            |set_trigger_callback.png|

        MicroPython Code Block:

            .. code-block:: python

                def motion_detected_callback(args):
                    print("Motion detected")

                def motion_ended_callback(args):
                    print("Motion ended")

                # Listen for motion detected only
                chain_pir_0.set_trigger_callback(PIRChain.TRIGGER_MOTION_DETECTED, motion_detected_callback)

                # Listen for motion ended only
                chain_pir_0.set_trigger_callback(PIRChain.TRIGGER_MOTION_ENDED, motion_ended_callback)
        """
        if trigger_type == self.TRIGGER_MOTION_DETECTED:
            # Register for motion detected (01 00)
            self.bus.register_event(self, self.CMD_AUTO_SEND_IR, b"\x01\x05", callback)
        elif trigger_type == self.TRIGGER_MOTION_ENDED:
            # Register for motion ended (00 00)
            self.bus.register_event(self, self.CMD_AUTO_SEND_IR, b"\x00\x05", callback)
        else:
            raise ValueError(
                "Invalid trigger_type. Use TRIGGER_MOTION_DETECTED (1) or TRIGGER_MOTION_ENDED (0)"
            )
