import M5
from . import base


class Image(base.Base):
    def __init__(self, use_sprite=True, parent=M5.Lcd) -> None:
        super().__init__(parent)
        self._src = None
        self._scale_x = 1.0
        self._scale_y = 0.0
        self._use_sprite = use_sprite
        self._sprite = None
        self._sprite_init()

    def set_width(self, w):
        self._sprite_init()
        self._draw(True)

    def set_height(self, h):
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
        self._x = x
        self._draw(False)

    def set_y(self, y):
        self._y = y
        self._draw(False)

    def set_pos(self, x, y):
        self._x = x
        self._y = y
        self._draw(False)

    def set_scale(self, scale_x, scale_y):
        self._scale_x = scale_x
        self._scale_y = scale_y

    def refresh(self):
        self._draw(False)

    def _draw(self, is_decode):
        if self._src is None or len(self._src) is 0:
            return
        if self._sprite:
            is_decode and self._sprite.drawImage(
                self._src, 0, 0, self._w, self._h, 0, 0, self._scale_x, self._scale_y
            )
            self._sprite.push(self._x, self._y)
        else:
            self._parent.drawImage(
                self._src, self._x, self._y, self._w, self._h, 0, 0, self._scale_x, self._scale_y
            )

    def _sprite_init(self):
        if self._use_sprite is False:
            return
        self._sprite and self._sprite.delete()
        if self._w is not 0 and self._h is not 0:
            self._sprite = self._parent.newCanvas(self._w, self._h, 16, True)
            self._src and self._sprite.drawImage(
                self._src, 0, 0, self._w, self._h, 0, 0, self._scale_x, self._scale_y
            )

    def clear(self, color):
        if self._sprite:
            self._sprite.clear(color)
        else:
            self._parent.fillRect(self._x, self._y, self._w, self._h, color)

    def __del__(self):
        self._sprite and self._sprite.delete()
