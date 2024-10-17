# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import sys
import machine
from driver.jrd4035 import JRD4035

if sys.platform != "esp32":
    from typing import Literal


class UHFRFIDUnit(JRD4035):
    def __init__(self, id: Literal[0, 1, 2], port: list | tuple, verbose: bool = False):
        uart = machine.UART(id, 115200, tx=port[1], rx=port[0])
        super().__init__(uart, verbose=verbose)

    def inventory(self) -> str:
        return super().inventory().hex()

    def read_mem_bank(
        self, bank: int, offset: int, length: int, access_password: str = "00000000"
    ):
        return (
            super()
            .read_mem_bank(bank, offset, length, access=bytes.fromhex(access_password))
            .hex()
        )

    def write_mem_bank(
        self, bank: int, offset: int, data: bytes, access_password: str = "00000000"
    ):
        return super().write_mem_bank(bank, offset, data, access=bytes.fromhex(access_password))

    def select(
        self, target: int, action: int, membank: int, pointer: int, truncate: bool, mask: str
    ):
        return super().select(target, action, membank, pointer, truncate, bytes.fromhex(mask))

    def set_access_password(self, old_password: str, new_password: str):
        return super().set_access_password(
            bytes.fromhex(old_password), bytes.fromhex(new_password)
        )

    def set_kill_password(self, password: str):
        return super().set_kill_password(bytes.fromhex(password))

    def kill(self, password: str):
        return super().kill(bytes.fromhex(password))

    def lock_mem_bank(
        self,
        kill_lock: int = 0b00,
        access_lock: int = 0b00,
        epc_lock: int = 0b00,
        tid_lock: int = 0b00,
        user_lock: int = 0b00,
        access: str = "00000000",
    ):
        return super().lock_mem_bank(
            kill_lock, access_lock, epc_lock, tid_lock, user_lock, bytes.fromhex(access)
        )

    def get_impinj_monza_qt_sr(self, persistence, password: str = "00000000"):
        return super().get_impinj_monza_qt_sr(persistence, bytes.fromhex(password))

    def get_impinj_monza_qt_mem(self, persistence, password: str = "00000000"):
        return super().get_impinj_monza_qt_mem(persistence, bytes.fromhex(password))

    def set_impinj_monza_qt_sr(self, qt_sr: bool, persistence: int, password: str = "00000000"):
        return super().set_impinj_monza_qt_sr(persistence, qt_sr, bytes.fromhex(password))

    def set_impinj_monza_qt_mem(self, qt_mem: bool, persistence: int, password: str = "00000000"):
        return super().set_impinj_monza_qt_mem(persistence, qt_mem, bytes.fromhex(password))

    def nxp_eas_alarm(self):
        return super().nxp_eas_alarm().hex()

    def get_nxp_config_word(self, password: str = "00000000") -> int:
        return super().nxp_read_config_word(bytes.fromhex(password))

    def set_nxp_config_word(self, config_word: int, password: str = "00000000"):
        return super().set_nxp_confog_word(config_word, bytes.fromhex(password))

    def nxp_read_protect(self, set, password: str = "00000000"):
        return super().nxp_read_protect(set, bytes.fromhex(password))

    def nxp_change_eas(self, set, password: str = "00000000"):
        return super().nxp_change_eas(set, bytes.fromhex(password))
