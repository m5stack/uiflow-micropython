# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

_attrs = {
    "ADCHat": "adc",
    "DACHat": "dac",
    "DAC2Hat": "dac2",
    "DLightHat": "dlight",
    "MiniEncoderCHat": "mini_encoder_c",
    "NCIRHat": "ncir",
    "PIRHat": "pir",
    "RS485Hat": "rs485",
    "ServoHat": "servo",
    "Servos8Hat": "servo8",
    "ToFHat": "tof",
    "VibratorHat": "vibrator",
    "YUNHat": "yun",
}


def __getattr__(attr):
    mod = _attrs.get(attr, None)
    if mod is None:
        raise AttributeError(attr)
    value = getattr(__import__(mod, None, None, True, 1), attr)
    globals()[attr] = value
    return value
