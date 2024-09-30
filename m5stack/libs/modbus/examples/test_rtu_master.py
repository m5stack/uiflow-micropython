import sys
import time

uart = None
device_addr = 4

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
    import os

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import serial

    uart = serial.Serial("COM20", 115200)

import modbus

rtu_master = modbus.ModbusRTUMaster(uart=uart)

# while True:
rtu_master.write_single_coil(device_addr, 1000, False)
time.sleep(1)
res = rtu_master.read_coils(device_addr, 1000, 1)
print("read:", res)
time.sleep(1)
rtu_master.write_single_coil(device_addr, 1000, True)
res = rtu_master.read_coils(device_addr, 1000, 1)
print("read:", res)
time.sleep(1)
