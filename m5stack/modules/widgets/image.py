import M5
from . import base


class Image(base.Base):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self._src = None

    def set_src(self, src):
        self._src = src
        self._draw()

    def set_x(self, x):
        self._x = x
        self._draw()

    def set_y(self, y):
        self._y = y
        self._draw()

    def set_pos(self, x, y):
        self._x = x
        self._y = y
        self._draw()

    def _draw(self):
        self._src and M5.Lcd.drawImage(self._src, self._x, self._y)
