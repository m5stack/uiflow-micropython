# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


def _logging(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"func {func.__name__} return: {result}")
        return result

    return wrapper


class Parser:
    def __init__(self, data):
        self.data = data
        self.index = 0

    @_logging
    def skipuntil(self, chr: str) -> int:
        index = self.data.find(chr, self.index)
        if index != -1:
            self.index = index + len(chr)
        return self.index

    @_logging
    def parseint(self, chr=",") -> int:
        s = self.parseutil(chr)
        if s == "":
            return -9999
        return int(s)

    @_logging
    def parseutil(self, chr: str) -> str:
        index = self.data.find(chr, self.index)
        if index == -1:
            return ""
        ret = self.data[self.index : index]
        self.index += len(ret) + len(chr)
        return ret

    def reset(self):
        self.index = 0
