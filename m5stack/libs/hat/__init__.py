# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

_attrs = {
    "DAC2Hat": "dac2",
    "Servos8Hat": "servo8",
}


def __getattr__(attr):
    mod = _attrs.get(attr, None)
    if mod is None:
        raise AttributeError(attr)
    value = getattr(__import__(mod, None, None, True, 1), attr)
    globals()[attr] = value
    return value
