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
import _thread

if sys.implementation.name == "micropython":
    import machine
if sys.implementation.name == "cpython":
    import serial
import time

running = False


def slave_loop(args):
    global running
    sl = args
    time.sleep(1)
    while running:
        sl.tick()
        time.sleep(0.1)


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
            uart=self.sl_ser,
            verbose=True,
            device_address=self.device_address,
        )
        global running
        running = True
        self.thread_id = _thread.start_new_thread(slave_loop, (self.sl,))
        time.sleep(1)

    #         return super().setUp()

    def tearDown(self):
        global running
        running = False
        time.sleep(3)
        if sys.implementation.name == "micropython":
            # self.sm_ser.deinit()
            # self.sl_ser.deinit()
            pass
        if sys.implementation.name == "cpython":
            self.sm_ser.close()
            self.sl_ser.close()
        # return super().tearDown()

    def test_read_coils(self):
        ms = ModbusRTUMaster(uart=self.sm_ser)
        self.assertEqual(ms.read_coils(self.device_address, 1000, 1), [True])
        self.assertEqual(ms.read_coils(self.device_address, 1001, 1), [False])
        self.assertEqual(ms.read_coils(self.device_address, 1000, 2), [True, False])
        self.assertEqual(ms.read_coils(self.device_address, 1001, 2), [False, True])
        self.assertEqual(ms.read_coils(self.device_address, 1000, 3), [True, False, True])
        self.sl.stop()

    def test_read_discrete_inputs(self):
        ms = ModbusRTUMaster(uart=self.sm_ser)
        self.assertEqual(ms.read_discrete_inputs(self.device_address, 1000, 1), [True])
        self.assertEqual(ms.read_discrete_inputs(self.device_address, 1000, 2), [True, False])
        self.assertEqual(
            ms.read_discrete_inputs(self.device_address, 1000, 3),
            [True, False, True],
        )
        self.assertEqual(ms.read_discrete_inputs(self.device_address, 1001, 1), [False])
        self.assertEqual(ms.read_discrete_inputs(self.device_address, 1001, 2), [False, True])
        self.assertEqual(
            ms.read_discrete_inputs(self.device_address, 1001, 3),
            [False, True, False],
        )
        self.sl.stop()

    def test_read_holding_registers(self):
        ms = ModbusRTUMaster(uart=self.sm_ser)
        self.assertEqual(
            ms.read_holding_registers(self.device_address, 1000, 1),
            [0x0001],
        )
        self.assertEqual(
            ms.read_holding_registers(self.device_address, 1000, 2),
            [0x0001, 0x0203],
        )
        self.assertEqual(
            ms.read_holding_registers(self.device_address, 1001, 2),
            [0x0203, 0x0405],
        )
        self.assertEqual(
            ms.read_holding_registers(self.device_address, 1002, 3),
            [0x0405, 0x0607, 0x0809],
        )
        self.sl.stop()

    def test_read_input_registers(self):
        ms = ModbusRTUMaster(uart=self.sm_ser)
        self.assertEqual(
            ms.read_input_registers(self.device_address, 1000, 1),
            [0x0001],
        )
        self.assertEqual(
            ms.read_input_registers(self.device_address, 1000, 2),
            [0x0001, 0x0203],
        )
        self.assertEqual(
            ms.read_input_registers(self.device_address, 1001, 2),
            [0x0203, 0x0405],
        )
        self.assertEqual(
            ms.read_input_registers(self.device_address, 1002, 3),
            [0x0405, 0x0607, 0x0809],
        )
        self.sl.stop()

    def test_read_write_coils(self):
        ms = ModbusRTUMaster(uart=self.sm_ser)
        self.assertEqual(ms.write_single_coil(self.device_address, 1001, 1), True)
        self.assertEqual(ms.read_coils(self.device_address, 1000, 3), [True, True, True])
        self.assertEqual(ms.write_single_coil(self.device_address, 1001, 0), False)
        self.assertEqual(ms.read_coils(self.device_address, 1000, 3), [True, False, True])
        self.assertEqual(
            ms.write_multiple_coils(self.device_address, 1000, [True, True, True]),
            3,
        )
        self.assertEqual(ms.read_coils(self.device_address, 1000, 3), [True, True, True])
        self.assertEqual(
            ms.write_multiple_coils(self.device_address, 1000, [False, False, False]),
            3,
        )
        self.assertEqual(ms.read_coils(self.device_address, 1000, 3), [False, False, False])
        self.sl.stop()

    def test_read_write_holding_register(self):
        ms = ModbusRTUMaster(uart=self.sm_ser)
        self.assertEqual(
            ms.write_single_register(self.device_address, 1000, 0xFFEE),
            0xFFEE,
        )
        self.assertEqual(ms.read_holding_registers(self.device_address, 1000, 1), [0xFFEE])
        self.assertEqual(
            ms.write_single_register(self.device_address, 1001, 0xFFEE),
            0xFFEE,
        )
        self.assertEqual(ms.read_holding_registers(self.device_address, 1000, 2), [0xFFEE, 0xFFEE])
        self.sl.stop()


if __name__ == "__main__":
    unittest.main()
