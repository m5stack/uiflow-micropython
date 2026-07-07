# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import struct
import warnings
from .chain import ChainBus
from .key import KeyChain


class MonoChain(KeyChain):
    """Mono Chain class for interacting with 8x8 monochrome display devices over Chain bus.

    :param ChainBus bus: The Chain bus instance.
    :param int device_id: The device ID of the Mono display on the Chain bus.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from chain import ChainBus
            from chain import MonoChain

            bus2 = ChainBus(2, tx=21, rx=22)
            chain_mono_0 = MonoChain(bus2, 1)
    """

    CMD_SET_DISPLAY_MODE = 0x10
    CMD_GET_DISPLAY_MODE = 0x11
    CMD_SET_PIXEL = 0x30
    CMD_SET_DISPLAY_BUFFER = 0x31
    CMD_GET_PIXEL = 0x32
    CMD_GET_DISPLAY_BUFFER = 0x33
    CMD_SET_DISPLAY_CHAR = 0x34
    CMD_SET_SCROLL_TEXT = 0x40
    CMD_SET_SCROLL_STATE = 0x42
    CMD_GET_SCROLL_STATE = 0x43
    CMD_SET_DISPLAY_ROTATION = 0xE0
    CMD_GET_DISPLAY_ROTATION = 0xE1
    CMD_SET_BRIGHTNESS = 0xE2
    CMD_GET_BRIGHTNESS = 0xE3
    CMD_CLEAR_DISPLAY = 0xE4

    MODE_PIXEL = 0
    MODE_SCROLL = 1

    STATUS_FAILED = 0
    STATUS_OK = 1
    STATUS_MODE_MISMATCH = 2

    SCROLL_DIR_LEFT = 0
    SCROLL_DIR_RIGHT = 1
    SCROLL_DIR_UP = 2
    SCROLL_DIR_DOWN = 3

    SCROLL_MODE_ONCE = 0
    SCROLL_MODE_LOOP = 1
    SCROLL_MODE_BOUNCE = 3

    SCROLL_STATE_START = 0
    SCROLL_STATE_PAUSE = 1
    SCROLL_STATE_RESET = 2

    ROTATION_0 = 0
    ROTATION_90 = 1
    ROTATION_180 = 2
    ROTATION_270 = 3

    def __init__(self, bus: ChainBus, device_id: int):
        super().__init__(bus, device_id)

    def _send_status(self, cmd: int, payload: bytes = bytes()) -> bool:
        state, response = self.bus.chainll.send(self.device_id, cmd, payload)
        if state and response:
            return response[0] == self.STATUS_OK
        return False

    def _send_value(self, cmd: int, payload: bytes = bytes(), default=None):
        state, response = self.bus.chainll.send(self.device_id, cmd, payload)
        if state and response:
            return response[0]
        return default

    def _limit(self, value: int, minimum: int, maximum: int, name: str) -> int:
        if value < minimum:
            warnings.warn("%s too small, set to %d" % (name, minimum))
            return minimum
        if value > maximum:
            warnings.warn("%s too large, set to %d" % (name, maximum))
            return maximum
        return value

    def _check_xy(self, x: int, y: int) -> None:
        if not 0 <= x <= 7:
            raise ValueError("x must be in range 0-7")
        if not 0 <= y <= 7:
            raise ValueError("y must be in range 0-7")

    def _pack_xy(self, x: int, y: int) -> int:
        self._check_xy(x, y)
        return ((x & 0x07) << 3) | (y & 0x07)

    def _pack_pixel(self, x: int, y: int, state: bool = True) -> int:
        return (0x40 if state else 0x00) | self._pack_xy(x, y)

    def _encode_ascii(self, text) -> bytes:
        if isinstance(text, str):
            for ch in text:
                code = ord(ch)
                if code < 32 or code > 127:
                    raise ValueError("Mono only supports ASCII characters 32-127")
            return text.encode()
        data = bytes(text)
        for ch in data:
            if ch < 32 or ch > 127:
                raise ValueError("Mono only supports ASCII characters 32-127")
        return data

    def set_display_mode(self, mode: int = MODE_PIXEL) -> bool:
        """Set the display mode.

        :param int mode: Display mode. Use :attr:`MonoChain.MODE_PIXEL` (0) for pixel mode or :attr:`MonoChain.MODE_SCROLL` (1) for scrolling string mode.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_display_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_mono_0.set_display_mode(MonoChain.MODE_PIXEL)
        """
        mode = self._limit(mode, self.MODE_PIXEL, self.MODE_SCROLL, "mode")
        return self._send_status(self.CMD_SET_DISPLAY_MODE, bytes([mode & 0xFF]))

    def get_display_mode(self) -> int:
        """Get the display mode.

        :return: Display mode. 0 means pixel mode, 1 means scrolling string mode. Returns None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_display_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                mode = chain_mono_0.get_display_mode()
        """
        return self._send_value(self.CMD_GET_DISPLAY_MODE, default=None)

    def set_pixel(self, x: int, y: int, state: bool = True) -> bool:
        """Set one pixel state on the 8x8 display.

        :param int x: X coordinate, range 0-7.
        :param int y: Y coordinate, range 0-7.
        :param bool state: Pixel state. True means on, False means off.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_pixel.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_mono_0.set_pixel(0, 0, True)
        """
        self._check_xy(x, y)
        payload = bytes([1, self._pack_pixel(x, y, state)])
        return self._send_status(self.CMD_SET_PIXEL, payload)

    def set_pixels(self, coordinates=None) -> bool:
        """Set multiple pixel states on the 8x8 display.

        :param coordinates: Iterable of ``(x, y, state)`` or ``(x, y)`` values. Supports 1-64 pixels.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_pixels.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_mono_0.set_pixels(((0, 0, True), (1, 0, False)))
        """
        if coordinates is None:
            return False

        payload = bytearray()
        payload.append(0)
        count = 0
        for pixel in coordinates:
            if pixel is None:
                continue
            try:
                pixel_len = len(pixel)
                if pixel_len == 2:
                    x, y = pixel
                    state = True
                elif pixel_len == 3:
                    x, y, state = pixel
                else:
                    continue
            except (TypeError, ValueError):
                continue
            self._check_xy(x, y)
            payload.append(self._pack_pixel(x, y, state))
            count += 1
            if count >= 64:
                break
        if count < 1:
            return False
        payload[0] = count
        return self._send_status(self.CMD_SET_PIXEL, bytes(payload))

    def get_pixel(self, x: int, y: int):
        """Get one pixel state from the 8x8 display.

        :param int x: X coordinate, range 0-7.
        :param int y: Y coordinate, range 0-7.
        :return: Pixel state. True means on, False means off. Returns None if failed.
        :rtype: bool

        UiFlow2 Code Block:

            |get_pixel.png|

        MicroPython Code Block:

            .. code-block:: python

                state = chain_mono_0.get_pixel(0, 0)
        """
        self._check_xy(x, y)
        states = self.get_pixels(((x, y),))
        if states is None:
            return None
        return states[0] == 1

    def get_pixels(self, coordinates):
        """Get multiple pixel states from the 8x8 display.

        :param coordinates: Iterable of ``(x, y)`` coordinates. Supports 1-64 pixels.
        :return: Tuple of 0/1 pixel states, or None if failed.
        :rtype: tuple

        UiFlow2 Code Block:

            |get_pixels.png|

        MicroPython Code Block:

            .. code-block:: python

                states = chain_mono_0.get_pixels(((0, 0), (1, 0)))
        """
        payload = bytearray()
        payload.append(0)
        count = 0
        for coordinate in coordinates:
            if coordinate is None:
                continue
            try:
                if len(coordinate) != 2:
                    continue
                x, y = coordinate
            except (TypeError, ValueError):
                continue
            self._check_xy(x, y)
            payload.append(self._pack_xy(x, y))
            count += 1
            if count >= 64:
                break
        if count < 1:
            return None
        payload[0] = count
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_PIXEL, bytes(payload))
        if state and len(response) >= count:
            return tuple(response[:count])
        return None

    def set_display_buffer(self, buffer) -> bool:
        """Refresh the full 8x8 display buffer.

        :param buffer: 8 row bytes. Row 0 is Y=0, bit7 maps to X=0 and bit0 maps to X=7.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_display_buffer.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_mono_0.set_display_buffer((0xFF, 0x81, 0x81, 0x81, 0x81, 0x81, 0x81, 0xFF))
        """
        data = bytes(buffer)
        if len(data) != 8:
            raise ValueError("display buffer must contain 8 bytes")
        return self._send_status(self.CMD_SET_DISPLAY_BUFFER, data)

    def get_display_buffer(self):
        """Get the full 8-byte display buffer.

        :return: Tuple of 8 row bytes, or None if failed.
        :rtype: tuple

        UiFlow2 Code Block:

            |get_display_buffer.png|

        MicroPython Code Block:

            .. code-block:: python

                buffer = chain_mono_0.get_display_buffer()
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_DISPLAY_BUFFER, bytes()
        )
        if state and len(response) >= 8:
            return tuple(response[:8])
        return None

    def set_matrix(self, matrix) -> bool:
        """Refresh the display from an 8x8 matrix.

        :param matrix: 8 rows of row bytes or boolean/0/1 values.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        MicroPython Code Block:

            .. code-block:: python

                success = chain_mono_0.set_matrix(((1, 0, 0, 0, 0, 0, 0, 1),) * 8)
        """
        rows = bytearray()
        for row in matrix:
            if isinstance(row, int):
                rows.append(row & 0xFF)
            else:
                value = 0
                x = 0
                for point in row:
                    if point:
                        value |= 0x80 >> x
                    x += 1
                    if x >= 8:
                        break
                rows.append(value)
            if len(rows) >= 8:
                break
        if len(rows) != 8:
            raise ValueError("matrix must contain 8 rows")
        return self.set_display_buffer(rows)

    def set_display_char(self, char, x_offset: int = 0, y_offset: int = 0) -> bool:
        """Set one ASCII character in pixel mode.

        :param char: Character or ASCII code in range 32-127.
        :param int x_offset: X offset, range 0-7.
        :param int y_offset: Y offset, range 0-7.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_display_char.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_mono_0.set_display_char("A", 1, 0)
        """
        if isinstance(char, str):
            if len(char) != 1:
                raise ValueError("char must be a single character")
            char = ord(char)
        char = self._limit(char, 32, 127, "char")
        x_offset = self._limit(x_offset, 0, 7, "x_offset")
        y_offset = self._limit(y_offset, 0, 7, "y_offset")
        payload = struct.pack("<BB", char & 0xFF, (x_offset << 4) | y_offset)
        return self._send_status(self.CMD_SET_DISPLAY_CHAR, payload)

    def set_scroll_text(
        self,
        text,
        direction: int = SCROLL_DIR_LEFT,
        mode: int = SCROLL_MODE_LOOP,
        speed: int = 100,
    ) -> bool:
        """Set the scrolling ASCII text.

        :param text: ASCII string or bytes to display. Supports ASCII characters 32-127.
        :param int direction: Scroll direction. Use :attr:`MonoChain.SCROLL_DIR_RIGHT` (0), :attr:`MonoChain.SCROLL_DIR_LEFT` (1), :attr:`MonoChain.SCROLL_DIR_UP` (2), or :attr:`MonoChain.SCROLL_DIR_DOWN` (3).
        :param int mode: Scroll mode. Use :attr:`MonoChain.SCROLL_MODE_ONCE` (0), :attr:`MonoChain.SCROLL_MODE_LOOP` (1), or :attr:`MonoChain.SCROLL_MODE_BOUNCE` (3).
        :param int speed: Scroll speed in milliseconds per pixel. Range: 0-65535.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_scroll_text.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_mono_0.set_scroll_text("M5Stack", MonoChain.SCROLL_DIR_LEFT, MonoChain.SCROLL_MODE_LOOP, 100)
        """
        data = self._encode_ascii(text)
        if len(data) > 245:
            raise ValueError("scroll text is too long")
        direction = self._limit(direction, 0, 3, "direction")
        if mode not in (self.SCROLL_MODE_ONCE, self.SCROLL_MODE_LOOP, self.SCROLL_MODE_BOUNCE):
            warnings.warn("invalid scroll mode, set to loop")
            mode = self.SCROLL_MODE_LOOP
        speed = self._limit(speed, 0, 65535, "speed")
        scroll_mode = ((direction & 0x0F) << 4) | (mode & 0x0F)
        payload = struct.pack("<BBBB", scroll_mode, speed & 0xFF, speed >> 8, len(data))
        payload += data
        return self._send_status(self.CMD_SET_SCROLL_TEXT, payload)

    def set_scroll_state(self, state: int = SCROLL_STATE_START) -> bool:
        """Set the scrolling text state.

        :param int state: Scroll state. Use :attr:`MonoChain.SCROLL_STATE_START` (0), :attr:`MonoChain.SCROLL_STATE_PAUSE` (1), or :attr:`MonoChain.SCROLL_STATE_RESET` (2).
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_scroll_state.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_mono_0.set_scroll_state(MonoChain.SCROLL_STATE_START)
        """
        state = self._limit(state, self.SCROLL_STATE_START, self.SCROLL_STATE_RESET, "state")
        return self._send_status(self.CMD_SET_SCROLL_STATE, bytes([state & 0xFF]))

    def get_scroll_state(self) -> int:
        """Get the scrolling text state.

        :return: Scroll state. 0 means scrolling, 1 means paused, 2 means reset/idle. Returns None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_scroll_state.png|

        MicroPython Code Block:

            .. code-block:: python

                state = chain_mono_0.get_scroll_state()
        """
        return self._send_value(self.CMD_GET_SCROLL_STATE, default=None)

    def set_display_rotation(self, rotation: int = ROTATION_0, save: bool = False) -> bool:
        """Set the display rotation.

        :param int rotation: Display rotation. 0 default, 1 clockwise 90 degrees, 2 clockwise 180 degrees, 3 clockwise 270 degrees.
        :param bool save: Whether to save the setting to flash.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_display_rotation.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_mono_0.set_display_rotation(MonoChain.ROTATION_0, save=False)
        """
        rotation = self._limit(rotation, self.ROTATION_0, self.ROTATION_270, "rotation")
        payload = struct.pack("<BB", rotation & 0xFF, 1 if save else 0)
        return self._send_status(self.CMD_SET_DISPLAY_ROTATION, payload)

    def get_display_rotation(self) -> int:
        """Get the display rotation.

        :return: Display rotation. 0 default, 1 clockwise 90 degrees, 2 clockwise 180 degrees, 3 clockwise 270 degrees. Returns None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_display_rotation.png|

        MicroPython Code Block:

            .. code-block:: python

                rotation = chain_mono_0.get_display_rotation()
        """
        return self._send_value(self.CMD_GET_DISPLAY_ROTATION, default=None)

    def set_brightness(self, brightness: int = 7, save: bool = False) -> bool:
        """Set the screen brightness level.

        :param int brightness: Brightness level. Range: 0-7.
        :param bool save: Whether to save the setting to flash.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_brightness.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_mono_0.set_brightness(7, save=False)
        """
        brightness = self._limit(brightness, 0, 7, "brightness")
        payload = struct.pack("<BB", brightness & 0xFF, 1 if save else 0)
        return self._send_status(self.CMD_SET_BRIGHTNESS, payload)

    def get_brightness(self) -> int:
        """Get the screen brightness level.

        :return: Brightness level, range 0-7. Returns None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_brightness.png|

        MicroPython Code Block:

            .. code-block:: python

                brightness = chain_mono_0.get_brightness()
        """
        return self._send_value(self.CMD_GET_BRIGHTNESS, default=None)

    def set_rgb_color(self, color: int) -> bool:
        """Set Chain RGB LED color.

        Mono display modules do not provide a separate Chain RGB LED, so this method returns False.

        :param int color: RGB color value.
        :return: Always False.
        :rtype: bool

        UiFlow2 Code Block:

            |set_rgb_color.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_mono_0.set_rgb_color(0xFF0000)
        """
        warnings.warn("MonoChain does not support set_rgb_color()")
        return False

    def get_rgb_color(self) -> int:
        """Get Chain RGB LED color.

        Mono display modules do not provide a separate Chain RGB LED, so this method returns -1.

        :return: Always -1.
        :rtype: int

        UiFlow2 Code Block:

            |get_rgb_color.png|

        MicroPython Code Block:

            .. code-block:: python

                color = chain_mono_0.get_rgb_color()
        """
        warnings.warn("MonoChain does not support get_rgb_color()")
        return -1

    def set_rgb_brightness(self, brightness: int, save: bool = False) -> bool:
        """Set Chain RGB LED brightness.

        Mono display modules do not provide a separate Chain RGB LED, so this method returns False.

        :param int brightness: Brightness value.
        :param bool save: Whether to save the setting to flash.
        :return: Always False.
        :rtype: bool

        UiFlow2 Code Block:

            |set_rgb_brightness.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_mono_0.set_rgb_brightness(50, save=False)
        """
        warnings.warn("MonoChain does not support set_rgb_brightness()")
        return False

    def get_rgb_brightness(self) -> int:
        """Get Chain RGB LED brightness.

        Mono display modules do not provide a separate Chain RGB LED, so this method returns -1.

        :return: Always -1.
        :rtype: int

        UiFlow2 Code Block:

            |get_rgb_brightness.png|

        MicroPython Code Block:

            .. code-block:: python

                brightness = chain_mono_0.get_rgb_brightness()
        """
        warnings.warn("MonoChain does not support get_rgb_brightness()")
        return -1

    def clear_display(self) -> bool:
        """Clear the display.

        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        MicroPython Code Block:

            .. code-block:: python

                success = chain_mono_0.clear_display()
        """
        return self._send_status(self.CMD_CLEAR_DISPLAY, bytes())
