# MIT license; Copyright (c) 2023-2024 Angus Gratton
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
from micropython import const
import time
import usb.device
from usb.device.hid import HIDInterface
import struct


_INTERFACE_PROTOCOL_KEYBOARD = const(0x01)

_KEY_ARRAY_LEN = const(6)  # Size of HID key array, must match report descriptor
_KEY_REPORT_LEN = const(_KEY_ARRAY_LEN + 2)  # Modifier Byte + Reserved Byte + Array entries


# ASCII to Standard HID keycodes
KEYMAP = {
    # 字母
    "a": 0x04,
    "b": 0x05,
    "c": 0x06,
    "d": 0x07,
    "e": 0x08,
    "f": 0x09,
    "g": 0x0A,
    "h": 0x0B,
    "i": 0x0C,
    "j": 0x0D,
    "k": 0x0E,
    "l": 0x0F,
    "m": 0x10,
    "n": 0x11,
    "o": 0x12,
    "p": 0x13,
    "q": 0x14,
    "r": 0x15,
    "s": 0x16,
    "t": 0x17,
    "u": 0x18,
    "v": 0x19,
    "w": 0x1A,
    "x": 0x1B,
    "y": 0x1C,
    "z": 0x1D,
    "A": 0x04,
    "B": 0x05,
    "C": 0x06,
    "D": 0x07,
    "E": 0x08,
    "F": 0x09,
    "G": 0x0A,
    "H": 0x0B,
    "I": 0x0C,
    "J": 0x0D,
    "K": 0x0E,
    "L": 0x0F,
    "M": 0x10,
    "N": 0x11,
    "O": 0x12,
    "P": 0x13,
    "Q": 0x14,
    "R": 0x15,
    "S": 0x16,
    "T": 0x17,
    "U": 0x18,
    "V": 0x19,
    "W": 0x1A,
    "X": 0x1B,
    "Y": 0x1C,
    "Z": 0x1D,
    # 数字
    "1": 0x1E,
    "2": 0x1F,
    "3": 0x20,
    "4": 0x21,
    "5": 0x22,
    "6": 0x23,
    "7": 0x24,
    "8": 0x25,
    "9": 0x26,
    "0": 0x27,
    # 空格
    " ": 0x2C,  # 空格键
    # 特殊符号
    "!": 0x1E,  # 感叹号（Shift + 1）
    "@": 0x1F,  # @ 符号（Shift + 2）
    "#": 0x20,  # # 符号（Shift + 3）
    "$": 0x21,  # $ 符号（Shift + 4）
    "%": 0x22,  # % 符号（Shift + 5）
    "^": 0x23,  # ^ 符号（Shift + 6）
    "&": 0x24,  # & 符号（Shift + 7）
    "*": 0x25,  # * 符号（Shift + 8）
    "(": 0x26,  # ( 符号（Shift + 9）
    ")": 0x27,  # ) 符号（Shift + 0）
    "{": 0x2F,
    "}": 0x30,
    "<": 0x36,
    ">": 0x37,
    "?": 0x38,
    # 其他符号
    "[": 0x2F,
    "]": 0x30,
    "-": 0x56,  # 减号
    "+": 0x57,  # 加号
    "=": 0x2E,  # 等号
    ",": 0x36,  # 逗号
    ".": 0x37,  # 句号
    "/": 0x38,  # 斜杠
    ";": 0x27,  # 分号
    ":": 0x33,  # 冒号
    "'": 0x34,  # 单引号
    "`": 0x35,  # 反引号
    # 特殊控制键
    "\n": 0x28,  # 回车（Enter）
    "\t": 0x2B,  # Tab
    "\b": 0x2A,  # Backspace
}

