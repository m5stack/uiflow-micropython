# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

package(
    "usb",
    (
        "device/__init__.py",
        "device/core.py",
        "device/hid.py",
        "device/mouse.py",
        "device/keyboard.py",
    ),
    base_path="..",
    opt=0,
)
