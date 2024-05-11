# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import UART
from micropython import const

try:
    import struct
except ImportError:
    import ustruct as struct

try:
    from typing import Literal, Union
except ImportError:
    pass

import time
import binascii

from . import types as t


class CommandId:
    SLEEP = const(0x2C)
    ADD_MODE = const(0x2D)
    ADD_1 = const(0x01)
    ADD_2 = const(0x02)
    ADD_3 = const(0x03)
    DELETE_USER = const(0x04)
    DELETE_ALL_USER = const(0x05)
    GET_USER_CNT = const(0x09)
    GET_USER_PERMISSIONS = const(0x0A)
    MATCH_1 = const(0x0B)
    MATCH_N = const(0x0C)
    CAPTURE_CHARACTERISTIC = const(0x23)
    CAPTURE_RAW_IMG = const(0x24)
    GET_VERSION = const(0x26)
    MATCH_LEVEL = const(0x28)
    GET_USER_INFO = const(0x2B)
    GET_USER_CHARACTERISTIC = const(0x31)
    UPLOAD_USER_INFO = const(0x41)
    UPLOAD_CHARACTERISTIC = const(0x44)
    GET_UNREGISTERED_USER_ID = const(0x47)


COMMANDS = {
    CommandId.SLEEP: (t.uint8_t, t.uint8_t, t.uint8_t, t.uint8_t),
    CommandId.ADD_MODE: (t.uint8_t, t.uint8_t, t.uint8_t, t.uint8_t),
    CommandId.ADD_1: (t.uint16_t, t.uint8_t, t.uint8_t),
    CommandId.ADD_2: (t.uint16_t, t.uint8_t, t.uint8_t),
    CommandId.ADD_3: (t.uint16_t, t.uint8_t, t.uint8_t),
    CommandId.DELETE_USER: (t.uint16_t, t.uint8_t, t.uint8_t),
    CommandId.DELETE_ALL_USER: (t.uint8_t, t.uint8_t, t.uint8_t, t.uint8_t),
    CommandId.GET_USER_CNT: (t.uint8_t, t.uint8_t, t.uint8_t, t.uint8_t),
    CommandId.GET_USER_PERMISSIONS: (t.uint16_t, t.uint8_t, t.uint8_t),
    CommandId.MATCH_1: (t.uint16_t, t.uint8_t, t.uint8_t),
    CommandId.MATCH_N: (t.uint8_t, t.uint8_t, t.uint8_t, t.uint8_t),
    CommandId.CAPTURE_CHARACTERISTIC: (t.uint8_t, t.uint8_t, t.uint8_t, t.uint8_t),
    CommandId.CAPTURE_RAW_IMG: (t.uint8_t, t.uint8_t, t.uint8_t, t.uint8_t),
    CommandId.GET_VERSION: (t.uint8_t, t.uint8_t, t.uint8_t, t.uint8_t),
    CommandId.MATCH_LEVEL: (t.uint8_t, t.uint8_t, t.uint8_t, t.uint8_t),
    CommandId.GET_USER_INFO: (t.uint8_t, t.uint8_t, t.uint8_t, t.uint8_t),
    CommandId.GET_USER_CHARACTERISTIC: (t.uint16_t, t.uint8_t, t.uint8_t),
    CommandId.UPLOAD_USER_INFO: (t.uint16_t, t.uint8_t, t.uint8_t),
    CommandId.UPLOAD_CHARACTERISTIC: (t.uint16_t, t.uint8_t, t.uint8_t),
    CommandId.GET_UNREGISTERED_USER_ID: (t.uint16_t, t.uint8_t, t.uint8_t),
}

