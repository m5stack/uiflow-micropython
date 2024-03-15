# Copyright (c) 2022 Sebastian Wicki
# Copyright (c) 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


def crc8(data):
    crc = 0xFF
    for d in data:
        crc ^= d
        for _ in range(8):
            if crc & 0x80:
                crc <<= 1
                crc ^= 0x31
            else:
                crc <<= 1
        crc &= 0xFF
    return crc
