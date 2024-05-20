# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

_attrs = {
    "ACMeasureUnit": "ac_measure",  # 2.0.3 添加
    "AC_MEASUREUnit": "ac_measure",  # TODO: 类名/型参不符合规范, 2.0.6 移除
    "ADCV11Unit": "adc_v11",
    "ADCUnit": "adc",
    "AMeterUnit": "ameter",
    "AngleUnit": "angle",
    "Angle8Unit": "angle8",
    "BLDCDriverUnit": "bldc_driver",
    "ButtonUnit": "button",
    "BuzzerUnit": "buzzer",
    "CANUnit": "can",
    "MiniCANUnit": "can",
    "CardKBUnit": "cardkb",
    "KeyCode": "cardkb",
    "CATMGNSSUnit": "catm_gnss",
    "CATMUnit": "catm",
    "CO2Unit": "co2",
    "CO2LUnit": "co2l",
    "ColorUnit": "color",
    "DACUnit": "dac",
    "DAC2Unit": "dac2",
    "DLightUnit": "dlight",
    "DualButtonUnit": "dual_button",
    "EarthUnit": "earth",
    "EncoderUnit": "encoder",
    "Encoder8Unit": "encoder8",  # 2.0.3 添加
    "ENCODER8Unit": "encoder8",  # TODO: 类名/型参不符合规范, 2.0.6 移除
    "ENVUnit": "env",
    "ENVPROUnit": "envpro",
    "ExtEncoderUnit": "extencoder",
    "EXTIOUnit": "extio",
    "EXTIO2Unit": "extio2",
    "FaderUnit": "fader",
    "FanUnit": "fan",
    "FingerUnit": "finger",
    "GestureUnit": "gesture",  # 2.0.3 添加
    "GESTUREUnit": "gesture",  # TODO: 类名/型参不符合规范, 2.0.6 移除
    "GPSUnit": "gps",
    "HallEffectUnit": "hall_effect",
    "HbridgeUnit": "hbridge",  # 2.0.3 添加
    "HBRIDGEUnit": "hbridge",  # TODO: 类名/型参不符合规范, 2.0.6 移除
    "IRUnit": "ir",
    "KMeterISOUnit": "kmeter_iso",  # 2.0.3 添加
    "KMETER_ISOUnit": "kmeter_iso",  # TODO: 类名/型参不符合规范, 2.0.6 移除
    "LaserRXUnit": "laser_rx",
    "LaserTXUnit": "laser_tx",
    "LightUnit": "light",
    "LIMITUnit": "limit",
    "LoRaE220JPUnit": "lora_e220_jp",
    "LoRaWANUnit": "lorawan",
    "MiniScaleUnit": "miniscale",
    "NCIRUnit": "ncir",
    "NCIR2Unit": "ncir2",
    "OPUnit": "op",
    "PAHUBUnit": "pahub",
    "PBHUBUnit": "pbhub",
    "PIRUnit": "pir",
    "ReflectiveIRUnit": "reflective_ir",
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
    "SSRUnit": "ssr",
    "SynthUnit": "synth",  # 2.0.3 添加
    "SYNTHUnit": "synth",  # TODO: 类名/型参不符合规范, 2.0.6 移除
    "ThermalUnit": "thermal",  # 2.0.3 添加
    "THERMALUnit": "thermal",  # TODO: 类名/型参不符合规范, 2.0.6 移除
    "Thermal2Unit": "thermal2",
    "ToFUnit": "tof",
    "TOF4MUnit": "tof4m",
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
    "WateringUnit": "watering",
}


def __getattr__(attr):
    mod = _attrs.get(attr, None)
    if mod is None:
        raise AttributeError(attr)
    value = getattr(__import__(mod, None, None, True, 1), attr)
    globals()[attr] = value
    return value
