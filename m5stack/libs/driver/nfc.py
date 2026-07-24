# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
from driver.st25r3916 import ST25R3916


def uid_to_hex(uid):
    """Format UID or any ``bytes`` as upper-case hex string."""
    return "".join("%02X" % b for b in uid)


# m5::nfc::a::Type family sets — skip misleading Type 2 dump on DESFire / Classic / Plus.
_T_CLASSIC = frozenset((1, 2, 3, 4))
_T_TYPE2_FAMILY = frozenset(range(5, 20))
_T_PLUS = frozenset((22, 23, 24))
_T_DESFIRE = frozenset((25, 26, 27, 28))

# nfca.cpp max_block_table for Classic types 1..4
CLASSIC_BLOCK_COUNT = {1: 20, 2: 64, 3: 128, 4: 256}

_TYPE_NAMES = (
    "Unknown",
    "MIFARE_Classic_Mini",
    "MIFARE_Classic_1K",
    "MIFARE_Classic_2K",
    "MIFARE_Classic_4K",
    "MIFARE_Ultralight",
    "MIFARE_Ultralight_EV1_1",
    "MIFARE_Ultralight_EV1_2",
    "MIFARE_Ultralight_Nano",
    "MIFARE_UltralightC",
    "NTAG_203",
    "NTAG_210u",
    "NTAG_210",
    "NTAG_212",
    "NTAG_213",
    "NTAG_215",
    "NTAG_216",
    "ST25TA_512B",
    "ST25TA_2K",
    "ST25TA_16K",
    "ST25TA_64K",
    "ISO_14443_4",
    "MIFARE_Plus_2K",
    "MIFARE_Plus_4K",
    "MIFARE_Plus_SE",
    "MIFARE_DESFire_2K",
    "MIFARE_DESFire_4K",
    "MIFARE_DESFire_8K",
    "MIFARE_DESFire_Light",
    "NTAG_4XX",
    "ISO_18092",
)

_USER_MEMORY = (
    0,
    240,
    752,
    1520,
    3440,
    48,
    48,
    128,
    40,
    144,
    144,
    48,
    144,
    208,
    144,
    504,
    888,
    64,
    256,
    2048,
    8192,
    0,
    1520,
    3440,
    752,
    2048,
    4096,
    8192,
    256,
    0,
    0,
)

_T_ISO14443_4 = 21

_HIST_S = bytes((0xC1, 0x05, 0x2F, 0x2F, 0x00, 0x35, 0xC7))
_HIST_X_EV = bytes((0xC1, 0x05, 0x2F, 0x2F, 0x01, 0xBC, 0xD6))
_HIST_SE0 = bytes((0xC1, 0x05, 0x21, 0x30, 0x00, 0xF6, 0xD1))
_HIST_SE1 = bytes((0xC1, 0x05, 0x21, 0x30, 0x10, 0xF6, 0xD1))
_HIST_SE2 = bytes((0xC1, 0x05, 0x21, 0x30, 0x00, 0x77, 0xC1))

_SAK20_HIST = (
    (_HIST_S, 22, 3),
    (_HIST_X_EV, 22, 5),
    (_HIST_SE0, 24, 0),
    (_HIST_SE1, 24, 0),
    (_HIST_SE2, 24, 0),
)


def unitnfc_sak_to_type(sak):
    s = sak & 0xFF
    # Bit1/Bit2 set => unsupported/reserved in this mapping.
    if s & 0x06:
        return 0
    if s & 0x08:
        # Classic family branch.
        if s & 0x10:
            return 3 if (s & 0x01) else 4
        return 1 if (s & 0x01) else 2
    if s & 0x10:
        return 23 if (s & 0x01) else 22
    if s & 0x01:
        return 0
    if s & 0x20:
        return _T_ISO14443_4
    return 5


def parse_ats_historical(body_no_crc):
    if len(body_no_crc) < 2:
        return b""
    ats_len = body_no_crc[0]
    if len(body_no_crc) < ats_len or ats_len < 2:
        return b""
    offset = 1
    t0 = body_no_crc[offset]
    offset += 1
    if offset < ats_len and (t0 & 0x10):
        offset += 1
    if offset < ats_len and (t0 & 0x20):
        offset += 1
    if offset < ats_len and (t0 & 0x40):
        offset += 1
    if offset < ats_len:
        return body_no_crc[offset:ats_len]
    return b""