RESPONSES = {
    CommandId.SLEEP: (t.uint8_t, t.uint8_t, t.uint8_t, t.uint8_t),
    CommandId.ADD_MODE: (t.uint8_t, t.uint8_t, t.uint8_t, t.uint8_t),
    CommandId.ADD_1: (t.uint8_t, t.uint8_t, t.uint8_t, t.uint8_t),
    CommandId.ADD_2: (t.uint8_t, t.uint8_t, t.uint8_t, t.uint8_t),
    CommandId.ADD_3: (t.uint8_t, t.uint8_t, t.uint8_t, t.uint8_t),
    CommandId.DELETE_USER: (t.uint8_t, t.uint8_t, t.uint8_t, t.uint8_t),
    CommandId.DELETE_ALL_USER: (t.uint8_t, t.uint8_t, t.uint8_t, t.uint8_t),
    CommandId.GET_USER_CNT: (t.uint16_t, t.uint8_t, t.uint8_t),
    CommandId.MATCH_1: (t.uint8_t, t.uint8_t, t.uint8_t, t.uint8_t),
    CommandId.MATCH_N: (t.uint16_t, t.uint8_t, t.uint8_t),
    CommandId.GET_USER_PERMISSIONS: (t.uint8_t, t.uint8_t, t.uint8_t, t.uint8_t),
    CommandId.MATCH_LEVEL: (t.uint8_t, t.uint8_t, t.uint8_t, t.uint8_t),
    CommandId.GET_USER_INFO: (t.uint16_t, t.uint8_t, t.uint8_t),
    CommandId.GET_USER_CHARACTERISTIC: (t.uint16_t, t.uint8_t, t.uint8_t),
    CommandId.UPLOAD_USER_INFO: (t.uint8_t, t.uint8_t, t.uint8_t, t.uint8_t),
    CommandId.CAPTURE_RAW_IMG: (t.uint16_t, t.uint8_t, t.uint8_t),
    CommandId.GET_VERSION: (t.uint16_t, t.uint8_t, t.uint8_t),
    CommandId.CAPTURE_CHARACTERISTIC: (t.uint16_t, t.uint8_t, t.uint8_t),
    CommandId.UPLOAD_CHARACTERISTIC: (t.uint8_t, t.uint8_t, t.uint8_t, t.uint8_t),
    CommandId.GET_UNREGISTERED_USER_ID: (t.uint16_t, t.uint8_t, t.uint8_t),
}


