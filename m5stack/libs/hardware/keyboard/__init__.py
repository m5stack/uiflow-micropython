# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
import micropython
from collections import namedtuple
from . import asciimap
from driver import tca8418

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
        KeyValue(0x08, 0x08),
    ),
    (
        KeyValue(asciimap.KEY_TAB, asciimap.KEY_TAB),
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
        KeyValue(asciimap.KEY_FN, asciimap.KEY_FN),
        KeyValue(asciimap.KEY_LEFT_SHIFT, asciimap.KEY_LEFT_SHIFT),
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
        KeyValue(0x0A, 0x0A),
    ),
    (
        KeyValue(asciimap.KEY_LEFT_CTRL, asciimap.KEY_LEFT_CTRL),
        KeyValue(asciimap.KEY_LEFT_OPT, asciimap.KEY_LEFT_OPT),
        KeyValue(asciimap.KEY_LEFT_ALT, asciimap.KEY_LEFT_ALT),
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
    def __init__(
        self, row_pins: tuple = (8, 9, 11), col_pins: tuple = (13, 15, 3, 4, 5, 6, 7)
    ) -> None:
        self.output_list = [
            machine.Pin(pin, machine.Pin.OUT, machine.Pin.PULL_DOWN) for pin in row_pins
        ]
        self.input_list = [
            machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP) for pin in col_pins
        ]

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
        n = len(pin_list)
        mask = (1 << n) - 1
        output = output & mask
        for i in range(n):
            pin_list[i].value(output & (1 << i))

    @staticmethod
    def _get_input(pin_list):
        buffer = 0x00
        pin_value = 0x00
        n = len(pin_list)

        for i in range(n):
            pin_value = 0x00 if pin_list[i].value() == 1 else 0x01
            pin_value = pin_value << i
            buffer = buffer | pin_value

        return buffer

    def get_key(self, point: Point2D):
        ret = 0

        if point.x < 0 or point.y < 0:
            return ret

        if self._keys_state_buffer.ctrl or self._keys_state_buffer.shift or self._is_caps_locked:
            ret = _key_value_map[point.x][point.y].second
        else:
            ret = _key_value_map[point.x][point.y].first
        return ret

    def update_key_list(self):
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

    def key_list(self) -> list:
        return self._key_list_buffer

    def get_key_value(self, point: Point2D) -> KeyValue:
        return _key_value_map[point.y][point.x]

    def is_pressed(self) -> bool:
        return len(self._key_list_buffer) > 0

    def is_change(self) -> bool:
        if self._last_key_size is not len(self._key_list_buffer):
            self._last_key_size = len(self._key_list_buffer)
            return True
        else:
            return False

    def is_key_pressed(self, ch):
        if self._key_list_buffer:
            for i in self._key_list_buffer:
                if self.get_key_value(i).first == ch:
                    return True
        return False

    def update_keys_state(self):
        self._keys_state_buffer.reset()
        self._key_pos_print_keys.clear()
        self._key_pos_hid_keys.clear()
        self._key_pos_modifier_keys.clear()

        # Get special keys
        for i in self._key_list_buffer:
            # modifier
            if self.get_key_value(i).first == asciimap.KEY_FN:
                self._keys_state_buffer.fn = True
                continue
            if self.get_key_value(i).first == asciimap.KEY_LEFT_OPT:
                self._keys_state_buffer.opt = True
                continue

            if self.get_key_value(i).first == asciimap.KEY_LEFT_CTRL:
                self._keys_state_buffer.ctrl = True
                self._key_pos_modifier_keys.append(i)
                continue

            if self.get_key_value(i).first == asciimap.KEY_LEFT_SHIFT:
                self._keys_state_buffer.shift = True
                self._key_pos_modifier_keys.append(i)
                continue

            if self.get_key_value(i).first == asciimap.KEY_LEFT_ALT:
                self._keys_state_buffer.alt = True
                self._key_pos_modifier_keys.append(i)
                continue

            # function
            if self.get_key_value(i).first == asciimap.KEY_TAB:
                self._keys_state_buffer.tab = True
                self._key_pos_hid_keys.append(i)
                continue

            if self.get_key_value(i).first == asciimap.KEY_BACKSPACE:
                self._keys_state_buffer.delete = True
                self._key_pos_hid_keys.append(i)
                continue

            if self.get_key_value(i).first == asciimap.KEY_ENTER:
                self._keys_state_buffer.enter = True
                self._key_pos_hid_keys.append(i)
                continue

            if self.get_key_value(i).first == " ":
                self._keys_state_buffer.space = True

            self._key_pos_hid_keys.append(i)
            self._key_pos_print_keys.append(i)

        for i in self._key_pos_modifier_keys:
            key = self.get_key_value(i).first
            self._keys_state_buffer.modifier_keys.append(key)

        for k in self._keys_state_buffer.modifier_keys:
            self._keys_state_buffer.modifiers |= 1 << (k - 0x80)

        for i in self._key_pos_hid_keys:
            k = self.get_key_value(i).first
            if k in (asciimap.KEY_TAB, asciimap.KEY_BACKSPACE, asciimap.KEY_ENTER):
                self._keys_state_buffer.hid_keys.append(k)
                continue
            key = asciimap.kb_asciimap[k]
            if key:
                self._keys_state_buffer.hid_keys.append(key)

        # Deal with what's left
        for i in self._key_pos_print_keys:
            if (
                self._keys_state_buffer.ctrl
                or self._keys_state_buffer.shift
                or self._is_caps_locked
            ):
                self._keys_state_buffer.word.append(self.get_key_value(i).second)
            else:
                self._keys_state_buffer.word.append(self.get_key_value(i).first)

    def keys_state(self) -> KeysState:
        return self._keys_state_buffer

    def capslocked(self) -> bool:
        return self._is_caps_locked

    def set_caps_locked(self, isLocked: bool):
        self._is_caps_locked = isLocked


