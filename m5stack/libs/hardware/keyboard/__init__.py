# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import Pin
from collections import namedtuple
from .asciimap import (
    KEY_BACKSPACE,
    KEY_TAB,
    KEY_FN,
    KEY_LEFT_SHIFT,
    KEY_ENTER,
    KEY_LEFT_CTRL,
    KEY_OPT,
    KEY_LEFT_ALT,
    kb_asciimap,
)

Point2D = namedtuple("Point2D", ["x", "y"])
Chart = namedtuple("Chart", ["value", "x_1", "x_2"])
KeyValue = namedtuple("KeyValue", ["first", "second"])

_X_map_chart = (
    Chart(1, 0, 1),
    Chart(2, 2, 3),
    Chart(4, 4, 5),
    Chart(8, 6, 7),
    Chart(16, 8, 9),
    Chart(32, 10, 11),
    Chart(64, 12, 13),
)

_key_value_map = (
    (
        KeyValue(ord("`"), ord("~")),
        KeyValue(ord("1"), ord("!")),
        KeyValue(ord("2"), ord("@")),
        KeyValue(ord("3"), ord("#")),
        KeyValue(ord("4"), ord("$")),
        KeyValue(ord("5"), ord("%")),
        KeyValue(ord("6"), ord("^")),
        KeyValue(ord("7"), ord("&")),
        KeyValue(ord("8"), ord("*")),
        KeyValue(ord("9"), ord("(")),
        KeyValue(ord("0"), ord(")")),
        KeyValue(ord("-"), ord("_")),
        KeyValue(ord("="), ord("+")),
        KeyValue(KEY_BACKSPACE, KEY_BACKSPACE),
    ),
    (
        KeyValue(KEY_TAB, KEY_TAB),
        KeyValue(ord("q"), ord("Q")),
        KeyValue(ord("w"), ord("W")),
        KeyValue(ord("e"), ord("E")),
        KeyValue(ord("r"), ord("R")),
        KeyValue(ord("t"), ord("T")),
        KeyValue(ord("y"), ord("Y")),
        KeyValue(ord("u"), ord("U")),
        KeyValue(ord("i"), ord("I")),
        KeyValue(ord("o"), ord("O")),
        KeyValue(ord("p"), ord("P")),
        KeyValue(ord("["), ord("{")),
        KeyValue(ord("]"), ord("}")),
        KeyValue(ord("\\"), ord("|")),
    ),
    (
        KeyValue(KEY_FN, KEY_FN),
        KeyValue(KEY_LEFT_SHIFT, KEY_LEFT_SHIFT),
        KeyValue(ord("a"), ord("A")),
        KeyValue(ord("s"), ord("S")),
        KeyValue(ord("d"), ord("D")),
        KeyValue(ord("f"), ord("F")),
        KeyValue(ord("g"), ord("G")),
        KeyValue(ord("h"), ord("H")),
        KeyValue(ord("j"), ord("J")),
        KeyValue(ord("k"), ord("K")),
        KeyValue(ord("l"), ord("L")),
        KeyValue(ord(";"), ord(":")),
        KeyValue(ord("'"), ord('"')),
        KeyValue(KEY_ENTER, KEY_ENTER),
    ),
    (
        KeyValue(KEY_LEFT_CTRL, KEY_LEFT_CTRL),
        KeyValue(KEY_OPT, KEY_OPT),
        KeyValue(KEY_LEFT_ALT, KEY_LEFT_ALT),
        KeyValue(ord("z"), ord("Z")),
        KeyValue(ord("x"), ord("X")),
        KeyValue(ord("c"), ord("C")),
        KeyValue(ord("v"), ord("V")),
        KeyValue(ord("b"), ord("B")),
        KeyValue(ord("n"), ord("N")),
        KeyValue(ord("m"), ord("M")),
        KeyValue(ord(","), ord("<")),
        KeyValue(ord("."), ord(">")),
        KeyValue(ord("/"), ord("?")),
        KeyValue(ord(" "), ord(" ")),
    ),
)


class KeysState:
    tab = False
    fn = False
    shift = False
    ctrl = False
    opt = False
    alt = False
    delete = False
    enter = False
    space = False
    modifiers = 0

    def __init__(self) -> None:
        self.word = bytearray(0)
        self.hid_keys = bytearray(0)
        self.modifier_keys = bytearray(0)

    def reset(self):
        self.tab = False
        self.fn = False
        self.shift = False
        self.ctrl = False
        self.opt = False
        self.alt = False
        self.delete = False
        self.enter = False
        self.space = False
        self.modifiers = 0
        self.word = bytearray(0)
        self.hid_keys = bytearray(0)
        self.modifier_keys = bytearray(0)


