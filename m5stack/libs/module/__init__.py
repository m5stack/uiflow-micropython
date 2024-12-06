# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from . import mbus

_attrs = {
    "AIN4Module": "ain4",
    "DisplayModule": "display",
    "DMX512Module": "dmx",
    "DualKmeterModule": "dual_kmeter",
    "Encoder4MotorModule": "encoder4_motor",
    "GNSSModule": "gnss",
    "GPSModule": "gps",
    "GRBLModule": "grbl",
    "HMIModule": "hmi",
    "IotBaseCatmModule": "iot_base_catm",
    "LlmModule": "llm",
    "LoraModule": "lora",
    "LoRaWANModule": "lorawan",
    "LoRaWAN868Module": "lorawan868",
    "Module4In8Out": "module_4in8out",
    "NBIOTModule": "nbiot",
    "ODriveModule": "odrive",
    "PLUSModule": "plus",
    "PM25Module": "pm25",
    "PPSModule": "pps",
    "RCAModule": "rca",
    "Relay2Module": "relay_2",
    "Relay4Module": "relay_4",
    "RS232Module": "rs232",
    "Servo2Module": "servo2",
    "StepMotorDriverModule": "step_motor_driver",
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
