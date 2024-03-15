# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

_attrs = {
    "ENVUnit": "env",
    "PAHUBUnit": "pahub",
    "ColorUnit": "color",
    "ToFUnit": "tof",
    "ADCUnit": "adc",
    "DACUnit": "dac",
    "EXTIOUnit": "extio",
    "EarthUnit": "earth",
    "AngleUnit": "angle",
    "RGBUnit": "rgb",
    "EXTIO2Unit": "extio2",
    "FingerUnit": "finger",
    "PIRUnit": "pir",
    "IRUnit": "ir",
    "DualButtonUnit": "dual_button",
    "NCIRUnit": "ncir",
    "RelayUnit": "relay",
    "RFIDUnit": "rfid",
    "LightUnit": "light",
    "DLightUnit": "dlight",
    "CardKBUnit": "cardkb",
    "KeyCode": "cardkb",
    "ENCODER8Unit": "encoder8",
    "LoRaWANUnit": "lorawan",
    "GPSUnit": "gps",
    "HBRIDGEUnit": "hbridge",
    "PBHUBUnit": "pbhub",
    "UWBUnit": "uwb",
    "AC_MEASUREUnit": "ac_measure",
    "RS485Unit": "rs485",
    "ISO485Unit": "rs485_iso",
    "ULTRASONIC_IOUnit": "ultrasonic_io",
    "ULTRASONIC_I2CUnit": "ultrasonic_i2c",
    "LIMITUnit": "limit",
    "OPUnit": "op",
    "LoRaE220JPUnit": "lora_e220_jp",
    "WEIGHTUnit": "weight",
    "SCALESUnit": "scales",
    "MiniScaleUnit": "miniscale",
    "DAC2Unit": "dac2",
    "GESTUREUnit": "gesture",
    "THERMALUnit": "thermal",
    "SYNTHUnit": "synth",
    "SERVOS8Unit": "servos8",
    "RTC8563Unit": "rtc8563",
    "VMeterUnit": "vmeter",
    "AMeterUnit": "ameter",
    "WEIGHT_I2CUnit": "weight_i2c",
    "KMETER_ISOUnit": "kmeter_iso",
    "Thermal2Unit": "thermal2",
}


def __getattr__(attr):
    mod = _attrs.get(attr, None)
    if mod is None:
        raise AttributeError(attr)
    value = getattr(__import__(mod, None, None, True, 1), attr)
    globals()[attr] = value
    return value
