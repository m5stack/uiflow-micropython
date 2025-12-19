# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from . import Keyboard
from . import KeyboardI2C
import micropython
import machine
import M5


class MatrixKeyboard:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MatrixKeyboard, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return

        board_id = M5.getBoard()
        if M5.BOARD.M5Cardputer == board_id:
            self._keyboard = Keyboard()
        elif M5.BOARD.M5CardputerADV == board_id:
            i2c1 = machine.I2C(1, scl=machine.Pin(9), sda=machine.Pin(8), freq=400000)
            self._keyboard = KeyboardI2C(
                i2c1,
                intr_pin=machine.Pin(11, mode=machine.Pin.IN, pull=None),
                mode=KeyboardI2C.ASCII_MODE,
            )
        else:
            self._keyboard = None

        self._keys = []
        self._handler = None
        self._initialized = True

    def get_key(self) -> int:
        if self._keyboard and hasattr(self._keyboard, "_keyevents"):
            if self._keyboard._keyevents:
                keyevent = self._keyboard._keyevents.pop(0)
                return keyevent.keycode
            else:
                return None

        if self._keys:
            return self._keys.pop(0)
        else:
            return None

    def get_string(self) -> str:
        key = self.get_key()
        return chr(key) if key is not None else None

    def is_pressed(self) -> bool:
        if self._keyboard and hasattr(self._keyboard, "_keyevents"):
            if self._keyboard._keyevents:
                return True
            else:
                return False

        if self._keys:
            return True
        else:
            return False

    def set_callback(self, handler) -> None:
        if isinstance(self._keyboard, KeyboardI2C):
            self._keyboard.set_keyevent_callback(handler)
            return
        self._handler = handler

    def tick(self) -> None:
        if not self._keyboard or not hasattr(self._keyboard, "update_key_list"):
            return

        self._keyboard.update_key_list()
        self._keyboard.update_keys_state()
        if self._keyboard.is_change():
            if self._keyboard.is_pressed():
                status = self._keyboard.keys_state()
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
