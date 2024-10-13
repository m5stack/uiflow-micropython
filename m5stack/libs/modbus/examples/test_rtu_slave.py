import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import modbus
import serial
import time
import asyncio


ser = serial.Serial("COM22", 115200)
slave = modbus.ModbusRTUSlave(
    uart=ser,
    verbose=True,
    context={
        "discrete_inputs": [
            {
                "register": 67,  # register address of the input status register
                "val": [
                    0,
                ],  # used to set a register, not possible for ISTS
                "description": "Optional description of the input status register",
                "range": [0, 1],
                "unit": "activated",
            }
        ],
        "coils": [
            {
                "register": 1000,  # register address of the coil
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
                ],  # used to set a register
                "description": "Optional description of the coil",  # the onwards mentioned keys are optional
                "range": [
                    0,
                    1,
                ],  # may provide a range of the value, only for documentation purpose
                "unit": "BOOL",  # may provide a unit of the value, only for documentation purpose
            }
        ],
        "input_registers": [
            {
                "register": 10,  # register address of the input register
                "val": [
                    60001,
                ],  # used to set a register, not possible for IREGS
                "description": "Optional description of the static input register",
                "range": [0, 65535],
                "unit": "millivolt",
            }
        ],
        "holding_registers": [
            {
                "register": 93,  # register address of the holding register
                "val": [
                    19,
                ],  # used to set a register
                "description": "Optional description of the holding register",
                "range": [0, 65535],
                "unit": "Hz",
            }
        ],
    },
)


def cb_01(start_reg, reg_num, context):
    print("cb_01:")
    print("\tstart register:", start_reg)
    print("\tregister number:", reg_num)
    print("\tcontext:", context)


def cb_02(start_reg, reg_num, context):
    print("cb_02:")
    print("\tstart register:", start_reg)
    print("\tregister number:", reg_num)
    print("\tcontext:", context)


def cb_03(start_reg, reg_num, context):
    print("cb_03:")
    print("\tstart register:", start_reg)
    print("\tregister number:", reg_num)
    print("\tcontext:", context)


def cb_04(start_reg, reg_num, context):
    print("cb_04:")
    print("\tstart register:", start_reg)
    print("\tregister number:", reg_num)
    print("\tcontext:", context)


def cb_05(reg_addr, data, context):
    print("cb_05:")
    print("\tregister address:", reg_addr)
    print("\tdata:", data)


def cb_06(reg_addr, data, context):
    print("cb_06:")
    print("\tregister address:", reg_addr)
    print("\tdata:", data)


# https://blog.csdn.net/xukai871105/article/details/16368567
def cb_15(start_reg, reg_num, data, context):
    print("cb_15:")


# https://blog.csdn.net/xukai871105/article/details/16368567
def cb_16(start_reg, reg_num, data, context):
    print("cb_16:")


slave.cb[0x01] = cb_01

asyncio.run(slave.run_async())
