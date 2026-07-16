# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

"""ST25R3916 ISO14443A reader driver.

The transport layer supports both the original Unit NFC I2C wiring and SPI
wiring used by NFCCap. Pass ``i2c`` for I2C mode, or pass ``spi`` together with
``cs`` for SPI mode. The high-level NFC helpers in ``unit.nfc`` can wrap either
transport through this driver.
"""

import time
import random

from .mifare_classic1 import (
    append_parity_bitstream,
    byteswap_u32,
    crc16_iso14443a,
    Crypto1,
    key_to_u48,
    nt_from_rb,
    suc_23,
    uid_tail_u32_be,
)


OP_TRAILER_MASK = 0x3F
OP_READ = 0x40
OP_WRITE = 0x00
CMD_SPACE_B = 0xFB
OP_LOAD_FIFO = 0x80
OP_READ_FIFO = 0x9F

CMD_SET_DEFAULT = 0xC1
CMD_STOP_ALL_ACTIVITIES = 0xC2
CMD_TRANSMIT_WITH_CRC = 0xC4
CMD_TRANSMIT_WITHOUT_CRC = 0xC5
CMD_TRANSMIT_REQA = 0xC6
CMD_TRANSMIT_WUPA = 0xC7
CMD_NFC_INITIAL_FIELD_ON = 0xC8
CMD_RESET_RX_GAIN = 0xD5
CMD_ADJUST_REGULATORS = 0xD6
CMD_CLEAR_FIFO = 0xDB
CMD_TEST_ACCESS = 0xFC

REG_IO_CONFIGURATION_1 = 0x00
REG_IO_CONFIGURATION_2 = 0x01
REG_OPERATION_CONTROL = 0x02
REG_MODE_DEFINITION = 0x03
REG_BITRATE_DEFINITION = 0x04
REG_ISO14443A_SETTINGS = 0x05
REG_AUXILIARY_DEFINITION = 0x0A
REG_RECEIVER_CONFIGURATION_1 = 0x0B
REG_RECEIVER_CONFIGURATION_2 = 0x0C
REG_RECEIVER_CONFIGURATION_3 = 0x0D
REG_RECEIVER_CONFIGURATION_4 = 0x0E
REG_NO_RESPONSE_TIMER_1 = 0x10
REG_TIMER_AND_EMV_CONTROL = 0x12
REG_MASK_MAIN_INTERRUPT = 0x16
REG_MAIN_INTERRUPT = 0x1A
REG_FIFO_STATUS_1 = 0x1E
REG_NUMBER_OF_TRANSMITTED_BYTES_1 = 0x22
REG_TX_DRIVER = 0x28
REG_NFCIP_1_PASSIVE_TARGET_DEFINITION = 0x08
REG_PASSIVE_TARGET_MODULATION = 0x29
REG_EXTERNAL_FIELD_DETECTOR_ACTIVATION_THRESHOLD = 0x2A
REG_EXTERNAL_FIELD_DETECTOR_DEACTIVATION_THRESHOLD = 0x2B
REG_ANTENNA_TUNING_CONTROL_1 = 0x26
REG_ANTENNA_TUNING_CONTROL_2 = 0x27
REG_AUXILIARY_DISPLAY = 0x31
REG_IC_IDENTITY = 0x3F

REG_SPACE_B_EMD_SUPPRESSION = 0x0005
REG_SPACE_B_RESISTIVE_AM = 0x002A
REG_CORRELATOR_CONFIGURATION_1 = 0x0C
REG_CORRELATOR_CONFIGURATION_2 = 0x0D
REG_OVERSHOOT_PROTECTION_CONFIGURATION_1 = 0x30
REG_OVERSHOOT_PROTECTION_CONFIGURATION_2 = 0x31
REG_UNDERSHOOT_PROTECTION_CONFIGURATION_1 = 0x32
REG_UNDERSHOOT_PROTECTION_CONFIGURATION_2 = 0x33

VALID_IDENTIFY_TYPE = 0x05
IO_CONFIGURATION_I2C_400K_3V3 = 0x1084
TX_AM_DEFAULT_NIBBLE = 13
OP_EN = 0x80
WU = 0x04
I_OSC = 0x80
OSC_OK = 0x10
AAT_EN = 0x20
MASK_PRE_ADJUST = 0xFFFF00FF

TX_EN = 0x08
RX_EN = 0x40
NO_CRC_RX = 0x80
ANTCL = 0x01
DIS_CORR = 0x04

RXCFG1_Z600K = 0x08
RXCFG2_STABLE = 0x2D
RXCFG3_STABLE = 0xD8
RXCFG4_STABLE = 0x22

TIMEOUT_REQ_WUP_MS = 12
TIMEOUT_ANTICOLL_MS = 8
TIMEOUT_SELECT_MS = 8
TIMEOUT_RATS_MS = 12
TIMEOUT_DEP_MS = 30

