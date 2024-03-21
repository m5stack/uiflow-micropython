# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.mfrc522 import MFRC522


class RFIDUnit(MFRC522):
    def __init__(self, i2c, addr=0x28, address: int | list | tuple = 0x28) -> None:
        # TODO: 2.0.6 移除 addr 参数
        address = addr
        super().__init__(i2c, address)
        self.pcd_init()

    def is_new_card_present(self) -> bool:
        buffer_atqa = bytearray(2)
        result = self.picc_request_a(buffer_atqa)
        if result == self.STATUS_OK or result == self.STATUS_COLLISION:
            return True
        result = self.picc_wakeup_a(buffer_atqa)
        return result == self.STATUS_OK

    def read_card_uid(self):
        if self.picc_read_card_serial():
            return self._uid.uid

    def read(self, block_addr):
        buffer = bytearray(16)
        self.pcd_authenticate(0x60, block_addr, bytearray(b"\xff\xff\xff\xff\xff\xff"), self._uid)
        if self.mifare_read(block_addr, buffer) == self.STATUS_OK:
            return buffer
        else:
            return None

    def write(self, block_addr, buffer) -> int:
        buffer16 = bytearray(16)
        self.pcd_authenticate(0x60, block_addr, bytearray(b"\xff\xff\xff\xff\xff\xff"), self._uid)
        self.mifare_read(block_addr, buffer16)
        l = 16 if len(buffer) > 16 else len(buffer)
        buffer16[:l] = buffer[:l]

        if self.mifare_write(block_addr, buffer16) == self.STATUS_OK:
            del buffer16
            return l
        else:
            del buffer16
            return 0

    def close(self) -> None:
        self.picc_halt_a()  # Halt the PICC before stopping the encrypted session.
        self.pcd_stop_crypto1()

    def wakeup_all(self) -> bool:
        buffer_atqa = bytearray()
        return self.picc_wakeup_a(buffer_atqa) == self.STATUS_OK

    def picc_select_card(self) -> bool:
        return self.picc_select(self._uid) == self.STATUS_OK