class FPC1020A:
    _START = b"\xf5"
    _END = b"\xf5"

    _ACK_SUCCESS = 0x00
    _ACK_FAIL = 0x01
    _ACK_FULL = 0x04
    _ACK_NOUSER = 0x05
    _ACK_USER_OCCUPIED = 0x06
    _ACK_USER_EXIST = 0x07
    _ACK_TIMEOUT = 0x08
    _ACK_RESEND = 0x09

    REPEAT_ALLOWED = 0x00
    NO_REPETITION = 0x01

    def __init__(self, uart: UART, verbose=False) -> None:
        self._uart = uart
        self._verbose = verbose
        self._add_mode = self.NO_REPETITION
        self._match_level = 5
        while self._uart.any():
            self._uart.read(self._uart.any())
        if self.get_version() not in ("B1.10.00", "B1.07.00"):
            raise RuntimeError("FPC1020A not found")

    def sleep(self) -> bool:
        """After calling this method successfully, FPC1020A will not be able to
        respond to any messages.
        """
        data = t.serialize([0, 0, 0, 0], COMMANDS[CommandId.SLEEP])
        rxcmd, _, rest = self.command(CommandId.SLEEP, data)
        if rest is True and rxcmd == CommandId.SLEEP:
            return True

    def get_add_mode(self) -> int:
        """In the no-repeat mode, only one user can be added with the same
        finger, and an error message will be returned if the second round of
        adding is forced.
        """
        data = t.serialize([0, 0, 1, 0], COMMANDS[CommandId.ADD_MODE])
        rxcmd, rxdata, rest = self.command(CommandId.ADD_MODE, data)
        if rest is True and rxcmd == CommandId.ADD_MODE:
            r, _ = t.deserialize(rxdata, RESPONSES[rxcmd])
            if r[2] == self._ACK_SUCCESS:
                self._add_mode = r[1]
        return self._add_mode

    def set_add_mode(self, mode: Literal[0, 1]) -> int:
        data = t.serialize([0, mode, 0, 0], COMMANDS[CommandId.ADD_MODE])
        rxcmd, rxdata, rest = self.command(CommandId.ADD_MODE, data)
        if rest is True and rxcmd == CommandId.ADD_MODE:
            r, _ = t.deserialize(rxdata, RESPONSES[rxcmd])
            if r[2] == self._ACK_SUCCESS:
                self._add_mode = mode
        return self._add_mode

    def _add(
        self, cmd: Literal[1, 2, 3], id: int, permission: Literal[1, 2, 3], timeout=5000
    ) -> bool:
        data = t.serialize([id, permission, 0], COMMANDS[cmd])
        rxcmd, rxdata, rest = self.command(cmd, data, timeout)
        if rest is True and rxcmd == cmd:
            r, _ = t.deserialize(rxdata, RESPONSES[rxcmd])
            if r[2] == self._ACK_SUCCESS:
                return True
        return False

    def add_user(self, id: int, permission: Literal[1, 2, 3]) -> int:
        """add new user

        After calling this method, you need to put your finger on the fingerprint module.
        """
        rest = self._add(1, id, permission)
        if rest is True:
            for _ in range(4):
                rest = self._add(2, id, permission)
                if rest is not True:
                    return -1
            rest = self._add(3, id, permission)
            return id if rest is True else -1
        else:
            return -1

    def delete_user(self, id: int) -> int:
        """Delete the user with the specified id."""
        data = t.serialize([id, 0, 0], COMMANDS[CommandId.DELETE_USER])
        rxcmd, rxdata, rest = self.command(CommandId.DELETE_USER, data)
        if rest is True and rxcmd == CommandId.DELETE_USER:
            r, _ = t.deserialize(rxdata, RESPONSES[rxcmd])
            return id if r[2] == self._ACK_SUCCESS else -1
        else:
            return -1

    def delete_all_user(self) -> bool:
        """Delete all users."""
        data = t.serialize([0, 0, 0, 0], COMMANDS[CommandId.DELETE_ALL_USER])
        rxcmd, rxdata, rest = self.command(CommandId.DELETE_ALL_USER, data)
        if rest is True and rxcmd == CommandId.DELETE_ALL_USER:
            r, _ = t.deserialize(rxdata, RESPONSES[rxcmd])
            return True if r[2] == self._ACK_SUCCESS else False
        else:
            return False

    def get_user_count(self) -> int:
        """Get registered users"""
        return self._get_user_count(False)

    def get_user_capacity(self) -> int:
        """Get user capacity"""
        return self._get_user_count(True)

    def _get_user_count(self, is_cap) -> int:
        cap = 0xFF if is_cap else 0x00
        data = t.serialize([0, 0, cap, 0], COMMANDS[CommandId.GET_USER_CNT])
        rxcmd, rxdata, rest = self.command(CommandId.GET_USER_CNT, data)
        if rest is True and rxcmd == CommandId.GET_USER_CNT:
            r, _ = t.deserialize(rxdata, RESPONSES[rxcmd])
            if r[1] == self._ACK_SUCCESS or r[1] == 0xFF:
                return int(r[0])
        else:
            return -1

    def compare_id(self, id, timeout=5000) -> bool:
        """Check whether the currently collected fingerprint matches
        the specified user id.
        """
        data = t.serialize([id, 0, 0], COMMANDS[CommandId.MATCH_1])
        rxcmd, rxdata, rest = self.command(CommandId.MATCH_1, data, timeout)
        if rest is True and rxcmd == CommandId.MATCH_1:
            r, _ = t.deserialize(rxdata, RESPONSES[rxcmd])
            return True if r[2] == self._ACK_SUCCESS else False
        else:
            return False

    def compare_finger(self, timeout=5000) -> int:
        """Detect whether the currently collected fingerprint is a registered user."""
        data = t.serialize([0, 0, 0, 0], COMMANDS[CommandId.MATCH_N])
        rxcmd, rxdata, rest = self.command(CommandId.MATCH_N, data, timeout)
        if rest is True and rxcmd == CommandId.MATCH_N:
            r, _ = t.deserialize(rxdata, RESPONSES[rxcmd])
            if r[1] in [1, 2, 3]:
                return r[0]
        else:
            return -1

    def get_user_list(self) -> tuple:
        infos = []
        data = t.serialize([0, 0, 0, 0], COMMANDS[CommandId.GET_USER_INFO])
        rxcmd, rxdata, rest = self.command(CommandId.GET_USER_INFO, data)
        if rest is not True or rxcmd != CommandId.GET_USER_INFO:
            return infos
        r, _ = t.deserialize(rxdata, RESPONSES[rxcmd])
        if r[1] != self._ACK_SUCCESS:
            return infos

        rxdata, rest = self._receive(length=int(r[0]) + 3, timeout=5000)
        if rest is not True or r[0] != len(rxdata):
            return infos
        rxdata = memoryview(rxdata)
        user_count, _ = t.deserialize(rxdata[0:2], (t.uint16_t,))
        for i in range(int(user_count[0])):
            pos = 2 + i * 3
            r, _ = t.deserialize(rxdata[pos : pos + 3], (t.uint16_t, t.uint8_t))
            infos.append((int(r[0])))
        return infos

    def get_user_info(self, id: int) -> Union[tuple, None]:
        data = t.serialize([id, 0, 0], COMMANDS[CommandId.GET_USER_CHARACTERISTIC])
        rxcmd, rxdata, rest = self.command(CommandId.GET_USER_CHARACTERISTIC, data)
        if rest is not True or rxcmd != CommandId.GET_USER_CHARACTERISTIC:
            return None
        r, _ = t.deserialize(rxdata, RESPONSES[rxcmd])
        if r[1] != self._ACK_SUCCESS:
            return None

        rxdata, rest = self._receive(length=int(r[0]) + 3, timeout=5000)
        if rest is not True or r[0] != len(rxdata):
            return None
        info, _ = t.deserialize(rxdata, (t.uint16_t, t.uint8_t, t.Bytes))
        return (int(info[0]), int(info[1]), info[2])

    def get_user_permission(self, id: int) -> Literal[1, 2, 3]:
        data = t.serialize([id, 0, 0], COMMANDS[CommandId.GET_USER_PERMISSIONS])
        rxcmd, rxdata, rest = self.command(CommandId.GET_USER_PERMISSIONS, data)
        if rest is True and rxcmd == CommandId.GET_USER_PERMISSIONS:
            r, _ = t.deserialize(rxdata, RESPONSES[rxcmd])
            return r[2] if r[2] in (1, 2, 3) else -1
        else:
            return -1

    def get_user_characteristic(self, id: int) -> bytes:
        info = self.get_user_info(id)
        return info[2] if info is not None else b""

    def add_user_info(self, id, permissions, characteristic, timeout=5000) -> bool:
        """Register a new user with FPC1020A."""
        head = t.serialize([196, 0, 0], COMMANDS[CommandId.UPLOAD_USER_INFO])
        data = t.serialize([id, permissions], (t.uint16_t, t.uint8_t))
        data += characteristic
        rxcmd, rxdata, rest = self.command_ext(
            CommandId.UPLOAD_USER_INFO, head, data, timeout=timeout
        )
        if rest is not True or rxcmd != CommandId.UPLOAD_USER_INFO:
            return False

        r, _ = t.deserialize(rxdata, RESPONSES[CommandId.UPLOAD_USER_INFO])
        return True if r[1] == self._ACK_SUCCESS else False

    def capture_characteristic(self, timeout=5000):
        img = b""
        data = t.serialize([0, 0, 0, 0], COMMANDS[CommandId.CAPTURE_CHARACTERISTIC])
        rxcmd, rxdata, rest = self.command(CommandId.CAPTURE_CHARACTERISTIC, data, timeout=timeout)
        if rest is not True or rxcmd != CommandId.CAPTURE_CHARACTERISTIC:
            return img
        r, _ = t.deserialize(rxdata, RESPONSES[rxcmd])
        if r[1] != self._ACK_SUCCESS:
            return img

        rxdata, rest = self._receive(length=int(r[0]) + 3, timeout=timeout)
        if rest is not True or r[0] != len(rxdata):
            return img
        info, _ = t.deserialize(rxdata, (t.uint8_t, t.uint8_t, t.uint8_t, t.Bytes))
        return info[3]

    def get_match_level(self) -> int:
        """The comparison level ranges from 0 to 9, the larger the value,
        the stricter the comparison, and the default value is 5.
        """
        data = t.serialize([0, 0, 1, 0], COMMANDS[CommandId.MATCH_LEVEL])
        rxcmd, rxdata, rest = self.command(CommandId.MATCH_LEVEL, data)
        if rest is True and rxcmd == CommandId.MATCH_LEVEL:
            r, _ = t.deserialize(rxdata, RESPONSES[rxcmd])
            if r[2] == self._ACK_SUCCESS:
                self._match_level = r[1]
        return self._match_level

    def set_match_level(self, level: int) -> int:
        data = t.serialize([0, level, 0, 0], COMMANDS[CommandId.MATCH_LEVEL])
        rxcmd, rxdata, rest = self.command(CommandId.MATCH_LEVEL, data)
        if rest is True and rxcmd == CommandId.MATCH_LEVEL:
            r, _ = t.deserialize(rxdata, RESPONSES[rxcmd])
            if r[2] == self._ACK_SUCCESS:
                self._match_level = level
        return self._match_level

    def get_version(self) -> str:
        """Get the version information of FPC1020A"""
        data = t.serialize([0, 0, 0, 0], COMMANDS[CommandId.GET_VERSION])
        rxcmd, rxdata, rest = self.command(CommandId.GET_VERSION, data)
        if rest is not True or rxcmd != CommandId.GET_VERSION:
            return ""
        r, _ = t.deserialize(rxdata, RESPONSES[rxcmd])
        if r[1] != self._ACK_SUCCESS:
            return ""

        rxdata, rest = self._receive(length=int(r[0]) + 3, timeout=5000)
        if rest is not True or r[0] != len(rxdata):
            return ""
        return rxdata[:8].decode()

    def capture_raw_img(self, file_name: str, hd: bool = False) -> bytes:
        """TODO: 保存到文件"""
        data = t.serialize([0, 0, 0x20 if hd else 0, 0], COMMANDS[CommandId.CAPTURE_RAW_IMG])
        rxcmd, rxdata, rest = self.command(CommandId.CAPTURE_RAW_IMG, data)
        if rest is not True or rxcmd != CommandId.CAPTURE_RAW_IMG:
            return b""
        r, _ = t.deserialize(rxdata, RESPONSES[CommandId.CAPTURE_RAW_IMG])
        if r[1] != self._ACK_SUCCESS:
            return b""

        rxdata, rest = self._receive(timeout=100000)
        if rest is not True or int(r[0]) != len(rxdata):
            return b""
        return rxdata

    def upload_characteristic(self, characteristic: bytes, timeout=5000) -> bool:
        head = t.serialize([196, 0, 0], COMMANDS[CommandId.UPLOAD_CHARACTERISTIC])
        data = t.serialize([0, 0, 0], (t.uint8_t, t.uint8_t, t.uint8_t))
        data += characteristic
        rxcmd, rxdata, rest = self.command_ext(
            CommandId.UPLOAD_CHARACTERISTIC, head, data, timeout=timeout
        )
        if rest is not True or rxcmd != CommandId.UPLOAD_CHARACTERISTIC:
            return False

        r, _ = t.deserialize(rxdata, RESPONSES[CommandId.UPLOAD_CHARACTERISTIC])
        return True if r[1] == self._ACK_SUCCESS else False

    def get_unregistered_user_id(self):
        """FIXME"""
        head = t.serialize([4, 0, 0], COMMANDS[CommandId.GET_UNREGISTERED_USER_ID])
        data = t.serialize([0, 150], (t.uint16_t, t.uint16_t))
        rxcmd, rxdata, rest = self.command_ext(CommandId.GET_UNREGISTERED_USER_ID, head, data)
        if rest is not True or rxcmd != CommandId.GET_UNREGISTERED_USER_ID:
            return -1

        r, _ = t.deserialize(rxdata, RESPONSES[CommandId.GET_UNREGISTERED_USER_ID])
        return int(r[0]) if r[1] == self._ACK_SUCCESS else -1

    def command(self, cmd, data=b"", timeout=5000):
        self._send(cmd, data)
        rxdata, rest = self._receive(timeout=timeout)
        if rest is not True:
            return 0, b"", False

        cmd, data = struct.unpack(">B%ds" % (len(rxdata) - 1), rxdata)
        return cmd, data, True

    def command_ext(self, cmd, head, data, timeout=1000):
        checksum = self._checksum(cmd, head)
        frame = struct.pack("sB%dsBs" % len(head), self._START, cmd, head, checksum, self._END)
        checksum = self._checksum(data)
        frame += struct.pack("s%dsBs" % len(data), self._START, data, checksum, self._END)
        self._verbose and print("Frame to send: %s" % (binascii.hexlify(frame)))
        txdata = memoryview(frame)
        pos = 0
        while pos < len(frame):
            rest = self._uart.write(txdata[pos : pos + 32])
            if rest is None:
                break
            pos += rest

        rxdata, rest = self._receive(timeout=timeout)
        if rest is not True:
            return 0, b"", False

        cmd, data = struct.unpack(">B%ds" % (len(rxdata) - 1), rxdata)
        return cmd, data, True

    def _send(self, cmd, data=b""):
        checksum = self._checksum(cmd, data)
        frame = struct.pack("sB%dsBs" % len(data), self._START, cmd, data, checksum, self._END)
        self._verbose and print("Frame to send: %s" % (binascii.hexlify(frame)))
        self._uart.write(frame)

    def _send_data(self, data):
        checksum = self._checksum(data)
        frame = struct.pack("s%dsBs" % len(data), self._START, data, checksum, self._END)
        self._verbose and print("Frame to send: %s" % (binascii.hexlify(frame)))
        txdata = memoryview(frame)
        pos = 0
        while pos < len(frame):
            rest = self._uart.write(txdata[pos : pos + 32])
            if rest is None:
                break
            pos += rest

    def _receive(self, length: int = 8, timeout=1000):
        _buffer = b""
        startpos = -1
        endpos = -1
        count = timeout
        l = 0
        while count > 0 and (l - startpos) < length:
            if self._uart.any() == 0:
                time.sleep_ms(10)
                count -= 10
                continue
            _buffer += self._uart.read(1)
            l += 1
            if startpos == -1:
                startpos = _buffer.find(self._START)
            # if startpos != -1 and endpos == -1:
            #     endpos = _buffer.rfind(self._END, startpos + 1)
            # if startpos != -1 and endpos != -1:
            #     break

        endpos = _buffer.rfind(self._END, startpos)
        if startpos != -1 and endpos != -1:
            self._verbose and print("Recv buffer: %s" % binascii.hexlify(_buffer))
            frame = _buffer[startpos + 1 : endpos]
            rxdata, checksum = struct.unpack(">%dsB" % (len(frame) - 1), frame)
            if self._checksum(rxdata) != checksum:
                self._verbose and print(
                    "Invalid checksum: %s, data: 0x%s" % (checksum, binascii.hexlify(frame))
                )
                return b"", False
            return rxdata, True
        else:
            self._verbose and print("Malformed packet received, ignore it")
            return b"", False

    def _checksum(self, *args):
        chcksum = 0
        for arg in args:
            if isinstance(arg, int):
                chcksum ^= arg
                continue
            for x in arg:
                chcksum ^= x
        return chcksum
