# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

package(
    "hardware",
    (
        "__init__.py",
        "keyboard/__init__.py",
        "keyboard/asciimap.py",
        "button.py",
        "can.py",
        "dualkey.py",
        "ir.py",
        "lora.py",
        "matrix_keyboard.py",
        "pwr485.py",
        "rfid.py",
        "rgb.py",
        "rotary.py",
        "scd40.py",
        "sdcard.py",
        "sen55.py",
        "sht30.py",
        "sht4x.py",
        "stackchan.py",
    ),
    base_path="..",
    # opt=2,
)
