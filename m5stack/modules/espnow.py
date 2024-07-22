# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# espnow module for MicroPython on ESP32
# MIT license; Copyright (c) 2022 Glenn Moloney @glenn20
#
# SPDX-License-Identifier: MIT

from _espnow import *
import binascii
import struct


class ESPNow(ESPNowBase):
    # Static buffers for alloc free receipt of messages with ESPNow.irecv().
    _data = [None, bytearray(MAX_DATA_LEN)]
    _none_tuple = (None, None)

    def __init__(self):
        super().__init__()

    def irecv(self, timeout_ms=None):
        n = self.recvinto(self._data, timeout_ms)
        return self._data if n else self._none_tuple

    def recv(self, timeout_ms=None):
        n = self.recvinto(self._data, timeout_ms)
        return [bytes(x) for x in self._data] if n else self._none_tuple

    def irq(self, callback):
        super().irq(callback, self)

    def __iter__(self):
        return self

    def __next__(self):
        return self.irecv()  # Use alloc free irecv() method

    def _bytes_to_hex_str(self, bins):
        return "".join(["%02X" % x for x in bins]).strip()

    def _hex_str_to_bytes(self, hexStr):
        return binascii.unhexlify(hexStr)

    def _bytes_to(self, buf, format=0):
        return struct.unpack(">d", buf)[0] if format else int.from_bytes(buf, byteorder="little")

    def _from_bytes(self, value, format=0):
        return struct.pack(">d", value) if format else value.to_bytes(4, "little")
