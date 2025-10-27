# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import m5can
import sys

if sys.platform != "esp32":
    from typing import Literal


class CAN(m5can.CAN):
    def __init__(
        self,
        id: Literal[0, 1] = 0,
        port: list | tuple = None,
        mode: int = m5can.CAN.NORMAL,
        prescaler: int = 0,
        sjw: int = 0,
        bs1: int = 0,
        bs2: int = 0,
        triple_sampling: bool = False,
        quantum_resolution_hz: int = 0,
        baudrate: int = 0,
        verbose: bool = False,
    ):
        verbose and print(
            f"mode={mode}, tx={port[1]}, rx={port[0]}, quantum_resolution_hz={quantum_resolution_hz}, brp={prescaler}, sjw={sjw}, tseg_1={bs1}, tseg_2={bs2}, triple_sampling={triple_sampling}, baudrate={baudrate}"
        )
        super().__init__(
            id,
            mode,
            port[1],
            port[0],
            quantum_resolution_hz,
            brp=prescaler,
            sjw=sjw,
            tseg_1=bs1,
            tseg_2=bs2,
            triple_sampling=triple_sampling,
            baudrate=baudrate // 1000,
        )


PWRCAN = CAN
