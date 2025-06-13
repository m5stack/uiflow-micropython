# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import M5
from collections import namedtuple
from driver.dmx512 import DMX512

MBusIO = namedtuple("MBusIO", ["bus_tx", "bus_rx", "en"])

iomap = {
    M5.BOARD.M5Stack: MBusIO(13, 35, 12),
    M5.BOARD.M5StackCore2: MBusIO(19, 35, 27),
    M5.BOARD.M5StackCoreS3: MBusIO(7, 10, 6),
    M5.BOARD.M5Tough: MBusIO(19, 35, 27),
    M5.BOARD.M5Tab5: MBusIO(48, 16, 2),
}.get(M5.getBoard())


class DMX512Module(DMX512):
    def __init__(self, id=1, mode=DMX512.DMX_MASTER):
        super().__init__(id, [iomap.bus_rx, iomap.bus_tx], mode, iomap.en)
