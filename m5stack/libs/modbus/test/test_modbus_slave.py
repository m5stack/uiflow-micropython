# SPDX-FileCopyrightText: Copyright (c) 2021 Tobias Eydam
# SPDX-FileCopyrightText: Copyright (c) 2024 lbuque, written for M5Stack
#
# SPDX-License-Identifier: MIT
import os
import sys

if sys.implementation.name == "cpython":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest

from modbus.slave import ModbusTCPServer
from modbus.frame import ModbusTCPFrame


class Test(unittest.TestCase):
    def test_server_handle_message_1(self):
        srv = ModbusTCPServer(
            "",
            0,
            context={
                "coils": [
                    {
                        "register": 1000,
                        "val": [
                            True,
                            False,
                            True,
                            False,
                            True,
                            False,
                            True,
                            False,
                            True,
                            False,
                        ],
                    }
                ]
            },
        )

        msg = ModbusTCPFrame(
            transaction_id=1, unit_id=2, func_code=1, register=1000, length=2, fr_type="request"
        )
        self.assertEqual(srv.handle_message(msg).data, bytearray([0x01]))

        msg = ModbusTCPFrame(
            transaction_id=1, unit_id=2, func_code=1, register=1001, length=2, fr_type="request"
        )
        self.assertEqual(srv.handle_message(msg).data, bytearray([0x02]))

        msg = ModbusTCPFrame(
            transaction_id=1, unit_id=2, func_code=1, register=1000, length=3, fr_type="request"
        )
        self.assertEqual(srv.handle_message(msg).data, bytearray([0x05]))

    def test_server_handle_message_2(self):
        srv = ModbusTCPServer(
            "",
            0,
            context={
                "discrete_inputs": [
                    {
                        "register": 1000,
                        "val": [
                            True,
                            False,
                            True,
                            False,
                            True,
                            False,
                            True,
                            False,
                            True,
                            False,
                        ],
                    }
                ]
            },
        )

        msg = ModbusTCPFrame(
            transaction_id=1, unit_id=2, func_code=2, register=1000, length=2, fr_type="request"
        )
        self.assertEqual(srv.handle_message(msg).data, bytearray([0x01]))

        msg = ModbusTCPFrame(
            transaction_id=1, unit_id=2, func_code=2, register=1001, length=2, fr_type="request"
        )
        self.assertEqual(srv.handle_message(msg).data, bytearray([0x02]))

        msg = ModbusTCPFrame(
            transaction_id=1, unit_id=2, func_code=2, register=1000, length=3, fr_type="request"
        )
        self.assertEqual(srv.handle_message(msg).data, bytearray([0x05]))

    def test_server_handle_message_3(self):
        srv = ModbusTCPServer(
            "",
            0,
            context={
                "holding_registers": [
                    {
                        "register": 1000,
                        "val": [
                            0x0001,
                            0x0203,
                            0x0405,
                            0x0607,
                            0x0809,
                            0x0A0B,
                            0x0C0D,
                            0x0E0F,
                        ],
                    }
                ]
            },
        )

        msg = ModbusTCPFrame(
            transaction_id=1, unit_id=2, func_code=3, register=1000, length=2, fr_type="request"
        )
        self.assertEqual(srv.handle_message(msg).data, bytearray([0x00, 0x01, 0x02, 0x03]))

        msg = ModbusTCPFrame(
            transaction_id=1, unit_id=2, func_code=3, register=1001, length=2, fr_type="request"
        )
        self.assertEqual(srv.handle_message(msg).data, bytearray([0x02, 0x03, 0x04, 0x05]))

        msg = ModbusTCPFrame(
            transaction_id=1, unit_id=2, func_code=3, register=1000, length=3, fr_type="request"
        )
        self.assertEqual(
            srv.handle_message(msg).data, bytearray([0x00, 0x01, 0x02, 0x03, 0x04, 0x05])
        )

    def test_server_handle_message_4(self):
        srv = ModbusTCPServer(
            "",
            0,
            context={
                "input_registers": [
                    {
                        "register": 1000,
                        "val": [
                            0x0001,
                            0x0203,
                            0x0405,
                            0x0607,
                            0x0809,
                            0x0A0B,
                            0x0C0D,
                            0x0E0F,
                        ],
                    },
                ],
            },
        )

        msg = ModbusTCPFrame(
            transaction_id=1, unit_id=2, func_code=4, register=1000, length=2, fr_type="request"
        )
        self.assertEqual(srv.handle_message(msg).data, bytearray([0x00, 0x01, 0x02, 0x03]))

        msg = ModbusTCPFrame(
            transaction_id=1, unit_id=2, func_code=4, register=1001, length=2, fr_type="request"
        )
        self.assertEqual(srv.handle_message(msg).data, bytearray([0x02, 0x03, 0x04, 0x05]))

        msg = ModbusTCPFrame(
            transaction_id=1, unit_id=2, func_code=4, register=1000, length=3, fr_type="request"
        )
        self.assertEqual(
            srv.handle_message(msg).data, bytearray([0x00, 0x01, 0x02, 0x03, 0x04, 0x05])
        )

    def test_server_handle_message_5(self):
        srv = ModbusTCPServer(
            "", 0, context={"coils": [{"register": 1000, "val": [True, True, True]}]}
        )

        msg = ModbusTCPFrame(
            transaction_id=1,
            unit_id=2,
            func_code=5,
            register=1000,
            fr_type="request",
            data=bytearray([0xFF, 0x00]),
        )
        srv.handle_message(msg)
        self.assertEqual(srv.context["coils"][0]["val"], [True, True, True])

        msg = ModbusTCPFrame(
            transaction_id=1,
            unit_id=2,
            func_code=5,
            register=1001,
            fr_type="request",
            data=bytearray([0x00, 0x00]),
        )
        srv.handle_message(msg)
        self.assertEqual(srv.context["coils"][0]["val"], [True, False, True])

    def test_server_handle_message_6(self):
        srv = ModbusTCPServer(
            "",
            0,
            context={"holding_registers": [{"register": 1000, "val": [0x0000, 0x0000, 0x0000]}]},
        )

        msg = ModbusTCPFrame(
            transaction_id=1,
            unit_id=2,
            func_code=6,
            register=1000,
            fr_type="request",
            data=bytearray([0xFF, 0x00]),
        )
        srv.handle_message(msg)
        self.assertEqual(
            srv.context["holding_registers"][0]["val"],
            [0xFF00, 0x0000, 0x0000],
        )

        msg = ModbusTCPFrame(
            transaction_id=1,
            unit_id=2,
            func_code=6,
            register=1001,
            fr_type="request",
            data=bytearray([0xAB, 0xCD]),
        )
        srv.handle_message(msg)
        self.assertEqual(
            srv.context["holding_registers"][0]["val"],
            [0xFF00, 0xABCD, 0x0000],
        )

    def test_server_handle_message_15(self):
        srv = ModbusTCPServer(
            "", 0, context={"coils": [{"register": 1000, "val": [True, True, True, True]}]}
        )

        msg = ModbusTCPFrame(
            transaction_id=1,
            unit_id=2,
            func_code=15,
            register=1000,
            fr_type="request",
            data=bytearray([0x0F]),
            length=4,
        )
        self.assertEqual(
            srv.handle_message(msg).get_frame(),
            bytearray([0x00, 0x01, 0x00, 0x00, 0x00, 0x06, 0x02, 0x0F, 0x03, 0xE8, 0x00, 0x04]),
        )
        self.assertEqual(
            srv.context["coils"][0]["val"],
            [True, True, True, True],
        )

        msg = ModbusTCPFrame(
            transaction_id=1,
            unit_id=2,
            func_code=15,
            register=1000,
            fr_type="request",
            data=bytearray([0x00]),
            length=2,
        )
        self.assertEqual(
            srv.handle_message(msg).get_frame(),
            bytearray([0x00, 0x01, 0x00, 0x00, 0x00, 0x06, 0x02, 0x0F, 0x03, 0xE8, 0x00, 0x02]),
        )
        self.assertEqual(
            srv.context["coils"][0]["val"],
            [False, False, True, True],
        )

    def test_server_handle_message_16(self):
        srv = ModbusTCPServer(
            "",
            0,
            context={
                "holding_registers": [{"register": 1000, "val": [0x0000, 0x0000, 0x0000, 0x0000]}]
            },
        )

        msg = ModbusTCPFrame(
            transaction_id=1,
            unit_id=2,
            func_code=16,
            register=1000,
            fr_type="request",
            data=bytearray([0xAB, 0xCD, 0x12, 0x34]),
            length=2,
        )
        self.assertEqual(
            srv.handle_message(msg).get_frame(),
            bytearray([0x00, 0x01, 0x00, 0x00, 0x00, 0x06, 0x02, 0x10, 0x03, 0xE8, 0x00, 0x02]),
        )
        self.assertEqual(
            srv.context["holding_registers"][0]["val"],
            [0xABCD, 0x1234, 0x0000, 0x0000],
        )

        msg = ModbusTCPFrame(
            transaction_id=1,
            unit_id=2,
            func_code=16,
            register=1001,
            fr_type="request",
            data=bytearray([0xAB, 0xCD]),
            length=1,
        )
        self.assertEqual(
            srv.handle_message(msg).get_frame(),
            bytearray([0x00, 0x01, 0x00, 0x00, 0x00, 0x06, 0x02, 0x10, 0x03, 0xE9, 0x00, 0x01]),
        )
        self.assertEqual(
            srv.context["holding_registers"][0]["val"],
            [0xABCD, 0xABCD, 0x0000, 0x0000],
        )


if __name__ == "__main__":
    unittest.main()
