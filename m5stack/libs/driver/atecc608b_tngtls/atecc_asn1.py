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


import struct


# pylint: disable=invalid-name
def get_signature(signature: bytearray, data: bytearray) -> int:
    """
    Appends signature data to buffer.

    :param bytearray signature: The signature to append
    :param bytearray data: The buffer to append the signature to
    :return: Updated length of the buffer
    """
    # Signature algorithm
    data += b"\x30\x0a\x06\x08"
    # ECDSA with SHA256
    data += b"\x2a\x86\x48\xce\x3d\x04\x03\x02"
    r = signature[0]
    s = signature[32]
    r_len = 32
    s_len = 32

    while r == 0x00 and r_len > 1:
        r += 1
        r_len -= 1

    while s == 0x00 and s_len > 1:
        s += 1
        s_len -= 1

    if r & 0x80:
        r_len += 1

    if s & 0x80:
        s_len += 1

    data += b"\x03" + struct.pack("B", r_len + s_len + 7) + b"\x00"

    data += b"\x30" + struct.pack("B", r_len + s_len + 4)

    data += b"\x02" + struct.pack("B", r_len)

    if r & 0x80:
        data += b"\x00"
        r_len -= 1
    data += signature[0:r_len]

    if r & 0x80:
        r_len += 1

    data += b"\x02" + struct.pack("B", s_len)
    if s & 0x80:
        data += b"\x00"
        s_len -= 1

    data += signature[s_len:]

    if s & 0x80:
        s_len += 1

    return 21 + r_len + s_len


# pylint: disable=too-many-arguments
def get_issuer_or_subject(
    data: bytearray,
    country: str,
    state_prov: str,
    locality: str,
    org: str,
    org_unit: str,
    common: str,
):
    """
    Appends issuer or subject, if they exist, to data.

    :param bytearray data: buffer to append to
    :param str country: The country to append to the buffer
    :param str state_prov: The state/province to append to the buffer
    :param str locality: The locality to append to the buffer
    :param str org: The organization to append to the buffer
    :param str org_unit: The organizational unit to append to the buffer
    :param str common: The common data to append to the buffer
    """
    if country:
        get_name(country, 0x06, data)
    if state_prov:
        get_name(state_prov, 0x08, data)
    if locality:
        get_name(locality, 0x07, data)
    if org:
        get_name(org, 0x0A, data)
    if org_unit:
        get_name(org_unit, 0x0B, data)
    if common:
        get_name(common, 0x03, data)


def get_name(name: str, obj_type: int, data: bytearray) -> int:
    """
    Appends ASN.1 string in form: set -> seq -> objid -> string

    :param str name: String to append to buffer.
    :param int obj_type: Object identifier type.
    :param bytearray data: Buffer to write to.
    :return: Length of the updated buffer
    """
    # ASN.1 SET
    data += b"\x31" + struct.pack("B", len(name) + 9)
    # ASN.1 SEQUENCE
    data += b"\x30" + struct.pack("B", len(name) + 7)
    # ASN.1 OBJECT IDENTIFIER
    data += b"\x06\x03\x55\x04" + struct.pack("B", obj_type)

    # ASN.1 PRINTABLE STRING
    data += b"\x13" + struct.pack("B", len(name))
    data.extend(name)
    return len(name) + 11


def get_version(data: bytearray) -> None:
    """
    Appends X.509 version to data.

    :param bytearray data: Buffer to append the version to
    """
    #  If no extensions are present, but a UniqueIdentifier
    #  is present, the version SHOULD be 2 (value is 1) [4-1-2]
    data += b"\x02\x01\x00"


def get_sequence_header(length: int, data: bytearray) -> None:
    """
    Appends sequence header to provided data.

    :param int length: Length of the buffer
    :param bytearray data: The buffer
    """
    data += b"\x30"
    if length > 255:
        data += b"\x82"
        data.append((length >> 8) & 0xFF)
    elif length > 127:
        data += b"\x81"
    length_byte = struct.pack("B", (length) & 0xFF)
    data += length_byte


def get_public_key(data: bytearray, public_key: bytearray) -> None:
    """
    Appends public key subject and object identifiers.

    :param bytearray data: buffer
    :param bytearray public_key: Public key to append
    """
    # Subject: Public Key
    data += b"\x30" + struct.pack("B", (0x59) & 0xFF) + b"\x30\x13"
    # Object identifier: EC Public Key
    data += b"\x06\x07\x2a\x86\x48\xce\x3d\x02\x01"
    # Object identifier: PRIME 256 v1
    data += b"\x06\x08\x2a\x86\x48\xce\x3d\x03\x01\x07\x03\x42\x00\x04"
    # Extend the buffer by the public key
    data += public_key


def get_signature_length(signature: bytearray) -> int:
    """
    Return length of ECDSA signature.

    :param bytearray signature: Signed SHA256 hash.
    :return: length of ECDSA signature.
    """
    r = signature[0]
    s = signature[32]
    r_len = 32
    s_len = 32

    while r == 0x00 and r_len > 1:
        r += 1
        r_len -= 1

    if r & 0x80:
        r_len += 1

    while s == 0x00 and s_len > 1:
        s += 1
        s_len -= 1

    if s & 0x80:
        s_len += 1
    return 21 + r_len + s_len


def get_sequence_header_length(seq_header_len: int) -> int:
    """
    Returns length of SEQUENCE header.

    :param int seq_header_len: Sequence header length
    :return: Length of the sequence header
    """
    if seq_header_len > 255:
        return 4
    if seq_header_len > 127:
        return 3
    return 2


def issuer_or_subject_length(
    country: str, state_prov: str, city: str, org: str, org_unit: str, common: str
) -> int:
    """
    Returns total length of provided certificate information.

    :param str country: Country of certificate
    :param str state_prov: State/province of certificate
    :param str city: City of certificate
    :param str org: Organization of certificate
    :param str org_unit: Organization unit of certificate
    :param str common: Common data of certificate
    :raises: TypeError if return value is 0
    :return: Total length of provided certificate information.
    """
    tot_len = 0
    if country:
        tot_len += 11 + len(country)
    if state_prov:
        tot_len += 11 + len(state_prov)
    if city:
        tot_len += 11 + len(city)
    if org:
        tot_len += 11 + len(org)
    if org_unit:
        tot_len += 11 + len(org_unit)
    if common:
        tot_len += 11 + len(common)
    else:
        raise TypeError("Provided length must be > 0")
    return tot_len
