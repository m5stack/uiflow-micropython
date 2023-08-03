import M5
from . import base


class Image(base.Base):
    def __init__(self, parent=M5.Lcd) -> None:
        super().__init__(parent)
        self._src = None
        self._sprite = None
        self._sprite_init()

    def set_width(self, w):
        if self._w is w:
            return
        self._sprite_init()
        self._draw(True)

    def set_height(self, h):
        if self._h is h:
            return
        self._sprite_init()
        self._draw(True)

    def set_size(self, w, h):
        super().set_size(w, h)
        self._sprite_init()
        self._draw(True)

    def set_src(self, src):
        self._src = src
        self._draw(True)

    def set_x(self, x):
        if self._x is x:
            return
        self._x = x
        self._draw(False)

    def set_y(self, y):
        if self._y is y:
            return
        self._y = y
        self._draw(False)

    def set_pos(self, x, y):
        if self._x is x and self._y is y:
            return
        self._x = x
        self._y = y
        self._draw(False)

    def _draw(self, is_decode):
        if self._src is None or len(self._src) is 0:
            return
        if self._sprite:
            is_decode and self._sprite.drawImage(self._src, 0, 0)
            self._sprite.push(self._x, self._y)
        else:
            self._parent.drawImage(self._src, self._x, self._y)

    def _sprite_init(self):
        self._sprite and self._sprite.delete()
        if self._w is not 0 and self._h is not 0:
            self._sprite = self._parent.newCanvas(self._w, self._h, 16, True)
            self._src and self._sprite.drawImage(self._src, 0, 0)
