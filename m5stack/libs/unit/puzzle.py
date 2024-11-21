# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.neopixel.ws2812 import WS2812
import random
import time


class PuzzleUnit(WS2812):
    """
    note:
        en: Unit Puzzle is a multi-color light control unit consisting of an 8x8 RGB array made up of 64 WS2812E RGB LEDs. Each LED is separated by a grid structure to prevent interference between adjacent lights, ensuring the light effect is clearer and purer.

    details:
        color: "#0FE6D7"
        link: https://docs.m5stack.com/en/unit/Unit-Puzzle
        image: https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/products/unit/Unit-Puzzle/4.webp
        category: Unit

    example:
        - ../../../examples/unit/puzzle/puzzle_core2_example.py

    m5f2:
        - unit/puzzle/puzzle_core2_example.m5f2
    """

    def __init__(self, port: tuple, led_board_count: int = 1) -> None:
        """
        note:
            en: Initialize the PuzzleUnit.

        params:
            port:
                note: The port to connect the WS2812 LED strip.
            led_board_count:
                note: Number of connected PuzzleUnit boards.
        """
        self.led_per_board = 64
        self.led_board_count = led_board_count
        self.total_led = self.led_per_board * led_board_count
        WS2812.__init__(self, port[1], self.total_led)
        self.set_brightness(10)

    def set_color_from(
        self, board_num: int, begin: int, end: int, rgb: int, per_delay: int = 0
    ) -> None:
        """
        note:
            en: Set color on a range of LEDs starting from a specified board and range.

        params:
            board_num:
                note: The board number (starting from 1) where the LEDs are located.
            begin:
                note: The starting LED index on the board.
            end:
                note: The ending LED index on the board.
            rgb:
                note: The color to set, specified in RGB format.
            per_delay:
                note: Delay in milliseconds between setting each LED color.
        """
        begin, end, step = self._get_led_range(board_num, begin, end)
        for i in range(begin, end + step, step):
            self._set_color(i, rgb)
            time.sleep_ms(per_delay)

    def _set_color(self, index: int, rgb: int) -> None:
        super().set_color(index - 1, rgb)

    def set_color(self, board_num: int, index: int, rgb: int) -> None:
        """
        note:
            en: Set the color of a single LED.

        params:
            board_num:
                note: The board number (starting from 1) where the LED is located.
            index:
                note: The LED index to set the color on (1-based index).
            rgb:
                note: The color to set, specified in RGB format.
        """
        super().set_color((board_num - 1) * self.led_per_board + index - 1, rgb)

    def set_color_saturation_from(
        self, board_num: int, begin: int, end: int, rgb_color: int, per_delay: int = 0
    ) -> None:
        """
        note:
            en: Gradually change the color saturation from begin to end on a range of LEDs.

        params:
            board_num:
                note: The board number (starting from 1) where the LEDs are located.
            begin:
                note: The starting LED index on the board.
            end:
                note: The ending LED index on the board.
            rgb_color:
                note: The base RGB color to apply saturation to.
            per_delay:
                note: Delay in milliseconds between each LED color change.
        """
        begin, end, step = self._get_led_range(board_num, begin, end)
        for i in range(begin, end + step, step):
            saturation = 100 - ((i - begin) * step)
            self._set_color(i, self._color_saturation(rgb_color, saturation))
            time.sleep_ms(per_delay)

    def _color_saturation(self, rgb: int, saturation: float) -> int:
        """
        note:
            en: Adjust the color saturation for a given RGB color.

        params:
            rgb:
                note: The base RGB color to adjust.
            saturation:
                note: The saturation percentage (0-100).
        return:
            note: The adjusted RGB value after applying the saturation.
        """
        factor = saturation / 100
        r = int(((rgb >> 16) & 0xFF) * factor)
        g = int(((rgb >> 8) & 0xFF) * factor)
        b = int((rgb & 0xFF) * factor)
        return (r << 16) | (g << 8) | b

    def set_color_running_from(
        self, board_num: int, begin: int, end: int, rgb: int, per_delay: int = 0
    ) -> None:
        """
        note:
            en: Create a running color effect on a range of LEDs from begin to end.

        params:
            board_num:
                note: The board number (starting from 1) where the LEDs are located.
            begin:
                note: The starting LED index on the board.
            end:
                note: The ending LED index on the board.
            rgb:
                note: The color to set, specified in RGB format.
            per_delay:
                note: Delay in milliseconds between setting each LED color.
        """
        begin, end, step = self._get_led_range(board_num, begin, end)
        for i in range(begin, end + step, step):
            self._set_color(i, rgb)
            time.sleep_ms(per_delay)
            self._set_color(i, 0x00)

    def set_random_color_random_led_from(self, board_num: int, begin: int, end: int) -> None:
        """
        note:
            en: Set a random color to each LED within the specified range.

        params:
            board_num:
                note: The board number (starting from 1) where the LEDs are located.
            begin:
                note: The starting LED index on the board.
            end:
                note: The ending LED index on the board.
        """
        begin, end, step = self._get_led_range(board_num, begin, end)
        for i in range(begin, end + step, step):
            color_in = random.randint(0, 0xFFFFFF)
            self._set_color(i, color_in)

    def _get_led_range(self, board_num: int, begin: int, end: int) -> list[int]:
        """
        note:
            en: Calculate the range of LED indices for a given board and range.

        params:
            board_num:
                note: The board number (starting from 1).
            begin:
                note: The starting LED index.
            end:
                note: The ending LED index.

        return:
            note: A list containing the start index, end index, and step direction for the range.

        raises:
            ValueError:
                note: If the begin or end index is out of range for the specified board.
        """
        if begin not in range(1, self.led_per_board + 1) or end not in range(
            1, self.led_per_board + 1
        ):
            raise ValueError("begin or end is out of range")
        start_index = (board_num - 1) * self.led_per_board
        begin += start_index
        end += start_index
        return [
            max(board_num * self.led_per_board - 63, min(begin, self.total_led)),
            max(board_num * self.led_per_board - 63, min(end, self.total_led)),
            1 if begin < end else -1,
        ]

    def set_screen(self, board_num: int, color_list: list) -> None:
        """
        note:
            en: Set the screen of a specific board with a list of colors.

        params:
            board_num:
                note: The board number to which the colors should be applied.
            color_list:
                note: A list of colors to apply to the screen.
        """
        start_index = (board_num - 1) * self.led_per_board
        color_list = color_list[: self.led_per_board]

        for i in range(len(color_list)):
            offset = (start_index + i) * self.bpp  # 起始偏移加上当前 LED 偏移
            if self.bpp == 3:
                v = self.color_to_rgb(color_list[i])
            elif self.bpp == 4:
                v = self.color_to_wrgb(color_list[i])
            for j in range(self.bpp):
                self.buf[offset + self.ORDER[j]] = v[j]

        self.write()
