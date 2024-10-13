# SPDX-FileCopyrightText: 2018 Arduino SA
# SPDX-FileCopyrightText: 2019 Brent Rubell for Adafruit Industries
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# Copyright (c) 2018 Arduino SA. All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA


import time
import struct
from micropython import const
import binascii


# Device Address
_I2C_ADDR = 0x35


# Command Opcodes (9-1-3)
_OP_COUNTER = const(0x24)
_OP_INFO = const(0x30)
_OP_NONCE = const(0x16)
_OP_RANDOM = const(0x1B)
_OP_SHA = const(0x47)
_OP_LOCK = const(0x17)
_OP_GEN_KEY = const(0x40)
_OP_SIGN = const(0x41)
_OP_WRITE = const(0x12)

# Maximum execution times, in milliseconds (9-4)
EXEC_TIME = {
    _OP_COUNTER: const(20),
    _OP_INFO: const(1),
    _OP_NONCE: const(7),
    _OP_RANDOM: const(23),
    _OP_SHA: const(47),
    _OP_LOCK: const(32),
    _OP_GEN_KEY: const(115),
    _OP_SIGN: const(70),
    _OP_WRITE: const(26),
}

# pylint: disable=line-too-long
"""
Configuration Zone Bytes

Serial Number (Bytes 0-3 and 8-12), Revision Number (Bytes 4-7)
AES Enable (Byte 13), I2C Enable (Byte 14), Reserved (Byte 15)
I2C Address (Byte 16), Reserved (Byte 17); Count Match (Byte 18)
Chip Mode (Byte 19), Slot Config (Bytes 20-51)
Counter 0 (Bytes 52-59), Counter 1 (Bytes 60-67)
Use Lock (Byte 68), Volatile Key Permission (Byte 69)
Secure Boot (Bytes 70-71), KDF (Bytes 72-74)
Reserved (Bytes 75-83), User Extra (Bytes 84-85)
Lock Config (Bytes 86-89), Chip Options (Bytes 90-91)
X509 (Bytes 92-95), Key Config (Bytes 96-127)

I2C Config

+------+-------+---------+-------------+---------------------------------------------------------------+
| HEX          | DEC     | BIN         | Description                                                   |
+======+=======+=========+=============+===============================================================+
| Byte 14: C0  |   192   |  1100 0000  |                                                               |
|              |         |   ^xxx xxxx |  Bit 0 (MSB): 0:Single Wire, 1:I2C; Bit 1-7: Set by Microchip |
+--------------+---------+-------------+---------------------------------------------------------------+
| Byte 16: C0  |  192    | 1100 0000   | Default 7 bit I2C Address: 0xC0>>1: 0x60 ATECC608A-MAHDA      |
+--------------+---------+-------------+---------------------------------------------------------------+
| Byte 16: 6A  |  106    | 0110 1010   | Default 7 bit I2C Address: 0x6A>>1: 0x35 ATECC608A-TNGTLS     |
+--------------+---------+-------------+---------------------------------------------------------------+
| Byte 16: 20  |    32   |  0010 0000  | Default 7 bit I2C Address: 0x20>>1: 0x10 ATECC608A-UNKNOWN    |
+--------------+---------+-------------+---------------------------------------------------------------+

"""

CFG_TLS = bytes(
    bytearray(
        binascii.unhexlify(
            (
                "01 23 00 00 00 00 50 00  00 00 00 00 00 c0 71 00"
                "20 20 20 20 20 20 20 20  20 20 20 20 20 c0 00 55"
                "00 83 20 87 20 87 20 87  2f 87 2f 8f 8f 9f 8f af"
                "20 20 20 20 20 20 20 20  20 20 20 20 20 8f 00 00"
                "00 00 00 00 00 00 00 00  00 00 00 00 20 20 20 20"
                "20 20 20 20 20 20 20 20  20 af 8f ff ff ff ff 00"
                "00 00 00 ff ff ff ff 00  20 20 20 20 20 20 20 20"
                "20 20 20 20 20 00 00 00  ff ff ff ff ff ff ff ff"
                "ff ff ff ff 20 20 20 20  20 20 20 20 20 20 20 20"
                "20 ff ff ff ff 00 00 55  55 ff ff 00 00 00 00 00"
                "00 33 20 20 20 20 20 20  20 20 20 20 20 20 20 00"
                "33 00 33 00 33 00 33 00  1c 00 1c 00 1c 00 3c 00"
                "3c 00 3c 00 3c 20 20 20  20 20 20 20 20 20 20 20"
                "20 20 00 3c 00 3c 00 3c  00 1c 00"
            ).replace(" ", "")
        )
    )
)

