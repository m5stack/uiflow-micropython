from driver.mfrc522 import MFRC522


class RFIDUnit(MFRC522):
    def __init__(self, i2c, addr=0x28) -> None:
        super().__init__(i2c, addr)
        self.pcd_init()

    def is_new_card_present(self) -> bool:
        bufferATQA = bytearray(2)
        result = self.picc_request_a(bufferATQA)
        if result == self.STATUS_OK or result == self.STATUS_COLLISION:
            return True
        result = self.picc_wakeup_a(bufferATQA)
        return result == self.STATUS_OK

    def read_card_uid(self):
        if self.picc_read_card_serial():
            return self._uid.uid

    def read(self, block_addr):
        buffer = bytearray(16)
        self.pcd_authenticate(0x60, block_addr, bytearray(b"\xFF\xFF\xFF\xFF\xFF\xFF"), self._uid)
        if self.mifare_read(block_addr, buffer) == self.STATUS_OK:
            return buffer
        else:
            return None

    def write(self, block_addr, buffer) -> int:
        BUFFER16 = bytearray(16)
        self.pcd_authenticate(0x60, block_addr, bytearray(b"\xFF\xFF\xFF\xFF\xFF\xFF"), self._uid)
        self.mifare_read(block_addr, BUFFER16)
        l = 16 if len(buffer) > 16 else len(buffer)
        BUFFER16[:l] = buffer[:l]

        if self.mifare_write(block_addr, BUFFER16) == self.STATUS_OK:
            del BUFFER16
            return l
        else:
            del BUFFER16
            return 0

    def close(self) -> None:
        self.picc_halt_a()  # Halt the PICC before stopping the encrypted session.
        self.pcd_stop_crypto1()

    def wakeup_all(self) -> bool:
        bufferATQA = bytearray()
        return self.picc_wakeup_a(bufferATQA) == self.STATUS_OK

    def picc_select_card(self) -> bool:
        return self.picc_select(self._uid) == self.STATUS_OK
