# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from . import mbus

_attrs = {
    "DualKmeterModule": "dual_kmeter",
    "Relay4Module": "relay_4",
    "Encoder4MotorModule": "encoder4_motor",
    "PPSModule": "pps",
    "IotBaseCatmModule": "iot_base_catm",
}

# Lazy loader, effectively does:
#   global attr
#   from .mod import attr
# Filched from uasyncio.__init__.py


def __getattr__(attr):
    mod = _attrs.get(attr, None)
    if mod is None:
        raise AttributeError(attr)
    value = getattr(__import__(mod, None, None, True, 1), attr)
    globals()[attr] = value
    return value
