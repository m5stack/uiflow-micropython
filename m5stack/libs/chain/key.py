# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import struct
import warnings
from .base import ChainDevice


class KeyChain(ChainDevice):
    """Create a KeyChain object.

    :param ChainBus bus: ChainBus object.
    :param int device_id: Device ID.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from chain import ChainBus
            from chain import KeyChain

            chainbus_0 = ChainBus(2, 32, 33, verbose=True)
            keychain_0 = KeyChain(chainbus_0, 1)

    """

    CMD_KEY_PRESS = 0xE0
    CMD_KEY_STATE = 0xE1
    CMD_SET_BUTTON_TRIGGER_TIMEOUT = 0xE2
    CMD_GET_BUTTON_TRIGGER_TIMEOUT = 0xE3
    CMD_SET_BUTTON_MODE = 0xE4
    CMD_GET_BUTTON_MODE = 0xE5

    MODE_POLL = 0x00
    """Button Polling mode"""
    MODE_EVENT = 0x01
    """Button Event mode"""

    def set_rgb_color(self, color: int) -> bool:
        """set RGB color.

        :param int color: RGB color value.
        :return: True if success, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_rgb_color.png|

        MicroPython Code Block:

            .. code-block:: python

                keychain_0.set_rgb_color(0xFF0000)
        """
        return super().set_rgb_color(0, color)

    def get_rgb_color(self) -> int:
        """get RGB color.

        :return: RGB color value.
        :rtype: int

        UiFlow2 Code Block:

            |get_rgb_color.png|

        MicroPython Code Block:

            .. code-block:: python

                color = keychain_0.get_rgb_color()
        """
        return super().get_rgb_color(0)

    def get_button_state(self) -> bool:
        """get button state.

        :return: Button state, True if pressed, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |get_button_state.png|

        MicroPython Code Block:

            .. code-block:: python

                keychain_0.get_button_state()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_KEY_STATE, bytes())
        if state:
            return response[0] == 1
        return False

    def set_click_callback(self, callback) -> None:
        """set button click callback.

        :param callback: Callback function.

        .. note::
            Chain related methods cannot be called in the callback function.

        UiFlow2 Code Block:

            |key_click_callback.png|

        MicroPython Code Block:

            .. code-block:: python

                def keychain_0_click_callback(args):
                    print("click")

                keychain_0.set_click_callback(keychain_0_click_callback)
        """
        self.bus.register_event(self, self.CMD_KEY_PRESS, b"\x00\x00", callback)

    def set_double_click_callback(self, callback) -> None:
        """set button double click callback.

        :param callback: Callback function.

        .. note::
            Chain related methods cannot be called in the callback function.

        UiFlow2 Code Block:

            |double_click_callback.png|

        MicroPython Code Block:

            .. code-block:: python

                def keychain_0_double_click_callback(args):
                    print("double click")

                keychain_0.set_double_click_callback(keychain_0_double_click_callback)
        """
        self.bus.register_event(self, self.CMD_KEY_PRESS, b"\x01\x00", callback)

    def set_long_press_callback(self, callback) -> None:
        """set button long press callback.

        :param callback: Callback function.

        .. note::
            Chain related methods cannot be called in the callback function.

        UiFlow2 Code Block:

            |long_press_callback.png|

        MicroPython Code Block:

            .. code-block:: python

                def keychain_0_long_press_callback(args):
                    print("long press")

                keychain_0.set_long_press_callback(keychain_0_long_press_callback)
        """
        self.bus.register_event(self, self.CMD_KEY_PRESS, b"\x02\x00", callback)

    def _set_button_trigger_timeout(
        self, double_click_interval: int, long_press_interval: int
    ) -> bool:
        payload = struct.pack("<BB", double_click_interval, long_press_interval)
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_BUTTON_TRIGGER_TIMEOUT, payload
        )
        if state:
            return response[0] == 1
        return False

    def set_button_double_click_trigger_interval(self, interval_ms: int) -> bool:
        """set button double click trigger interval.

        :param int interval_ms: Interval time in milliseconds. range: 100-1000
        :return: True if success, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_button_double_click_trigger_interval.png|

        MicroPython Code Block:

            .. code-block:: python

                keychain_0.set_button_double_click_trigger_interval(100)
        """
        if interval_ms < 100:
            warnings.warn("Interval time too small, set to 100ms")
            interval_ms = 100
        elif interval_ms > 1000:
            warnings.warn("Interval time too large, set to 1000ms")
            interval_ms = 1000

        double_click_interval = (interval_ms // 100) - 1
        long_press_interval = self.get_button_long_press_trigger_interval() // 1000 - 3
        return self._set_button_trigger_timeout(double_click_interval, long_press_interval)

    def set_button_long_press_trigger_interval(self, interval_ms: int) -> bool:
        """set button long press trigger interval.

        :param int interval_ms: Interval time in milliseconds. range: 3000-30000
        :return: True if success, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_button_long_press_trigger_interval.png|

        MicroPython Code Block:

            .. code-block:: python

                keychain_0.set_button_long_press_trigger_interval(3000)
        """
        if interval_ms < 3000:
            warnings.warn("Interval time too small, set to 3000ms")
            interval_ms = 3000
        elif interval_ms > 10000:
            warnings.warn("Interval time too large, set to 10000ms")
            interval_ms = 10000

        long_press_interval = (interval_ms // 1000) - 3
        double_click_interval = self.get_button_double_click_trigger_interval() // 100 - 1
        return self._set_button_trigger_timeout(double_click_interval, long_press_interval)

    def get_button_double_click_trigger_interval(self) -> int:
        """get button double click trigger interval.

        :return: Interval time in milliseconds.
        :rtype: int

        UiFlow2 Code Block:

            |get_button_double_click_trigger_interval.png|

        MicroPython Code Block:

            .. code-block:: python

                interval = keychain_0.get_button_double_click_trigger_interval()
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_BUTTON_TRIGGER_TIMEOUT, bytes()
        )
        if state:
            return (response[0] + 1) * 100
        return 100

    def get_button_long_press_trigger_interval(self) -> int:
        """get button long press trigger interval.

        :return: Interval time in milliseconds.
        :rtype: int

        UiFlow2 Code Block:

            |get_button_long_press_trigger_interval.png|

        MicroPython Code Block:

            .. code-block:: python

                interval = keychain_0.get_button_long_press_trigger_interval()
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_BUTTON_TRIGGER_TIMEOUT, bytes()
        )
        if state:
            return (response[1] + 3) * 1000
        return 3000

    def set_button_mode(self, mode: int) -> bool:
        """set button mode.

        :param int mode: Button mode. Use :attr:`KeyChain.MODE_POLL` or :attr:`KeyChain.MODE_EVENT`.
        :return: True if success, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_button_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                keychain_0.set_button_mode(KeyChain.MODE_EVENT)
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_BUTTON_MODE, struct.pack("<B", mode)
        )
        if state:
            return response[0] == 1
        return False

    def get_button_mode(self) -> int:
        """get button mode.

        :return: Button mode. :attr:`KeyChain.MODE_POLL` or :attr:`KeyChain.MODE_EVENT`.
        :rtype: int

        UiFlow2 Code Block:

            |get_button_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                mode = keychain_0.get_button_mode()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_BUTTON_MODE, bytes())
        if state:
            return response[0]
        return -1
