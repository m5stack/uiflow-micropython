# MFRC522 commands. Described in chapter 10 of the datasheet.

# no action, cancels current command execution
PCD_IDLE = const(0x00)

# stores 25 bytes into the internal buffer
PCD_MEM = const(0x01)

# generates a 10-uint8_t random ID number
PCD_GENERATERANDOMID = const(0x02)

# activates the CRC coprocessor or performs a self test
PCD_CALCCRC = const(0x03)

# transmits data from the FIFO buffer
PCD_TRANSMIT = const(0x04)

# no command change, can be used to modify the CommandReg register bits without
# affecting the command, for example, the PowerDown bit
PCD_NOCMDCHANGE = const(0x07)

# activates the receiver circuits
PCD_RECEIVE = const(0x08)

# transmits data from FIFO buffer to antenna and automatically activates the
# receiver after transmission
PCD_TRANSCEIVE = const(0x0C)

# performs the MIFARE standard authentication as a reader
PCD_MFAUTHENT = const(0x0E)

# resets the MFRC522
PCD_SOFTRESET = const(0x0F)

# Commands sent to the PICC.
# The commands used by the PCD to manage communication with several PICCs (ISO 14443-3, Type A, section 6.4)

# REQuest command, Type A. 
# Invites PICCs in state IDLE to go to READY and prepare for anticollision or
# selection. 7 bit frame.
PICC_CMD_REQA = const(0x26)

# Wake-UP command, Type A. 
# Invites PICCs in state IDLE and HALT to go to READY(*) and prepare for 
# anticollision or selection. 7 bit frame.
PICC_CMD_WUPA = const(0x52)

# Cascade Tag. Not really a command, but used during anti collision.
PICC_CMD_CT = const(0x88)

# Anti collision/Select, Cascade Level 1
PICC_CMD_SEL_CL1 = const(0x93)

# Anti collision/Select, Cascade Level 2
PICC_CMD_SEL_CL2 = const(0x95)

# Anti collision/Select, Cascade Level 3
PICC_CMD_SEL_CL3 = const(0x97)

# HaLT command, Type A. Instructs an ACTIVE PICC to go to state HALT.
PICC_CMD_HLTA = const(0x50)

# The commands used for MIFARE Classic (from http://www.nxp.com/documents/data_sheet/MF1S503x.pdf, Section 9)
# Use PCD_MFAuthent to authenticate access to a sector, then use these commands
# to read/write/modify the blocks on the sector.
#
# The read/write commands can also be used for MIFARE Ultralight.

# Perform authentication with Key A
PICC_CMD_MF_AUTH_KEY_A = const(0x60)

# Perform authentication with Key B
PICC_CMD_MF_AUTH_KEY_B = const(0x61)

# Reads one 16 uint8_t block from the authenticated sector of the PICC.
# Also used for MIFARE Ultralight.
PICC_CMD_MF_READ = const(0x30)

# Writes one 16 uint8_t block to the authenticated sector of the PICC.
# Called "COMPATIBILITY WRITE" for MIFARE Ultralight.
PICC_CMD_MF_WRITE = const(0xA0)

# Decrements the contents of a block and stores the result in the internal data
# register.
PICC_CMD_MF_DECREMENT = const(0xC0)

# Increments the contents of a block and stores the result in the internal data
# register.
PICC_CMD_MF_INCREMENT = const(0xC1)

# Reads the contents of a block into the internal data register.
PICC_CMD_MF_RESTORE = const(0xC2)

# Writes the contents of the internal data register to a block.
PICC_CMD_MF_TRANSFER = const(0xB0)

# The commands used for MIFARE Ultralight (from http://www.nxp.com/documents/data_sheet/MF0ICU1.pdf, Section 8.6)
# The PICC_CMD_MF_READ and PICC_CMD_MF_WRITE can also be used for MIFARE Ultralight.

# Writes one 4 uint8_t page to the PICC.
PICC_CMD_UL_WRITE = const(0xA2)
