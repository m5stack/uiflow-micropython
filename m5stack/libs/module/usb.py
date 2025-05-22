# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import micropython
from . import mbus
from .usb_hid import *
from driver.max3421e import Max3421e
import machine


HID_PROTOCOL_NONE = micropython.const(0x00)
HID_PROTOCOL_KEYBOARD = micropython.const(0x01)
HID_PROTOCOL_MOUSE = micropython.const(0x02)


DEVADDR = 1
CONFVALUE = 1


KEYCODE2ASCII = [
    (0, 0),  # HID_KEY_NO_PRESS
    (0, 0),  # HID_KEY_ROLLOVER
    (0, 0),  # HID_KEY_POST_FAIL
    (0, 0),  # HID_KEY_ERROR_UNDEFINED
    ("a", "A"),  # HID_KEY_A
    ("b", "B"),  # HID_KEY_B
    ("c", "C"),  # HID_KEY_C
    ("d", "D"),  # HID_KEY_D
    ("e", "E"),  # HID_KEY_E
    ("f", "F"),  # HID_KEY_F
    ("g", "G"),  # HID_KEY_G
    ("h", "H"),  # HID_KEY_H
    ("i", "I"),  # HID_KEY_I
    ("j", "J"),  # HID_KEY_J
    ("k", "K"),  # HID_KEY_K
    ("l", "L"),  # HID_KEY_L
    ("m", "M"),  # HID_KEY_M
    ("n", "N"),  # HID_KEY_N
    ("o", "O"),  # HID_KEY_O
    ("p", "P"),  # HID_KEY_P
    ("q", "Q"),  # HID_KEY_Q
    ("r", "R"),  # HID_KEY_R
    ("s", "S"),  # HID_KEY_S
    ("t", "T"),  # HID_KEY_T
    ("u", "U"),  # HID_KEY_U
    ("v", "V"),  # HID_KEY_V
    ("w", "W"),  # HID_KEY_W
    ("x", "X"),  # HID_KEY_X
    ("y", "Y"),  # HID_KEY_Y
    ("z", "Z"),  # HID_KEY_Z
    ("1", "!"),  # HID_KEY_1
    ("2", "@"),  # HID_KEY_2
    ("3", "#"),  # HID_KEY_3
    ("4", "$"),  # HID_KEY_4
    ("5", "%"),  # HID_KEY_5
    ("6", "^"),  # HID_KEY_6
    ("7", "&"),  # HID_KEY_7
    ("8", "*"),  # HID_KEY_8
    ("9", "("),  # HID_KEY_9
    ("0", ")"),  # HID_KEY_0
    ("\n", "\n"),  # HID_KEY_ENTER
    (None, None),  # HID_KEY_ESC
    ("\b", "\b"),  # HID_KEY_DEL (Backspace)
    (None, None),  # HID_KEY_TAB
    (" ", " "),  # HID_KEY_SPACE
    ("-", "_"),  # HID_KEY_MINUS
    ("=", "+"),  # HID_KEY_EQUAL
    ("[", "{"),  # HID_KEY_OPEN_BRACKET
    ("]", "}"),  # HID_KEY_CLOSE_BRACKET
    ("\\", "|"),  # HID_KEY_BACK_SLASH
    ("\\", "|"),  # HID_KEY_SHARP (Hotfix for non-US keyboards)
    (";", ":"),  # HID_KEY_COLON
    ("'", '"'),  # HID_KEY_QUOTE
    ("`", "~"),  # HID_KEY_TILDE
    (",", "<"),  # HID_KEY_LESS
    (".", ">"),  # HID_KEY_GREATER
    ("/", "?"),  # HID_KEY_SLASH
]


def keycode_to_ascii(keycode, shift=False):
    if keycode < 0 or keycode >= len(KEYCODE2ASCII):
        return None
    normal, shift_char = KEYCODE2ASCII[keycode]
    if shift and shift_char is not None:
        return shift_char
    return normal


