# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import M5
from .headless import Headless_Startup


_FONT_CHARS = "0123456789"
_FONT_ROWS = (
    b"\x07\x05\x05\x05\x07"  # 0
    b"\x02\x06\x02\x02\x07"  # 1
    b"\x06\x01\x02\x04\x07"  # 2
    b"\x06\x01\x02\x01\x06"  # 3
    b"\x05\x05\x07\x01\x01"  # 4
    b"\x07\x04\x06\x01\x06"  # 5
    b"\x03\x04\x07\x05\x07"  # 6
    b"\x07\x01\x02\x02\x02"  # 7
    b"\x07\x05\x07\x05\x07"  # 8
    b"\x07\x05\x07\x01\x06"  # 9
)


class MatrixStatusDisplay:
    def _draw_wifi(self, level: int = 3) -> None:
        if level >= 3:
            for x, y, w, h in ((3, 2, 10, 2), (1, 4, 3, 2), (12, 4, 3, 2)):
                M5.Lcd.fillRect(x, y, w, h, 0xFFFFFF)
        if level >= 2:
            for x, y, w, h in ((4, 7, 8, 2), (2, 9, 3, 2), (11, 9, 3, 2)):
                M5.Lcd.fillRect(x, y, w, h, 0xFFFFFF)
        M5.Lcd.fillRect(7, 12, 2, 2, 0xFFFFFF)

    def _draw_check(self) -> None:
        for x, y in ((2, 8), (4, 10), (6, 11), (8, 9), (10, 7), (12, 5)):
            M5.Lcd.fillRect(x, y, 3, 3, 0xFFFFFF)

    def _draw_cross(self) -> None:
        for offset in range(0, 10, 2):
            M5.Lcd.fillRect(3 + offset, 3 + offset, 2, 2, 0xFFFFFF)
            M5.Lcd.fillRect(11 - offset, 3 + offset, 2, 2, 0xFFFFFF)

    def _draw_download(self) -> None:
        M5.Lcd.fillRect(7, 2, 2, 8, 0xFFFFFF)
        for x, y in ((3, 7), (5, 9), (7, 11), (9, 9), (11, 7)):
            M5.Lcd.fillRect(x, y, 2, 2, 0xFFFFFF)
        M5.Lcd.fillRect(3, 14, 10, 2, 0xFFFFFF)

    def _draw_char(self, char: str, x: int, y: int) -> None:
        glyph_index = _FONT_CHARS.find(char)
        if glyph_index < 0:
            return
        glyph_offset = glyph_index * 5
        for row in range(5):
            bits = _FONT_ROWS[glyph_offset + row]
            for column in range(3):
                if bits & (1 << (2 - column)):
                    M5.Lcd.fillRect(x + column, y + row, 1, 1, 0xFFFFFF)

    def show_access_code(self, access_code: str) -> None:
        text = str(access_code)
        M5.Lcd.clear(0x000000)
        if len(text) != 6 or any(char < "0" or char > "9" for char in text):
            self._draw_cross()
            return

        rows = (text[:3], text[3:])
        for row_index, row_text in enumerate(rows):
            y = 2 + row_index * 7
            for column, char in enumerate(row_text):
                self._draw_char(char, 1 + column * 5, y)

    def show_connecting(self, frame: int) -> None:
        M5.Lcd.clear(0x000000)
        self._draw_wifi((1, 2, 3, 2)[frame % 4])

    def fill_color(self, color: int) -> None:
        self.set_color(0, color)

    def set_color(self, index: int, color: int) -> None:
        M5.Lcd.clear(0x000000)
        if color == 0x000000:
            return
        if color == 0xFF0000:
            self._draw_cross()
        elif color == 0x00FF00:
            self._draw_check()
        elif color == 0x0000FF:
            self._draw_wifi()
        elif color == 0xFFFF00:
            self._draw_download()
        else:
            M5.Lcd.clear(0xFFFFFF)

    def set_brightness(self, brightness: int) -> None:
        M5.Lcd.setBrightness(min(255, brightness * 255 // 100))


class CoreMatrix_Startup(Headless_Startup):
    def __init__(self) -> None:
        self._board = M5.getBoard()
        self._wifi_led = None
        self.rgb = MatrixStatusDisplay()
        self.rgb.set_brightness(50)
        self.rgb.fill_color(self.COLOR_BLUE)

    def show_access_code(self, access_code: str) -> None:
        self.rgb.show_access_code(access_code)

    def show_connecting(self, frame: int) -> None:
        self.rgb.show_connecting(frame)

    def show_error(self, ssid: str, error: str) -> None:
        super().show_error(ssid, error)
        self.rgb.fill_color(self.COLOR_RED)
