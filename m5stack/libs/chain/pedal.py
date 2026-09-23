# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import struct
import time

from chain.base import ChainDevice
from chain.chain import ChainBus


class PedalChain(ChainDevice):
    """Pedal Chain class for interacting with pedal devices over Chain bus.

    :param ChainBus bus: The Chain bus instance.
    :param int device_id: The device ID of the pedal on the Chain bus.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from chain import ChainBus, PedalChain

            chainbus_0 = ChainBus(2, tx=32, rx=33)
            pedalchain_0 = PedalChain(chainbus_0, 1)
    """

    CMD_KEY_PRESS = 0xE0
    CMD_KEY_STATE = 0xE1
    CMD_GET_SWITCH_STATUS = 0xE2
    CMD_SET_WORK_MODE = 0xE3
    CMD_GET_WORK_MODE = 0xE4
    CMD_SET_BUTTON_MODE = 0xE5
    CMD_GET_BUTTON_MODE = 0xE6
    CMD_SET_ENTER_CONFIG_TIME = 0xE7
    CMD_GET_ENTER_CONFIG_TIME = 0xE8
    CMD_SET_RGB_OVERLAY = 0xE9
    CMD_GET_RGB_OVERLAY = 0xEA

    RGB_COUNT = 4
    """Number of independently addressable RGB LEDs."""

    WORK_MODE_SINGLE = 0
    """Handle a short press-and-release as a click outside configuration mode."""
    WORK_MODE_SWITCH = 1
    """Toggle the logical switch on a short press-and-release outside configuration mode."""

    MODE_POLL = 0
    """Disable active event reports while keeping polling available."""
    MODE_EVENT = 1
    """Enable active event reports. This is the power-on default."""

    STATUS_CLOSE = 0
    """Logical switch off."""
    STATUS_OPEN = 1
    """Logical switch on."""

    def _send_status(self, cmd: int, payload: bytes) -> bool:
        state, response = self.bus.chainll.send(self.device_id, cmd, payload)
        return bool(state and response == b"\x01")

    def _send_value(self, cmd: int) -> int:
        state, response = self.bus.chainll.send(self.device_id, cmd, bytes())
        if state and response and len(response) == 1:
            return response[0]
        return -1

    def get_button_state(self) -> bool:
        """get button state.

        :return: Button state, True if pressed, False if released or failed.
        :rtype: bool

        UiFlow2 Code Block:

            |get_button_state.png|

        MicroPython Code Block:

            .. code-block:: python

                state = pedalchain_0.get_button_state()

        """
        return self._send_value(self.CMD_KEY_STATE) == 1

    def get_switch_status(self) -> int:
        """get switch status.

        :return: Switch status, 0 for close, 1 for open, or -1 if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_switch_status.png|

        MicroPython Code Block:

            .. code-block:: python

                status = pedalchain_0.get_switch_status()

        """
        return self._send_value(self.CMD_GET_SWITCH_STATUS)

    def set_click_callback(self, callback) -> None:
        """set button click callback.

        :param callback: Callback function accepting one argument, or None to
            disable it.

        .. note::
            Chain related methods cannot be called in the callback function.

        UiFlow2 Code Block:

            |click_callback.png|

        MicroPython Code Block:

            .. code-block:: python

                def pedal_click_callback(args):
                    print("click")

                pedalchain_0.set_click_callback(pedal_click_callback)

        """
        self.bus.register_event(self, self.CMD_KEY_PRESS, b"\x00\x00", callback)

    def set_trigger_callback(self, trigger_type: int, callback) -> None:
        """set callback for switch status change events.

        :param int trigger_type: Trigger type, 0 for close or 1 for open.
        :param callback: Callback function accepting one argument, or None to
            disable it.
        :raises ValueError: If ``trigger_type`` is not 0 or 1.

        .. note::
            Chain related methods cannot be called in the callback function.

        UiFlow2 Code Block:

            |status_callback.png|

        MicroPython Code Block:

            .. code-block:: python

                def pedal_status_callback(args):
                    print("switch status changed")

                pedalchain_0.set_trigger_callback(
                    PedalChain.STATUS_OPEN, pedal_status_callback
                )

        """
        if trigger_type not in (self.STATUS_CLOSE, self.STATUS_OPEN):
            raise ValueError("trigger_type must be STATUS_CLOSE (0) or STATUS_OPEN (1)")
        payload = struct.pack("<BB", trigger_type, 0x04)
        self.bus.register_event(self, self.CMD_KEY_PRESS, payload, callback)

    def set_work_mode(self, mode: int, save: bool = False) -> bool:
        """set pedal work mode.

        :param int mode: Work mode. Use ``WORK_MODE_SINGLE`` or
            ``WORK_MODE_SWITCH``.
        :param bool save: Whether to save the setting to flash. Default: False.
        :return: True if success, False otherwise.
        :rtype: bool
        :raises ValueError: If ``mode`` is not a supported work mode.

        UiFlow2 Code Block:

            |set_work_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                pedalchain_0.set_work_mode(PedalChain.WORK_MODE_SWITCH)

        """
        if mode not in (self.WORK_MODE_SINGLE, self.WORK_MODE_SWITCH):
            raise ValueError("mode must be WORK_MODE_SINGLE (0) or WORK_MODE_SWITCH (1)")
        return self._send_status(self.CMD_SET_WORK_MODE, struct.pack("<BB", mode, bool(save)))

    def get_work_mode(self) -> int:
        """get pedal work mode.

        :return: Work mode, 0 for single click, 1 for switch, or -1 if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_work_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                mode = pedalchain_0.get_work_mode()
        """
        return self._send_value(self.CMD_GET_WORK_MODE)

    def set_button_mode(self, mode: int) -> bool:
        """set button reporting mode.

        :param int mode: Reporting mode. Use ``MODE_POLL`` or ``MODE_EVENT``.
        :return: True if success, False otherwise.
        :rtype: bool
        :raises ValueError: If ``mode`` is not a supported reporting mode.

        UiFlow2 Code Block:

            |set_button_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                pedalchain_0.set_button_mode(PedalChain.MODE_EVENT)

        """
        if mode not in (self.MODE_POLL, self.MODE_EVENT):
            raise ValueError("mode must be MODE_POLL (0) or MODE_EVENT (1)")
        return self._send_status(self.CMD_SET_BUTTON_MODE, struct.pack("<B", mode))

    def get_button_mode(self) -> int:
        """get button reporting mode.

        :return: Reporting mode, 0 for polling, 1 for events, or -1 if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_button_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                mode = pedalchain_0.get_button_mode()
        """
        return self._send_value(self.CMD_GET_BUTTON_MODE)

    def set_enter_config_time(self, seconds: int, save: bool = False) -> bool:
        """set local configuration entry time.

        :param int seconds: Time in seconds from 1 to 30. Use 0 to disable
            local configuration entry.
        :param bool save: Whether to save the setting to flash. Default: False.
        :return: True if success, False otherwise.
        :rtype: bool
        :raises ValueError: If ``seconds`` is outside the range 0-30.

        UiFlow2 Code Block:

            |set_enter_config_time.png|

        MicroPython Code Block:

            .. code-block:: python

                pedalchain_0.set_enter_config_time(10)

        """
        if not 0 <= seconds <= 30:
            raise ValueError("seconds must be in range 0-30")
        payload = struct.pack("<BB", seconds, bool(save))
        return self._send_status(self.CMD_SET_ENTER_CONFIG_TIME, payload)

    def get_enter_config_time(self) -> int:
        """get local configuration entry time.

        :return: Time in seconds, 0 if disabled, or -1 if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_enter_config_time.png|

        MicroPython Code Block:

            .. code-block:: python

                seconds = pedalchain_0.get_enter_config_time()
        """
        return self._send_value(self.CMD_GET_ENTER_CONFIG_TIME)

    def set_rgb_overlay(self, overlay_mask: int, save: bool = False) -> bool:
        """set the pedal event RGB overlay mask.

        :param int overlay_mask: Bitmask from 0x00 to 0x0F. Bits 0-3 select LEDs
            0-3.
        :param bool save: Whether to save the setting to flash. Default: False.
        :return: True if success, False otherwise.
        :rtype: bool
        :raises ValueError: If ``overlay_mask`` is outside the range
            0x00-0x0F.

        UiFlow2 Code Block:

            |set_rgb_overlay.png|

        MicroPython Code Block:

            .. code-block:: python

                pedalchain_0.set_rgb_overlay(0x0F)

        """
        if not 0 <= overlay_mask <= 0x0F:
            raise ValueError("overlay_mask must be in range 0x00-0x0F")
        payload = struct.pack("<BB", overlay_mask, bool(save))
        return self._send_status(self.CMD_SET_RGB_OVERLAY, payload)

    def get_rgb_overlay(self) -> int:
        """get the pedal event RGB overlay mask.

        :return: Bitmask from 0x00 to 0x0F, or -1 if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_rgb_overlay.png|

        MicroPython Code Block:

            .. code-block:: python

                overlay_mask = pedalchain_0.get_rgb_overlay()
        """
        return self._send_value(self.CMD_GET_RGB_OVERLAY)
