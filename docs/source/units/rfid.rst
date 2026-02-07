
RFID Unit
==========
.. sku:U031
.. include:: ../refs/unit.rfid.ref

RFIDUnit is a hardware module designed for RFID card reading and writing operations. It extends the MFRC522 driver, supporting card detection, reading, writing, and advanced features like selecting and waking up RFID cards.

Support the following products:

|RFIDUnit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/rfid/rfid_cores3_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |rfid_cores3_example.m5f2|

class RFIDUnit
--------------

Constructors
------------

.. class:: RFIDUnit(i2c, address)

    Initialize the RFIDUnit with I2C communication and an optional address.

    :param  i2c: The I2C interface instance.
    :param int address: The I2C address of the RFIDUnit. Default is 0x28.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: RFIDUnit.is_new_card_present()

    Check if a new RFID card is present.


    UIFLOW2:

        |is_new_card_present.png|

.. method:: RFIDUnit.read_card_uid()

    Read the UID of the RFID card if available.


    UIFLOW2:

        |read_card_uid.png|

.. method:: RFIDUnit.read(block_addr)

    Read a specific block from the RFID card.

    :param  block_addr: The block address to read data from.

    UIFLOW2:

        |read.png|

.. method:: RFIDUnit.write(block_addr, buffer)

    Write data to a specific block on the RFID card.

    :param  block_addr: The block address to write data to.
    :param  buffer: The data buffer to write to the block.

    UIFLOW2:

        |write.png|

.. method:: RFIDUnit.close()

    Halt the PICC and stop the encrypted communication session.


    UIFLOW2:

        |close.png|

.. method:: RFIDUnit.wakeup_all()

    Wake up all RFID cards within range.

.. method:: RFIDUnit.picc_select_card()

    Select the currently active RFID card.