def historical_bytes_to_type_sak20(atqa, hist):
    if len(hist) < 7:
        return 0, 0
    h7 = hist[:7]
    for pat, tid, sub in _SAK20_HIST:
        if h7 == pat:
            if tid == 22 and (atqa & 0x000F) == 0x02:
                tid = 23
            return tid, sub
    return 0, 0


def historical_bytes_to_type(atqa, sak, hist):
    s = sak & 0xFF
    if s == 0x20:
        return historical_bytes_to_type_sak20(atqa, hist)
    return 0, 0


def version3_to_type(ver):
    if not ver or len(ver) < 8:
        return 0
    if ver[0] != 0x00 or ver[1] != 0x04 or ver[7] != 0x03:
        return 0
    hw_type, hw_version, size = ver[2], ver[4], ver[6]
    if hw_type == 0x04:
        if size == 0x0E:
            return 12
        if size == 0x0F:
            return 13
        if size == 0x11:
            return 14
        if size == 0x13:
            return 15
        if size == 0x0B:
            return 11 if hw_version == 0x02 else 10
        return 0
    if hw_type == 0x03:
        if hw_version == 0x01:
            if size == 0x0B:
                return 6
            if size == 0x0E:
                return 7
            return 0
        if hw_version == 0x02:
            return 8
        return 0
    return 0


def version4_to_type(ver):
    if not ver or len(ver) < 8:
        return 0, None, None
    hw_type, hw_version, size = ver[1], ver[3], ver[5]
    plus_sub = des_sub = None

    if hw_type in (0x02, 0x82):
        if hw_version == 0x11:
            plus_sub = 1
        elif hw_version == 0x22:
            plus_sub = 2
        else:
            return 0, None, None
        if size == 0x16:
            return 22, plus_sub, None
        if size == 0x18:
            return 23, plus_sub, None
        return 0, plus_sub, None

    if hw_type in (0x01, 0x81):
        ev = hw_version & 0x0F
        if ev == 1:
            des_sub = 1
        elif ev == 2:
            des_sub = 2
        elif ev == 3:
            des_sub = 3
        tdf = 0
        if size == 0x16:
            tdf = 25
        elif size == 0x18:
            tdf = 26
        elif size == 0x1A:
            tdf = 27
        return tdf, None, des_sub
    if hw_type == 0x08:
        return 28, None, None
    if hw_type == 0x04:
        return 29, None, None
    return 0, None, None


def identify_picc(nfc, atqa, sak):
    tid = unitnfc_sak_to_type(sak)
    plus_sub = des_sub = None
    hist = b""

    if tid == _T_ISO14443_4:
        raw = nfc.nfca_rats()
        if raw and len(raw) >= 2:
            body = raw[:-2] if len(raw) >= 2 else raw
            hist = parse_ats_historical(body)

        if raw:
            v4 = nfc.try_get_version_l4_wrapped()
            if v4:
                t4, ps, ds = version4_to_type(v4)
                if t4:
                    tid = t4
                    if ps is not None:
                        plus_sub = ps
                    if ds is not None:
                        des_sub = ds

        if tid == _T_ISO14443_4:
            htid, hsub = historical_bytes_to_type(atqa, sak, hist)
            if htid:
                tid = htid
                plus_sub = hsub

    if tid == 5:
        v3 = nfc.try_get_version_l3()
        if v3 and len(v3) >= 8:
            t3 = version3_to_type(v3)
            if t3:
                tid = t3

    return {
        "type_id": tid,
        "type_name": _TYPE_NAMES[tid] if tid < len(_TYPE_NAMES) else "Unknown",
        "user_memory": _USER_MEMORY[tid] if tid < len(_USER_MEMORY) else 0,
        "plus_sub": plus_sub,
        "des_sub": des_sub,
        "ats_hist_len": len(hist),
    }


# Public aliases for apps.
CLASSIC_TYPE_IDS = _T_CLASSIC
TYPE2_FAMILY_TYPE_IDS = _T_TYPE2_FAMILY
PLUS_TYPE_IDS = _T_PLUS
DESFIRE_TYPE_IDS = _T_DESFIRE
TYPE_NAMES = _TYPE_NAMES


