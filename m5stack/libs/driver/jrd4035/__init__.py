# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import struct
import time


class JRD4035:
    _HEADER = 0xBB  # const(0xBB)
    _END = 0x7E  # const(0x7E)

    _FRAME_CMD = 0x00  # const(0x00)
    _FRAME_RSP = 0x01  # const(0x01)
    _FRAME_NOTIFY = 0x02  # const(0x02)

    RFU = 0b00
    EPC = 0b01
    TID = 0b10
    USER = 0b11

    S0 = 0b000
    S1 = 0b001
    S2 = 0b010
    S3 = 0b011
    SL = 0b100
    RFU101 = 0b101
    RFU110 = 0b110
    RFU111 = 0b111

    OPEN = 0b00
    LOCK = 0b01
    PERMA_OPEN = 0b10
    PERMA_LOCK = 0b11

    CN_900MHZ = 0x01
    CN_800MHZ = 0x04
    USA = 0x02
    EUR = 0x03
    KR = 0x06

    def __init__(self, uart, verbose=False) -> None:
        self._uart = uart
        self._verbose = verbose
        self._buffer = memoryview(bytearray(16))
        self._buffer1 = bytearray(1)
        self._buffer2 = bytearray(2)
        self._buffer3 = bytearray(3)
        self._buffer7 = bytearray(7)
        self._buffer8 = bytearray(8)
        self._buffer9 = bytearray(9)
        self._buffer13 = bytearray(13)

    def get_hardware_version(self) -> str:
        return self._get_module_info(0x00)

    def get_firmware_version(self) -> str:
        return self._get_module_info(0x01)

    def get_manufacturer_id(self) -> str:
        return self._get_module_info(0x02)

    def _get_module_info(self, info_type) -> str:
        self._buffer1[0] = info_type
        rxdata, status = self.command(0x03, data=bytes(self._buffer1))
        if status:
            (version,) = struct.unpack_from(">%ds" % (len(rxdata) - 1), rxdata, 1)
            return version.decode("utf-8")
        return ""

    def inventory(self) -> bytes:
        rxdata, status = self.command(0x22)
        if status is False:
            return b""
        rssi, pc, epc, crc = struct.unpack_from(">BH%dsH" % (len(rxdata) - 5), rxdata)
        self._verbose and print("RSSI: %d, PC: %d, EPC: %s, CRC: %d" % (rssi, pc, epc, crc))
        return epc

    def continuous_inventory(self, count: int) -> tuple:
        struct.pack_into(">BH", self._buffer3, 0, 0x22, count)
        rxdata, status = self.command(0x27, data=bytes(self._buffer1))
        if status is False:
            return (0, 0, b"", 0)
        rssi, pc, epc, crc = struct.unpack_from(">BH%dsH" % (len(rxdata) - 5), rxdata)
        self._verbose and print("RSSI: %d, PC: %d, EPC: %s, CRC: %d" % (rssi, pc, epc, crc))
        return (rssi, pc, epc, crc)

    def stop_continuous_inventory(self) -> bool:
        rxdata, status = self.command(0x28)
        return True if status and rxdata == b"\x00" else False

    def select(
        self,
        target: int,
        action: int,
        membank: int,
        pointer: int,
        truncate: bool,
        mask: bytes,
    ) -> bool:
        buffer = struct.pack(
            ">BIBB%ds" % (len(mask)),
            (target << 5 | action << 3 | membank),
            pointer,
            0x60,
            0x80 if truncate else 0x00,
            mask,
        )
        rxdata, status = self.command(0x0C, data=buffer)
        return False if (status is False) or (rxdata != b"\x00") else True

    def get_select_param(self) -> tuple:
        rxdata, status = self.command(0x0B)
        if status is False:
            return (0, 0, 0, 0, False, b"")
        (param, pointer, mask_len, truncate) = struct.unpack_from(">BIBB", rxdata)
        target = param >> 5
        action = (param >> 3) & 0x07
        membank = param & 0x07
        truncate = True if truncate == 0x80 else False

        mask = b""
        if mask_len > 0:
            (mask,) = struct.unpack_from(">%ds" % (mask_len // 8), rxdata, 7)
        self._verbose and print(
            "Target: %d, Action: %d, MemBank: %d, Pointer: %d, Truncate: %s, Mask: %s"
            % (target, action, membank, pointer, truncate, mask)
        )
        return (
            (param >> 5),
            ((param >> 3) & 0x07),
            (param & 0x07),
            pointer,
            truncate,
            mask,
        )

    def set_select_mode(self, mode: int) -> bool:
        self._buffer1[0] = mode
        rxdata, status = self.command(0x12, data=(self._buffer1))
        return False if (status is False) or (rxdata != b"\x00") else True

    def read_mem_bank(
        self, bank: int, offset: int, length: int, access: bytes = b"\x00\x00\x00\x00"
    ) -> bytes:
        start = offset // 2
        l = (length + 2) // 2
        struct.pack_into(">4sBHH", self._buffer9, 0, access, bank, start, l)
        rxdata, status = self.command(0x39, data=self._buffer9)
        if status is False:
            (err_code,) = struct.unpack_from(">B", rxdata, 0)
            if err_code == 0x16:
                self._verbose and print("Access Password error")
            return b""

        # TODO
        (ul, pc) = struct.unpack_from(">BH", rxdata, 0)
        (epc, data) = struct.unpack_from(">%ds%ds" % ((ul - 2), (len(rxdata) - 1 - ul)), rxdata, 3)
        return data[offset % 2 : offset % 2 + length]

    def write_mem_bank(
        self, bank: int, offset: int, data: str, access: bytes = b"\x00\x00\x00\x00"
    ) -> bool:
        data = bytes.fromhex(data)
        buffer = bytearray(9 + len(data))
        struct.pack_into(
            ">4sBHH%ds" % (len(data)), buffer, 0, access, bank, offset, len(data) // 2, data
        )
        rxdata, status = self.command(0x49, data=buffer)
        if status is False:
            return False

        # TODO
        (ul, pc, epc, param) = struct.unpack_from(">BH%dsB" % (len(rxdata) - 4), rxdata)
        return True

    def lock_mem_bank(
        self,
        kill_lock: int = 0b00,
        access_lock: int = 0b00,
        epc_lock: int = 0b00,
        tid_lock: int = 0b00,
        user_lock: int = 0b00,
        access: bytes = b"\x00\x00\x00\x00",
    ) -> bool:
        payload = 0b1111_1111_1100_0000_0000
        payload |= kill_lock << 8
        payload |= access_lock << 6
        payload |= epc_lock << 4
        payload |= tid_lock << 2
        payload |= user_lock
        struct.pack_into(
            ">BBB4s",
            self._buffer7,
            0,
            (payload >> 16) & 0xFF,
            (payload >> 8) & 0xFF,
            payload & 0xFF,
            access,
        )
        rxdata, status = self.command(0x82, data=self._buffer7)
        if status is False:
            return False

        (_, _, _, param) = struct.unpack_from(">BH%dsB" % (len(rxdata) - 4), rxdata)
        return True if param == 0x00 else False

    def set_access_password(self, password: bytes) -> None:
        self.write_mem_bank(self, self.RFU, 0x00, password)

    def set_kill_password(self, password: bytes) -> None:
        self.write_mem_bank(self, self.RFU, 0x20, password)

    def kill(self, password: bytes = b"\x00\x00\x00\x00") -> bool:
        rxdata, status = self.command(0x65, data=password)
        return True if status and rxdata == b"\x00" else False

    def set_query_param(
        self, dr=0b0, m=0b00, tr_ext=0b1, sel=0b00, session=0b00, target=0b0, q=0b0100
    ) -> bool:
        if dr != 0b0 and m != 0b00 and tr_ext != 0b1:
            raise ValueError("Invalid query parameters")
        payload = 0b0000_0000_0000_0000
        payload |= dr << 15
        payload |= m << 13
        payload |= tr_ext << 12
        payload |= sel << 10
        payload |= session << 8
        payload |= target << 7
        payload |= q << 3
        struct.pack_into(">H", self._buffer2, 0, payload)
        rxdata, status = self.command(0x0A, data=self._buffer2)
        return True if status and rxdata == b"\x00" else False

    def set_working_region(self, region: int) -> bool:
        self._buffer1[0] = region
        rxdata, status = self.command(0x07, data=self._buffer1)
        return True if status and rxdata == b"\x00" else False

    def get_working_region(self) -> int:
        rxdata, status = self.command(0x08)
        if status is False:
            return 0
        (region,) = struct.unpack_from(">B", rxdata)
        return region

    def set_working_channel(self, channel: int) -> bool:
        self._buffer1[0] = channel
        rxdata, status = self.command(0xAB, data=self._buffer1)
        return True if status and rxdata == b"\x00" else False

    def get_working_channel(self) -> int:
        rxdata, status = self.command(0xAA)
        if status is False:
            return -1
        (channel,) = struct.unpack_from(">B", rxdata)
        return channel

    def set_automatic_hopping(self, enable: bool) -> bool:
        self._buffer1[0] = 0xFF if enable else 0x00
        rxdata, status = self.command(0xAD, data=self._buffer1)
        return True if status and rxdata == b"\x00" else False

    def clear_working_channel(self) -> bool:
        rxdata, status = self.command(0xA9)
        return True if status and rxdata == b"\x00" else False

    def insert_working_channel(self, channel: int) -> bool:
        struct.pack_into(">BB", self._buffer2, 0, 0x01, channel)
        rxdata, status = self.command(0xA9, data=self._buffer2)
        return True if status and rxdata == b"\x00" else False

    def get_tx_power(self) -> int:
        rxdata, status = self.command(0xB7)
        if status is False:
            return -1
        (power,) = struct.unpack_from(">H", rxdata, 1)
        return power // 100

    def set_tx_power(self, power: int) -> bool:
        struct.pack_into(">H", self._buffer2, 0, power * 100)
        rxdata, status = self.command(0xB6, data=self._buffer2)
        return True if status and rxdata == b"\x00" else False

    def set_continuous_wave(self, enable: bool) -> bool:
        self._buffer1[0] = 0xFF if enable else 0x00
        rxdata, status = self.command(0xB0, data=bytes(self._buffer1))
        return True if status and rxdata == b"\x00" else False

    def get_demodulator_mixer(self) -> int:
        return self._get_receive_demodulator_parameters()[0]

    def get_demodulator_amplifier(self) -> int:
        return self._get_receive_demodulator_parameters()[1]

    def get_demodulator_threshold(self) -> int:
        return self._get_receive_demodulator_parameters()[2]

    def _get_receive_demodulator_parameters(self) -> tuple:
        rxdata, status = self.command(0xF1)
        if status is False:
            return (-1, -1, -1)
        (mixer, amp, threshold) = struct.unpack_from(">BBH", rxdata)
        return (mixer, amp, threshold)

    def set_demodulator_mixer(self, mixer: int) -> bool:
        (_, amp, threshold) = self._get_receive_demodulator_parameters()
        return self._set_receive_demodulator_parameters(mixer, amp, threshold)

    def set_demodulator_amplifier(self, amplifier: int) -> bool:
        (mixer, _, threshold) = self._get_receive_demodulator_parameters()
        return self._set_receive_demodulator_parameters(mixer, amplifier, threshold)

    def set_demodulator_threshold(self, threshold: int) -> bool:
        (mixer, amp, _) = self._get_receive_demodulator_parameters()
        return self._set_receive_demodulator_parameters(mixer, amp, threshold)

    def _set_receive_demodulator_parameters(
        self, mixer: int, amplifier: int, threshold: int
    ) -> bool:
        struct.pack_into(">BBH", self._buffer, 0, mixer, amplifier, threshold)
        rxdata, status = self.command(0xF0, data=self._buffer)
        return True if status and rxdata == b"\x00" else False

    def get_blocking_signal_strength(self, channel: int) -> int:
        strengths = self.get_blocking_signal_strength_all()
        return strengths[channel] if strengths else -1

    def get_blocking_signal_strength_all(self) -> tuple:
        rxdata, status = self.command(0xF2)
        if status is False:
            return (-1 for _ in range(20))
        fmt = "".join("b" for _ in range((len(rxdata) - 2)))
        return struct.unpack_from(">%s" % (fmt), rxdata, 2)

    def get_channel_rssi(self, channel: int) -> int:
        return self.get_channel_rssi_all()[channel]

    def get_channel_rssi_all(self) -> tuple:
        rxdata, status = self.command(0xF3)
        if status is False:
            return (-1 for _ in range(20))
        fmt = "".join("b" for _ in range((len(rxdata) - 2)))
        return struct.unpack_from(">%s" % (fmt), rxdata, 2)

    def sleep(self) -> bool:
        rxdata, status = self.command(0x17)
        return True if status and rxdata == b"\x00" else False

    def wake(self) -> None:
        self._uart.write(b"\x55")
        time.sleep(0.1)

    def set_automatic_sleep_time(self, min: int) -> bool:
        struct.pack_into(">B", self._buffer1, 0, min)
        rxdata, status = self.command(0x1D, data=self._buffer1)
        return True if status and rxdata == b"\x00" else False

    def disable_automatic_sleep(self) -> bool:
        return self.set_automatic_sleep_time(0)

    def nxp_read_protect(self, set, access_password: bytes = b"\x00\x00\x00\x00") -> bool:
        struct.pack_into(">4sB", self._buffer, 0, access_password, set)
        rxdata, status = self.command(0xE1, data=self._buffer[0:5])
        return True if status and rxdata == b"\x00" else False

    def nxp_change_eas(self, set, access_password: bytes = b"\x00\x00\x00\x00") -> bool:
        struct.pack_into(">4sB", self._buffer, 0, access_password, set)
        rxdata, status = self.command(0xE3, data=self._buffer[0:5])
        return True if status and rxdata == b"\x00" else False

    def nxp_eas_alarm(self) -> bytes:
        rxdata, status = self.command(0xE4)
        if status is False:
            return b""

        (code,) = struct.unpack_from(">8s", rxdata)
        return code

    def nxp_read_config_word(self, access_password: bytes = b"\x00\x00\x00\x00") -> int:
        struct.pack_into(">4sH", self._buffer, 0, access_password, 0x0000)
        rxdata, status = self.command(0xE2, data=self._buffer[0:6])
        if status is False:
            return 0

        (config_word,) = struct.unpack_from(">H", rxdata, 1)
        return config_word

    def set_nxp_confog_word(
        self, config_word: int, access_password: bytes = b"\x00\x00\x00\x00"
    ) -> bool:
        old_config_word = self.nxp_read_config_word(access_password)
        config_word = config_word ^ old_config_word
        struct.pack_into(">4sH", self._buffer, 0, access_password, config_word)
        rxdata, status = self.command(0xE2, data=self._buffer[0:6])
        return True if status and rxdata == b"\x00" else False

    def get_impinj_monza_qt_sr(self, persistence, password: bytes = b"\x00\x00\x00\x00") -> bool:
        return self.impinj_monza_qt_read_cmd(persistence, password=password)[0]

    def get_impinj_monza_qt_mem(self, persistence, password: bytes = b"\x00\x00\x00\x00") -> bool:
        return self.impinj_monza_qt_read_cmd(persistence, password=password)[1]

    def impinj_monza_qt_read_cmd(
        self, persistence, password: bytes = b"\x00\x00\x00\x00"
    ) -> tuple:
        # TODO
        payload = 0b0000_0000_0000_0000
        struct.pack_into(">4sBBH", self._buffer8, 0, password, 0x00, persistence, payload)
        rxdata, status = self.command(0xE5, data=self._buffer8)
        if status is False:
            return (False, False)

        (ul, pc, epc, ctl) = struct.unpack_from(">BH%dsH" % (len(rxdata) - 4), rxdata)
        return (bool(ctl & 0b1000_0000_0000_0000), bool(ctl & 0b0100_0000_0000_0000))

    def set_impinj_monza_qt_sr(
        self, persistence, qt_sr: bool, password: bytes = b"\x00\x00\x00\x00"
    ) -> bool:
        _, qt_mem = self.impinj_monza_qt_read_cmd(persistence, password)
        return self.impinj_monza_qt_write_cmd(persistence, qt_sr, qt_mem, password)

    def set_impinj_monza_qt_mem(
        self, persistence, qt_mem: bool, password: bytes = b"\x00\x00\x00\x00"
    ) -> bool:
        qt_sr, _ = self.impinj_monza_qt_read_cmd(persistence, password)
        return self.impinj_monza_qt_write_cmd(persistence, qt_sr, qt_mem, password)

    def impinj_monza_qt_write_cmd(
        self, persistence, qt_sr: bool, qt_mem: bool, password: bytes = b"\x00\x00\x00\x00"
    ) -> bool:
        payload = 0b0000_0000_0000_0000
        payload |= int(qt_sr) << 15
        payload |= int(qt_mem) << 14
        struct.pack_into(">4sBBH", self._buffer8, 0, password, 0x01, persistence, payload)
        rxdata, status = self.command(0xE5, data=self._buffer8)
        if status is False:
            return False

        (ul, pc, epc, param) = struct.unpack_from(">BH%dsH" % (len(rxdata) - 4), rxdata)
        return True if param == 0x00 else False

    def command(self, cmd, data=b"", timeout=5000) -> tuple:
        self._send(cmd, data)
        rxdata, status = self._receive(length=100, timeout=timeout)
        return rxdata, status

    def _send(self, cmd, data=b"") -> None:
        checksum = self._checksum(self._FRAME_CMD, cmd, len(data), data)
        frame = struct.pack(
            "!BBBH%dsBB" % len(data),
            self._HEADER,
            self._FRAME_CMD,
            cmd,
            len(data),
            data,
            checksum,
            self._END,
        )
        self._verbose and print("Frame to send: %s" % (" ".join(f"{byte:02x}" for byte in frame)))
        self._uart.write(frame)

    def _receive(self, length: int = 8, timeout=1000) -> tuple:
        _buffer = b""
        startpos = -1
        endpos = -1
        count = timeout
        l = 0
        while count > 0 and (l - startpos) < length:
            if self._uart.any() == 0:
                time.sleep(0.01)
                count -= 10
                continue
            _buffer += self._uart.read(1)
            l += 1
            if startpos == -1:
                startpos = _buffer.find(self._HEADER.to_bytes(1, "Big"))
            if startpos != -1 and endpos == -1:
                endpos = _buffer.rfind(self._END.to_bytes(1, "Big"), startpos + 1)
            if startpos != -1 and endpos != -1:
                break

        endpos = _buffer.rfind(self._END.to_bytes(1, "Big"), startpos)
        if startpos != -1 and endpos != -1:
            self._verbose and print(
                "Recv buffer: %s" % (" ".join(f"{byte:02x}" for byte in _buffer))
            )
            frame = _buffer[startpos + 1 : endpos]
            ftype, cmd, length = struct.unpack_from("!BBH", frame, 0)
            rxdata, checksum = struct.unpack_from("!%dsB" % (length), frame, 4)
            if self._checksum(ftype, cmd, len(rxdata), rxdata) != checksum:
                self._verbose and print(
                    "Invalid checksum: %s, data: 0x%s"
                    % (checksum, " ".join(f"{byte:02x}" for byte in frame))
                )
                return b"", False
            return rxdata, False if cmd == 0xFF else True
        else:
            self._verbose and print("Malformed packet received, ignore it")
            return b"", False

    def _checksum(self, *args) -> int:
        chcksum = 0
        for arg in args:
            if isinstance(arg, int):
                chcksum += arg
                continue
            for x in arg:
                chcksum += x
        return chcksum & 0xFF

    def check_error_code(self, code) -> None:
        if code == 0x17:
            raise Exception("Invalid command")
        if code == 0x20:
            raise Exception("FHSS Fail")
        if code == 0x15:
            raise Exception("Inventory Fail")
        if code == 0x16:
            raise Exception("Access Fail")
        if code == 0x09:
            raise Exception("Read Fail")
        if code == 0xA0 | 0b0000_0000:
            raise Exception("Read Error: Other error")
        if code == 0xA0 | 0b0000_0011:
            raise Exception("Read Error: Memory overrun")
        if code == 0xA0 | 0b0000_0100:
            raise Exception("Read Error: Memory locked")
        if code == 0xA0 | 0b0000_1011:
            raise Exception("Read Error: Insufficient power")
        if code == 0xA0 | 0b0000_1111:
            raise Exception("Read Error: Non-specific error")

        if code == 0x10:
            raise Exception("Write Fail")
        if code == 0xB0 | 0b0000_0000:
            raise Exception("Write Error: Other error")
        if code == 0xB0 | 0b0000_0011:
            raise Exception("Write Error: Memory overrun")
        if code == 0xB0 | 0b0000_0100:
            raise Exception("Write Error: Memory locked")
        if code == 0xB0 | 0b0000_1011:
            raise Exception("Write Error: Insufficient power")
        if code == 0xB0 | 0b0000_1111:
            raise Exception("Write Error: Non-specific error")

        if code == 0x13:
            raise Exception("Lock Fail")
        if code == 0xC0 | 0b0000_0000:
            raise Exception("Lock Error: Other error")
        if code == 0xC0 | 0b0000_0011:
            raise Exception("Lock Error: Memory overrun")
        if code == 0xC0 | 0b0000_0100:
            raise Exception("Lock Error: Memory locked")
        if code == 0xC0 | 0b0000_1011:
            raise Exception("Lock Error: Insufficient power")
        if code == 0xC0 | 0b0000_1111:
            raise Exception("Lock Error: Non-specific error")

        if code == 0x12:
            raise Exception("Kill Fail")
        if code == 0xD0 | 0b0000_0000:
            raise Exception("Lock Error: Other error")
        if code == 0xD0 | 0b0000_0011:
            raise Exception("Lock Error: Memory overrun")
        if code == 0xD0 | 0b0000_0100:
            raise Exception("Lock Error: Memory locked")
        if code == 0xD0 | 0b0000_1011:
            raise Exception("Lock Error: Insufficient power")
        if code == 0xD0 | 0b0000_1111:
            raise Exception("Lock Error: Non-specific error")

        if code == 0x14:
            raise Exception("BlockPermalock Fail")
        if code == 0xD0 | 0b0000_0000:
            raise Exception("BlockPermalock Error: Other error")
        if code == 0xD0 | 0b0000_0011:
            raise Exception("BlockPermalock Error: Memory overrun")
        if code == 0xD0 | 0b0000_0100:
            raise Exception("BlockPermalock Error: Memory locked")
        if code == 0xD0 | 0b0000_1011:
            raise Exception("BlockPermalock Error: Insufficient power")
        if code == 0xD0 | 0b0000_1111:
            raise Exception("BlockPermalock Error: Non-specific error")
