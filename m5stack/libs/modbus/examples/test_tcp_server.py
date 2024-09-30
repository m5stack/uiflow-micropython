import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import modbus

srv = modbus.ModbusTCPServer(
    "127.0.0.1",
    505,
    context={
        "co": {
            "startAddr": 1000,
            "registers": bytearray([0xFF, 0x00, 0x00, 0x00] * 5),
        },  # Coils: ON OFF ON OFF ON OFF ON OFF ON OFF
        "di": {
            "startAddr": 1000,
            "registers": bytearray([0xFF, 0x00, 0x00, 0x00] * 5),
        },  # Digital Inputs: ON OFF ON OFF ON OFF ON OFF ON OFF
        "hr": {
            "startAddr": 1000,
            "registers": bytearray(
                [
                    0x00,
                    0x01,
                    0x02,
                    0x03,
                    0x04,
                    0x05,
                    0x06,
                    0x07,
                    0x08,
                    0x09,
                    0x0A,
                    0x0B,
                    0x0C,
                    0x0D,
                    0x0E,
                    0x0F,
                ]
            ),
        },
        "ir": {
            "startAddr": 1000,
            "registers": bytearray(
                [
                    0x00,
                    0x01,
                    0x02,
                    0x03,
                    0x04,
                    0x05,
                    0x06,
                    0x07,
                    0x08,
                    0x09,
                    0x0A,
                    0x0B,
                    0x0C,
                    0x0D,
                    0x0E,
                    0x0F,
                ]
            ),
        },
    },
)

asyncio.run(srv.run_async())
