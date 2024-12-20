# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.mfrc522 import MFRC522


class RFIDUnit(MFRC522):
    """
    note:
        en: RFIDUnit is a hardware module designed for RFID card reading and writing operations. It extends the MFRC522 driver, supporting card detection, reading, writing, and advanced features like selecting and waking up RFID cards.

    details:
        link: https://docs.m5stack.com/en/unit/rfid
        image: https://static-cdn.m5stack.com/resource/docs/products/unit/rfid/rfid_01.webp
        category: Unit

    example:
        - ../../../examples/unit/rfid/rfid_cores3_example.py

    m5f2:
        - unit/rfid/rfid_cores3_example.m5f2
    """

    def __init__(self, i2c, address: int | list | tuple = 0x28) -> None:
        """
        note:
            en: Initialize the RFIDUnit with I2C communication and an optional address.

        params:
            i2c:
                note: The I2C interface instance.
            address:
                note: The I2C address of the RFIDUnit. Default is 0x28.
        """
        super().__init__(i2c, address)
        self.pcd_init()

    def is_new_card_present(self) -> bool:
        """
        note:
            en: Check if a new RFID card is present.

        params:
            note:

        returns:
            note: True if a new card is detected, False otherwise.
        """
        buffer_atqa = bytearray(2)
        result = self.picc_request_a(buffer_atqa)
        if result == self.STATUS_OK or result == self.STATUS_COLLISION:
            return True
        result = self.picc_wakeup_a(buffer_atqa)
        return result == self.STATUS_OK

    def read_card_uid(self):
        """
        note:
            en: Read the UID of the RFID card if available.

        params:
            note:

        returns:
            note: The UID of the RFID card as a bytearray, or None if unavailable.
        """
        if self.picc_read_card_serial():
            return self._uid.uid

    def read(self, block_addr):
        """
        note:
            en: Read a specific block from the RFID card.

        params:
            block_addr:
                note: The block address to read data from.

        returns:
            note: A bytearray of 16 bytes from the specified block, or None if the operation fails.
        """
        buffer = bytearray(16)
        self.pcd_authenticate(0x60, block_addr, bytearray(b"\xff\xff\xff\xff\xff\xff"), self._uid)
        if self.mifare_read(block_addr, buffer) == self.STATUS_OK:
            return buffer
        else:
            return None

    def write(self, block_addr, buffer) -> int:
        """
        note:
            en: Write data to a specific block on the RFID card.

        params:
            block_addr:
                note: The block address to write data to.
            buffer:
                note: The data buffer to write to the block.

        returns:
            note: The number of bytes written, or 0 if the operation fails.
        """
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
        """
        note:
            en: Halt the PICC and stop the encrypted communication session.

        params:
            note:
        """
        self.picc_halt_a()
        self.pcd_stop_crypto1()

    def wakeup_all(self) -> bool:
        """
        note:
            en: Wake up all RFID cards within range.

        params:
            note:

        returns:
            note: True if successful, False otherwise.
        """
        buffer_atqa = bytearray()
        return self.picc_wakeup_a(buffer_atqa) == self.STATUS_OK

    def picc_select_card(self) -> bool:
        """
        note:
            en: Select the currently active RFID card.

        params:
            note:

        returns:
            note: True if the card selection is successful, False otherwise.
        """
        return self.picc_select(self._uid) == self.STATUS_OK
