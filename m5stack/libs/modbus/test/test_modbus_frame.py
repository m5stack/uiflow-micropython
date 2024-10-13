# SPDX-FileCopyrightText: Copyright (c) 2021 Tobias Eydam
# SPDX-FileCopyrightText: Copyright (c) 2024 lbuque, written for M5Stack
#
# SPDX-License-Identifier: MIT

import os
import sys

if sys.implementation.name == "cpython":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import modbus.frame as frame


class Test(unittest.TestCase):
    def test_modbus_rtu_frame_init(self):
        test_list = [
            {
                "params": {
                    "fr_type": "request",
                    "func_code": 1,
                    "device_addr": 1,
                    "register": 18,
                    "length": 8,
                },
                "frame": bytearray([0x01, 0x01, 0x00, 0x12, 0x00, 0x08, 0x9D, 0xC9]),
            },
            {
                "params": {
                    "fr_type": "request",
                    "func_code": 2,
                    "device_addr": 1,
                    "register": 18,
                    "length": 8,
                },
                "frame": bytearray([0x01, 0x02, 0x00, 0x12, 0x00, 0x08, 0xD9, 0xC9]),
            },
            {
                "params": {
                    "fr_type": "request",
                    "func_code": 3,
                    "device_addr": 1,
                    "register": 18,
                    "length": 8,
                },
                "frame": bytearray([0x01, 0x03, 0x00, 0x12, 0x00, 0x08, 0xE4, 0x09]),
            },
            {
                "params": {
                    "fr_type": "request",
                    "func_code": 4,
                    "device_addr": 1,
                    "register": 18,
                    "length": 8,
                },
                "frame": bytearray([0x01, 0x04, 0x00, 0x12, 0x00, 0x08, 0x51, 0xC9]),
            },
            {
                "params": {
                    "fr_type": "request",
                    "func_code": 5,
                    "device_addr": 1,
                    "register": 18,
                    "data": bytearray([0xFF, 0x00]),
                },
                "frame": bytearray([0x01, 0x05, 0x00, 0x12, 0xFF, 0x00, 0x2C, 0x3F]),
            },
            {
                "params": {
                    "fr_type": "request",
                    "func_code": 6,
                    "device_addr": 1,
                    "register": 18,
                    "data": bytearray([0x00, 0x01]),
                },
                "frame": bytearray([0x01, 0x06, 0x00, 0x12, 0x00, 0x01, 0xE8, 0x0F]),
            },
            {
                "params": {
                    "fr_type": "request",
                    "func_code": 15,
                    "device_addr": 1,
                    "register": 18,
                    "length": 8,
                    "data": bytearray([0xFF]),
                },
                "frame": bytearray([0x01, 0x0F, 0x00, 0x12, 0x00, 0x08, 0x01, 0xFF, 0x06, 0xD6]),
            },
            {
                "params": {
                    "fr_type": "request",
                    "func_code": 16,
                    "device_addr": 1,
                    "register": 18,
                    "length": 8,
                    "data": bytearray(
                        [
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                        ]
                    ),
                },
                "frame": bytearray(
                    [
                        0x01,
                        0x10,
                        0x00,
                        0x12,
                        0x00,
                        0x08,
                        0x10,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0xD5,
                        0x51,
                    ]
                ),
            },
            {
                "params": {
                    "fr_type": "response",
                    "func_code": 1,
                    "device_addr": 1,
                    "data": bytearray([0xFF]),
                },
                "frame": bytearray([0x01, 0x01, 0x01, 0xFF, 0x11, 0xC8]),
            },
            {
                "params": {
                    "fr_type": "response",
                    "func_code": 2,
                    "device_addr": 1,
                    "data": bytearray([0xFF]),
                },
                "frame": bytearray([0x01, 0x02, 0x01, 0xFF, 0xE1, 0xC8]),
            },
            {
                "params": {
                    "fr_type": "response",
                    "func_code": 3,
                    "device_addr": 1,
                    "data": bytearray(
                        [
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                        ]
                    ),
                },
                "frame": bytearray(
                    [
                        0x01,
                        0x03,
                        0x10,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x93,
                        0xB4,
                    ]
                ),
            },
            {
                "params": {
                    "fr_type": "response",
                    "func_code": 4,
                    "device_addr": 1,
                    "data": bytearray(
                        [
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                        ]
                    ),
                },
                "frame": bytearray(
                    [
                        0x01,
                        0x04,
                        0x10,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x22,
                        0xC1,
                    ]
                ),
            },
            {
                "params": {
                    "fr_type": "response",
                    "func_code": 5,
                    "device_addr": 1,
                    "register": 18,
                    "data": bytearray([0xFF, 0x00]),
                },
                "frame": bytearray([0x01, 0x05, 0x00, 0x12, 0xFF, 0x00, 0x2C, 0x3F]),
            },
            {
                "params": {
                    "fr_type": "response",
                    "func_code": 6,
                    "device_addr": 1,
                    "register": 18,
                    "data": bytearray([0x00, 0x01]),
                },
                "frame": bytearray([0x01, 0x06, 0x00, 0x12, 0x00, 0x01, 0xE8, 0x0F]),
            },
            {
                "params": {
                    "fr_type": "response",
                    "func_code": 15,
                    "device_addr": 1,
                    "register": 18,
                    "length": 8,
                },
                "frame": bytearray([0x01, 0x0F, 0x00, 0x12, 0x00, 0x08, 0xF4, 0x08]),
            },
            {
                "params": {
                    "fr_type": "response",
                    "func_code": 16,
                    "device_addr": 1,
                    "register": 18,
                    "length": 8,
                },
                "frame": bytearray([0x01, 0x10, 0x00, 0x12, 0x00, 0x08, 0x61, 0xCA]),
            },
            {
                "params": {
                    "fr_type": "response",
                    "func_code": 0x81,
                    "device_addr": 1,
                    "error_code": 0x01,
                },
                "frame": bytearray([0x01, 0x81, 0x01, 0x81, 0x90]),
            },
            {
                "params": {
                    "fr_type": "response",
                    "func_code": 0x82,
                    "device_addr": 1,
                    "error_code": 0x02,
                },
                "frame": bytearray([0x01, 0x82, 0x02, 0xC1, 0x61]),
            },
            {
                "params": {
                    "fr_type": "response",
                    "func_code": 0x83,
                    "device_addr": 1,
                    "error_code": 0x03,
                },
                "frame": bytearray([0x01, 0x83, 0x03, 0x01, 0x31]),
            },
            {
                "params": {
                    "fr_type": "response",
                    "func_code": 0x84,
                    "device_addr": 1,
                    "error_code": 0x04,
                },
                "frame": bytearray([0x01, 0x84, 0x04, 0x42, 0xC3]),
            },
            {
                "params": {
                    "fr_type": "response",
                    "func_code": 0x85,
                    "device_addr": 1,
                    "error_code": 0x01,
                },
                "frame": bytearray([0x01, 0x85, 0x01, 0x83, 0x50]),
            },
            {
                "params": {
                    "fr_type": "response",
                    "func_code": 0x86,
                    "device_addr": 1,
                    "error_code": 0x02,
                },
                "frame": bytearray([0x01, 0x86, 0x02, 0xC3, 0xA1]),
            },
            {
                "params": {
                    "fr_type": "response",
                    "func_code": 0x8F,
                    "device_addr": 1,
                    "error_code": 0x03,
                },
                "frame": bytearray([0x01, 0x8F, 0x03, 0x04, 0x31]),
            },
            {
                "params": {
                    "fr_type": "response",
                    "func_code": 0x90,
                    "device_addr": 1,
                    "error_code": 0x04,
                },
                "frame": bytearray([0x01, 0x90, 0x04, 0x4D, 0xC3]),
            },
        ]

        for test in test_list:
            f = frame.ModbusRTUFrame(**test["params"])
            self.assertEqual(f.get_frame(), test["frame"])

            parsed_frame = frame.ModbusRTUFrame.parse_frame(test["frame"])
            self.assertEqual(f.get_frame(), parsed_frame.get_frame())

    def test_modbus_tcp_frame_init(self):
        test_list = [
            {
                "params": {
                    "transaction_id": 1,
                    "fr_type": "request",
                    "func_code": 1,
                    "unit_id": 1,
                    "register": 18,
                    "length": 8,
                },
                "frame": bytearray(
                    [0x00, 0x01, 0x00, 0x00, 0x00, 0x06, 0x01, 0x01, 0x00, 0x12, 0x00, 0x08]
                ),
            },
            {
                "params": {
                    "transaction_id": 1,
                    "fr_type": "request",
                    "func_code": 2,
                    "unit_id": 1,
                    "register": 18,
                    "length": 8,
                },
                "frame": bytearray(
                    [0x00, 0x01, 0x00, 0x00, 0x00, 0x06, 0x01, 0x02, 0x00, 0x12, 0x00, 0x08]
                ),
            },
            {
                "params": {
                    "transaction_id": 1,
                    "fr_type": "request",
                    "func_code": 3,
                    "unit_id": 1,
                    "register": 18,
                    "length": 8,
                },
                "frame": bytearray(
                    [0x00, 0x01, 0x00, 0x00, 0x00, 0x06, 0x01, 0x03, 0x00, 0x12, 0x00, 0x08]
                ),
            },
            {
                "params": {
                    "transaction_id": 1,
                    "fr_type": "request",
                    "func_code": 4,
                    "unit_id": 1,
                    "register": 18,
                    "length": 8,
                },
                "frame": bytearray(
                    [0x00, 0x01, 0x00, 0x00, 0x00, 0x06, 0x01, 0x04, 0x00, 0x12, 0x00, 0x08]
                ),
            },
            {
                "params": {
                    "transaction_id": 1,
                    "fr_type": "request",
                    "func_code": 5,
                    "unit_id": 1,
                    "register": 18,
                    "data": bytearray([0xFF, 0x00]),
                },
                "frame": bytearray(
                    [0x00, 0x01, 0x00, 0x00, 0x00, 0x06, 0x01, 0x05, 0x00, 0x12, 0xFF, 0x00]
                ),
            },
            {
                "params": {
                    "transaction_id": 1,
                    "fr_type": "request",
                    "func_code": 6,
                    "unit_id": 1,
                    "register": 18,
                    "data": bytearray([0x00, 0x01]),
                },
                "frame": bytearray(
                    [0x00, 0x01, 0x00, 0x00, 0x00, 0x06, 0x01, 0x06, 0x00, 0x12, 0x00, 0x01]
                ),
            },
            {
                "params": {
                    "transaction_id": 1,
                    "fr_type": "request",
                    "func_code": 15,
                    "unit_id": 1,
                    "register": 18,
                    "length": 8,
                    "data": bytearray([0xFF]),
                },
                "frame": bytearray(
                    [
                        0x00,
                        0x01,
                        0x00,
                        0x00,
                        0x00,
                        0x08,
                        0x01,
                        0x0F,
                        0x00,
                        0x12,
                        0x00,
                        0x08,
                        0x01,
                        0xFF,
                    ]
                ),
            },
            {
                "params": {
                    "transaction_id": 1,
                    "fr_type": "request",
                    "func_code": 16,
                    "unit_id": 1,
                    "register": 18,
                    "length": 8,
                    "data": bytearray(
                        [
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                        ]
                    ),
                },
                "frame": bytearray(
                    [
                        0x00,
                        0x01,
                        0x00,
                        0x00,
                        0x00,
                        0x17,
                        0x01,
                        0x10,
                        0x00,
                        0x12,
                        0x00,
                        0x08,
                        0x10,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                    ]
                ),
            },
            {
                "params": {
                    "transaction_id": 1,
                    "fr_type": "response",
                    "func_code": 1,
                    "unit_id": 1,
                    "data": bytearray([0xFF]),
                },
                "frame": bytearray([0x00, 0x01, 0x00, 0x00, 0x00, 0x04, 0x01, 0x01, 0x01, 0xFF]),
            },
            {
                "params": {
                    "transaction_id": 1,
                    "fr_type": "response",
                    "func_code": 2,
                    "unit_id": 1,
                    "data": bytearray([0xFF]),
                },
                "frame": bytearray([0x00, 0x01, 0x00, 0x00, 0x00, 0x04, 0x01, 0x02, 0x01, 0xFF]),
            },
            {
                "params": {
                    "transaction_id": 1,
                    "fr_type": "response",
                    "func_code": 3,
                    "unit_id": 1,
                    "data": bytearray(
                        [
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                        ]
                    ),
                },
                "frame": bytearray(
                    [
                        0x00,
                        0x01,
                        0x00,
                        0x00,
                        0x00,
                        0x13,
                        0x01,
                        0x03,
                        0x10,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                    ]
                ),
            },
            {
                "params": {
                    "transaction_id": 1,
                    "fr_type": "response",
                    "func_code": 4,
                    "unit_id": 1,
                    "data": bytearray(
                        [
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                            0x00,
                            0x01,
                        ]
                    ),
                },
                "frame": bytearray(
                    [
                        0x00,
                        0x01,
                        0x00,
                        0x00,
                        0x00,
                        0x13,
                        0x01,
                        0x04,
                        0x10,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                        0x00,
                        0x01,
                    ]
                ),
            },
            {
                "params": {
                    "transaction_id": 1,
                    "fr_type": "response",
                    "func_code": 5,
                    "unit_id": 1,
                    "register": 18,
                    "data": bytearray([0xFF, 0x00]),
                },
                "frame": bytearray(
                    [0x00, 0x01, 0x00, 0x00, 0x00, 0x06, 0x01, 0x05, 0x00, 0x12, 0xFF, 0x00]
                ),
            },
            {
                "params": {
                    "transaction_id": 1,
                    "fr_type": "response",
                    "func_code": 6,
                    "unit_id": 1,
                    "register": 18,
                    "data": bytearray([0x00, 0x01]),
                },
                "frame": bytearray(
                    [0x00, 0x01, 0x00, 0x00, 0x00, 0x06, 0x01, 0x06, 0x00, 0x12, 0x00, 0x01]
                ),
            },
            {
                "params": {
                    "transaction_id": 1,
                    "fr_type": "response",
                    "func_code": 15,
                    "unit_id": 1,
                    "register": 18,
                    "length": 8,
                },
                "frame": bytearray(
                    [0x00, 0x01, 0x00, 0x00, 0x00, 0x06, 0x01, 0x0F, 0x00, 0x12, 0x00, 0x08]
                ),
            },
            {
                "params": {
                    "transaction_id": 1,
                    "fr_type": "response",
                    "func_code": 16,
                    "unit_id": 1,
                    "register": 18,
                    "length": 8,
                },
                "frame": bytearray(
                    [0x00, 0x01, 0x00, 0x00, 0x00, 0x06, 0x01, 0x10, 0x00, 0x12, 0x00, 0x08]
                ),
            },
            {
                "params": {
                    "transaction_id": 1,
                    "fr_type": "response",
                    "func_code": 0x81,
                    "unit_id": 1,
                    "error_code": 0x01,
                },
                "frame": bytearray([0x00, 0x01, 0x00, 0x00, 0x00, 0x03, 0x01, 0x81, 0x01]),
            },
        ]

        for test in test_list:
            f = frame.ModbusTCPFrame(**test["params"])
            self.assertEqual(f.get_frame(), test["frame"])

            parsed_frame = frame.ModbusTCPFrame.parse_frame(test["frame"])
            self.assertEqual(f.get_frame(), parsed_frame.get_frame())


if __name__ == "__main__":
    unittest.main()
