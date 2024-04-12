# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

_attrs = {
    "ACMeasureUnit": "ac_measure",  # 2.0.3 添加
    "AC_MEASUREUnit": "ac_measure",  # TODO: 类名/型参不符合规范, 2.0.6 移除
    "ADCUnit": "adc",
    "AMeterUnit": "ameter",
    "AngleUnit": "angle",
    "CardKBUnit": "cardkb",
    "KeyCode": "cardkb",
    "ColorUnit": "color",
    "DACUnit": "dac",
    "DAC2Unit": "dac2",
    "DLightUnit": "dlight",
    "DualButtonUnit": "dual_button",
    "EarthUnit": "earth",
    "Encoder8Unit": "encoder8",  # 2.0.3 添加
    "ENCODER8Unit": "encoder8",  # TODO: 类名/型参不符合规范, 2.0.6 移除
    "ENVUnit": "env",
    "ENVPROUnit": "envpro",
    "EXTIOUnit": "extio",
    "EXTIO2Unit": "extio2",
    "FingerUnit": "finger",
    "GestureUnit": "gesture",  # 2.0.3 添加
    "GESTUREUnit": "gesture",  # TODO: 类名/型参不符合规范, 2.0.6 移除
    "GPSUnit": "gps",
    "HbridgeUnit": "hbridge",  # 2.0.3 添加
    "HBRIDGEUnit": "hbridge",  # TODO: 类名/型参不符合规范, 2.0.6 移除
    "IRUnit": "ir",
    "KMeterISOUnit": "kmeter_iso",  # 2.0.3 添加
    "KMETER_ISOUnit": "kmeter_iso",  # TODO: 类名/型参不符合规范, 2.0.6 移除
    "LightUnit": "light",
    "LIMITUnit": "limit",
    "LoRaE220JPUnit": "lora_e220_jp",
    "LoRaWANUnit": "lorawan",
    "MiniScaleUnit": "miniscale",
    "NCIRUnit": "ncir",
    "OPUnit": "op",
    "PAHUBUnit": "pahub",
    "PBHUBUnit": "pbhub",
    "PIRUnit": "pir",
    "RelayUnit": "relay",
    "RFIDUnit": "rfid",
    "RGBUnit": "rgb",
    "ISO485Unit": "rs485_iso",
    "RS485Unit": "rs485",
    "RTC8563Unit": "rtc8563",
    "ScalesUnit": "scales",  # 2.0.3 添加
    "SCALESUnit": "scales",  # TODO: 类名/型参不符合规范, 2.0.6 移除
    "Servos8Unit": "servos8",
    "SERVOS8Unit": "servos8",
    "SynthUnit": "synth",  # 2.0.3 添加
    "SYNTHUnit": "synth",  # TODO: 类名/型参不符合规范, 2.0.6 移除
    "ThermalUnit": "thermal",  # 2.0.3 添加
    "THERMALUnit": "thermal",  # TODO: 类名/型参不符合规范, 2.0.6 移除
    "ToFUnit": "tof",
    "UltrasoundI2CUnit": "ultrasonic_i2c",  # 2.0.3 添加
    "ULTRASONIC_I2CUnit": "ultrasonic_i2c",  # TODO: 类名/型参不符合规范, 2.0.6 移除
    "UltrasoundIOUnit": "ultrasonic_io",  # 2.0.3 添加
    "ULTRASONIC_IOUnit": "ultrasonic_io",  # TODO: 类名不符合规范, 2.0.6 移除
    "UWBUnit": "uwb",
    "VoltmeterUnit": "vmeter",  # 2.0.3 添加
    "VMeterUnit": "vmeter",  # TODO: 类名/型参不符合规范, 2.0.6 移除
    "WeightI2CUnit": "weight_i2c",  # 2.0.3 添加
    "WEIGHT_I2CUnit": "weight_i2c",  # TODO: 类名/型参不符合规范, 2.0.6 移除
    "WeightUnit": "weight",  # 2.0.3 添加
    "WEIGHTUnit": "weight",  # TODO: 类名不符合规范, 2.0.6 移除
    "Thermal2Unit": "thermal2",
    "NCIR2Unit": "ncir2",
    "TOF4MUnit": "tof4m",
}


def __getattr__(attr):
    mod = _attrs.get(attr, None)
    if mod is None:
        raise AttributeError(attr)
    value = getattr(__import__(mod, None, None, True, 1), attr)
    globals()[attr] = value
    return value
