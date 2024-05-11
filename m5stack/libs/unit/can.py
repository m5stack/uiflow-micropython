# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from m5can import CAN


class CANUnit(CAN):
    def __init__(self, port, mode, baudrate=125000):
        timing_table = {
            25000: (128, 16, 8, 3, False),
            50000: (80, 15, 4, 3, False),
            100000: (40, 15, 4, 3, False),
            125000: (32, 15, 4, 3, False),
            250000: (16, 15, 4, 3, False),
            500000: (8, 15, 4, 3, False),
            800000: (4, 16, 8, 3, False),
            1000000: (4, 15, 4, 3, False),
        }
        timing = timing_table.get(baudrate)
        super().__init__(
            0,
            mode,
            port[1],
            port[0],
            timing[0],  # prescaler
            timing[3],  # sjw
            timing[1],  # bs1
            timing[2],  # bs2
            timing[4],  # triple_sampling
        )


MiniCANUnit = CANUnit
