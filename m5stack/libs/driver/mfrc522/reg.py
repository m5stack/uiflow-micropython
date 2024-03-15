# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from micropython import const
# MFRC522 registers. Described in chapter 9 of the datasheet.
# Page 0: Command and status

# starts and stops command execution
COMMAND_REG = const(0x01)

# enable and disable interrupt request control bits
COMIEN_REG = const(0x02)

# enable and disable interrupt request control bits
DIVIEN_REG = const(0x03)

# interrupt request bits
COMIRQ_REG = const(0x04)

# interrupt request bits
DIVIRQ_REG = const(0x05)

# error bits showing the error status of the last command executed
ERROR_REG = const(0x06)

# communication status bits
STATUS1_REG = const(0x07)

# receiver and transmitter status bits
STATUS2_REG = const(0x08)

# input and output of 64 uint8_t FIFO buffer
FIFODATA_REG = const(0x09)

# number of bytes stored in the FIFO buffer
FIFOLEVEL_REG = const(0x0A)

# level for FIFO underflow and overflow warning
WATERLEVEL_REG = const(0x0B)

# miscellaneous control registers
CONTROL_REG = const(0x0C)

# adjustments for bit-oriented frames
BITFRAMING_REG = const(0x0D)

# bit position of the first bit-collision detected on the RF interface
COLL_REG = const(0x0E)

# Page 1: Command
# defines general modes for transmitting and receiving
MODE_REG = const(0x11)

# defines transmission data rate and framing
TXMODE_REG = const(0x12)

# defines reception data rate and framing
RXMODE_REG = const(0x13)

# controls the logical behavior of the antenna driver pins TX1 and TX2
TXCONTROL_REG = const(0x14)

# controls the setting of the transmission modulation
TXASK_REG = const(0x15)

# selects the internal sources for the antenna driver
TXSEL_REG = const(0x16)

# selects internal receiver settings
RXSEL_REG = const(0x17)

# selects thresholds for the bit decoder
RXTHRESHOLD_REG = const(0x18)

# defines demodulator settings
DEMOD_REG = const(0x19)

# controls some MIFARE communication transmit parameters
MFTX_REG = const(0x1C)

# controls some MIFARE communication receive parameters
MFRX_REG = const(0x1D)

# selects the speed of the serial UART interface
SERIALSPEED_REG = const(0x1F)

# Page 2: Configuration
# shows the MSB and LSB values of the CRC calculation
CRCRESULT_REGH = const(0x21)
CRCRESULT_REGL = const(0x22)

# controls the ModWidth setting?
MODWIDTH_REG = const(0x24)

# configures the receiver gain
RFCFG_REG = const(0x26)

# selects the conductance of the antenna driver pins TX1 and TX2 for modulation
GSN_REG = const(0x27)

# defines the conductance of the p-driver output during periods of no modulation
CWGSP_REG = const(0x28)

# defines the conductance of the p-driver output during periods of modulation
MODGSP_REG = const(0x29)

# defines settings for the internal timer
TMODE_REG = const(0x2A)

# the lower 8 bits of the TPrescaler value. The 4 high bits are in TModeReg.
TPRESCALER_REG = const(0x2B)

# defines the 16-bit timer reload value
TRELOAD_REGH = const(0x2C)
TRELOAD_REGL = const(0x2D)

# shows the 16-bit timer value
TCOUNTERVALUE_REGH = const(0x2E)
TCOUNTERVALUE_REGL = const(0x2F)

# Page 3: Test Registers
# general test signal configuration
TESTSEL1_REG = const(0x31)

# general test signal configuration
TESTSEL2_REG = const(0x32)

# enables pin output driver on pins D1 to D7
TESTPINEN_REG = const(0x33)

# defines the values for D1 to D7 when it is used as an I/O bus
TESTPINVALUE_REG = const(0x34)

# shows the status of the internal test bus
TESTBUS_REG = const(0x35)

# controls the digital self test
AUTOTEST_REG = const(0x36)

# shows the software version
VERSION_REG = const(0x37)

# controls the pins AUX1 and AUX2
ANALOGTEST_REG = const(0x38)

# defines the test value for TestDAC1
TESTDAC1_REG = const(0x39)

# defines the test value for TestDAC2
TESTDAC2_REG = const(0x3A)

# shows the value of ADC I and Q channels
TESTADC_REG = const(0x3B)
