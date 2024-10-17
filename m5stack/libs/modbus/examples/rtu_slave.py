# SPDX-FileCopyrightText: Copyright (c) 2024 lbuque, written for M5Stack
#
# SPDX-License-Identifier: MIT

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
                "value": [
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
                "value": [
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
                "value": [
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
                "value": [
                    19,
                ],  # used to set a register
                "description": "Optional description of the holding register",
                "range": [0, 65535],
                "unit": "Hz",
            }
        ],
    },
)


def modbus_read_coils_cb(modbus_obj, starting_register: int, value: list):
    print("modbus_read_coils_cb", starting_register, value)


def modbus_read_discrete_inputs_cb(modbus_obj, starting_register: int, value: list):
    print("modbus_read_discrete_inputs_cb", starting_register, value)


def modbus_read_holding_registers_cb(modbus_obj, starting_register: int, value: list):
    print("modbus_read_holding_registers_cb", starting_register, value)


def modbus_read_input_registers_cb(modbus_obj, starting_register: int, value: list):
    print("modbus_read_input_registers_cb", starting_register, value)


def modbus_write_single_coil_cb(modbus_obj, register: int, value: bool):
    print("modbus_write_single_coil_cb", register, value)


def modbus_write_single_registers_cb(modbus_obj, register: int, value: int):
    print("modbus_write_single_registers_cb", register, value)


def modbus_write_multiple_coils_cb(modbus_obj, starting_register: int, value: list):
    print("modbus_write_multiple_coils_cb", starting_register, value)


def modbus_write_multiple_registers_cb(modbus_obj, starting_register: int, value: list):
    print("modbus_write_multiple_registers_cb", starting_register, value)


# READ_COILS_EVENT = 0x01
# READ_DISCRETE_INPUTS_EVENT = 0x02
# READ_HOLDING_REGISTERS_EVENT = 0x03
# READ_INPUT_REGISTERS_EVENT = 0x04
# WRITE_SINGLE_COIL_EVENT = 0x05
# WRITE_SINGLE_REGISTER_EVENT = 0x06
# WRITE_MULTIPLE_COILS_EVENT = 0x0F
# WRITE_MULTIPLE_REGISTERS_EVENT = 0x10

slave.set_callback(slave.READ_COILS_EVENT, modbus_read_coils_cb)
slave.set_callback(slave.READ_DISCRETE_INPUTS_EVENT, modbus_read_discrete_inputs_cb)
slave.set_callback(slave.READ_HOLDING_REGISTERS_EVENT, modbus_read_holding_registers_cb)
slave.set_callback(slave.READ_INPUT_REGISTERS_EVENT, modbus_read_input_registers_cb)
slave.set_callback(slave.WRITE_SINGLE_COIL_EVENT, modbus_write_single_coil_cb)
slave.set_callback(slave.WRITE_SINGLE_REGISTER_EVENT, modbus_write_single_registers_cb)
slave.set_callback(slave.WRITE_MULTIPLE_COILS_EVENT, modbus_write_multiple_coils_cb)
slave.set_callback(slave.WRITE_MULTIPLE_REGISTERS_EVENT, modbus_write_multiple_registers_cb)

asyncio.run(slave.run_async())
