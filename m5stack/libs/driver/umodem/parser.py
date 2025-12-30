# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


def _logging(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        # print(f"func {func.__name__} return: {result}")
        return result

    return wrapper


class Parser:
    def __init__(self, data):
        self.data = data
        self.index = 0

    @_logging
    def skipuntil(self, chr: bytearray | bytes) -> int:
        index = self.data.find(chr, self.index)
        if index != -1:
            self.index = index + len(chr)
        return self.index

    @_logging
    def parseint(self, chr=b",") -> int:
        s = self.parseutil(chr)
        if not s:
            return -9999
        return int(s, 0)

    @_logging
    def parsestr(self, chr=b",") -> str:
        s = self.parseutil(chr)
        if not s:
            return ""
        return s.decode().strip('"')

    @_logging
    def parseutil(self, chr: str | bytearray | bytes) -> bytes:
        if isinstance(chr, str):
            chr_bytes = chr.encode()
        else:
            chr_bytes = chr
        index = self.data.find(chr_bytes, self.index)
        if index == -1:
            return b""
        ret = self.data[self.index : index]
        self.index += len(ret) + len(chr_bytes)
        return ret

    def reset(self):
        self.index = 0
