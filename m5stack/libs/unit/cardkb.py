from micropython import schedule

class CardKB:
    def __init__(self, i2c, address=0x5F):
        self._i2c = i2c
        self._addr = address
        self._keys = []
        self._handler = None
        try:
            while True:
                buf = self._i2c.readfrom(self._addr, 1)
                if buf[0] is 0x00:
                    break
        except OSError:
            pass

    def _get_key(self):
        buf = self._i2c.readfrom(self._addr, 1)
        if buf[0] is not 0:
            self._keys.append(buf[0])
            return True
        return False

    def get_key(self):
        if self._keys:
            return self._keys.pop(0)
        else:
            if self._get_key():
                return None
            else:
                return self._keys.pop(0)

    def get_string(self):
        return str(self.get_key())

    def is_pressed(self) -> bool:
        if self._keys:
            return True
        return self._get_key()

    def set_callback(self, handler):
        self._handler = handler

    def tick(self):
        if self.is_pressed() and self._handler:
            schedule(self._handler, self)