class Keyboard:
    def __init__(self):
        self.output_list = [Pin(id, Pin.OUT, Pin.PULL_DOWN) for id in (8, 9, 11)]
        self.input_list = [Pin(id, Pin.IN, Pin.PULL_UP) for id in (13, 15, 3, 4, 5, 6, 7)]

        for pin in self.output_list:
            pin.value(0)

        self._set_output(self.output_list, 0)

        self._key_list_buffer = []
        self._key_pos_print_keys = []
        self._key_pos_hid_keys = []
        self._key_pos_modifier_keys = []
        self._keys_state_buffer = KeysState()
        self._is_caps_locked = False
        self._last_key_size = 0

    @staticmethod
    def _set_output(pin_list, output):
        output = output & 0b00000111
        pin_list[0].value(output & 0b00000001)
        pin_list[1].value(output & 0b00000010)
        pin_list[2].value(output & 0b00000100)

    @staticmethod
    def _get_input(pin_list):
        buffer = 0x00
        pin_value = 0x00

        for i in range(7):
            pin_value = 0x00 if pin_list[i].value() == 1 else 0x01
            pin_value = pin_value << i
            buffer = buffer | pin_value

        return buffer

    def getKey(self, point: Point2D):
        ret = 0

        if point.x < 0 or point.y < 0:
            return ret

        if self._keys_state_buffer.ctrl or self._keys_state_buffer.shift or self._is_caps_locked:
            ret = _key_value_map[point.x][point.y].second
        else:
            ret = _key_value_map[point.x][point.y].first
        return ret

    def updateKeyList(self):
        self._key_list_buffer.clear()
        for i in range(8):
            self._set_output(self.output_list, i)
            input_value = self._get_input(self.input_list)

            if input_value != 0:
                # Get X
                for j in range(7):
                    if input_value & (0x01 << j):
                        x = _X_map_chart[j].x_1 if (i > 3) else _X_map_chart[j].x_2

                        # Get Y
                        y = (i - 4) if (i > 3) else i

                        # Keep the same as picture
                        y = -y
                        y = y + 3

                        self._key_list_buffer.append(Point2D(x, y))

    def keyList(self) -> list:
        return self._key_list_buffer

    def getKeyValue(self, point: Point2D) -> KeyValue:
        return _key_value_map[point.y][point.x]

    def isPressed(self) -> bool:
        return len(self._key_list_buffer) > 0

    def isChange(self) -> bool:
        if self._last_key_size is not len(self._key_list_buffer):
            self._last_key_size = len(self._key_list_buffer)
            return True
        else:
            return False

    def isKeyPressed(self, ch):
        if self._key_list_buffer:
            for i in self._key_list_buffer:
                if self.getKeyValue(i).first == ch:
                    return True
        return False

    def updateKeysState(self):
        self._keys_state_buffer.reset()
        self._key_pos_print_keys.clear()
        self._key_pos_hid_keys.clear()
        self._key_pos_modifier_keys.clear()

        # Get special keys
        for i in self._key_list_buffer:
            # modifier
            if self.getKeyValue(i).first == KEY_FN:
                self._keys_state_buffer.fn = True
                continue
            if self.getKeyValue(i).first == KEY_OPT:
                self._keys_state_buffer.opt = True
                continue

            if self.getKeyValue(i).first == KEY_LEFT_CTRL:
                self._keys_state_buffer.ctrl = True
                self._key_pos_modifier_keys.append(i)
                continue

            if self.getKeyValue(i).first == KEY_LEFT_SHIFT:
                self._keys_state_buffer.shift = True
                self._key_pos_modifier_keys.append(i)
                continue

            if self.getKeyValue(i).first == KEY_LEFT_ALT:
                self._keys_state_buffer.alt = True
                self._key_pos_modifier_keys.append(i)
                continue

            # function
            if self.getKeyValue(i).first == KEY_TAB:
                self._keys_state_buffer.tab = True
                self._key_pos_hid_keys.append(i)
                continue

            if self.getKeyValue(i).first == KEY_BACKSPACE:
                self._keys_state_buffer.delete = True
                self._key_pos_hid_keys.append(i)
                continue

            if self.getKeyValue(i).first == KEY_ENTER:
                self._keys_state_buffer.enter = True
                self._key_pos_hid_keys.append(i)
                continue

            if self.getKeyValue(i).first == " ":
                self._keys_state_buffer.space = True

            self._key_pos_hid_keys.append(i)
            self._key_pos_print_keys.append(i)

        for i in self._key_pos_modifier_keys:
            key = self.getKeyValue(i).first
            self._keys_state_buffer.modifier_keys.append(key)

        for k in self._keys_state_buffer.modifier_keys:
            self._keys_state_buffer.modifiers |= 1 << (k - 0x80)

        for i in self._key_pos_hid_keys:
            k = self.getKeyValue(i).first
            if k in (KEY_TAB, KEY_BACKSPACE, KEY_ENTER):
                self._keys_state_buffer.hid_keys.append(k)
                continue
            key = kb_asciimap[k]
            if key:
                self._keys_state_buffer.hid_keys.append(key)

        # Deal with what's left
        for i in self._key_pos_print_keys:
            if (
                self._keys_state_buffer.ctrl
                or self._keys_state_buffer.shift
                or self._is_caps_locked
            ):
                self._keys_state_buffer.word.append(self.getKeyValue(i).second)
            else:
                self._keys_state_buffer.word.append(self.getKeyValue(i).first)

    def keysState(self) -> KeysState:
        return self._keys_state_buffer

    def capslocked(self) -> bool:
        return self._is_caps_locked

    def setCapsLocked(self, isLocked: bool):
        self._is_caps_locked = isLocked
