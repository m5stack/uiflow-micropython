# SPDX-FileCopyrightText: Copyright (c) 2024 lbuque, written for M5Stack
#
# SPDX-License-Identifier: MIT

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import modbus
import time

device_addr = 4

cl = modbus.ModbusTCPClient("127.0.0.1", 505)
cl.connect()
# while True:
cl.write_single_coil(device_addr, 1000, False)
time.sleep(1)
res = cl.read_coils(device_addr, 1000, 1)
print("read:", res)
time.sleep(1)
cl.write_single_coil(device_addr, 1000, True)
res = cl.read_coils(device_addr, 1000, 1)
print("read:", res)
time.sleep(1)
cl.disconnect()