# Convert I2C address to config byte 16 and update CFG_TLS
_CFG_BYTES_LIST = list(bytearray(CFG_TLS))
_CFG_BYTE_16 = bytes(bytearray(binascii.unhexlify(hex(_I2C_ADDR << 1).replace("0x", ""))))
_CFG_BYTES_LIST_MOD = _CFG_BYTES_LIST[0:16] + list(_CFG_BYTE_16) + _CFG_BYTES_LIST[17:]
CFG_TLS = bytes(_CFG_BYTES_LIST_MOD)


class ATECC:
    #! uPython interface for ATECCx08A Crypto Co-Processor Devices.

    def __init__(self, i2c, address: int = _I2C_ADDR, debug: bool = False) -> None:
        #! Initializes an ATECC device.
        self._debug = debug
        self._i2cbuf = bytearray(12)
        # don't probe, the device will NACK until woken up
        self._i2c = i2c
        self._i2c_addr = address

    def wakeup(self) -> None:
        #! Wakes up THE ATECC608A from sleep or idle modes.
        try:
            self._i2c.writeto(0, bytes([0x00]))
        except:
            pass
        time.sleep(0.0015)

    def idle(self) -> None:
        #! Puts the chip into idle mode until wakeup is called.
        self._i2c.writeto(self._i2c_addr, bytes([0x02]))
        time.sleep(0.001)

    def sleep(self) -> None:
        #! Puts the chip into low-power sleep mode until wakeup is called.
        self._i2c.writeto(self._i2c_addr, bytes([0x01]))
        time.sleep(0.001)

    def locked(self) -> bool:
        #! Returns if the ATECC is locked.
        config = bytearray(4)
        self._read(0x00, 0x15, config)
        time.sleep(0.001)
        return config[2] == 0x0 and config[3] == 0x00

    def serial_number(self) -> str:
        #! Returns the ATECC serial number.
        serial_num = bytearray(9)
        # 4-byte reads only
        temp_sn = bytearray(4)
        # SN<0:3>
        self._read(0, 0x00, temp_sn)
        serial_num[0:4] = temp_sn
        time.sleep(0.001)
        # SN<4:8>
        self._read(0, 0x02, temp_sn)
        serial_num[4:8] = temp_sn
        time.sleep(0.001)
        # Append Rev
        self._read(0, 0x03, temp_sn)
        serial_num[8] = temp_sn[0]
        time.sleep(0.001)
        # neaten up the serial for printing
        serial_num = str(binascii.hexlify(serial_num), "utf-8")
        serial_num = serial_num.upper()
        return serial_num

    def version(self) -> int:
        #! Returns the ATECC608As revision number.
        self.wakeup()
        self.idle()
        vers = bytearray(4)
        vers = self.info(0x00)
        return (vers[2] << 8) | vers[3]

    def lock_all_zones(self) -> None:
        #! Locks Config, Data and OTP Zones.
        self.lock(0)
        self.lock(1)

    def lock(self, zone: int) -> None:
        #! Locks specific ATECC zones.
        self.wakeup()
        self._send_command(0x17, 0x80 | zone, 0x0000)
        time.sleep(EXEC_TIME[_OP_LOCK] / 1000)
        res = bytearray(1)
        self._get_response(res)
        assert res[0] == 0x00, "Failed locking ATECC!"
        self.idle()

    def info(self, mode: int, param=None) -> bytearray:
        #! Returns device state information.
        self.wakeup()
        if not param:
            self._send_command(_OP_INFO, mode)
        else:
            self._send_command(_OP_INFO, mode, param)
        time.sleep(EXEC_TIME[_OP_INFO] / 1000)
        info_out = bytearray(4)
        self._get_response(info_out)
        self.idle()
        return info_out

    def nonce(self, data: bytearray, mode: int = 0, zero: int = 0x0000) -> bytearray:
        #! Generates a nonce by combining internally generated random number with an input value.
        self.wakeup()
        if mode in (0x00, 0x01):
            if zero == 0x00:
                assert len(data) == 20, "Data value must be 20 bytes long."
            self._send_command(_OP_NONCE, mode, zero, data)
            # nonce returns 32 bytes
            calculated_nonce = bytearray(32)
        elif mode == 0x03:
            # Operating in Nonce pass-through mode
            assert len(data) == 32, "Data value must be 32 bytes long."
            self._send_command(_OP_NONCE, mode, zero, data)
            # nonce returns 1 byte
            calculated_nonce = bytearray(1)
        else:
            raise RuntimeError("Invalid mode specified!")
        time.sleep(EXEC_TIME[_OP_NONCE] / 1000)
        self._get_response(calculated_nonce)
        time.sleep(1 / 1000)
        if mode == 0x03:
            assert calculated_nonce[0] == 0x00, "Incorrectly calculated nonce in pass-thru mode"
        self.idle()
        return calculated_nonce

    def counter(self, counter: int = 0, increment_counter: bool = True) -> bytearray:
        #! Reads the binary count value from one of the two monotonic
        #! counters located on the device within the configuration zone.
        #! The maximum value that the counter may have is 2,097,151.
        counter = 0x00
        self.wakeup()
        if counter == 1:
            counter = 0x01
        if increment_counter:
            self._send_command(_OP_COUNTER, 0x01, counter)
        else:
            self._send_command(_OP_COUNTER, 0x00, counter)
        time.sleep(EXEC_TIME[_OP_COUNTER] / 1000)
        count = bytearray(4)
        self._get_response(count)
        self.idle()
        return count

    def random(self, rnd_min: int = 0, rnd_max: int = 0) -> int:
        #! Generates a random number for use by the system.
        if rnd_max:
            rnd_min = 0
        if rnd_min >= rnd_max:
            return rnd_min
        delta = rnd_max - rnd_min
        r = bytearray(16)
        r = self._random(r)
        data = 0
        for i in enumerate(r):
            data += r[i[0]]
        if data < 0:
            data = -data
        data = data % delta
        return data + rnd_min

    def _random(self, data: bytearray) -> bytearray:
        #! Initializes the random number generator and returns.
        self.wakeup()
        data_len = len(data)
        while data_len:
            self._send_command(_OP_RANDOM, 0x00, 0x0000)
            time.sleep(EXEC_TIME[_OP_RANDOM] / 1000)
            resp = bytearray(32)
            self._get_response(resp)
            copy_len = min(32, data_len)
            data = resp[0:copy_len]
            data_len -= copy_len
        self.idle()
        return data

    # SHA-256 Commands
    def sha_start(self) -> bytearray:
        #! Initializes the SHA-256 calculation engine and the SHA context in memory.
        #! This method MUST be called before sha_update or sha_digest
        self.wakeup()
        self._send_command(_OP_SHA, 0x00)
        time.sleep(EXEC_TIME[_OP_SHA] / 1000)
        status = bytearray(1)
        self._get_response(status)
        assert status[0] == 0x00, "Error during sha_start."
        self.idle()
        return status

    def sha_update(self, message: bytes) -> bytearray:
        #! Appends bytes to the message. Can be repeatedly called.
        self.wakeup()
        self._send_command(_OP_SHA, 0x01, 64, message)
        time.sleep(EXEC_TIME[_OP_SHA] / 1000)
        status = bytearray(1)
        self._get_response(status)
        assert status[0] == 0x00, "Error during SHA Update"
        self.idle()
        return status

    def sha_digest(self, message: bytearray = None) -> bytearray:
        #! Returns the digest of the data passed to the sha_update method so far.
        if not hasattr(message, "append") and message is not None:
            message = struct.pack("B", message)
        self.wakeup()
        # Include optional message
        if message:
            self._send_command(_OP_SHA, 0x02, len(message), message)
        else:
            self._send_command(_OP_SHA, 0x02)
        time.sleep(EXEC_TIME[_OP_SHA] / 1000)
        digest = bytearray(32)
        self._get_response(digest)
        assert len(digest) == 32, "SHA response length does not match expected length."
        self.idle()
        return digest

    def gen_key(self, key: bytearray, slot_num: int, private_key: bool = False) -> bytearray:
        #! Generates a private or public key.
        assert 0 <= slot_num <= 4, "Provided slot must be between 0 and 4."
        self.wakeup()
        if private_key:
            self._send_command(_OP_GEN_KEY, 0x04, slot_num)
        else:
            self._send_command(_OP_GEN_KEY, 0x00, slot_num)
        time.sleep(EXEC_TIME[_OP_GEN_KEY] / 1000)
        self._get_response(key)
        time.sleep(0.001)
        self.idle()
        return key

    def ecdsa_sign(self, slot: int, message: bytearray) -> bytearray:
        #! Generates and returns a signature using the ECDSA algorithm.
        # Load the message digest into TempKey using Nonce (9.1.8)
        self.nonce(message, 0x03)
        # Generate and return a signature
        sig = bytearray(64)
        sig = self.sign(slot)
        return sig

    def sign(self, slot_id: int) -> bytearray:
        #! Performs ECDSA signature calculation with key in provided slot.
        self.wakeup()
        self._send_command(0x41, 0x80, slot_id)
        time.sleep(EXEC_TIME[_OP_SIGN] / 1000)
        signature = bytearray(64)
        self._get_response(signature)
        self.idle()
        return signature

    def verify_sign(self, message: bytearray, sign: bytearray, key: bytearray):
        temp_sign = bytearray(128)
        # Load the message digest into TempKey using Nonce (9.1.8)
        self.nonce(message, 0x03)
        temp_sign[0:64] = sign
        temp_sign[64:128] = key
        self.wakeup()
        self._send_command(0x45, 0x02, 0x0004, temp_sign)
        time.sleep(0.058)
        status = bytearray(1)
        self._get_response(status)
        self.idle()
        return status

    def write_config(self, data: bytearray) -> None:
        #! Writes configuration data to the device's EEPROM.
        # First 16 bytes of data are skipped, not writable
        for i in range(16, 128, 4):
            if i == 84:
                # can't write
                continue
            self._write(0, i // 4, data[i : i + 4])

    def _write(self, zone, address: int, buffer: bytearray) -> None:
        #! Writes to the I2C.
        self.wakeup()
        if len(buffer) not in (4, 32):
            raise RuntimeError("Only 4 or 32-byte writes supported.")
        if len(buffer) == 32:
            zone |= 0x80
        self._send_command(0x12, zone, address, buffer)
        time.sleep(0.026)
        status = bytearray(1)
        self._get_response(status)
        self.idle()

    def _read(self, zone: int, address: int, buffer: bytearray) -> None:
        #! Reads from the I2C.
        self.wakeup()
        if len(buffer) not in (4, 32):
            raise RuntimeError("Only 4 and 32 byte reads supported")
        if len(buffer) == 32:
            zone |= 0x80
        self._send_command(2, zone, address)
        time.sleep(0.005)
        self._get_response(buffer)
        time.sleep(0.001)
        self.idle()

    def _send_command(self, opcode: int, param_1: int, param_2: int = 0x00, data="") -> None:
        #! Sends a security command packet over i2c.
        #! assembling command packet
        command_packet = bytearray(8 + len(data))
        #! word address
        command_packet[0] = 0x03
        #! i/o group: count
        command_packet[1] = len(command_packet) - 1  # count
        #! security command packets
        command_packet[2] = opcode
        command_packet[3] = param_1
        command_packet[4] = param_2 & 0xFF
        command_packet[5] = param_2 >> 8
        for i, cmd in enumerate(data):
            command_packet[6 + i] = cmd
        if self._debug:
            print("Command Packet Sz: ", len(command_packet))
            print("\tSending:", [hex(i) for i in command_packet])
        # Checksum, CRC16 verification
        crc = self._at_crc(command_packet[1:-2])
        command_packet[-1] = crc >> 8
        command_packet[-2] = crc & 0xFF
        self.wakeup()
        self._i2c.writeto(self._i2c_addr, command_packet)
        # small sleep
        time.sleep(0.001)

    def _get_response(self, buf, length: int = None, retries: int = 20) -> int:
        self.wakeup()
        if length is None:
            length = len(buf)
        response = bytearray(length + 3)  # 1 byte header, 2 bytes CRC, len bytes data
        for _ in range(retries):
            try:
                self._i2c.readfrom_into(self._i2c_addr, response)
                break
            except OSError:
                pass
        else:
            raise RuntimeError("Failed to read data from chip")
        if self._debug:
            print("\tReceived: ", [hex(i) for i in response])
        crc = response[-2] | (response[-1] << 8)
        crc2 = self._at_crc(response[0:-2])
        if crc != crc2:
            raise RuntimeError("CRC Mismatch")
        for i in range(length):
            buf[i] = response[i + 1]
        return response[1]

    @staticmethod
    def _at_crc(data, length: int = None) -> int:
        if length is None:
            length = len(data)
        if not data or not length:
            return 0
        polynom = 0x8005
        crc = 0x0
        for b in data:
            for shift in range(8):
                data_bit = 0
                if b & (1 << shift):
                    data_bit = 1
                crc_bit = (crc >> 15) & 0x1
                crc <<= 1
                crc &= 0xFFFF
                if data_bit != crc_bit:
                    crc ^= polynom
                    crc &= 0xFFFF
        return crc & 0xFFFF
