# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from . import mbus

_attrs = {
    "AIN4Module": "ain4",
    "AudioModule": "audio",
    "Bala2Module": "bala2",
    "CommuModuleCAN": "commu",
    "CommuModuleI2C": "commu",
    "CommuModuleRS485": "commu",
    "DCMotorModule": "dc_motor",
    "DisplayModule": "display",
    "DMX512Module": "dmx",
    "DualKmeterModule": "dual_kmeter",
    "ECGModule": "ecg",
    "Encoder4MotorModule": "encoder4_motor",
    "FanModule": "fan",
    "GatewayH2Module": "gateway_h2",
    "GNSSModule": "gnss",
    "GPSModule": "gps",
    "GPSV2Module": "gpsv2",
    "GRBLModule": "grbl",
    "GoPlus2Module": "goplus2",
    "HMIModule": "hmi",
    "IotBaseCatmModule": "iot_base_catm",
    "LANModule": "lan",
    "LlmModule": "llm",
    "LoraModule": "lora",
    "LoRa868V12Module": "lora868_v12",
    "LoRaWANModule": "lorawan",
    "LoRaWAN868Module": "lorawan868",
    "LTEModule": "lte",
    "Module4In8Out": "module_4in8out",
    "NBIOTModule": "nbiot",
    "ODriveModule": "odrive",
    "PLUSModule": "plus",
    "PM25Module": "pm25",
    "PPSModule": "pps",
    "RCAModule": "rca",
    "PwrCANModule": "pwrcan",
    "PwrCANModuleRS485": "pwrcan",
    "QRCodeModule": "qrcode",
    "Relay2Module": "relay_2",
    "Relay4Module": "relay_4",
    "RS232Module": "rs232",
    "Servo2Module": "servo2",
    "StepMotorDriverModule": "step_motor_driver",
    "USBModule": "usb",
    "ZigbeeModule": "zigbee",
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
