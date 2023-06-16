class Base:
    def __init__(self, parent) -> None:
        self._x = 0
        self._y = 0
        self._w = 0
        self._h = 0
        self._buf = None
        self._parent = parent
        self._event_handler = None

    def set_width(self, w):
        self._w = w

    def set_height(self, h):
        self._h = h

    def set_size(self, w, h):
        self._w = w
        self._h = h

    def set_x(self, x):
        self._x = x

    def set_y(self, y):
        self._y = y

    def get_x(self):
        return self._x

    def get_(self):
        return self._y

    def set_pos(self, x, y):
        self._x = x
        self._y = y

    def _draw(self):
        pass

    def add_event(self, handler):
        self._event_handler = handler

    def handle(self, x, y):
        if self._is_select(x, y) and self._event_handler:
            self._event_handler(None)
            return True
        return False

    def _is_select(self, x, y):
        if x < self._x:
            return False
        if x > (self._x + self._w):
            return False
        if y < self._y:
            return False
        if y > (self._y + self._h):
            return False
        return True
