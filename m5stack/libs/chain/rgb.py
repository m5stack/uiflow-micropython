# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import struct
import warnings
from .chain import ChainBus
from .key import KeyChain


class RGBChain(KeyChain):
    """RGB Chain class for interacting with 8x8 RGB display devices over Chain bus.

    :param ChainBus bus: The Chain bus instance.
    :param int device_id: The device ID of the RGB display on the Chain bus.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from chain import ChainBus
            from chain import RGBChain

            bus2 = ChainBus(2, tx=21, rx=22)
            chain_rgb_0 = RGBChain(bus2, 1)
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

    @staticmethod
    def rgb888_to_rgb565(r: int, g: int, b: int) -> int:
        """Convert 8-bit RGB channel values to RGB565.

        :param int r: Red channel, range 0-255.
        :param int g: Green channel, range 0-255.
        :param int b: Blue channel, range 0-255.
        :return: RGB565 color value.
        :rtype: int

        UiFlow2 Code Block:

            |rgb888_to_rgb565.png|

        MicroPython Code Block:

            .. code-block:: python

                color = RGBChain.rgb888_to_rgb565(255, 0, 0)
        """
        return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

    @staticmethod
    def color888_to_rgb565(color: int) -> int:
        """Convert a 0xRRGGBB color value to RGB565.

        :param int color: 24-bit RGB color value in 0xRRGGBB format.
        :return: RGB565 color value.
        :rtype: int

        UiFlow2 Code Block:

            |color888_to_rgb565.png|

        MicroPython Code Block:

            .. code-block:: python

                color = RGBChain.color888_to_rgb565(0xFF0000)
        """
        if color < 0 or color > 0xFFFFFF:
            raise ValueError("RGB888 color must be in range 0x000000-0xFFFFFF")
        return RGBChain.rgb888_to_rgb565((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)

    @staticmethod
    def rgb565_to_color888(color: int) -> int:
        """Convert an RGB565 color value to a 0xRRGGBB color value.

        :param int color: RGB565 color value.
        :return: 24-bit RGB color value in 0xRRGGBB format.
        :rtype: int
        """
        color = int(color) & 0xFFFF
        r5 = (color >> 11) & 0x1F
        g6 = (color >> 5) & 0x3F
        b5 = color & 0x1F
        r = (r5 << 3) | (r5 >> 2)
        g = (g6 << 2) | (g6 >> 4)
        b = (b5 << 3) | (b5 >> 2)
        return (r << 16) | (g << 8) | b

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

    def _pack_color(self, color) -> int:
        color = int(color)
        return self.color888_to_rgb565(color)

    def _encode_ascii(self, text) -> bytes:
        if isinstance(text, str):
            for ch in text:
                code = ord(ch)
                if code < 32 or code > 127:
                    raise ValueError("RGB Chain only supports ASCII characters 32-127")
            return text.encode()
        data = bytes(text)
        for ch in data:
            if ch < 32 or ch > 127:
                raise ValueError("RGB Chain only supports ASCII characters 32-127")
        return data

    def set_display_mode(self, mode: int = MODE_PIXEL) -> bool:
        """Set the display mode.

        :param int mode: Display mode. Use :attr:`RGBChain.MODE_PIXEL` (0) for pixel mode or :attr:`RGBChain.MODE_SCROLL` (1) for scrolling string mode.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_display_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_rgb_0.set_display_mode(RGBChain.MODE_PIXEL)
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

                mode = chain_rgb_0.get_display_mode()
        """
        return self._send_value(self.CMD_GET_DISPLAY_MODE, default=None)

    def set_pixel(self, x: int, y: int, color=0xFFFFFF) -> bool:
        """Set one pixel color on the 8x8 display.

        :param int x: X coordinate, range 0-7.
        :param int y: Y coordinate, range 0-7.
        :param int color: RGB888 color value in ``0xRRGGBB`` format.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_pixel.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_rgb_0.set_pixel(0, 0, 0xFF0000)
        """
        self._check_xy(x, y)
        color565 = self._pack_color(color)
        payload = bytes([1, self._pack_xy(x, y), color565 & 0xFF, (color565 >> 8) & 0xFF])
        return self._send_status(self.CMD_SET_PIXEL, payload)

    def set_pixels(self, coordinates=None) -> bool:
        """Set multiple pixel colors on the 8x8 display.

        :param coordinates: Iterable of ``(x, y, color)`` values. Supports 1-64 pixels.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_pixels.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_rgb_0.set_pixels(((0, 0, 0xFF0000), (1, 0, 0x00FF00)))
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
                if len(pixel) != 3:
                    continue
                x, y, color = pixel
            except (TypeError, ValueError):
                continue
            self._check_xy(x, y)
            color565 = self._pack_color(color)
            payload.append(self._pack_xy(x, y))
            payload.append(color565 & 0xFF)
            payload.append((color565 >> 8) & 0xFF)
            count += 1
            if count >= 64:
                break
        if count < 1:
            return False
        payload[0] = count
        return self._send_status(self.CMD_SET_PIXEL, bytes(payload))

    def get_pixel(self, x: int, y: int):
        """Get one pixel RGB888 color from the 8x8 display.

        :param int x: X coordinate, range 0-7.
        :param int y: Y coordinate, range 0-7.
        :return: RGB888 color value in 0xRRGGBB format, or None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_pixel.png|

        MicroPython Code Block:

            .. code-block:: python

                color = chain_rgb_0.get_pixel(0, 0)
        """
        self._check_xy(x, y)
        colors = self.get_pixels(((x, y),))
        if colors is None:
            return None
        return colors[0]

    def get_pixels(self, coordinates):
        """Get multiple pixel RGB888 colors from the 8x8 display.

        :param coordinates: Iterable of ``(x, y)`` coordinates. Supports 1-64 pixels.
        :return: Tuple of RGB888 color values in 0xRRGGBB format, or None if failed.
        :rtype: tuple

        UiFlow2 Code Block:

            |get_pixels.png|

        MicroPython Code Block:

            .. code-block:: python

                colors = chain_rgb_0.get_pixels(((0, 0), (1, 0)))
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
        if state and len(response) >= count * 2:
            colors = []
            for i in range(count):
                color565 = response[i * 2] | (response[i * 2 + 1] << 8)
                colors.append(self.rgb565_to_color888(color565))
            return tuple(colors)
        return None

    def set_display_buffer(self, buffer) -> bool:
        """Refresh the full 8x8 display buffer.

        :param buffer: 64 RGB888 color values in 0xRRGGBB format, row-major order, left to right and top to bottom.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_display_buffer.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_rgb_0.set_display_buffer((0xFF0000,) * 64)
        """
        payload = bytearray()
        count = 0
        for color in buffer:
            color565 = self._pack_color(color)
            payload.append(color565 & 0xFF)
            payload.append((color565 >> 8) & 0xFF)
            count += 1
            if count >= 64:
                break
        if count != 64:
            raise ValueError("display buffer must contain 64 colors")
        return self._send_status(self.CMD_SET_DISPLAY_BUFFER, bytes(payload))

    def get_display_buffer(self):
        """Get the full 64-color RGB888 display buffer.

        :return: Tuple of 64 RGB888 color values in 0xRRGGBB format, or None if failed.
        :rtype: tuple

        UiFlow2 Code Block:

            |get_display_buffer.png|

        MicroPython Code Block:

            .. code-block:: python

                buffer = chain_rgb_0.get_display_buffer()
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_DISPLAY_BUFFER, bytes()
        )
        if state and len(response) >= 128:
            colors = []
            for i in range(64):
                color565 = response[i * 2] | (response[i * 2 + 1] << 8)
                colors.append(self.rgb565_to_color888(color565))
            return tuple(colors)
        return None

    def set_matrix(self, matrix) -> bool:
        """Refresh the display from an 8x8 color matrix.

        :param matrix: 8 rows x 8 columns of RGB888 color values in 0xRRGGBB format.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        MicroPython Code Block:

            .. code-block:: python

                success = chain_rgb_0.set_matrix(((0xFF0000,) * 8,) * 8)
        """
        colors = []
        for row in matrix:
            for color in row:
                colors.append(color)
                if len(colors) >= 64:
                    break
            if len(colors) >= 64:
                break
        return self.set_display_buffer(colors)

    def fill(self, color=0x000000) -> bool:
        """Fill all 64 pixels with one RGB888 color.

        :param int color: RGB888 color value in 0xRRGGBB format.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |fill.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_rgb_0.fill(0x0000FF)
        """
        color = int(color)
        self._pack_color(color)
        return self.set_display_buffer((color,) * 64)

    def set_display_char(self, char, x_offset: int = 0, y_offset: int = 0, color=0xFFFFFF) -> bool:
        """Set one ASCII character in pixel mode.

        :param char: Character or ASCII code in range 32-127.
        :param int x_offset: X offset, range 0-7.
        :param int y_offset: Y offset, range 0-7.
        :param int color: RGB888 color value in 0xRRGGBB format.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_display_char.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_rgb_0.set_display_char("R", 1, 0, 0x00FF00)
        """
        if isinstance(char, str):
            if len(char) != 1:
                raise ValueError("char must be a single character")
            char = ord(char)
        char = self._limit(char, 32, 127, "char")
        x_offset = self._limit(x_offset, 0, 7, "x_offset")
        y_offset = self._limit(y_offset, 0, 7, "y_offset")
        color565 = self._pack_color(color)
        payload = struct.pack(
            "<BBBB", char & 0xFF, (x_offset << 4) | y_offset, color565 & 0xFF, color565 >> 8
        )
        return self._send_status(self.CMD_SET_DISPLAY_CHAR, payload)

    def set_scroll_text(
        self,
        text,
        direction: int = SCROLL_DIR_LEFT,
        mode: int = SCROLL_MODE_LOOP,
        speed: int = 100,
        color=0x000000,
    ) -> bool:
        """Set the scrolling ASCII text.

        :param text: ASCII string or bytes to display. Supports ASCII characters 32-127.
        :param int direction: Scroll direction. Use :attr:`RGBChain.SCROLL_DIR_LEFT` (0), :attr:`RGBChain.SCROLL_DIR_RIGHT` (1), :attr:`RGBChain.SCROLL_DIR_UP` (2), or :attr:`RGBChain.SCROLL_DIR_DOWN` (3).
        :param int mode: Scroll mode. Use :attr:`RGBChain.SCROLL_MODE_ONCE` (0), :attr:`RGBChain.SCROLL_MODE_LOOP` (1), or :attr:`RGBChain.SCROLL_MODE_BOUNCE` (3).
        :param int speed: Scroll speed in milliseconds per pixel. Range: 0-65535.
        :param int color: RGB888 text color in 0xRRGGBB format. 0x000000 enables gradient rainbow color for scroll text.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_scroll_text.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_rgb_0.set_scroll_text("M5Stack", RGBChain.SCROLL_DIR_LEFT, RGBChain.SCROLL_MODE_LOOP, 100, 0x000000)
        """
        data = self._encode_ascii(text)
        if len(data) > 243:
            raise ValueError("scroll text is too long")
        direction = self._limit(direction, 0, 3, "direction")
        if mode not in (self.SCROLL_MODE_ONCE, self.SCROLL_MODE_LOOP, self.SCROLL_MODE_BOUNCE):
            warnings.warn("invalid scroll mode, set to loop")
            mode = self.SCROLL_MODE_LOOP
        speed = self._limit(speed, 0, 65535, "speed")
        color565 = self._pack_color(color)
        scroll_mode = ((direction & 0x0F) << 4) | (mode & 0x0F)
        payload = struct.pack(
            "<BBBBBB",
            scroll_mode,
            speed & 0xFF,
            speed >> 8,
            color565 & 0xFF,
            color565 >> 8,
            len(data),
        )
        payload += data
        return self._send_status(self.CMD_SET_SCROLL_TEXT, payload)

    def set_scroll_state(self, state: int = SCROLL_STATE_START) -> bool:
        """Set the scrolling text state.

        :param int state: Scroll state. Use :attr:`RGBChain.SCROLL_STATE_START` (0), :attr:`RGBChain.SCROLL_STATE_PAUSE` (1), or :attr:`RGBChain.SCROLL_STATE_RESET` (2).
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_scroll_state.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_rgb_0.set_scroll_state(RGBChain.SCROLL_STATE_START)
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

                state = chain_rgb_0.get_scroll_state()
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

                success = chain_rgb_0.set_display_rotation(RGBChain.ROTATION_0, save=False)
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

                rotation = chain_rgb_0.get_display_rotation()
        """
        return self._send_value(self.CMD_GET_DISPLAY_ROTATION, default=None)

    def set_brightness(self, brightness: int = 50, save: bool = False) -> bool:
        """Set the screen brightness percentage.

        :param int brightness: Brightness percentage. Range: 0-100.
        :param bool save: Whether to save the setting to flash.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_brightness.png|

        MicroPython Code Block:

            .. code-block:: python

                success = chain_rgb_0.set_brightness(50, save=False)
        """
        brightness = self._limit(brightness, 0, 100, "brightness")
        payload = struct.pack("<BB", brightness & 0xFF, 1 if save else 0)
        return self._send_status(self.CMD_SET_BRIGHTNESS, payload)

    def get_brightness(self) -> int:
        """Get the screen brightness percentage.

        :return: Brightness percentage, range 0-100. Returns None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_brightness.png|

        MicroPython Code Block:

            .. code-block:: python

                brightness = chain_rgb_0.get_brightness()
        """
        return self._send_value(self.CMD_GET_BRIGHTNESS, default=None)

    def clear_display(self) -> bool:
        """Clear the display.

        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        MicroPython Code Block:

            .. code-block:: python

                success = chain_rgb_0.clear_display()
        """
        return self._send_status(self.CMD_CLEAR_DISPLAY, bytes())