CASCADE_TAG = 0x88
SAK_CASCADE_FLAG = 0x04

# nfca.hpp Command (subset)
CMD_RATS = 0xE0
CMD_GET_VERSION = 0x60
# Type 2 / Ultralight family (same 0x30 / 0xA2 on wire as MIFARE READ; Classic needs auth first)
CMD_READ = 0x30
CMD_WRITE_PAGE = 0xA2
MIFARE_WRITE_BLOCK = 0xA0
MIFARE_AUTH_KEY_A = 0x60
MIFARE_AUTH_KEY_B = 0x61
ACK_NIBBLE = 0x0A

# ISO14443A settings: TX with parity
NO_TX_PAR = 0x80

TIMEOUT_T2_READ_MS = 24
TIMEOUT_T2_WRITE_MS = 40

FC_HZ = 13560000


def _elapsed_ms(t0):
    return time.ticks_diff(time.ticks_ms(), t0)


class _ST25R3916I2CTransport:
    def __init__(self, i2c, addr=0x50):
        self.i2c = i2c
        self.addr = addr

    def direct_command(self, cmd, payload=None):
        if payload:
            self.i2c.writeto(self.addr, bytes((cmd,)) + payload, True)
        else:
            self.i2c.writeto(self.addr, bytes((cmd,)), True)

    def read_reg8(self, reg):
        return self.i2c.readfrom_mem(self.addr, reg | OP_READ, 1)[0]

    def write_reg8(self, reg, value):
        self.i2c.writeto_mem(self.addr, reg, bytes((value & 0xFF,)))

    def read_reg8_space_b_addr(self, reg_addr):
        mem = (CMD_SPACE_B << 8) | (OP_READ | (reg_addr & OP_TRAILER_MASK))
        return self.i2c.readfrom_mem(self.addr, mem, 1, addrsize=16)[0]

    def write_reg8_space_b_addr(self, reg_addr, value):
        mem = (CMD_SPACE_B << 8) | (OP_WRITE | (reg_addr & OP_TRAILER_MASK))
        self.i2c.writeto_mem(self.addr, mem, bytes((value & 0xFF,)), addrsize=16)

    def write_fifo(self, payload):
        self.i2c.writeto(self.addr, bytes((OP_LOAD_FIFO,)) + payload, True)

    def read_fifo(self, n):
        return self.i2c.readfrom_mem(self.addr, OP_READ_FIFO, n)

    def wait_irq(self, timeout_ms):
        return False


class _ST25R3916SPITransport:
    def __init__(self, spi, cs, irq=None):
        import machine

        self.spi = spi
        self.cs = cs if hasattr(cs, "value") else machine.Pin(cs, machine.Pin.OUT, value=1)
        self.irq = (
            irq if hasattr(irq, "value") or irq is None else machine.Pin(irq, machine.Pin.IN)
        )

    def _transfer(self, tx, rx_len=0):
        tx = bytes(tx)
        if hasattr(self.spi, "init"):
            self.spi.init(baudrate=2000000, polarity=0, phase=1)
        self.cs.value(0)
        try:
            if rx_len:
                write_buf = bytearray(len(tx) + rx_len)
                write_buf[: len(tx)] = tx
                read_buf = bytearray(len(write_buf))
                self.spi.write_readinto(write_buf, read_buf)
                return bytes(read_buf[len(tx) :])
            self.spi.write(tx)
            return b""
        finally:
            self.cs.value(1)

    def direct_command(self, cmd, payload=None):
        if payload:
            self._transfer(bytes((cmd,)) + payload)
        else:
            self._transfer((cmd,))

    def read_reg8(self, reg):
        return self._transfer((reg | OP_READ,), 1)[0]

    def write_reg8(self, reg, value):
        self._transfer((reg & OP_TRAILER_MASK, value & 0xFF))

    def read_reg8_space_b_addr(self, reg_addr):
        return self._transfer((CMD_SPACE_B, OP_READ | (reg_addr & OP_TRAILER_MASK)), 1)[0]

    def write_reg8_space_b_addr(self, reg_addr, value):
        self._transfer((CMD_SPACE_B, OP_WRITE | (reg_addr & OP_TRAILER_MASK), value & 0xFF))

    def write_fifo(self, payload):
        self._transfer(bytes((OP_LOAD_FIFO,)) + payload)

    def read_fifo(self, n):
        return self._transfer((OP_READ_FIFO,), n)

    def wait_irq(self, timeout_ms):
        if self.irq is None:
            return False
        t0 = time.ticks_ms()
        while _elapsed_ms(t0) < timeout_ms:
            if self.irq.value():
                return True
            time.sleep_ms(1)
        return bool(self.irq.value())


