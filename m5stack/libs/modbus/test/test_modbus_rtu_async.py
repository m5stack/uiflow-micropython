# SPDX-FileCopyrightText: Copyright (c) 2021 Tobias Eydam
# SPDX-FileCopyrightText: Copyright (c) 2024 lbuque, written for M5Stack
#
# SPDX-License-Identifier: MIT

import os
import sys

if sys.implementation.name == "cpython":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from modbus.master import ModbusRTUMaster
from modbus.slave import ModbusRTUSlave
import asyncio

if sys.implementation.name == "micropython":
    import machine
if sys.implementation.name == "cpython":
    import serial


class Test(unittest.TestCase):
    def setUp(self):
        # with serial.Serial("COM22") as uart1:
        self.device_address = 0x01
        if sys.implementation.name == "micropython":
            self.sm_ser = machine.UART(
                1,
                baudrate=115200,
                bits=8,
                parity=None,
                stop=1,
                tx=2,
                rx=1,
                txbuf=1024,
                rxbuf=1024,
                timeout=0,
                timeout_char=0,
                invert=0,
                flow=0,
            )
            self.sl_ser = machine.UART(
                2,
                baudrate=115200,
                bits=8,
                parity=None,
                stop=1,
                tx=17,
                rx=18,
                txbuf=1024,
                rxbuf=1024,
                timeout=0,
                timeout_char=0,
                invert=0,
                flow=0,
            )
        if sys.implementation.name == "cpython":
            self.sm_ser = serial.Serial("COM20")
            self.sl_ser = serial.Serial("COM22")
        self.sl = ModbusRTUSlave(
            context={
                "coils": [
                    {
                        "register": 1000,
                        "value": [True, False, True, False, True, False, True, False, True, False],
                    }
                ],  # Coils: ON OFF ON OFF ON OFF ON OFF ON OFF
                "discrete_inputs": [
                    {
                        "register": 1000,
                        "value": [True, False, True, False, True, False, True, False, True, False],
                    }
                ],  # Digital Inputs: ON OFF ON OFF ON OFF ON OFF ON OFF
                "holding_registers": [
                    {
                        "register": 1000,
                        "value": [0x0001, 0x0203, 0x0405, 0x0607, 0x0809, 0x0A0B, 0x0C0D, 0x0E0F],
                    }
                ],
                "input_registers": [
                    {
                        "register": 1000,
                        "value": [0x0001, 0x0203, 0x0405, 0x0607, 0x0809, 0x0A0B, 0x0C0D, 0x0E0F],
                    }
                ],
            },
            uart=self.sl_ser,
            verbose=True,
            device_address=self.device_address,
        )
        # return super().setUp()

    def tearDown(self):
        if sys.implementation.name == "micropython":
            # self.sm_ser.deinit()
            # self.sl_ser.deinit()
            pass
        if sys.implementation.name == "cpython":
            self.sm_ser.close()
            self.sl_ser.close()
        # return super().tearDown()

    async def run_coroutines(self, coro_list):
        await asyncio.gather(*coro_list)

    def test_read_coils_async(self):
        async def client_routine():
            ms = ModbusRTUMaster(uart=self.sm_ser)
            self.assertEqual(await ms.read_coils_async(self.device_address, 1000, 1), [True])
            self.assertEqual(await ms.read_coils_async(self.device_address, 1001, 1), [False])
            self.assertEqual(
                await ms.read_coils_async(self.device_address, 1000, 2), [True, False]
            )
            self.assertEqual(
                await ms.read_coils_async(self.device_address, 1001, 2), [False, True]
            )
            self.assertEqual(
                await ms.read_coils_async(self.device_address, 1000, 3), [True, False, True]
            )
            self.sl.stop()

        asyncio.run(self.run_coroutines([self.sl.run_async(), client_routine()]))

    def test_read_discrete_inputs_async(self):
        async def client_routine():
            ms = ModbusRTUMaster(uart=self.sm_ser)
            self.assertEqual(
                await ms.read_discrete_inputs_async(self.device_address, 1000, 1), [True]
            )
            self.assertEqual(
                await ms.read_discrete_inputs_async(self.device_address, 1000, 2), [True, False]
            )
            self.assertEqual(
                await ms.read_discrete_inputs_async(self.device_address, 1000, 3),
                [True, False, True],
            )
            self.assertEqual(
                await ms.read_discrete_inputs_async(self.device_address, 1001, 1), [False]
            )
            self.assertEqual(
                await ms.read_discrete_inputs_async(self.device_address, 1001, 2), [False, True]
            )
            self.assertEqual(
                await ms.read_discrete_inputs_async(self.device_address, 1001, 3),
                [False, True, False],
            )
            self.sl.stop()

        asyncio.run(self.run_coroutines([self.sl.run_async(), client_routine()]))

    def test_read_holding_registers_async(self):
        async def client_routine():
            ms = ModbusRTUMaster(uart=self.sm_ser)
            self.assertEqual(
                await ms.read_holding_registers_async(self.device_address, 1000, 1),
                [0x0001],
            )
            self.assertEqual(
                await ms.read_holding_registers_async(self.device_address, 1000, 2),
                [0x0001, 0x0203],
            )
            self.assertEqual(
                await ms.read_holding_registers_async(self.device_address, 1001, 2),
                [0x0203, 0x0405],
            )
            self.assertEqual(
                await ms.read_holding_registers_async(self.device_address, 1002, 3),
                [0x0405, 0x0607, 0x0809],
            )
            self.sl.stop()

        asyncio.run(self.run_coroutines([self.sl.run_async(), client_routine()]))

    def test_read_input_registers_async(self):
        async def client_routine():
            ms = ModbusRTUMaster(uart=self.sm_ser)
            self.assertEqual(
                await ms.read_input_registers_async(self.device_address, 1000, 1),
                [0x0001],
            )
            self.assertEqual(
                await ms.read_input_registers_async(self.device_address, 1000, 2),
                [0x0001, 0x0203],
            )
            self.assertEqual(
                await ms.read_input_registers_async(self.device_address, 1001, 2),
                [0x0203, 0x0405],
            )
            self.assertEqual(
                await ms.read_input_registers_async(self.device_address, 1002, 3),
                [0x0405, 0x0607, 0x0809],
            )
            self.sl.stop()

        asyncio.run(self.run_coroutines([self.sl.run_async(), client_routine()]))

    def test_read_write_coils_async(self):
        async def client_routine():
            ms = ModbusRTUMaster(uart=self.sm_ser)
            self.assertEqual(await ms.write_single_coil_async(self.device_address, 1001, 1), True)
            self.assertEqual(
                await ms.read_coils_async(self.device_address, 1000, 3), [True, True, True]
            )
            self.assertEqual(await ms.write_single_coil_async(self.device_address, 1001, 0), False)
            self.assertEqual(
                await ms.read_coils_async(self.device_address, 1000, 3), [True, False, True]
            )
            self.assertEqual(
                await ms.write_multiple_coils_async(self.device_address, 1000, [True, True, True]),
                3,
            )
            self.assertEqual(
                await ms.read_coils_async(self.device_address, 1000, 3), [True, True, True]
            )
            self.assertEqual(
                await ms.write_multiple_coils_async(
                    self.device_address, 1000, [False, False, False]
                ),
                3,
            )
            self.assertEqual(
                await ms.read_coils_async(self.device_address, 1000, 3), [False, False, False]
            )
            self.sl.stop()

        asyncio.run(self.run_coroutines([self.sl.run_async(), client_routine()]))

    def test_read_write_holding_register_async(self):
        async def client_routine():
            ms = ModbusRTUMaster(uart=self.sm_ser)
            self.assertEqual(
                await ms.write_single_register_async(self.device_address, 1000, 0xFFEE),
                0xFFEE,
            )
            self.assertEqual(
                await ms.read_holding_registers_async(self.device_address, 1000, 1), [0xFFEE]
            )
            self.assertEqual(
                await ms.write_single_register_async(self.device_address, 1001, 0xFFEE),
                0xFFEE,
            )
            self.assertEqual(
                await ms.read_holding_registers_async(self.device_address, 1000, 2),
                [0xFFEE, 0xFFEE],
            )
            self.sl.stop()

        asyncio.run(self.run_coroutines([self.sl.run_async(), client_routine()]))


if __name__ == "__main__":
    unittest.main()
