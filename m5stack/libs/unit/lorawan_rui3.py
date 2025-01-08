# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.rui3 import RUI3
import sys

if sys.platform != "esp32":
    from typing import Literal


class LoRaWANUnit_RUI3(RUI3):
    def __init__(self, id: Literal[0, 1, 2] = 1, port: list | tuple = None, debug=False):
        super().__init__(id, port[1], port[0], debug)

    def set_abp_config(self, dev_addr: str, apps_key: str, nwks_key: str):
        """
        note:
            en: Configure the device for ABP (Activation By Personalization) mode using the provided device address, application session key, and network session key.

        params:
            dev_addr:
                note: The device address for ABP configuration.
            apps_key:
                note: The application session key for encryption.
            nwks_key:
                note: The network session key for communication.
        """
        self.set_join_mode(0)
        self.set_device_address(dev_addr)
        self.set_apps_key(apps_key)
        self.set_networks_key(nwks_key)

    def get_abp_config(self) -> tuple[str | bool | None, str | bool | None, str | bool | None]:
        """
        note:
            en: Retrieve the current ABP configuration, including the device address, application session key, and network session key.

        params:
            note:

        returns:
            note: A tuple containing the device address, application session key, and network session key. Returns None or False for missing or invalid configurations.
        """
        return (self.get_device_address(), self.get_apps_key(), self.get_networks_key())

    def set_otaa_config(self, device_eui, app_eui, app_key):
        """
        note:
            en: Configure the device for OTAA (Over-The-Air Activation) mode using the provided device EUI, application EUI, and application key.

        params:
            device_eui:
                note: The device EUI for OTAA configuration.
            app_eui:
                note: The application EUI for OTAA configuration.
            app_key:
                note: The application key for encryption.
        """
        self.set_join_mode(1)
        self.set_device_eui(device_eui)
        self.set_app_eui(app_eui)
        self.set_app_key(app_key)

    def get_otaa_config(self):
        """
        note:
            en: Retrieve the current OTAA configuration, including the device EUI, application key, and application EUI.

        params:
            note:

        returns:
            note: A tuple containing the device EUI, application key, and application EUI.
        """
        return (self.get_device_eui(), self.get_app_key(), self.get_app_eui())