class USBModule(UsbHID):
    def __init__(self, pin_cs=0, pin_int=14):
        super().__init__(
            spi=mbus.spi2, cs=machine.Pin(pin_cs, machine.Pin.OUT), irq=machine.Pin(pin_int)
        )
        self.event = 0
        self.event_callback = None
        # mouse
        self.button_state = 0
        self.cursor_x = 0
        self.cursor_y = 0
        self.wheel = 0
        # mouse event
        self.EVENT_NONE = micropython.const(0)
        self.EVENT_MOVE = micropython.const(1)
        self.EVENT_LB_DOWN = micropython.const(2)
        self.EVENT_RB_DOWN = micropython.const(3)
        self.EVENT_MB_DOWN = micropython.const(4)
        self.EVENT_LB_UP = micropython.const(5)
        self.EVENT_RB_UP = micropython.const(6)
        self.EVENT_MB_UP = micropython.const(7)
        self.EVENT_LB_DBCLICK = micropython.const(8)
        self.EVENT_RB_DBCLICK = micropython.const(9)
        self.EVENT_MB_DBCLICK = micropython.const(10)
        self.EVENT_SCROLL = micropython.const(11)
        # keyboard event
        self.modifier = 0
        self.input = []
        self.input_convert = []
        # usb driver
        self.usbhost_init()
        self.device_addr = self.new_dev_addr
        self.hid_device = HID_PROTOCOL_MOUSE

    def set_event_cb(self, cb):
        self.event_callback = cb

    def poll_data(self):
        self.usbhost_task()
        self.dev_endpoint = 1
        if self.usb_task_state == USB_STATE_RUNNING:
            rcode, data = self.usbhost_in_transfer(self.new_dev_addr, self.dev_endpoint, 8, 0, 1)
            if rcode != 0:
                return
            if len(data) == 8:  # TODO: ...
                self.process_keyboard_report(data)
                if self.event_callback:
                    self.event_callback()
            else:
                self.process_mouse_report(data)
                if self.event_callback:
                    self.event_callback()

    def process_mouse_report(self, data):
        button_flags = data[0]
        delta_x = data[1]  # noqa: F841
        delta_y = data[2]  # noqa: F841
        self.wheel = data[3] if data[3] < 128 else data[3] - 256
        if self.wheel != 0:
            self.event = self.EVENT_SCROLL
        if button_flags & 0x01 != self.button_state & 0x01:
            self.event = self.EVENT_MB_DOWN if (button_flags & 0x01) else self.EVENT_MB_UP
        if button_flags & 0x02 != self.button_state & 0x02:
            self.event = self.EVENT_MB_DOWN if (button_flags & 0x02) else self.EVENT_MB_UP
        if button_flags & 0x04 != self.button_state & 0x04:
            self.event = self.EVENT_MB_DOWN if (button_flags & 0x04) else self.EVENT_MB_UP

        self.cursor_x = data[1] if data[1] < 128 else data[1] - 256
        self.cursor_y = data[2] if data[2] < 128 else data[2] - 256
        if self.cursor_x != 0 or self.cursor_y != 0:
            self.event = self.EVENT_MOVE

        self.button_state = button_flags

    def process_keyboard_report(self, data):
        modifier = data[0]
        keycodes = data[2:8]
        self.modifier = modifier
        self.input = keycodes
        self.input_convert.clear()
        for keycode in keycodes:
            if keycode != 0:
                mod = True if (modifier != 0) else False
                c = keycode_to_ascii(keycode, mod)
                self.input_convert.append(c)

    def is_left_btn_pressed(self):
        return bool(self.button_state & 0x01) if self.button_state else False

    def is_right_btn_pressed(self):
        return bool(self.button_state & 0x02) if self.button_state else False

    def is_middle_btn_pressed(self):
        return bool(self.button_state & 0x04) if self.button_state else False

    def is_forward_btn_pressed(self):
        return bool(self.button_state & 0x08) if self.button_state else False

    def is_back_btn_pressed(self):
        return bool(self.button_state & 0x10) if self.button_state else False

    def read_mouse_move(self):
        x, y = self.cursor_x, self.cursor_y
        self.cursor_x, self.cursor_y = 0, 0
        return x, y

    def read_wheel_move(self):
        w = self.wheel
        self.wheel = 0
        return w

    def read_kb_modifier(self):
        m = self.modifier
        self.modifier = 0
        return m

    def read_kb_input(self, convert=False):
        if convert:
            input_data = self.input_convert.copy()
        else:
            input_data = self.input.copy()
        self.input_convert.clear()
        self.input.clear()
        return input_data