class ST25R3916NFCA:
    """ST25R3916 NFC-A driver with selectable I2C/SPI transport.

    ``i2c`` keeps compatibility with Unit NFC. ``spi``/``cs`` selects SPI mode,
    used by NFCCap where ST25R3916 shares the SPI bus with CC1101.
    ``transport`` is mainly for tests or board-specific wrappers.
    """

    def __init__(self, i2c=None, addr=0x50, spi=None, cs=None, irq=None, transport=None):
        """Create the driver in I2C mode, SPI mode, or with a custom transport."""
        if transport is not None:
            self.io = transport
        elif spi is not None:
            if cs is None:
                raise ValueError("cs is required for ST25R3916 SPI mode")
            self.io = _ST25R3916SPITransport(spi, cs, irq)
        else:
            self.io = _ST25R3916I2CTransport(i2c, addr)
        self._mf_c1 = None

    def direct_command(self, cmd, payload=None):
        self.io.direct_command(cmd, payload)
        time.sleep_ms(2)

    def read_reg8(self, reg):
        return self.io.read_reg8(reg)

    def write_reg8(self, reg, value):
        self.io.write_reg8(reg, value)

    def read_reg16_be(self, reg):
        hi = self.read_reg8(reg)
        lo = self.read_reg8(reg + 1)
        return (hi << 8) | lo

    def write_reg16_be(self, reg, value):
        self.write_reg8(reg, (value >> 8) & 0xFF)
        self.write_reg8(reg + 1, value & 0xFF)

    def write_reg32_be(self, reg, value):
        self.write_reg8(reg, (value >> 24) & 0xFF)
        self.write_reg8(reg + 1, (value >> 16) & 0xFF)
        self.write_reg8(reg + 2, (value >> 8) & 0xFF)
        self.write_reg8(reg + 3, value & 0xFF)

    def read_reg8_space_b_addr(self, reg_addr):
        return self.io.read_reg8_space_b_addr(reg_addr)

    def write_reg8_space_b_addr(self, reg_addr, value):
        self.io.write_reg8_space_b_addr(reg_addr, value)
        time.sleep_us(50)

    def write_reg8_space_b(self, reg_low8, value):
        self.write_reg8_space_b_addr(reg_low8, value)

    def set_bits(self, reg, bits):
        v = self.read_reg8(reg)
        self.write_reg8(reg, v | bits)

    def clear_bits(self, reg, bits):
        v = self.read_reg8(reg)
        self.write_reg8(reg, v & (0xFF ^ bits))

    def clear_interrupts(self):
        self.read_reg8(REG_MAIN_INTERRUPT)
        self.read_reg8(REG_MAIN_INTERRUPT + 1)
        self.read_reg8(REG_MAIN_INTERRUPT + 2)
        self.read_reg8(REG_MAIN_INTERRUPT + 3)

    def write_fifo(self, payload):
        self.io.write_fifo(payload)
        time.sleep_us(50)

    def read_fifo(self, n):
        return self.io.read_fifo(n)

    def wait_irq(self, timeout_ms):
        return self.io.wait_irq(timeout_ms)

    def _wait_event_or_sleep(self, t0, timeout_ms):
        remain = timeout_ms - _elapsed_ms(t0)
        if remain <= 0:
            return False
        wait_ms = min(remain, 5)
        if self.wait_irq(wait_ms):
            time.sleep_ms(1)
            return True
        time.sleep_ms(1)
        return False

    def read_fifo_size(self):
        s = self.read_reg16_be(REG_FIFO_STATUS_1)
        bytes_cnt = (s >> 8) | ((s & 0x00C0) << 2)
        bits_cnt = (s >> 1) & 0x07
        return bytes_cnt, bits_cnt

    def _calculate_nrt(self, ms, nrt_step):
        us = ms * 1000
        step = (4096 * 1000000) if nrt_step else (64 * 1000000)
        nrt = (us * FC_HZ + step - 1) // step
        nrt = max(1, min(0xFFFF, nrt))
        return nrt

    def write_fwt_timer(self, timeout_ms):
        ctrl = self.read_reg8(REG_TIMER_AND_EMV_CONTROL)
        nrt_step = (ctrl & 0x01) != 0
        nrt = self._calculate_nrt(timeout_ms, nrt_step)
        self.write_reg16_be(REG_NO_RESPONSE_TIMER_1, nrt)
        return True

    def write_number_of_transmitted_bytes(self, full_bytes, extra_bits=0):
        v = ((full_bytes & 0x01FF) << 3) | (extra_bits & 0x07)
        self.write_reg16_be(REG_NUMBER_OF_TRANSMITTED_BYTES_1, v)
        return True

    def wait_fifo(self, need_bytes, timeout_ms):
        t0 = time.ticks_ms()
        while _elapsed_ms(t0) < timeout_ms:
            nb, _ = self.read_fifo_size()
            if nb >= need_bytes:
                return nb
            self._wait_event_or_sleep(t0, timeout_ms)
        return 0

    def enable_osc(self):
        op = self.read_reg8(REG_OPERATION_CONTROL)
        if (op & OP_EN) == 0:
            m = self.read_reg8(REG_MASK_MAIN_INTERRUPT)
            self.write_reg8(REG_MASK_MAIN_INTERRUPT, m & (0xFF ^ I_OSC))
            self.clear_interrupts()
            self.set_bits(REG_OPERATION_CONTROL, OP_EN)
            t0 = time.ticks_ms()
            got = False
            while _elapsed_ms(t0) < 25:
                self._wait_event_or_sleep(t0, 25)
                irq = self.read_reg8(REG_MAIN_INTERRUPT)
                if irq & I_OSC:
                    got = True
                    break
            self.set_bits(REG_MASK_MAIN_INTERRUPT, I_OSC)
            if not got:
                return False
        aux = self.read_reg8(REG_AUXILIARY_DISPLAY)
        return (aux & OSC_OK) != 0

    def init_chip(self):
        raw = self.read_reg8(REG_IC_IDENTITY)
        typ = (raw >> 3) & 0x1F
        rev = raw & 0x07
        if typ != VALID_IDENTIFY_TYPE or rev == 0 or raw == 0xFF:
            return False

        self.direct_command(CMD_SET_DEFAULT)
        time.sleep_ms(10)
        self.direct_command(CMD_TEST_ACCESS, b"\x04\x10")

        self.write_reg16_be(REG_IO_CONFIGURATION_1, IO_CONFIGURATION_I2C_400K_3V3)
        txd = (TX_AM_DEFAULT_NIBBLE & 0x0F) << 4
        self.write_reg8(REG_TX_DRIVER, txd)

        v = self.read_reg8(REG_IO_CONFIGURATION_1)
        self.write_reg8(REG_IO_CONFIGURATION_1, (v & ~0x07) | 0x07)

        self.write_reg8_space_b_addr(REG_SPACE_B_RESISTIVE_AM, 0x80)
        self.set_bits(REG_IO_CONFIGURATION_2, AAT_EN)
        self.write_reg8_space_b_addr(REG_SPACE_B_RESISTIVE_AM, 0x00)

        self.write_reg8(REG_EXTERNAL_FIELD_DETECTOR_ACTIVATION_THRESHOLD, 0x10 | 0x03)
        self.write_reg8(REG_EXTERNAL_FIELD_DETECTOR_DEACTIVATION_THRESHOLD, 0x00 | 0x02)

        nfcip = self.read_reg8(REG_NFCIP_1_PASSIVE_TARGET_DEFINITION)
        self.write_reg8(REG_NFCIP_1_PASSIVE_TARGET_DEFINITION, (nfcip & ~0xF0) | (0x05 << 4))

        self.write_reg8(REG_PASSIVE_TARGET_MODULATION, 0x5F)
        self.write_reg8_space_b_addr(REG_SPACE_B_EMD_SUPPRESSION, 0x40)
        self.write_reg8(REG_ANTENNA_TUNING_CONTROL_1, 0x82)
        self.write_reg8(REG_ANTENNA_TUNING_CONTROL_2, 0x82)

        self.set_bits(REG_OPERATION_CONTROL, 0x03)
        self.direct_command(CMD_CLEAR_FIFO)

        self.write_reg32_be(REG_MASK_MAIN_INTERRUPT, MASK_PRE_ADJUST)
        self.clear_interrupts()

        if not self.enable_osc():
            return False

        self.write_reg32_be(REG_MASK_MAIN_INTERRUPT, 0)
        self.direct_command(CMD_ADJUST_REGULATORS)
        time.sleep_ms(5)
        return True

    def configure_nfca(self):
        ok = True
        ok = ok and self._safe(lambda: self.direct_command(CMD_STOP_ALL_ACTIVITIES))
        ok = ok and self._safe(lambda: self.clear_bits(REG_OPERATION_CONTROL, WU))

        ok = ok and self._safe(lambda: self.write_reg8(REG_MODE_DEFINITION, 0x09))
        ok = ok and self._safe(lambda: self.write_reg8(REG_BITRATE_DEFINITION, 0x00))
        ok = ok and self._safe(lambda: self.write_reg8(REG_ISO14443A_SETTINGS, 0x00))

        ok = ok and self._safe(lambda: self.clear_bits(REG_AUXILIARY_DEFINITION, DIS_CORR))
        ok = ok and self._safe(
            lambda: self.write_reg8_space_b(REG_OVERSHOOT_PROTECTION_CONFIGURATION_1, 0x40)
        )
        ok = ok and self._safe(
            lambda: self.write_reg8_space_b(REG_OVERSHOOT_PROTECTION_CONFIGURATION_2, 0x03)
        )
        ok = ok and self._safe(
            lambda: self.write_reg8_space_b(REG_UNDERSHOOT_PROTECTION_CONFIGURATION_1, 0x40)
        )
        ok = ok and self._safe(
            lambda: self.write_reg8_space_b(REG_UNDERSHOOT_PROTECTION_CONFIGURATION_2, 0x03)
        )
        ok = ok and self._safe(
            lambda: self.write_reg8_space_b(REG_CORRELATOR_CONFIGURATION_1, 0x47)
        )
        ok = ok and self._safe(
            lambda: self.write_reg8_space_b(REG_CORRELATOR_CONFIGURATION_2, 0x00)
        )

        ok = ok and self._safe(lambda: self.write_reg8(REG_RECEIVER_CONFIGURATION_1, RXCFG1_Z600K))
        ok = ok and self._safe(
            lambda: self.write_reg8(REG_RECEIVER_CONFIGURATION_2, RXCFG2_STABLE)
        )
        ok = ok and self._safe(
            lambda: self.write_reg8(REG_RECEIVER_CONFIGURATION_3, RXCFG3_STABLE)
        )
        ok = ok and self._safe(
            lambda: self.write_reg8(REG_RECEIVER_CONFIGURATION_4, RXCFG4_STABLE)
        )

        ok = ok and self._safe(lambda: self.write_reg32_be(REG_MASK_MAIN_INTERRUPT, 0))
        ok = ok and self._safe(lambda: self.direct_command(CMD_RESET_RX_GAIN))
        ok = ok and self._safe(lambda: self.direct_command(CMD_NFC_INITIAL_FIELD_ON))
        time.sleep_ms(5)
        ok = ok and self._safe(lambda: self.set_bits(REG_OPERATION_CONTROL, TX_EN | RX_EN))
        return ok

    @staticmethod
    def _safe(fn):
        try:
            fn()
            return True
        except OSError:
            return False

    def begin(self):
        return self.init_chip() and self.configure_nfca()

    def stop_all_activities(self):
        self.direct_command(CMD_STOP_ALL_ACTIVITIES)

    def rf_off(self):
        self._mf_c1 = None
        self.direct_command(CMD_STOP_ALL_ACTIVITIES)
        time.sleep_ms(5)
        self.clear_bits(REG_OPERATION_CONTROL, TX_EN | RX_EN)

    def rf_on(self):
        self.nfc_initial_field_on()

    def nfc_initial_field_on(self):
        self.direct_command(CMD_NFC_INITIAL_FIELD_ON)
        time.sleep_ms(5)
        self.set_bits(REG_OPERATION_CONTROL, TX_EN | RX_EN)

    def request_wakeup(self, reqa):
        self.write_fwt_timer(TIMEOUT_REQ_WUP_MS)
        self.write_reg8(REG_ISO14443A_SETTINGS, ANTCL)
        self.set_bits(REG_AUXILIARY_DEFINITION, NO_CRC_RX)
        self.clear_interrupts()
        self.direct_command(CMD_CLEAR_FIFO)
        self.direct_command(CMD_TRANSMIT_REQA if reqa else CMD_TRANSMIT_WUPA)
        n = self.wait_fifo(2, TIMEOUT_REQ_WUP_MS)
        if n < 2:
            return None
        rb = self.read_fifo(n)
        if len(rb) < 2:
            return None
        atqa = (rb[1] << 8) | rb[0]
        if atqa == 0 or atqa == 0xFFFF:
            return None
        return atqa

    def _anti_collision(self, sel_cmd):
        self.write_fwt_timer(TIMEOUT_ANTICOLL_MS)
        self.write_reg8(REG_ISO14443A_SETTINGS, ANTCL)
        self.clear_bits(REG_AUXILIARY_DEFINITION, NO_CRC_RX)
        self.clear_interrupts()
        self.direct_command(CMD_CLEAR_FIFO)
        self.write_fifo(bytes((sel_cmd, 0x20)))
        self.write_number_of_transmitted_bytes(2, 0)
        self.direct_command(CMD_TRANSMIT_WITHOUT_CRC)
        n = self.wait_fifo(5, TIMEOUT_ANTICOLL_MS)
        if n < 5:
            return None
        rb = self.read_fifo(n)
        if len(rb) < 5:
            return None
        u0, u1, u2, u3, bcc = rb[0], rb[1], rb[2], rb[3], rb[4]
        if (u0 ^ u1 ^ u2 ^ u3) & 0xFF != bcc:
            return None
        return (u0, u1, u2, u3, bcc)

    def anti_collision_cl1(self):
        return self._anti_collision(0x93)

    def anti_collision_cl2(self):
        return self._anti_collision(0x95)

    def _select(self, sel_cmd, uid4, bcc):
        frame = bytes((sel_cmd, 0x70, uid4[0], uid4[1], uid4[2], uid4[3], bcc))
        self.write_fwt_timer(TIMEOUT_SELECT_MS)
        self.write_reg8(REG_ISO14443A_SETTINGS, 0x00)
        self.clear_bits(REG_AUXILIARY_DEFINITION, NO_CRC_RX)
        self.clear_interrupts()
        self.direct_command(CMD_CLEAR_FIFO)
        self.write_fifo(frame)
        self.write_number_of_transmitted_bytes(len(frame), 0)
        self.direct_command(CMD_TRANSMIT_WITH_CRC)
        n = self.wait_fifo(1, TIMEOUT_SELECT_MS)
        if n < 1:
            return None
        rb = self.read_fifo(n)
        if not rb:
            return None
        return rb[0]

    def select_cl1(self, uid4, bcc):
        return self._select(0x93, uid4, bcc)

    def select_cl2(self, uid4, bcc):
        return self._select(0x95, uid4, bcc)

    def hlta_nfca(self):
        self._mf_c1 = None
        self.write_fwt_timer(10)
        self.write_reg8(REG_ISO14443A_SETTINGS, 0x00)
        self.clear_bits(REG_AUXILIARY_DEFINITION, NO_CRC_RX)
        self.clear_interrupts()
        self.direct_command(CMD_CLEAR_FIFO)
        self.write_fifo(b"\x50\x00")
        self.write_number_of_transmitted_bytes(2, 0)
        try:
            self.direct_command(CMD_TRANSMIT_WITH_CRC)
        except OSError:
            pass
        time.sleep_ms(2)

    def read_uid_once(self):
        self._mf_c1 = None
        atqa = self.request_wakeup(True)
        if atqa is None:
            atqa = self.request_wakeup(False)
        if atqa is None:
            return None, 0, 0, 0

        r1 = self.anti_collision_cl1()
        if r1 is None:
            return None, 0, 0, 0
        cl1 = (r1[0], r1[1], r1[2], r1[3])
        bcc1 = r1[4]

        sak1 = self.select_cl1(cl1, bcc1)
        if sak1 is None:
            return None, 0, 0, 0

        if cl1[0] != CASCADE_TAG:
            return bytes(cl1), 4, atqa, sak1

        if (sak1 & SAK_CASCADE_FLAG) == 0:
            return None, 0, 0, 0

        r2 = self.anti_collision_cl2()
        if r2 is None:
            return None, 0, 0, 0
        cl2 = (r2[0], r2[1], r2[2], r2[3])
        bcc2 = r2[4]

        sak2 = self.select_cl2(cl2, bcc2)
        if sak2 is None:
            return None, 0, 0, 0

        if cl2[0] == CASCADE_TAG:
            return None, 0, 0, 0

        uid = bytes((cl1[1], cl1[2], cl1[3], cl2[0], cl2[1], cl2[2], cl2[3]))
        return uid, 7, atqa, sak2

    def nfca_transceive_crc(self, tx, timeout_ms=12, min_rx=2):
        self.write_fwt_timer(timeout_ms)
        self.write_reg8(REG_ISO14443A_SETTINGS, 0x00)
        self.clear_bits(REG_AUXILIARY_DEFINITION, NO_CRC_RX)
        self.clear_interrupts()
        self.direct_command(CMD_CLEAR_FIFO)
        self.write_fifo(tx)
        self.write_number_of_transmitted_bytes(len(tx), 0)
        self.direct_command(CMD_TRANSMIT_WITH_CRC)
        t0 = time.ticks_ms()
        while _elapsed_ms(t0) < timeout_ms:
            nb, _ = self.read_fifo_size()
            if nb >= min_rx:
                time.sleep_ms(1)
                nb2, _ = self.read_fifo_size()
                if nb2 == nb:
                    return self.read_fifo(nb2)
            self._wait_event_or_sleep(t0, timeout_ms)
        return None

    def _nfca_fifo_rx_stable(self, timeout_ms, min_bytes):
        t0 = time.ticks_ms()
        while _elapsed_ms(t0) < timeout_ms:
            nb, bi = self.read_fifo_size()
            if nb >= min_bytes:
                time.sleep_ms(1)
                nb2, bi2 = self.read_fifo_size()
                if nb2 == nb and bi2 == bi:
                    return nb2, bi2
            self._wait_event_or_sleep(t0, timeout_ms)
        return 0, 0

    def nfca_transceive_crc_ack(self, tx, timeout_ms=TIMEOUT_T2_WRITE_MS):
        self.write_fwt_timer(timeout_ms)
        self.write_reg8(REG_ISO14443A_SETTINGS, 0x00)
        self.clear_bits(REG_AUXILIARY_DEFINITION, NO_CRC_RX)
        self.clear_interrupts()
        self.direct_command(CMD_CLEAR_FIFO)
        self.write_fifo(tx)
        self.write_number_of_transmitted_bytes(len(tx), 0)
        self.direct_command(CMD_TRANSMIT_WITH_CRC)
        nb, _ = self._nfca_fifo_rx_stable(timeout_ms, 1)
        if nb < 1:
            return False
        b = self.read_fifo(nb)
        if not b:
            return False
        v = b[0] & 0xFF
        return v == ACK_NIBBLE or (v & 0x0F) == (ACK_NIBBLE & 0x0F)

    def type2_read_quad(self, first_page):
        rx = self.nfca_transceive_crc(
            bytes((CMD_READ, int(first_page) & 0xFF)),
            timeout_ms=TIMEOUT_T2_READ_MS,
            min_rx=18,
        )
        if not rx or len(rx) < 18:
            return None
        return bytes(rx[:16])

    def type2_read_page(self, page):
        base = int(page) & ~3
        off = int(page) & 3
        q = self.type2_read_quad(base)
        if not q:
            return None
        return bytes(q[off * 4 : off * 4 + 4])

    def type2_write_page(self, page, data):
        d = bytes(data)
        if len(d) != 4:
            return False
        frame = bytes((CMD_WRITE_PAGE, int(page) & 0xFF)) + d
        return self.nfca_transceive_crc_ack(frame, timeout_ms=TIMEOUT_T2_WRITE_MS)

    def mifare_classic_end_session(self):
        self._mf_c1 = None
        self.write_reg8(REG_ISO14443A_SETTINGS, 0x00)
        self.clear_bits(REG_AUXILIARY_DEFINITION, NO_CRC_RX)

    def mifare_classic_auth(self, uid, block, key6, use_key_b=False):
        self.mifare_classic_end_session()
        cmd = MIFARE_AUTH_KEY_B if use_key_b else MIFARE_AUTH_KEY_A
        # C++ ``nfcaReceive`` only waits for 4 bytes (nt); FIFO may or may not still hold CRC.
        rx = self.nfca_transceive_crc(
            bytes((cmd, int(block) & 0xFF)),
            timeout_ms=24,
            min_rx=4,
        )
        if not rx or len(rx) < 4:
            return False
        rb4 = rx[:4]
        time.sleep_us(87)
        u32 = uid_tail_u32_be(uid)
        nt = nt_from_rb(rb4)
        c1 = Crypto1()
        c1.init(key_to_u48(key6))
        c1.inject(u32, nt, False)
        nr = random.getrandbits(32)
        ar, suc3 = suc_23(byteswap_u32(nt))
        ab, parity = c1.encrypt_ab(nr, ar)
        bs = append_parity_bitstream(ab, parity)
        nbits = 72
        sbytes = nbits >> 3
        sbits = nbits & 7

        self.direct_command(CMD_RESET_RX_GAIN)
        self.write_fwt_timer(20)
        self.write_reg8(REG_ISO14443A_SETTINGS, NO_TX_PAR)
        self.set_bits(REG_AUXILIARY_DEFINITION, NO_CRC_RX)
        self.clear_interrupts()
        self.direct_command(CMD_CLEAR_FIFO)
        self.write_fifo(bs)
        self.write_number_of_transmitted_bytes(sbytes, sbits)
        self.direct_command(CMD_TRANSMIT_WITHOUT_CRC)

        t0 = time.ticks_ms()
        ba = None
        while _elapsed_ms(t0) < 40:
            nb, bi0 = self.read_fifo_size()
            if nb >= 4:
                time.sleep_ms(1)
                nb2, bi2 = self.read_fifo_size()
                if nb2 == nb and bi2 == bi0:
                    ba = self.read_fifo(4)
                    if len(ba) == 4:
                        break
            self._wait_event_or_sleep(t0, 40)
        if not ba or len(ba) != 4:
            self.mifare_classic_end_session()
            return False

        at2 = bytearray(4)
        for i in range(4):
            at2[i] = ba[i] ^ c1.step8(0)
        at32 = at2[0] | (at2[1] << 8) | (at2[2] << 16) | (at2[3] << 24)
        if (at32 & 0xFFFFFFFF) != (suc3 & 0xFFFFFFFF):
            self.mifare_classic_end_session()
            return False
        self._mf_c1 = c1
        self.write_reg8(REG_ISO14443A_SETTINGS, 0x00)
        self.clear_bits(REG_AUXILIARY_DEFINITION, NO_CRC_RX)
        return True

    def _mifare_classic_transceive_encrypt(
        self, tx_plain, rx_payload_len, include_crc, decrypt, timeout_ms
    ):
        c1 = self._mf_c1
        if c1 is None:
            return None
        txb = bytes(tx_plain)
        tmp_tx = bytearray(txb)
        cr = crc16_iso14443a(txb)
        tmp_tx.append(cr & 0xFF)
        tmp_tx.append((cr >> 8) & 0xFF)
        txwc = bytes(tmp_tx)
        enc, parity = c1.encrypt_stream(txwc)
        nbits = len(txwc) * 9
        bs = append_parity_bitstream(enc, parity)
        sbytes = nbits >> 3
        sbits = nbits & 7

        # M5 ``mifare_classic_transceive_encrypt``: ``set_bit_register8(AUX, include_crc ? no_crc_rx : 0)``.
        # OR with 0 is a no-op — when ``include_crc`` is false, leave ``NO_CRC_RX`` unchanged.
        # After an encrypted READ, AUX still has ``NO_CRC_RX``; clearing it before WRITE breaks ACK RX.
        if include_crc:
            self.set_bits(REG_AUXILIARY_DEFINITION, NO_CRC_RX)
        self.write_reg8(REG_ISO14443A_SETTINGS, NO_TX_PAR)
        self.write_fwt_timer(timeout_ms)
        self.clear_interrupts()
        self.direct_command(CMD_CLEAR_FIFO)
        self.write_fifo(bs)
        self.write_number_of_transmitted_bytes(sbytes, sbits)
        self.direct_command(CMD_TRANSMIT_WITHOUT_CRC)
        # M5: no ``RESET_RX_GAIN`` / extra delay between TX and ``wait_for_FIFO`` here.

        rlen = rx_payload_len + (2 if include_crc else 0)
        t0 = time.ticks_ms()
        raw = None
        while _elapsed_ms(t0) < timeout_ms:
            nb, _ = self.read_fifo_size()
            if nb >= rlen:
                time.sleep_ms(2)
                nb2, _ = self.read_fifo_size()
                if nb2 == nb:
                    raw = self.read_fifo(nb2)
                    if len(raw) >= rlen:
                        break
            self._wait_event_or_sleep(t0, timeout_ms)
        if not raw or len(raw) < rlen:
            return None
        rb = bytearray(raw[:rlen])

        if decrypt:
            if rlen == 1:
                ret = rb[0] & 0x0F
                res = 0
                for i in range(4):
                    res |= (c1.step_with(0) ^ ((ret >> i) & 1)) << i
                rb[0] = res
                if res != ACK_NIBBLE:
                    return None
                return bytes(rb[:1])
            for i in range(rlen):
                rb[i] ^= c1.step8(0)
            if include_crc:
                pl = rb[:rx_payload_len]
                calc = crc16_iso14443a(pl)
                lo, hi = calc & 0xFF, (calc >> 8) & 0xFF
                a, b = rb[rx_payload_len], rb[rx_payload_len + 1]
                if not ((lo == a and hi == b) or (lo == b and hi == a)):
                    return None
            return bytes(rb[:rx_payload_len])
        return bytes(rb[:rx_payload_len])

    def mifare_classic_read_block(self, block):
        return self._mifare_classic_transceive_encrypt(
            bytes((CMD_READ, int(block) & 0xFF)), 16, True, True, 48
        )

    def mifare_classic_write_block(self, block, data16):
        d = bytes(data16)
        if len(d) != 16:
            return False
        # M5 ``nfca.hpp``: TIMEOUT_WRITE1=5, TIMEOUT_WRITE2=10 ms. MicroPython FIFO poll uses
        # 1 ms steps; slightly larger values avoid false timeouts on busy interpreters.
        r = self._mifare_classic_transceive_encrypt(
            bytes((MIFARE_WRITE_BLOCK, int(block) & 0xFF)), 1, False, True, 12
        )
        if not r or (r[0] & 0x0F) != (ACK_NIBBLE & 0x0F):
            return False
        time.sleep_us(82)
        r2 = self._mifare_classic_transceive_encrypt(d, 1, False, True, 24)
        return bool(r2) and ((r2[0] & 0x0F) == (ACK_NIBBLE & 0x0F))

    def nfca_rats(self, fsdi=0, cid=0):
        p = ((fsdi & 0x0F) << 4) | (cid & 0x0F)
        return self.nfca_transceive_crc(bytes((CMD_RATS, p)), timeout_ms=TIMEOUT_RATS_MS, min_rx=2)

    def try_get_version_l3(self):
        rx = self.nfca_transceive_crc(bytes((CMD_GET_VERSION,)), timeout_ms=12, min_rx=10)
        if not rx or len(rx) < 10:
            return None
        return rx[:-2] if len(rx) >= 2 else rx

    def try_get_version_l4_wrapped(self):
        seq = 0
        acc = bytearray()
        first = True
        for _ in range(16):
            pcb = 0x02 | (seq & 0x01)
            if first:
                cmd = bytes((pcb, 0x90, CMD_GET_VERSION, 0x00, 0x00, 0x00))
            else:
                cmd = bytes((pcb, 0x90, 0xAF, 0x00, 0x00, 0x00))
            rx = self.nfca_transceive_crc(cmd, timeout_ms=TIMEOUT_DEP_MS, min_rx=4)
            seq += 1
            if not rx or len(rx) < 4:
                return None
            body = rx[:-2] if len(rx) >= 2 else rx
            if len(body) < 2:
                return None
            inf = body[1:]
            acc.extend(inf)
            if len(inf) >= 2 and inf[-2] == 0x91:
                st = inf[-1]
                if st == 0x00:
                    break
                if st != 0xAF:
                    return None
                first = False
                continue
            break
        if len(acc) >= 2 and acc[-2] == 0x91 and acc[-1] == 0x00:
            pl = acc[:-2]
        else:
            pl = acc
        if len(pl) < 8:
            return None
        return bytes(pl[:8])


ST25R3916 = ST25R3916NFCA
