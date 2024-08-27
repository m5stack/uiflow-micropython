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


import binascii
from . import atecc_asn1 as asn1
from .atecc import ATECC


class CSR:
    """Certificate Signing Request Builder.

    :param adafruit_atecc atecc: ATECC module.
    :param slot_num: ATECC module slot (from 0 to 4).
    :param bool private_key: Generate a new private
                             key in selected slot?
    :param str country: 2-letter country code.
    :param str state_prov: State or Province name,
    :param str city: City name.
    :param str org: Organization name.
    :param str org_unit: Organizational unit name.

    """

    # pylint: disable=too-many-arguments, too-many-instance-attributes
    def __init__(
        self,
        atecc: ATECC,
        slot_num: int,
        private_key: bool,
        country: str,
        state_prov: str,
        city: str,
        org: str,
        org_unit: str,
    ) -> None:
        self._atecc = atecc
        self.private_key = private_key
        self._slot = slot_num
        self._country = country
        self._state_province = state_prov
        self._locality = city
        self._org = org
        self._org_unit = org_unit
        self._common = self._atecc.serial_number()
        self._version_len = 3
        self._cert = None
        self._key = None

    def generate_csr(self) -> bytearray:
        """Generates and returns a certificate signing request."""
        self._csr_begin()
        csr = self._csr_end()
        return csr

    def _csr_begin(self) -> None:
        """Initializes CSR generation."""
        assert 0 <= self._slot <= 4, "Provided slot must be between 0 and 4."
        # Create a new key
        self._key = bytearray(64)
        self._atecc.gen_key(self._key, self._slot, self.private_key)

    def _csr_end(self) -> bytearray:
        """Generates and returns
        a certificate signing request as a base64 string."""
        len_issuer_subject = asn1.issuer_or_subject_length(
            self._country,
            self._state_province,
            self._locality,
            self._org,
            self._org_unit,
            self._common,
        )
        len_sub_header = asn1.get_sequence_header_length(len_issuer_subject)

        len_csr_info = self._version_len + len_issuer_subject
        len_csr_info += len_sub_header + 91 + 2
        len_csr_info_header = asn1.get_sequence_header_length(len_csr_info)

        # CSR Info Packet
        csr_info = bytearray()

        # Append CSR Info --> [0:2]
        asn1.get_sequence_header(len_csr_info, csr_info)

        # Append Version --> [3:5]
        asn1.get_version(csr_info)

        # Append Subject --> [6:7]
        asn1.get_sequence_header(len_issuer_subject, csr_info)

        # Append Issuer or Subject
        asn1.get_issuer_or_subject(
            csr_info,
            self._country,
            self._state_province,
            self._locality,
            self._org,
            self._org_unit,
            self._common,
        )

        # Append Public Key
        asn1.get_public_key(csr_info, self._key)

        # Terminator
        csr_info += b"\xa0\x00"

        # Init. SHA-256 Calculation
        csr_info_sha_256 = bytearray(64)
        self._atecc.sha_start()

        for i in range(0, len_csr_info + len_csr_info_header, 64):
            chunk_len = (len_csr_info_header + len_csr_info) - i

            chunk_len = min(chunk_len, 64)
            if chunk_len == 64:
                self._atecc.sha_update(csr_info[i : i + 64])
            else:
                csr_info_sha_256 = self._atecc.sha_digest(csr_info[i:])

        # Sign the SHA256 Digest
        signature = bytearray(64)
        signature = self._atecc.ecdsa_sign(self._slot, csr_info_sha_256)

        # Calculations for signature and csr length
        len_signature = asn1.get_signature_length(signature)
        len_csr = len_csr_info_header + len_csr_info + len_signature
        asn1.get_sequence_header_length(len_csr)

        # append signature to csr
        csr = bytearray()
        asn1.get_sequence_header(len_csr, csr)
        # append csr_info
        csr += csr_info
        asn1.get_signature(signature, csr)
        # encode and return
        csr = binascii.b2a_base64(csr)
        return csr
