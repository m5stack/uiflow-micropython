# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

_attrs = {
    "Keyboard": "keyboard",
    "KeyboardI2C": "keyboard",
    "Button": "button",
    "CAN": "can",
    "IR": "ir",
    "MatrixKeyboard": "matrix_keyboard",
    "DigitalInput": "plcio",
    "Relay": "plcio",
    "PWR485": "pwr485",
    "RFID": "rfid",
    "RGB": "rgb",
    "Rotary": "rotary",
    "SCD40": "scd40",
    "SDCard": "sdcard",
    "SEN55": "sen55",
    "SHT30": "sht30",
}


def __getattr__(attr):
    if attr == "sdcard":
        value = __import__("sdcard", None, None, True, 1)
        globals()[attr] = value
        return value

    mod = _attrs.get(attr, None)
    if mod is None:
        import machine

        value = getattr(machine, attr)
        if value is None:
            raise AttributeError(attr)
        else:
            globals()[attr] = value
            return value
    value = getattr(__import__(mod, None, None, True, 1), attr)
    globals()[attr] = value
    return value
