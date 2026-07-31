# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import M5
import machine
import time
from driver.m5ioe1 import M5ioe1, Pin
from driver.nfc import NFCReader


class NFC(NFCReader):
    """Onboard ST25R3916 NFC reader using the board-specific I2C bus."""

    def __init__(self) -> None:
        _i2c_map = {
            # i2c_id, scl_pin, sda_pin, freq
            M5.BOARD.M5PaperMono: (1, 48, 47, 100000),
            M5.BOARD.M5StackChan: (1, 11, 12, 100000),
        }
        board_id = M5.getBoard()
        if board_id not in _i2c_map:
            raise NotImplementedError("NFC is not supported on this board")
        i2c_id, scl_pin, sda_pin, freq = _i2c_map[board_id]
        i2c = machine.I2C(
            i2c_id,
            scl=machine.Pin(scl_pin),
            sda=machine.Pin(sda_pin),
            freq=freq,
        )
        if board_id == M5.BOARD.M5PaperMono:
            self._power_pin = Pin(M5ioe1(i2c, 0x4F), 4, Pin.OUT)
            self._power_pin.on()
        time.sleep(1)
        if 0x50 not in i2c.scan():
            raise RuntimeError("NFC device not found on I2C bus")
        super().__init__(i2c)
