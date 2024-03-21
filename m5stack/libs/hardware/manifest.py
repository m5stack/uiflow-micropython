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
        "ir.py",
        "matrix_keyboard.py",
        "rfid.py",
        "rgb.py",
        "rotary.py",
        "sdcard.py",
    ),
    base_path="..",
    opt=0,
)
