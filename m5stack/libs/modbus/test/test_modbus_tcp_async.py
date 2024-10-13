# SPDX-FileCopyrightText: Copyright (c) 2021 Tobias Eydam
# SPDX-FileCopyrightText: Copyright (c) 2024 lbuque, written for M5Stack
#
# SPDX-License-Identifier: MIT
import os
import sys

if sys.implementation.name == "cpython":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import asyncio
from modbus.slave import ModbusTCPServer
from modbus.master import ModbusTCPClient


class Test(unittest.TestCase):
    def setUp(self):
        self.slave_address = 0x01
        self.srv = ModbusTCPServer(
            "127.0.0.1",
            505,
            context={
                "coils": [
                    {
                        "register": 1000,
                        "val": [True, False, True, False, True, False, True, False, True, False],
                    }
                ],  # Coils: ON OFF ON OFF ON OFF ON OFF ON OFF
                "discrete_inputs": [
                    {
                        "register": 1000,
                        "val": [True, False, True, False, True, False, True, False, True, False],
                    }
                ],  # Digital Inputs: ON OFF ON OFF ON OFF ON OFF ON OFF
                "holding_registers": [
                    {
                        "register": 1000,
                        "val": [0x0001, 0x0203, 0x0405, 0x0607, 0x0809, 0x0A0B, 0x0C0D, 0x0E0F],
                    }
                ],
                "input_registers": [
                    {
                        "register": 1000,
                        "val": [0x0001, 0x0203, 0x0405, 0x0607, 0x0809, 0x0A0B, 0x0C0D, 0x0E0F],
                    }
                ],
            },
            verbose=True,
        )
        self.srv.start()
        return super().setUp()

    async def run_coroutines(self, coro_list):
        await asyncio.gather(*coro_list)

    def test_read_coils_async(self):
        async def client_routine():
            cl = ModbusTCPClient("127.0.0.1", 505)
            cl.connect()
            self.assertEqual(await cl.read_coils_async(self.slave_address, 1000, 1), [True])
            self.assertEqual(await cl.read_coils_async(self.slave_address, 1001, 1), [False])
            self.assertEqual(await cl.read_coils_async(self.slave_address, 1000, 2), [True, False])
            self.assertEqual(await cl.read_coils_async(self.slave_address, 1001, 2), [False, True])
            self.assertEqual(
                await cl.read_coils_async(self.slave_address, 1000, 3), [True, False, True]
            )
            cl.disconnect()
            self.srv.stop()

        asyncio.run(self.run_coroutines([self.srv.run_async(), client_routine()]))

    def test_read_digital_inputs_async(self):
        async def client_routine():
            cl = ModbusTCPClient("127.0.0.1", 505)
            cl.connect()
            self.assertEqual(
                await cl.read_discrete_inputs_async(self.slave_address, 1000, 1), [True]
            )
            self.assertEqual(
                await cl.read_discrete_inputs_async(self.slave_address, 1000, 2), [True, False]
            )
            self.assertEqual(
                await cl.read_discrete_inputs_async(self.slave_address, 1000, 3),
                [True, False, True],
            )
            self.assertEqual(
                await cl.read_discrete_inputs_async(self.slave_address, 1001, 1), [False]
            )
            self.assertEqual(
                await cl.read_discrete_inputs_async(self.slave_address, 1001, 2), [False, True]
            )
            self.assertEqual(
                await cl.read_discrete_inputs_async(self.slave_address, 1001, 3),
                [False, True, False],
            )
            cl.disconnect()
            self.srv.stop()

        asyncio.run(self.run_coroutines([self.srv.run_async(), client_routine()]))

    def test_read_holding_registers_async(self):
        async def client_routine():
            cl = ModbusTCPClient("127.0.0.1", 505)
            cl.connect()
            self.assertEqual(
                await cl.read_holding_registers_async(self.slave_address, 1000, 1), [0x0001]
            )
            self.assertEqual(
                await cl.read_holding_registers_async(self.slave_address, 1000, 2),
                [0x0001, 0x0203],
            )
            self.assertEqual(
                await cl.read_holding_registers_async(self.slave_address, 1001, 2),
                [0x0203, 0x0405],
            )
            self.assertEqual(
                await cl.read_holding_registers_async(self.slave_address, 1002, 3),
                [0x0405, 0x0607, 0x0809],
            )
            cl.disconnect()
            self.srv.stop()

        asyncio.run(self.run_coroutines([self.srv.run_async(), client_routine()]))

    def test_read_input_registers_async(self):
        async def client_routine():
            cl = ModbusTCPClient("127.0.0.1", 505)
            cl.connect()
            self.assertEqual(
                await cl.read_input_registers_async(self.slave_address, 1000, 1),
                [0x0001],
            )
            self.assertEqual(
                await cl.read_input_registers_async(self.slave_address, 1000, 2),
                [0x0001, 0x0203],
            )
            self.assertEqual(
                await cl.read_input_registers_async(self.slave_address, 1001, 2),
                [0x0203, 0x0405],
            )
            self.assertEqual(
                await cl.read_input_registers_async(self.slave_address, 1002, 3),
                [0x0405, 0x0607, 0x0809],
            )
            cl.disconnect()
            self.srv.stop()

        asyncio.run(self.run_coroutines([self.srv.run_async(), client_routine()]))

    def test_read_write_coils_async(self):
        async def client_routine():
            cl = ModbusTCPClient("127.0.0.1", 505)
            cl.connect()
            self.assertEqual(await cl.write_single_coil_async(self.slave_address, 1001, 1), True)
            self.assertEqual(
                await cl.read_coils_async(self.slave_address, 1000, 3), [True, True, True]
            )
            self.assertEqual(await cl.write_single_coil_async(self.slave_address, 1001, 0), False)
            self.assertEqual(
                await cl.read_coils_async(self.slave_address, 1000, 3), [True, False, True]
            )
            self.assertEqual(
                await cl.write_multiple_coils_async(self.slave_address, 1000, [True, True, True]),
                3,
            )
            self.assertEqual(
                await cl.read_coils_async(self.slave_address, 1000, 3), [True, True, True]
            )
            self.assertEqual(
                await cl.write_multiple_coils_async(
                    self.slave_address, 1000, [False, False, False]
                ),
                3,
            )
            self.assertEqual(
                await cl.read_coils_async(self.slave_address, 1000, 3), [False, False, False]
            )
            cl.disconnect()
            self.srv.stop()

        asyncio.run(self.run_coroutines([self.srv.run_async(), client_routine()]))

    def test_read_write_holding_register_async(self):
        async def client_routine():
            cl = ModbusTCPClient("127.0.0.1", 505)
            cl.connect()
            self.assertEqual(
                await cl.write_single_register_async(self.slave_address, 1000, 0xFFEE), 0xFFEE
            )
            self.assertEqual(
                await cl.read_holding_registers_async(self.slave_address, 1000, 1), [0xFFEE]
            )
            self.assertEqual(
                await cl.write_single_register_async(self.slave_address, 1001, 0xFFEE), 0xFFEE
            )
            self.assertEqual(
                await cl.read_holding_registers_async(self.slave_address, 1000, 2),
                [0xFFEE, 0xFFEE],
            )
            cl.disconnect()
            self.srv.stop()

        asyncio.run(self.run_coroutines([self.srv.run_async(), client_routine()]))

    def test_write_multiple_registers_async(self):
        async def client_routine():
            cl = ModbusTCPClient("127.0.0.1", 505)
            cl.connect()
            self.assertEqual(
                await cl.write_multiple_registers_async(self.slave_address, 1000, [0xFFEE]), 1
            )
            self.assertEqual(
                await cl.read_holding_registers_async(self.slave_address, 1000, 1), [0xFFEE]
            )
            self.assertEqual(
                await cl.write_multiple_registers_async(self.slave_address, 1001, [0xFFEE]), 1
            )
            self.assertEqual(
                await cl.read_holding_registers_async(self.slave_address, 1000, 2),
                [0xFFEE, 0xFFEE],
            )
            cl.disconnect()
            self.srv.stop()

        asyncio.run(self.run_coroutines([self.srv.run_async(), client_routine()]))


if __name__ == "__main__":
    unittest.main()