class _KeyEventConverter:
    state: bool = False
    row: int = 0
    col: int = 0

    def __init__(self, value) -> None:
        self.decode(value)

    def decode(self, value: int) -> str:
        # Decode the key event from a byte value
        self.state = bool(value & 0x80)
        value &= 0x7F
        value -= 1
        self.row = value // 10
        self.col = value % 10

        # Convert 7 * 8 matrix to 14 * 4
        col = self.row * 2
        if self.col > 3:
            col += 1

        row = (self.col + 4) % 4

        self.row = row
        self.col = col

    def __str__(self) -> str:
        return f"_KeyEventConverter(({self.row}, {self.col}), {'pressed' if self.state else 'released'})"


class KeyEvent:
    state: bool = False
    row: int = 0
    col: int = 0
    keycode: int = 0
    modifier_mask: int = 0

    def __init__(
        self,
        raw_event: _KeyEventConverter,
        modifier_mask,
        fn_state: bool = False,
        is_capslock_locked=False,
    ) -> None:
        self.convert(raw_event, modifier_mask, fn_state, is_capslock_locked)

    def convert(
        self, raw_event: _KeyEventConverter, modifier_mask, fn_state: bool, is_capslock_locked
    ) -> None:
        self.state = raw_event.state
        self.row = raw_event.row
        self.col = raw_event.col
        self.modifier_mask = modifier_mask

        if fn_state and (self.row, self.col) != (0, 2):  # FN key
            if (self.row, self.col) == (0, 0):  # ESC key
                self.keycode = 0x1B  # ascii ESC
            elif (self.row, self.col) == (0, 13):  # delete key
                self.keycode = 0x7F  # ascii DEL
            elif (self.row, self.col) == (2, 11):  # up key
                self.keycode = asciimap.KEY_UP
            elif (self.row, self.col) == (3, 10):  # left key
                self.keycode = asciimap.KEY_LEFT
            elif (self.row, self.col) == (3, 11):  # down key
                self.keycode = asciimap.KEY_DOWN
            elif (self.row, self.col) == (3, 12):  # right key
                self.keycode = asciimap.KEY_RIGHT
            return

        # self.toggle_state = (modifier_mask & asciimap.KEY_MOD_LCTRL) or (modifier_mask & asciimap.KEY_MOD_LSHIFT) or capslock_state or is_capslock_locked
        if (
            self.modifier_mask & (asciimap.KEY_MOD_LSHIFT | asciimap.KEY_MOD_RSHIFT)
            or is_capslock_locked
        ):
            self.keycode = _key_value_map[self.row][self.col].second
        else:
            self.keycode = _key_value_map[self.row][self.col].first

    def __str__(self) -> str:
        return f"KeyEvent(({self.row}, {self.col}), {'pressed' if self.state else 'released'}, keycode: {self.keycode}, modifier_mask: {self.modifier_mask})"


