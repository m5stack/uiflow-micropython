# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

_attrs = {
    "ATOMCANBase": "atom_can",
    "AtomDTULoRaWANBase": "dtu_lorawan",
    "AtomDTUNBIoT": "dtu_nbiot",
    "ATOMGPSBase": "atom_gps",
    "ATOMSocketBase": "atom_socket",
    "ATOMEchoBase": "echo",
    "AtomicDisplayBase": "display",
    "AtomicHDriverBase": "hdriver",
    "Motion": "motion",
    "MotionBase": "motion",
    "AtomicPWMBase": "pwm",
    "AtomicQRCodeBase": "qrcode",
    "AtomicQRCode2Base": "qrcode2",
    "AtomRS232": "rs232",
    "AtomRS485": "rs232",
    "SpeakerBase": "speaker",
    "AtomicStepmotorBase": "stepmotor",
    "AtomicTFCardBase": "tfcard",
}


def __getattr__(attr):
    mod = _attrs.get(attr, None)
    if mod is None:
        raise AttributeError(attr)
    value = getattr(__import__(mod, None, None, True, 1), attr)
    globals()[attr] = value
    return value
