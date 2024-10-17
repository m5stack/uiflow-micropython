# SPDX-FileCopyrightText: Copyright (c) 2024 lbuque, written for M5Stack
#
# SPDX-License-Identifier: MIT
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import modbus

srv = modbus.ModbusTCPServer(
    "0.0.0.0",
    5000,
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

# asyncio.run(srv.run_async())

srv.start()
while True:
    srv.tick()
