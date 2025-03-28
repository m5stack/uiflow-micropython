# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
import time
from collections import deque
from micropython import const


class ECGModule:
    """Create an ECGModule object.

    :param int id: UART id.
    :param int tx: the UART TX pin.
    :param int rx: the UART RX pin.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from module import ECGModule

            module_ecg = ECGModule(id = 1, tx = 7, rx = 1)
    """

    def __init__(self, id: int = 1, tx: int = 7, rx: int = 1):
        self.serial = machine.UART(id, baudrate=115200, tx=rx, rx=tx)  # 交叉
        self.serial.read()
        self.raw_ecg_buf_len = 320
        self.raw_ecg_buf = deque([], self.raw_ecg_buf_len)
        self._last_heartrate = -1
        self.FRAME_LEN = const(11)  # 帧固定为11字节

    def poll_data(self) -> None:
        """Poll data.

        This function checks for new data from the module and
        should be called repeatedly in a loop to ensure continuous
        data retrieval.

        UiFlow2 Code Block:

            |poll_data.png|

        MicroPython Code Block:

            .. code-block:: python

                module_ecg.poll_data()
        """
        while self.serial.any() >= self.FRAME_LEN:
            frame = self.serial.read(self.FRAME_LEN)
            if frame[0] != 0xAA or frame[-1] != 0xEF:
                continue
            data_length = frame[1] * 2
            if data_length != 8:
                continue
            raw_ecg = (frame[2] << 8) | frame[3]
            self.raw_ecg_buf.append(raw_ecg)
            self._last_heartrate = frame[9] if (frame[8] == 0x01) else -1

    def read_heartrate(self) -> int:
        """Read heartrate.

        :returns: heart rate
        :rtype: int

        If heart rate is no valid, return -1.

        UiFlow2 Code Block:

            |read_heartrate.png|

        MicroPython Code Block:

            .. code-block:: python

                module_ecg.read_heartrate()
        """
        return self._last_heartrate

    def read_raw_ecg_data(self) -> list:
        """Read raw ECG data.

        :returns: ECG data
        :rtype: list

        UiFlow2 Code Block:

            |read_raw_ecg_data.png|

        MicroPython Code Block:

            .. code-block:: python

                module_ecg.read_raw_ecg_data()
        """
        return list(self.raw_ecg_buf)
