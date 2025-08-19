# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from . import Keyboard
import micropython


class MatrixKeyboard(Keyboard):
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return

        super().__init__()
        self._keys = []
        self._handler = None
        self._initialized = True

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
        self.update_key_list()
        self.update_keys_state()
        if self.is_change():
            if super().is_pressed():
                status = self.keys_state()
                if status.tab:
                    self._keys.append(0x09)
                elif status.enter:
                    self._keys.append(0x0D)
                elif status.delete:
                    self._keys.append(0x08)
                elif status.space:
                    self._keys.append(0x20)
                elif status.fn:
                    if len(status.word) == 0:
                        return
                    if status.word[0] == 47:  # right
                        self._keys.append(183)
                    elif status.word[0] == 44:  # left
                        self._keys.append(180)
                    elif status.word[0] == 59:  # up
                        self._keys.append(181)
                    elif status.word[0] == 46:  # down
                        self._keys.append(182)
                    elif status.word[0] == 96:  # ESC
                        self._keys.append(0x1B)
                else:
                    for word in status.word:
                        self._keys.append(word)
        if self.is_pressed() and self._handler:
            micropython.schedule(self._handler, self)
