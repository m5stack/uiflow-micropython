# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from driver.atgm336h import ATGM336H
import sys

if sys.platform != "esp32":
    from typing import Literal


class GPSV11Unit(ATGM336H):
    """
    note:
        en: GPS Unit v1.1 is a GNSS global positioning navigation unit, integrating the high-performance CASIC navigation chip AT6668 and signal amplifier chip MAX2659, with a built-in ceramic antenna, providing more precise and reliable satellite positioning services.
        link: https://docs.m5stack.com/en/unit/Unit-GPS%20v1.1
        image: https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/products/unit/Unit-GPS%20v1.1/4.webp
        category: Unit

    example:
        - ../../../examples/unit/gps_example.py

    m5f2:
        - unit/gps_example.m5f2
    """

    def __init__(self, id: Literal[0, 1, 2] = 1, port: list | tuple = None):
        """
        note:
            en: Initialize the GPSUnit with a specific UART id and port for communication.

        params:
            id:
                note: The UART ID for communication with the GPS module. It can be 0, 1, or 2.
            port:
                note: A list or tuple containing the TX and RX pins for UART communication.
        """
        super().__init__(id, port[1], port[0])
