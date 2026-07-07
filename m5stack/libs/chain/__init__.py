# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

_attrs = {
    "AngleChain": "angle",
    "BuzzerChain": "buzzer",
    "ChainBus": "chain",
    "EncoderChain": "encoder",
    "JoystickChain": "joystick",
    "KeyChain": "key",
    "MicChain": "mic",
    "MonoChain": "mono",
    "PIRChain": "pir",
    "RGBChain": "rgb",
    "SwitchChain": "switch",
    "ToFChain": "tof",
    "BusChainUnit": "unit_bus",
}


def __getattr__(attr):
    mod = _attrs.get(attr, None)
    if mod is None:
        raise AttributeError(attr)
    value = getattr(__import__(mod, None, None, True, 1), attr)
    globals()[attr] = value
    return value
