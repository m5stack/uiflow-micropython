# SPDX-FileCopyrightText: Copyright (c) 2024 lbuque, written for M5Stack
#
# SPDX-License-Identifier: MIT

import sys
import os
import time

if sys.implementation.name == "micropython":
    import machine

    uart = machine.UART(
        1,
        baudrate=115200,
        bits=8,
        parity=None,
        stop=1,
        tx=14,
        rx=13,
        txbuf=256,
        rxbuf=256,
        timeout=0,
        timeout_char=0,
        invert=0,
        flow=0,
    )
else:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import serial

    uart = serial.Serial("COM20", 115200)

import modbus


device_addr = 4
rtu_master = modbus.ModbusRTUMaster(uart=uart, device_addr=device_addr)

ver = rtu_master.read_holding_registers(device_addr, 1, 1)
print("AC/DC SSR Control Example")
print("firmware version:", ver)
time.sleep(1)

while True:
    rtu_master.write_single_coil(device_addr, 0, False)
    time.sleep(1)
    rtu_master.write_single_register(device_addr, 0, 0xF800.to_bytes(2, "big"))
    time.sleep(1)
    rtu_master.write_single_register(device_addr, 0, 0x07E0.to_bytes(2, "big"))
    time.sleep(1)
    rtu_master.write_single_register(device_addr, 0, 0x001F.to_bytes(2, "big"))
    time.sleep(1)
    rtu_master.write_single_coil(device_addr, 0, True)
    time.sleep(1)
