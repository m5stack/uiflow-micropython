# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
from unit.pahub import PAHUBUnit
from unit.unit_helper import UnitError
import binascii
import struct
import time

from driver.atecc608b_tngtls.atecc import ATECC
from driver.atecc608b_tngtls.atecc_cert_util import CSR

# Device Address
_I2C_ADDR = 0x35


class IDUnit:
    #! uPython interface for ATECC608B Crypto Co-Processor Devices.

    def __init__(self, i2c: I2C | PAHUBUnit, address: int = _I2C_ADDR) -> None:
        #! Initializes an ATECC device.
        self._i2c = i2c
        self._i2c_addr = address
        if address not in self._i2c.scan():
            raise UnitError("ID unit maybe not found in Grove")
        self.atecc = ATECC(self._i2c, self._i2c_addr)

    def get_revision_number(self) -> int:
        #! Returns the ATECC608B revision number
        return hex(self.atecc.version())

    def get_serial_number(self) -> str:
        #! Returns the ATECC serial number.
        return self.atecc.serial_number()

    def randint(self, min: int = 0, max: int = 0) -> int:
        #! Generates a random number for use by the system.
        random = bytearray(4)
        min, max = (max, min) if min > max else (min, max)
        return (struct.unpack("I", self.atecc._random(random))[0] % (max - min)) + min

    def random(self) -> int:
        #! Generates a random floating point number in the range [0.0, 1.0).
        return float(self.randint(1, 9999999) / 9999999)

    def randrange(self, min: int = 0, max: int = 0, step: int = 1) -> int:
        #! Generates a random integer from the range [start, stop) in steps of step.
        random = self.randint(min, max)
        random -= random % step
        return random

    def uniform(self, min: float = 0, max: float = 0) -> float:
        min, max = (max, min) if min > max else (min, max)
        return min + (max - min) * self.random()

    def get_generate_key(self, slot_num: int, private_key: bool = False):
        #! Generates a private or public key.
        assert 0 <= slot_num <= 4, "Provided slot must be between 0 and 4."
        # Create a new key
        key = bytearray(64)
        self.atecc.gen_key(key, slot_num, private_key)
        return key

    def ecdh_stored_key(self, slot_num: int, mode: int, external_public_key: bytearray = None):
        if external_public_key is None:
            external_public_key = bytearray(64)
            self.atecc.gen_key(external_public_key, 0, private_key=False)

        if len(external_public_key) != 64:
            raise ValueError("External public key must be exactly 64 bytes.")

        self.atecc._send_command(
            opcode=0x43, param_1=mode, param_2=slot_num, data=external_public_key
        )

        if mode in (0x0C, 0x08):
            time.sleep(1)
            res = bytearray(32)
            self.atecc._get_response(res)
            return res
        else:
            return None

    def get_ecdsa_sign(self, slot: int, message: str | list | bytearray) -> bytearray | None:
        #! Generates and returns a signature using the ECDSA algorithm.
        if len(message) == 32:
            if isinstance(message, list):
                message = bytes(message)
            elif isinstance(message, str):
                message = message.encode()
            return self.atecc.ecdsa_sign(slot, message)

    def get_verify_ecdsa_sign(
        self, message: bytearray, sign: bytearray, key: bytearray
    ) -> bool | None:
        #! returns a verify signature using the ECDSA algorithm.
        if len(message) == 32:
            if isinstance(message, list):
                message = bytes(message)
            elif isinstance(message, str):
                message = message.encode()
            return bool(not self.atecc.verify_sign(message, sign, key)[0])

    def get_sha256_hash(self, message: str = None, format: int = 0) -> str:
        # Initialize the SHA256 calculation engine
        self.atecc.sha_start()
        # Append bytes to the SHA digest
        self.atecc.sha_update(message.encode())
        # Return the digest of the data passed to sha_update
        return (
            binascii.b2a_base64(self.atecc.sha_digest()).decode()[:-1]
            if format
            else binascii.hexlify(self.atecc.sha_digest()).decode()
        )

    def set_certificate_signing_request(
        self,
        slot_num: int,
        private_key: bool,
        country: str,
        state_prov: str,
        city: str,
        org: str,
        org_unit: str,
        file_path: str,
    ) -> str:
        #! Certificate Signing Request Builder.
        self.csr = CSR(self.atecc, slot_num, private_key, country, state_prov, city, org, org_unit)
        # Generate CSR
        my_csr = self.csr.generate_csr()
        #! "-----BEGIN CERTIFICATE REQUEST-----\n"
        encoded_data = my_csr.decode("utf-8")
        #! "-----END CERTIFICATE REQUEST-----"
        pem_content = (
            "-----BEGIN CERTIFICATE REQUEST-----\n"
            + encoded_data
            + "-----END CERTIFICATE REQUEST-----"
        )
        with open(file_path, "w+") as pem_file:
            pem_file.write(pem_content)

    # ref: ATECC608A-TFLXTLS 4.4.1 Table 4-5
    def read_data_zone(self, data_zone: int):
        self.atecc._send_command(
            opcode=0x02,
            param_1=0x00,
            param_2=data_zone,
        )
        time.sleep(0.1)
        temp = bytearray(4)
        self.atecc._get_response(temp)
        return temp

    def write_data_zone(self, data_zone: int, data: bytearray):
        self.atecc._send_command(
            opcode=0x12,
            param_1=0x02,
            param_2=data_zone,
            data=data,
        )

    def aes_ecb_encrypt(self, position: int, data: bytearray):
        if len(data) != 16:
            raise ValueError("Data must be 16 bytes")
        self.atecc._send_command(
            opcode=0x51,
            param_1=(position << 6),
            param_2=0x09,  # ATECC608B AES Key only stored in slot 9
            data=data,
        )
        time.sleep(1)
        res = bytearray(16)
        self.atecc._get_response(res)
        return res

    def aes_ecb_decrypt(self, position: int, data: bytearray):
        if len(data) != 16:
            raise ValueError("Data must be 16 bytes")
        self.atecc._send_command(
            opcode=0x51,
            param_1=(position << 6) + 1,
            param_2=0x09,  # ATECC608B AES Key only stored in slot 9
            data=data,
        )
        time.sleep(1)
        res = bytearray(16)
        self.atecc._get_response(res)
        return res

    def get_h_field(self):
        zero_block = bytearray([0x00] * 16)
        return self.aes_ecb_encrypt(0x00, zero_block)

    def aes_gfm_encrypt(self, data: bytearray):
        if len(data) != 16:
            raise ValueError("Data must be 16 bytes")
        data = self.get_h_field() + data
        time.sleep(1)
        self.atecc._send_command(opcode=0x51, param_1=0x03, param_2=0x00, data=data)
        time.sleep(1)
        res = bytearray(16)
        self.atecc._get_response(res)
        return res
