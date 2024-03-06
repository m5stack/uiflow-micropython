from .keyboard import Keyboard
from micropython import schedule


class MatrixKeyboard(Keyboard):
    def __init__(self) -> None:
        super().__init__()
        self._keys = []
        self._handler = None

    def get_key(self) -> int:
        if self._keys:
            return self._keys.pop(0)
        else:
            return None

    def get_string(self) -> str:
        return chr(self.get_key())

    def is_pressed(self) -> bool:
        if self._keys:
            return True
        else:
            return False

    def set_callback(self, handler) -> None:
        self._handler = handler

    def tick(self) -> None:
        self.updateKeyList()
        self.updateKeysState()
        if self.isChange():
            if self.isPressed():
                status = self.keysState()
                if status.tab:
                    self._keys.append(0x09)
                elif status.enter:
                    self._keys.append(0x0D)
                elif status.delete:
                    self._keys.append(0x08)
                elif status.space:
                    self._keys.append(0x20)
                else:
                    for word in status.word:
                        self._keys.append(word)
        if self.is_pressed() and self._handler:
            schedule(self._handler, self)