class HIDInputReport:

    """HID Input Report for keyboard events. only supports cardputer keyboard layout."""

    scancode = (
        # Row 0
        b"\x35"  # Keyboard ` and ~
        b"\x1e"  # Keyboard 1 and !
        b"\x1f"  # Keyboard 2 and @
        b"\x20"  # Keyboard 3 and #
        b"\x21"  # Keyboard 4 and $
        b"\x22"  # Keyboard 5 and %
        b"\x23"  # Keyboard 6 and ^
        b"\x24"  # Keyboard 7 and &
        b"\x25"  # Keyboard 8 and *
        b"\x26"  # Keyboard 9 and (
        b"\x27"  # Keyboard 0 and )
        b"\x2d"  # Keyboard - and _
        b"\x2e"  # Keyboard = and +
        b"\x2a"  # Keyboard DELETE (Backspace)
        # Row 1
        b"\x2b"  # Keyboard TAB
        b"\x14"  # Keyboard q and Q
        b"\x1a"  # Keyboard w and W
        b"\x08"  # Keyboard e and E
        b"\x15"  # Keyboard r and R
        b"\x17"  # Keyboard t and T
        b"\x1c"  # Keyboard y and Y
        b"\x18"  # Keyboard u and U
        b"\x0f"  # Keyboard i and I
        b"\x12"  # Keyboard o and O
        b"\x13"  # Keyboard p and P
        b"\x2f"  # Keyboard [ and {
        b"\x30"  # Keyboard ] and }
        b"\x31"  # Keyboard \ and |
        # Row 2
        b"\x00"  # No key pressed (FN POSITION)
        b"\x00"  # No key pressed (SHIFT POSITION)
        b"\x04"  # Keyboard a and A
        b"\x16"  # Keyboard s and S
        b"\x07"  # Keyboard d and D
        b"\x09"  # Keyboard f and F
        b"\x0a"  # Keyboard g and G
        b"\x0b"  # Keyboard h and H
        b"\x0d"  # Keyboard j and J
        b"\x0e"  # Keyboard k and K
        b"\x0c"  # Keyboard l and L
        b"\x33"  # Keyboard ; and :
        b"\x34"  # Keyboard ' and "
        b"\x28"  # Keyboard ENTER (Return)
        # Row 3
        b"\x00"  # No key pressed (CTRL POSITION)
        b"\x00"  # No key pressed (META/OPT POSITION)
        b"\x00"  # No key pressed (ALT POSITION)
        b"\x2c"  # Keyboard z and Z
        b"\x2d"  # Keyboard x and X
        b"\x2e"  # Keyboard c and C
        b"\x2f"  # Keyboard v and V
        b"\x30"  # Keyboard b and B
        b"\x31"  # Keyboard n and N
        b"\x32"  # Keyboard m and M
        b"\x33"  # Keyboard , and <
        b"\x34"  # Keyboard . and >
        b"\x35"  # Keyboard / and ?
        b"\x2c"  # Keyboard SPACE (Spacebar)
    )

    def __init__(self):
        self.modifiers = 0
        self.keypresses = bytearray(6)
        self.done = False

    def set_modifier_mask(self, mask: int):
        self.modifiers = mask

    def set_key(self, index: int, key: int):
        if 0 <= index < 6:
            self.keypresses[index] = key

    def append_key(self, row: int, col: int, fn_state: bool = False):
        for i in range(6):
            if self.keypresses[i] == 0:
                keycode = self.scancode[row * 14 + col]
                if fn_state:
                    if (row, col) == (0, 0):  # ESC key
                        keycode = 0x29
                    elif (row, col) == (0, 13):  # delete key
                        keycode = 0x2A
                    elif (row, col) == (2, 11):  # up key
                        keycode = 0x52
                    elif (row, col) == (3, 10):  # left key
                        keycode = 0x50
                    elif (row, col) == (3, 11):  # down key
                        keycode = 0x51
                    elif (row, col) == (3, 12):  # right key
                        keycode = 0x4F

                self.set_key(i, keycode)
                if i == 5:
                    self.done = True
                return

    def __str__(self) -> str:
        return f"HIDInputReport(modifiers: {self.modifiers}, keys: {self.keypresses})"


