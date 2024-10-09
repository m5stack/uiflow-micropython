# SPDX-FileCopyrightText: Copyright (c) 2021 Tobias Eydam
# SPDX-FileCopyrightText: Copyright (c) 2024 lbuque, written for M5Stack
#
# SPDX-License-Identifier: MIT

import os
import sys

if sys.implementation.name == "cpython":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from modbus.slave import ModbusSlave


class Test(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.sl = ModbusSlave()

    def test_coil(self):
        self.sl.add_coil(0, True)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [{"register": 0, "value": [True]}],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.add_coil(2, True)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [{"register": 0, "value": [True]}, {"register": 2, "value": [True]}],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.add_coil(3, False)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [
                    {"register": 0, "value": [True]},
                    {"register": 2, "value": [True, False]},
                ],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.add_coil(1, False)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [{"register": 0, "value": [True, False, True, False]}],
                "input_registers": [],
                "holding_registers": [],
            },
        )

        self.sl.remove_coil(0)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [{"register": 1, "value": [False, True, False]}],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.remove_coil(2)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [{"register": 1, "value": [False]}, {"register": 3, "value": [False]}],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.remove_coil(3)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [{"register": 1, "value": [False]}],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.add_coil(2, True)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [{"register": 1, "value": [False, True]}],
                "input_registers": [],
                "holding_registers": [],
            },
        )

        self.sl.add_coil(0, True)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [{"register": 0, "value": [True, False, True]}],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.add_coil(2, True)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [{"register": 0, "value": [True, False, True]}],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.add_coil(3, False)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [{"register": 0, "value": [True, False, True, False]}],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.add_coil(1, False)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [{"register": 0, "value": [True, False, True, False]}],
                "input_registers": [],
                "holding_registers": [],
            },
        )

        self.sl.set_coil(0, False)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [{"register": 0, "value": [False, False, True, False]}],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.set_coil(1, True)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [{"register": 0, "value": [False, True, True, False]}],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.set_coil(2, False)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [{"register": 0, "value": [False, True, False, False]}],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.set_coil(3, True)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [{"register": 0, "value": [False, True, False, True]}],
                "input_registers": [],
                "holding_registers": [],
            },
        )

        self.assertEqual(self.sl.get_coil(0), False)
        self.assertEqual(self.sl.get_coil(1), True)
        self.assertEqual(self.sl.get_coil(2), False)
        self.assertEqual(self.sl.get_coil(3), True)

        self.sl.set_multi_coils(0, [True, False, True, False, True])
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [{"register": 0, "value": [True, False, True, False]}],
                "input_registers": [],
                "holding_registers": [],
            },
        )

        self.sl.set_multi_coils(0, [False, True, False, True])
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [{"register": 0, "value": [False, True, False, True]}],
                "input_registers": [],
                "holding_registers": [],
            },
        )

    def test_discrete_input(self):
        self.sl.add_discrete_input(0, True)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [{"register": 0, "value": [True]}],
                "coils": [],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.add_discrete_input(2, True)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [
                    {"register": 0, "value": [True]},
                    {"register": 2, "value": [True]},
                ],
                "coils": [],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.add_discrete_input(3, False)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [
                    {"register": 0, "value": [True]},
                    {"register": 2, "value": [True, False]},
                ],
                "coils": [],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.add_discrete_input(1, False)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [{"register": 0, "value": [True, False, True, False]}],
                "coils": [],
                "input_registers": [],
                "holding_registers": [],
            },
        )

        self.sl.remove_discrete_input(0)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [{"register": 1, "value": [False, True, False]}],
                "coils": [],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.remove_discrete_input(2)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [
                    {"register": 1, "value": [False]},
                    {"register": 3, "value": [False]},
                ],
                "coils": [],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.remove_discrete_input(3)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [{"register": 1, "value": [False]}],
                "coils": [],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.add_discrete_input(2, True)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [{"register": 1, "value": [False, True]}],
                "coils": [],
                "input_registers": [],
                "holding_registers": [],
            },
        )

        self.sl.add_discrete_input(0, True)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [{"register": 0, "value": [True, False, True]}],
                "coils": [],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.add_discrete_input(2, True)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [{"register": 0, "value": [True, False, True]}],
                "coils": [],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.add_discrete_input(3, False)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [{"register": 0, "value": [True, False, True, False]}],
                "coils": [],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.add_discrete_input(1, False)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [{"register": 0, "value": [True, False, True, False]}],
                "coils": [],
                "input_registers": [],
                "holding_registers": [],
            },
        )

        self.sl.set_discrete_input(0, False)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [{"register": 0, "value": [False, False, True, False]}],
                "coils": [],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.set_discrete_input(1, True)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [{"register": 0, "value": [False, True, True, False]}],
                "coils": [],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.set_discrete_input(2, False)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [{"register": 0, "value": [False, True, False, False]}],
                "coils": [],
                "input_registers": [],
                "holding_registers": [],
            },
        )
        self.sl.set_discrete_input(3, True)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [{"register": 0, "value": [False, True, False, True]}],
                "coils": [],
                "input_registers": [],
                "holding_registers": [],
            },
        )

        self.assertEqual(self.sl.get_discrete_input(0), False)
        self.assertEqual(self.sl.get_discrete_input(1), True)
        self.assertEqual(self.sl.get_discrete_input(2), False)
        self.assertEqual(self.sl.get_discrete_input(3), True)

        self.sl.set_multi_discrete_input(0, [True, False, True, False, True])
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [{"register": 0, "value": [True, False, True, False]}],
                "coils": [],
                "input_registers": [],
                "holding_registers": [],
            },
        )

        self.sl.set_multi_discrete_input(0, [False, True, False, True])
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [{"register": 0, "value": [False, True, False, True]}],
                "coils": [],
                "input_registers": [],
                "holding_registers": [],
            },
        )

    def test_holding_register(self):
        self.sl.add_holding_register(0, 0x0001)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [],
                "holding_registers": [{"register": 0, "value": [0x0001]}],
            },
        )
        self.sl.add_holding_register(2, 0x0405)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [],
                "holding_registers": [
                    {"register": 0, "value": [0x0001]},
                    {"register": 2, "value": [0x0405]},
                ],
            },
        )
        self.sl.add_holding_register(3, 0x0607)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [],
                "holding_registers": [
                    {"register": 0, "value": [0x0001]},
                    {"register": 2, "value": [0x0405, 0x0607]},
                ],
            },
        )
        self.sl.add_holding_register(1, 0x0203)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [],
                "holding_registers": [{"register": 0, "value": [0x0001, 0x0203, 0x0405, 0x0607]}],
            },
        )

        self.sl.remove_holding_register(0)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [],
                "holding_registers": [{"register": 1, "value": [0x0203, 0x0405, 0x0607]}],
            },
        )
        self.sl.remove_holding_register(2)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [],
                "holding_registers": [
                    {"register": 1, "value": [0x0203]},
                    {"register": 3, "value": [0x0607]},
                ],
            },
        )
        self.sl.remove_holding_register(3)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [],
                "holding_registers": [{"register": 1, "value": [0x0203]}],
            },
        )
        self.sl.add_holding_register(2, 0x0405)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [],
                "holding_registers": [{"register": 1, "value": [0x0203, 0x0405]}],
            },
        )

        self.sl.add_holding_register(0, 0x0001)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [],
                "holding_registers": [{"register": 0, "value": [0x0001, 0x0203, 0x0405]}],
            },
        )
        self.sl.add_holding_register(2, 0x0405)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [],
                "holding_registers": [{"register": 0, "value": [0x0001, 0x0203, 0x0405]}],
            },
        )
        self.sl.add_holding_register(3, 0x0607)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [],
                "holding_registers": [{"register": 0, "value": [0x0001, 0x0203, 0x0405, 0x0607]}],
            },
        )
        self.sl.add_holding_register(1, 0x0203)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [],
                "holding_registers": [{"register": 0, "value": [0x0001, 0x0203, 0x0405, 0x0607]}],
            },
        )

        self.sl.set_holding_register(0, 0x0100)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [],
                "holding_registers": [{"register": 0, "value": [0x0100, 0x0203, 0x0405, 0x0607]}],
            },
        )
        self.sl.set_holding_register(1, 0x0302)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [],
                "holding_registers": [{"register": 0, "value": [0x0100, 0x0302, 0x0405, 0x0607]}],
            },
        )
        self.sl.set_holding_register(2, 0x0504)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [],
                "holding_registers": [{"register": 0, "value": [0x0100, 0x0302, 0x0504, 0x0607]}],
            },
        )
        self.sl.set_holding_register(3, 0x0706)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [],
                "holding_registers": [{"register": 0, "value": [0x0100, 0x0302, 0x0504, 0x0706]}],
            },
        )

        self.assertEqual(self.sl.get_holding_register(0), 0x0100)
        self.assertEqual(self.sl.get_holding_register(1), 0x0302)
        self.assertEqual(self.sl.get_holding_register(2), 0x0504)
        self.assertEqual(self.sl.get_holding_register(3), 0x0706)

        self.sl.set_multi_holding_register(0, [0x0001, 0x0203, 0x0405, 0x0607, 0x0809])
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [],
                "holding_registers": [{"register": 0, "value": [0x0001, 0x0203, 0x0405, 0x0607]}],
            },
        )

        self.sl.set_multi_holding_register(0, [0x0607, 0x0405, 0x0203, 0x0001])
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [],
                "holding_registers": [{"register": 0, "value": [0x0607, 0x0405, 0x0203, 0x0001]}],
            },
        )

    def test_input_registers(self):
        self.sl.add_input_register(0, 0x0001)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [{"register": 0, "value": [0x0001]}],
                "holding_registers": [],
            },
        )
        self.sl.add_input_register(2, 0x0405)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [
                    {"register": 0, "value": [0x0001]},
                    {"register": 2, "value": [0x0405]},
                ],
                "holding_registers": [],
            },
        )
        self.sl.add_input_register(3, 0x0607)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [
                    {"register": 0, "value": [0x0001]},
                    {"register": 2, "value": [0x0405, 0x0607]},
                ],
                "holding_registers": [],
            },
        )
        self.sl.add_input_register(1, 0x0203)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [{"register": 0, "value": [0x0001, 0x0203, 0x0405, 0x0607]}],
                "holding_registers": [],
            },
        )

        self.sl.remove_input_register(0)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [{"register": 1, "value": [0x0203, 0x0405, 0x0607]}],
                "holding_registers": [],
            },
        )
        self.sl.remove_input_register(2)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [
                    {"register": 1, "value": [0x0203]},
                    {"register": 3, "value": [0x0607]},
                ],
                "holding_registers": [],
            },
        )
        self.sl.remove_input_register(3)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [{"register": 1, "value": [0x0203]}],
                "holding_registers": [],
            },
        )
        self.sl.add_input_register(2, 0x0405)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [{"register": 1, "value": [0x0203, 0x0405]}],
                "holding_registers": [],
            },
        )

        self.sl.add_input_register(0, 0x0001)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [{"register": 0, "value": [0x0001, 0x0203, 0x0405]}],
                "holding_registers": [],
            },
        )
        self.sl.add_input_register(2, 0x0405)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [{"register": 0, "value": [0x0001, 0x0203, 0x0405]}],
                "holding_registers": [],
            },
        )
        self.sl.add_input_register(3, 0x0607)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [{"register": 0, "value": [0x0001, 0x0203, 0x0405, 0x0607]}],
                "holding_registers": [],
            },
        )
        self.sl.add_input_register(1, 0x0203)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [{"register": 0, "value": [0x0001, 0x0203, 0x0405, 0x0607]}],
                "holding_registers": [],
            },
        )

        self.sl.set_input_register(0, 0x0100)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [{"register": 0, "value": [0x0100, 0x0203, 0x0405, 0x0607]}],
                "holding_registers": [],
            },
        )
        self.sl.set_input_register(1, 0x0302)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [{"register": 0, "value": [0x0100, 0x0302, 0x0405, 0x0607]}],
                "holding_registers": [],
            },
        )
        self.sl.set_input_register(2, 0x0504)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [{"register": 0, "value": [0x0100, 0x0302, 0x0504, 0x0607]}],
                "holding_registers": [],
            },
        )
        self.sl.set_input_register(3, 0x0706)
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [{"register": 0, "value": [0x0100, 0x0302, 0x0504, 0x0706]}],
                "holding_registers": [],
            },
        )

        self.assertEqual(self.sl.get_input_register(0), 0x0100)
        self.assertEqual(self.sl.get_input_register(1), 0x0302)
        self.assertEqual(self.sl.get_input_register(2), 0x0504)
        self.assertEqual(self.sl.get_input_register(3), 0x0706)

        self.sl.set_multi_input_register(0, [0x0001, 0x0203, 0x0405, 0x0607, 0x0809])
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [{"register": 0, "value": [0x0001, 0x0203, 0x0405, 0x0607]}],
                "holding_registers": [],
            },
        )

        self.sl.set_multi_input_register(0, [0x0607, 0x0405, 0x0203, 0x0001])
        self.assertEqual(
            self.sl.context,
            {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [{"register": 0, "value": [0x0607, 0x0405, 0x0203, 0x0001]}],
                "holding_registers": [],
            },
        )


if __name__ == "__main__":
    unittest.main()
