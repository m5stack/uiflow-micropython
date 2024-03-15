# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import M5


class Label:
    LEFT_ALIGNED = 0
    CENTER_ALIGNED = 1
    RIGHT_ALIGNED = 2

    LONG_WARP = 0
    LONG_DOT = 1
    LONG_CLIP = 2

    def __init__(
        self,
        text: str,
        x: int,
        y: int,
        w: int = 0,
        h: int = 0,
        size: float = 1.0,
        font_align: int = LEFT_ALIGNED,
        fg_color: int = 0xFFFFFF,
        bg_color: int = 0x000000,
        font=M5.Lcd.FONTS.DejaVu12,
        parent=M5.Lcd,
    ) -> None:
        self._text = text
        self._texts = []
        self._x = x
        self._y = y
        self._max_w = w
        self._max_h = h
        self._size = size
        self._font_align = font_align
        self._fg_color = fg_color
        self._bg_color = bg_color
        self._font = font
        self._parent = parent
        self._long_fn = self._long_wrap
        self._load_font()
        self._line_spacing = int(self._parent.fontHeight() * 1.2)

    def _erase_helper(self):
        for text in self._texts:
            w = self._parent.textWidth(text)
            h = self._parent.fontHeight()
            if self._font_align == self.LEFT_ALIGNED:
                self._parent.fillRect(self._x, self._y, w, h, self._bg_color)
            elif self._font_align == self.CENTER_ALIGNED:
                self._parent.fillRect(self._x - int(w / 2), self._y, w, h, self._bg_color)
            elif self._font_align == self.RIGHT_ALIGNED:
                self._parent.fillRect(self._x - w, self._y, w, h, self._bg_color)

    def setText(self, text=None) -> None:
        self._load_font()
        self._erase_helper()
        self._texts.clear()
        if text is not None:
            self._text = text
        self._long_fn()
        self._parent.setTextColor(self._fg_color, self._bg_color)
        yy = self._y
        for text in self._texts:
            if self._font_align == self.LEFT_ALIGNED:
                self._parent.drawString(text, self._x, yy)
            elif self._font_align == self.CENTER_ALIGNED:
                self._parent.drawCenterString(text, self._x, yy)
            elif self._font_align == self.RIGHT_ALIGNED:
                self._parent.drawRightString(text, self._x, yy)
            else:
                print("Warning: unknown alignment")
            yy += self._line_spacing

    def _long_dot(self):
        w = self._parent.textWidth(self._text)
        start = 1
        end = 0
        if w < self._max_w:
            self._texts.append(self._text)
            return

        while True:
            ww = self._parent.textWidth(self._text[0:end])
            if ww > int(self._max_w / 2):
                end -= 1
                break
            end += 1

        start = end
        w = self._parent.textWidth("...")
        while True:
            ww = self._parent.textWidth(self._text[start:-1])
            if ww < (int(self._max_w / 2) - w):
                start += 1
                break
            start += 1

        self._texts.append(self._text[0:end] + "..." + self._text[start:])

    def _long_wrap(self):
        if self._parent.textWidth(self._text) < self._max_w:
            self._texts.append(self._text)
            return

        start = 0
        end = 0
        while end < len(self._text):
            ww = self._parent.textWidth(self._text[start:end])
            if ww > self._max_w:
                self._texts.append(self._text[start:end])
                start = end
                end = end + 1
            end += 1

        if start is not end:
            self._texts.append(self._text[start:end])

        text_h = self._parent.fontHeight()
        for _ in self._texts:
            if sum(text_h for _ in self._texts) > self._max_h:
                self._texts.pop()

    def setTextColor(self, fg_color, bg_color):
        self._fg_color = fg_color
        self._bg_color = bg_color

    def _load_font(self):
        if type(self._font) == bytes:
            self._parent.unloadFont()
            self._parent.loadFont(self._font)
        elif type(self._font) == str:
            self._parent.loadFont(self._font)
        else:
            self._parent.setFont(self._font)

    def setLongMode(self, mode):
        if mode is self.LONG_DOT:
            self._long_fn = self._long_dot
        elif mode is self.LONG_WARP:
            self._long_fn = self._long_wrap

    def setPos(self, x, y):
        self._x = x
        self._y = y
        self.setText(None)

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def setX(self, x):
        self._x = x

    def setY(self, y):
        self._y = y
