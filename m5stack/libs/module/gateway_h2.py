# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import esp_zigbee_host
from esp_zigbee_host import SwitchEndpoint


class GatewayH2Module:
    """Create GatewayH2Module object.

    :param int id: UART id. range:1~2
    :param int rx: the UART RX pin.
    :param int tx: the UART TX pin.

    """

    def __init__(self, id: int = 1, rx: int = 17, tx: int = 10, boot: int = 18, en: int = 7):
        self.id = id
        self.tx = rx  # 交叉
        self.rx = tx
        self.boot = boot
        self.en = en

    def create_switch_ep(self):
        return SwitchEndpoint(id=self.id, tx=self.tx, rx=self.rx)
