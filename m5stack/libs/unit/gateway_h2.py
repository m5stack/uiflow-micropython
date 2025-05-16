# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import esp_zigbee_host
from esp_zigbee_host import SwitchEndpoint
import sys

if sys.platform != "esp32":
    from typing import Literal


class GatewayH2Unit:
    """Create GatewayH2Unit object.

    :param int id: The UART ID for communication with the GatewayH2 Unit. It can be 1, 2.
    :param port: A list or tuple containing the TX and RX pins for UART communication.
    """

    def __init__(self, id: Literal[1, 2] = 2, port: list | tuple = None):
        self.id = id
        self.rx = port[0]  # 交叉
        self.tx = port[1]

    def create_switch_ep(self):
        return SwitchEndpoint(id=self.id, tx=self.tx, rx=self.rx)
