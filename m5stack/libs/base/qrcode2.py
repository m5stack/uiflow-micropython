# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
from driver.qrcode.qrcode_m14 import QRCodeM14


class AtomicQRCode2Base(QRCodeM14):
    """Create an AtomicQRCode2Base object.

    :param int id: UART id.
    :param int tx: the UART TX pin.
    :param int rx: the UART RX pin.
    :param int trig: the trigger pin.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from base import AtomicQRCode2Base

            base_qrcode2 = AtomicQRCode2Base(id = 1, tx = 6, rx = 5, trig = 7)
    """

    def __init__(self, id: int = 1, tx: int = 5, rx: int = 6, trig: int = 7):
        super().__init__(id, tx, rx, trig)
