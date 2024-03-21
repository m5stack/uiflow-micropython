# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import esp32


def set_boot_option(option):
    nvs = esp32.NVS("uiflow")
    nvs.set_u8("boot_option", option)
    nvs.commit()


def get_boot_option():
    nvs = esp32.NVS("uiflow")
    return nvs.get_u8("boot_option")