SPECIAL_CHARACTERS = ("!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "{", "}", "<", ">", "?")


def char_to_hid_key(char):
    if char in KEYMAP:
        keycode = KEYMAP[char]
        # 如果是大写字母或特殊符号，则需要按下 Shift 键
        if char.isupper() or char in SPECIAL_CHARACTERS:
            use_shift = True
        else:
            use_shift = False
        return use_shift, keycode
    else:
        return False, 0x00


class Keyboard(HIDInterface):
    # Synchronous USB keyboard HID interface

    def __init__(self, interface_str="M5Keyboard", builtin_driver=True):
        super().__init__(
            _KEYBOARD_REPORT_DESC,
            set_report_buf=bytearray(1),
            protocol=_INTERFACE_PROTOCOL_KEYBOARD,
            interface_str=interface_str,
        )
        self._key_reports = [
            bytearray(_KEY_REPORT_LEN),
            bytearray(_KEY_REPORT_LEN),
        ]  # Ping/pong report buffers
        self.numlock = False

        # Define the initial keyboard state.
        self._modifiers = 0  # 8 bits signifying Right GUI(Win/Command), Right ALT/Option, Right Shift, Right Control, Left GUI, Left ALT, Left Shift, Left Control.
        self._keypresses = [0x00] * 6  # 6 keys to hold.
        self._buf = bytearray(8)

        # 自动初始化 USB 设备
        self.builtin_driver = builtin_driver
        self._usb_device = usb.device.get()
        self._init_usb()

    def _init_usb(self):
        self._usb_device.init(self, builtin_driver=self.builtin_driver)

    def on_set_report(self, report_data, _report_id, _report_type):
        self.on_led_update(report_data[0])

    def on_led_update(self, led_mask):
        # Override to handle keyboard LED updates. led_mask is bitwise ORed
        # together values as defined in LEDCode.
        pass

    def send_keys(self, down_keys, timeout_ms=100):
        # Update the state of the keyboard by sending a report with down_keys
        # set, where down_keys is an iterable (list or similar) of integer
        # values such as the values defined in KeyCode.
        #
        # Will block for up to timeout_ms if a previous report is still
        # pending to be sent to the host. Returns True on success.

        r, s = self._key_reports  # next report buffer to send, spare report buffer
        r[0] = 0  # modifier byte
        i = 2  # index for next key array item to write to
        for k in down_keys:
            if k < 0:  # Modifier key
                r[0] |= -k
            elif i < _KEY_REPORT_LEN:
                r[i] = k
                i += 1
            else:  # Excess rollover! Can't report
                r[0] = 0
                for i in range(2, _KEY_REPORT_LEN):
                    r[i] = 0xFF
                break

        while i < _KEY_REPORT_LEN:
            r[i] = 0
            i += 1

        if super().send_report(r, timeout_ms):
            # Swap buffers if the previous one is newly queued to send, so
            # any subsequent call can't modify that buffer mid-send
            self._key_reports[0] = s
            self._key_reports[1] = r
            return True
        return False

    def send_report(self, timeout_ms=100):
        struct.pack_into(
            "8B",
            self._buf,
            0,
            self._modifiers,
            0,
            self._keypresses[0],
            self._keypresses[1],
            self._keypresses[2],
            self._keypresses[3],
            self._keypresses[4],
            self._keypresses[5],
        )
        if super().send_report(self._buf, timeout_ms):
            return True
        return False

    def set_modifiers(
        self,
        right_gui=0,
        right_alt=0,
        right_shift=0,
        right_control=0,
        left_gui=0,
        left_alt=0,
        left_shift=0,
        left_control=0,
    ):
        self._modifiers = (
            (right_gui << 7)
            + (right_alt << 6)
            + (right_shift << 5)
            + (right_control << 4)
            + (left_gui << 3)
            + (left_alt << 2)
            + (left_shift << 1)
            + left_control
        )

    def set_keys(self, k0=0x00, k1=0x00, k2=0x00, k3=0x00, k4=0x00, k5=0x00):
        self._keypresses = [k0, k1, k2, k3, k4, k5]

    def send_key(self, key):
        self.set_keys(k0=key)
        self.send_report()
        self.set_keys()
        self.send_report()

    def input(self, key):
        if isinstance(key, str):
            key_cache = []
            for k in key:
                use_shift, hid_key = char_to_hid_key(k)
                if use_shift:
                    if key_cache:
                        self.send_keypresses(key_cache)
                        key_cache.clear()
                    self.set_modifiers(left_shift=True)
                    self.set_keys(k0=hid_key)
                    self.send_report()
                    self.set_modifiers()
                    self.set_keys()
                    self.send_report()
                else:
                    key_cache.append(hid_key)
                    if len(key_cache) == 6:
                        self.send_keypresses(key_cache)
                        key_cache.clear()
            if key_cache:
                self.send_keypresses(key_cache)
                key_cache.clear()
            self.set_keys()
            self.send_report()
        else:
            self.send_key(key)

    def send_keypresses(self, key):
        last_k = 0
        cnt = 0
        for i, k in enumerate(key):
            if k == last_k:
                self._keypresses[cnt - 1] = 0x00
                self.send_report()
            self._keypresses[cnt] = k
            cnt += 1
            last_k = k
            self.send_report()
        self.set_keys()
        self.send_report()
        time.sleep_ms(10)


# HID keyboard report descriptor
#
# From p69 of http://www.usb.org/developers/devclass_docs/HID1_11.pdf
#
# fmt: off
_KEYBOARD_REPORT_DESC = (
    b'\x05\x01'     # Usage Page (Generic Desktop),
        b'\x09\x06'     # Usage (Keyboard),
    b'\xA1\x01'     # Collection (Application),
        b'\x05\x07'         # Usage Page (Key Codes);
            b'\x19\xE0'         # Usage Minimum (224),
            b'\x29\xE7'         # Usage Maximum (231),
            b'\x15\x00'         # Logical Minimum (0),
            b'\x25\x01'         # Logical Maximum (1),
            b'\x75\x01'         # Report Size (1),
            b'\x95\x08'         # Report Count (8),
            b'\x81\x02'         # Input (Data, Variable, Absolute), ;Modifier byte
            b'\x95\x01'         # Report Count (1),
            b'\x75\x08'         # Report Size (8),
            b'\x81\x01'         # Input (Constant), ;Reserved byte
            b'\x95\x05'         # Report Count (5),
            b'\x75\x01'         # Report Size (1),
        b'\x05\x08'         # Usage Page (Page# for LEDs),
            b'\x19\x01'         # Usage Minimum (1),
            b'\x29\x05'         # Usage Maximum (5),
            b'\x91\x02'         # Output (Data, Variable, Absolute), ;LED report
            b'\x95\x01'         # Report Count (1),
            b'\x75\x03'         # Report Size (3),
            b'\x91\x01'         # Output (Constant), ;LED report padding
            b'\x95\x06'         # Report Count (6),
            b'\x75\x08'         # Report Size (8),
            b'\x15\x00'         # Logical Minimum (0),
            b'\x25\x65'         # Logical Maximum(101),
        b'\x05\x07'         # Usage Page (Key Codes),
            b'\x19\x00'         # Usage Minimum (0),
            b'\x29\x65'         # Usage Maximum (101),
            b'\x81\x00'         # Input (Data, Array), ;Key arrays (6 bytes)
    b'\xC0'     # End Collection
)
# fmt: on


# HID LED values
class LEDCode:
    NUM_LOCK = 0x01
    CAPS_LOCK = 0x02
    SCROLL_LOCK = 0x04
    COMPOSE = 0x08
    KANA = 0x10
