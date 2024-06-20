# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

_attrs = {
    "ADCHat": "adc",
    "DACHat": "dac",
    "DAC2Hat": "dac2",
    "DLightHat": "dlight",
    "ENVHat": "env",
    "FingerHat": "finger",
    "JoyCHat": "joyc",
    "JoystickHat": "joystick",
    "MiniEncoderCHat": "mini_encoder_c",
    "MiniJoyHat": "mini_joyc",
    "NCIRHat": "ncir",
    "NeoFlashHat": "neoflash",
    "PIRHat": "pir",
    "RS485Hat": "rs485",
    "ServoHat": "servo",
    "Servos8Hat": "servo8",
    "ThermalHat": "thermal",
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
