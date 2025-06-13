# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import esp32

nvs = esp32.NVS("uiflow")


def set_boot_option(option):
    global nvs
    nvs.set_u8("boot_option", option)
    nvs.commit()


def get_boot_option():
    global nvs
    return nvs.get_u8("boot_option")