class KeyboardI2C:
    ASCII_MODE = 0
    HID_MODE = 1

    def __init__(
        self, i2c: machine.I2C, address: int = 0x34, intr_pin=None, mode=ASCII_MODE
    ) -> None:
        super().__init__()
        self._is_caps_locked = False

        self._modifier_mask = 0
        self._shift_state = False
        self._fn_state = False
        self._keyevent_converter = _KeyEventConverter(0)

        self._mode = mode
        self._tick_handler = self._ascii_handler if mode == self.ASCII_MODE else self._hid_handler
        self._keyevents = []
        self._hid_reports = []

        self._hid_report_callback = None
        self._keyevent_callback = None

        self._i2c = i2c
        self._address = address
        self._intr_pin = intr_pin
        self._tca = tca8418.TCA8418(i2c, address)

        keypad_pins = (
            tca8418.TCA8418.R0,
            tca8418.TCA8418.R1,
            tca8418.TCA8418.R2,
            tca8418.TCA8418.R3,
            tca8418.TCA8418.R4,
            tca8418.TCA8418.R5,
            tca8418.TCA8418.R6,
            tca8418.TCA8418.C0,
            tca8418.TCA8418.C1,
            tca8418.TCA8418.C2,
            tca8418.TCA8418.C3,
            tca8418.TCA8418.C4,
            tca8418.TCA8418.C5,
            tca8418.TCA8418.C6,
            tca8418.TCA8418.C7,
        )

        # make them inputs with pullups
        for pin in keypad_pins:
            self._tca.keypad_mode[pin] = True
            # make sure the key pins generate FIFO events
            self._tca.enable_int[pin] = True
            # we will stick events into the FIFO queue
            self._tca.event_mode_fifo[pin] = True

        if self._intr_pin is not None:
            self._intr_pin.init(machine.Pin.IN, pull=None)
            self._intr_pin.irq(self._irq_handler, machine.Pin.IRQ_FALLING)

        # turn on INT output pin
        self._tca.key_intenable = True

    def deinit(self):
        if self._intr_pin is not None:
            self._intr_pin.irq(None)
        self._tca.key_int = True  # clear the IRQ by writing 1 to it

    def set_hid_report_callback(self, callback):
        """
        Set a callback function to be called when a HID report is ready.
        The callback should accept one argument, which is the HIDInputReport object.
        """
        self._hid_report_callback = callback

    def set_keyevent_callback(self, callback):
        """
        Set a callback function to be called when a key event is ready.
        The callback should accept one argument, which is the KeyEvent object.
        """
        self._keyevent_callback = callback

    def _irq_handler(self, pin: machine.Pin):
        if self._tca.key_int:
            if self._tca.events_count:
                events = bytearray()
                while self._tca.events_count:
                    events.append(self._tca.next_event)
                micropython.schedule(self._tick_handler, events)
        # clear interrupt
        self._tca.key_int = True  # clear the IRQ by writing 1 to it

    def _ascii_handler(self, events):
        count = len(events)
        if count == 0:
            return

        for i in range(count):
            self._keyevent_converter.decode(events[i])
            self._update_modifier_mask(self._keyevent_converter)

            # ascii key event
            # !!! release event is ignored
            keyevent = KeyEvent(
                self._keyevent_converter, self._modifier_mask, self._fn_state, self._is_caps_locked
            )
            if self._keyevent_callback and keyevent.state:
                micropython.schedule(
                    self._keyevent_callback,
                    self,  # (self, keyevent.keycode, keyevent.state)
                )
            else:
                # append to the key events list
                keyevent.state and self._keyevents.append(keyevent)
            # print(keyevent)

    def _hid_handler(self, events):
        count = len(events)
        if count == 0:
            return

        hid_report = HIDInputReport()
        for i in range(count):
            self._keyevent_converter.decode(events[i])
            self._update_modifier_mask(self._keyevent_converter)

            # hid report
            hid_report.set_modifier_mask(self._modifier_mask)
            # !!! only append key if it's a press event
            if self._keyevent_converter.state:
                hid_report.append_key(
                    self._keyevent_converter.row, self._keyevent_converter.col, self._fn_state
                )
            if hid_report.done:
                # send the HID report
                if self._hid_report_callback:
                    micropython.schedule(
                        self._hid_report_callback,
                        (self, hid_report.modifiers, hid_report.keypresses),
                    )
                else:
                    self._hid_reports.append(hid_report)
                hid_report = HIDInputReport()

        if not hid_report.done:
            # send the HID report
            if self._hid_report_callback:
                micropython.schedule(
                    self._hid_report_callback, (self, hid_report.modifiers, hid_report.keypresses)
                )
            else:
                self._hid_reports.append(hid_report)

    def _update_modifier_mask(self, keyevent_converter: _KeyEventConverter):
        if (keyevent_converter.row, keyevent_converter.col) == (2, 0):  # FN
            self._fn_state = keyevent_converter.state

        if (keyevent_converter.row, keyevent_converter.col) == (2, 1):  # left shift
            self._shift_state = keyevent_converter.state
            if keyevent_converter.state:
                self._modifier_mask |= asciimap.KEY_MOD_LSHIFT
            else:
                self._modifier_mask &= ~asciimap.KEY_MOD_LSHIFT

        if (keyevent_converter.row, keyevent_converter.col) == (3, 0):  # left ctrl
            if keyevent_converter.state:
                self._modifier_mask |= asciimap.KEY_MOD_LCTRL
            else:
                self._modifier_mask &= ~asciimap.KEY_MOD_LCTRL

        if (keyevent_converter.row, keyevent_converter.col) == (3, 1):  # left opt
            if keyevent_converter.state:
                self._modifier_mask |= asciimap.KEY_MOD_LMETA
            else:
                self._modifier_mask &= ~asciimap.KEY_MOD_LMETA

        if (keyevent_converter.row, keyevent_converter.col) == (3, 2):  # left alt
            if keyevent_converter.state:
                self._modifier_mask |= asciimap.KEY_MOD_LALT
            else:
                self._modifier_mask &= ~asciimap.KEY_MOD_LALT