class Card:
    """One detected tag: UID + resolved type (``identify_picc``)."""

    __slots__ = ("uid", "uid_len", "atqa", "sak", "type_id", "type_name", "user_memory")

    def __init__(self, uid, uid_len, atqa, sak, info):
        buf = uid if isinstance(uid, (bytes, bytearray)) else bytes(uid)
        self.uid = bytes(buf[:uid_len]) if uid_len else b""
        self.uid_len = uid_len
        self.atqa = atqa
        self.sak = sak
        self.type_id = info["type_id"]
        self.type_name = info["type_name"]
        self.user_memory = info["user_memory"]

    @property
    def uid_str(self):
        """UID as upper-case hex string (same as ``uid_to_hex`` / ``NFCReader.uid_hex``)."""
        return uid_to_hex(self.uid)

    def is_classic(self):
        return self.type_id in CLASSIC_TYPE_IDS

    def is_type2_family(self):
        return self.type_id in TYPE2_FAMILY_TYPE_IDS


FACTORY_KEY = bytes((0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF))


def _sector_trailer_block(block_no):
    return (block_no // 4) * 4 + 3


def classic_read_block(chip, uid_tag, block_no, key=FACTORY_KEY):
    uid_tag = bytes(uid_tag)
    trailer = _sector_trailer_block(block_no)
    # AUTH block: try target block first (``unit_nfc_card_detect`` / p417 use ``nblk-2`` data block), then trailer.
    auth_blocks = (block_no, trailer) if block_no != trailer else (block_no,)
    # Always HLTA + re-select before AUTH. After ``mifare_classic_end_session`` / another read, the PICC is
    # no longer ACTIVE; using uid_tag bytes without read_uid_once() caused the next read to fail (e.g. dump then read).
    for use_key_b in (False, True):
        chip.hlta_nfca()
        time.sleep_ms(60)
        u2, ln2, _, _ = chip.read_uid_once()
        if ln2 == 0 or u2 is None or bytes(u2[:ln2]) != uid_tag:
            return None
        cur = bytes(u2[:ln2])
        for auth_cmd in auth_blocks:
            if not chip.mifare_classic_auth(cur, auth_cmd, key, use_key_b=use_key_b):
                continue
            data = chip.mifare_classic_read_block(block_no)
            chip.mifare_classic_end_session()
            if data and len(data) == 16:
                return bytes(data)
    return None


def classic_write_persist_for_block(chip, uid_tag, type_id, target_block, data16, key=FACTORY_KEY):
    """
    MIFARE Classic one-block write.
    """
    nblk = CLASSIC_BLOCK_COUNT.get(type_id)
    if not nblk or len(data16) != 16:
        return False, None, None
    t = int(target_block)
    if t <= 0 or t >= nblk or (t & 3) == 3:
        return False, None, None
    trailer = _sector_trailer_block(t)
    # M5 ``NFCLayerA::write_using_write16`` authenticates **sector trailer** only; try trailer first.
    auth_blocks = []
    for ab in (trailer, t):
        if ab not in auth_blocks:
            auth_blocks.append(ab)
    uid_tag = bytes(uid_tag)
    # Lazy read for ``snap_before`` only if we take the M5-style path (no READ in Crypto1 before WRITE).
    snap_outer = None

    def _snap_outer():
        nonlocal snap_outer
        if snap_outer is None:
            snap_outer = classic_read_block(chip, uid_tag, t, key)
        return snap_outer

    for auth_block in auth_blocks:
        for use_key_b in (False, True):
            for with_preread in (True, False):
                chip.hlta_nfca()
                time.sleep_ms(60)
                u2, ln2, _, _ = chip.read_uid_once()
                if ln2 == 0 or u2 is None or bytes(u2[:ln2]) != uid_tag:
                    continue
                cur_uid = bytes(u2[:ln2])
                if not chip.mifare_classic_auth(cur_uid, auth_block, key, use_key_b=use_key_b):
                    continue
                if with_preread:
                    chk0 = chip.mifare_classic_read_block(t)
                    if not chk0 or len(chk0) != 16:
                        chip.mifare_classic_end_session()
                        continue
                    snap = bytes(chk0)
                else:
                    s0 = _snap_outer()
                    snap = bytes(s0) if s0 else bytes(16)
                if not chip.mifare_classic_write_block(t, bytes(data16)):
                    chip.mifare_classic_end_session()
                    continue
                # EEPROM programming: NXP typ. ~3–5 ms, clones can be slower; verify read too soon can flake.
                time.sleep_ms(35)
                v = chip.mifare_classic_read_block(t)
                if not v or len(v) != 16 or bytes(v) != bytes(data16):
                    chip.mifare_classic_end_session()
                    continue
                chip.mifare_classic_end_session()
                return True, t, snap
    return False, None, None


def classic_write_block(chip, uid_tag, type_id, block_no, data16, key=FACTORY_KEY):
    """
    Write one Classic data block
    """
    ok, _, _ = classic_write_persist_for_block(chip, uid_tag, type_id, block_no, data16, key)
    return ok


def can_type2_read(card):
    return card.type_id in TYPE2_FAMILY_TYPE_IDS or card.type_id == 29


def type2_read_pages(chip, first_page, last_page_exclusive):
    out = []
    for base in range(int(first_page), int(last_page_exclusive), 4):
        q = chip.type2_read_quad(base)
        if not q or len(q) != 16:
            break
        for i in range(4):
            p = base + i
            if p >= last_page_exclusive:
                return out
            out.append((p, bytes(q[i * 4 : i * 4 + 4])))
    return out


class NFCReader:
    """High-level NFC reader backed by an ST25R3916 over I2C."""

    def __init__(self, i2c, address=0x50):
        self._i2c = i2c
        self.chip = ST25R3916(self._i2c, address)
        self.chip.begin()

    def read(self, card, index, key=FACTORY_KEY):
        """
        Read one address unit for the current tag.

        - **MIFARE Classic**: ``index`` is the global block number; returns **16** bytes or ``None``.
        - **Type 2** (Ultralight / NTAG / …): ``index`` is the page number; returns **4** bytes or ``None``.
        - Other types: ``None``.
        """
        if card.is_classic():
            return self.read_classic_block(card, int(index), key)
        if can_type2_read(card):
            return self.chip.type2_read_page(int(index))
        return None

    def write(self, card, index, data, key=FACTORY_KEY):
        """
        Write one address unit.

        - **Classic**: ``data`` must be **16** bytes; ``index`` is the block number.
        - **Type 2**: ``data`` must be **4** bytes; ``index`` is the page number (do not overwrite UID/CRC/locks unless you know the card).
        - Returns ``True`` on success.
        """
        data = bytes(data)
        if card.is_classic():
            if len(data) != 16:
                return False
            return self.write_classic_block(card, int(index), data, key)
        if can_type2_read(card):
            if len(data) != 4:
                return False
            return bool(self.chip.type2_write_page(int(index), data))
        return False

    def detect(self):
        uid, uid_len, atqa, sak = self.chip.read_uid_once()
        if not uid_len:
            return None
        info = identify_picc(self.chip, atqa, sak)
        return Card(uid, uid_len, atqa, sak, info)

    def halt(self):
        self.chip.hlta_nfca()

    def rf_off(self):
        self.chip.rf_off()

    def rf_on(self):
        self.chip.rf_on()

    def read_classic_block(self, card, block_no, key=FACTORY_KEY):
        if not card.is_classic():
            return None
        return classic_read_block(self.chip, card.uid, block_no, key)

    def write_classic_block(self, card, block_no, data16, key=FACTORY_KEY):
        if not card.is_classic():
            return False
        return classic_write_block(self.chip, card.uid, card.type_id, block_no, data16, key)

    def read_type2_pages(self, card, first_page=0, last_page_exclusive=16):
        if not can_type2_read(card):
            return []
        return type2_read_pages(self.chip, first_page, last_page_exclusive)

    @staticmethod
    def uid_hex(card_or_bytes):
        if isinstance(card_or_bytes, Card):
            return uid_to_hex(card_or_bytes.uid)
        return uid_to_hex(card_or_bytes)
