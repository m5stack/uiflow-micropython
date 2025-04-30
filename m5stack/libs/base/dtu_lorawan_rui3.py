# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.rui3 import RUI3
import sys

if sys.platform != "esp32":
    from typing import Literal


class AtomDTULoRaWANRUI3Base(RUI3):
    """Create an AtomDTULoRaWANRUI3Base object.

    :param int id: The UART ID to use (0, 1, or 2). Default is 2.
    :param port: A list or tuple containing the TX and RX pin numbers.
    :type port: list | tuple
    :param bool debug: Whether to enable debug mode. Default is False.

    MicroPython Code Block:

        .. code-block:: python

            from base import AtomDTULoRaWANRUI3Base

            lorawan_rui3 = AtomDTULoRaWANRUI3Base(2, port=(19, 22))
    """

    def __init__(self, id: Literal[0, 1, 2] = 2, port: list | tuple = None, debug=False):
        super().__init__(id, port[1], port[0], debug)

    def set_abp_config(self, dev_addr: str, apps_key: str, nwks_key: str) -> None:
        """Configure the device for ABP (Activation By Personalization) mode.

        :param str dev_addr: The device address for ABP configuration.
        :param str apps_key: The application session key for encryption.
        :param str nwks_key: The network session key for communication.

        MicroPython Code Block:

            .. code-block:: python

                lorawan_rui3.set_abp_config(
                    dev_addr="26011D89",
                    apps_key="2B7E151628AED2A6ABF7158809CF4F3C",
                    nwks_key="2B7E151628AED2A6ABF7158809CF4F3C"
                )
        """
        self.set_join_mode(0)
        self.set_device_address(dev_addr)
        self.set_apps_key(apps_key)
        self.set_networks_key(nwks_key)

    def get_abp_config(
        self,
    ) -> tuple[str | bool | None, str | bool | None, str | bool | None]:
        """Retrieve the current ABP configuration.

        :returns: A tuple containing (device_address, apps_key, networks_key).
        :rtype: tuple[str, str, str]

        MicroPython Code Block:

            .. code-block:: python

                print(lorawan_rui3.get_abp_config())
        """
        return (self.get_device_address(), self.get_apps_key(), self.get_networks_key())

    def set_otaa_config(self, device_eui: str, app_key: str, app_eui: str) -> None:
        """Configure the device for OTAA (Over-The-Air Activation) mode.

        :param str device_eui: The device EUI for OTAA configuration.
        :param str app_key: The application key for encryption.
        :param str app_eui: The application EUI for OTAA configuration.

        MicroPython Code Block:

            .. code-block:: python

                lorawan_rui3.set_otaa_config(
                    device_eui="2CF7F1C0420000AA",
                    app_key="2B7E151628AED2A6ABF7158809CF4F3C"
                    app_eui="80000000000000AA",
                )
        """
        self.set_join_mode(1)
        self.set_device_eui(device_eui)
        self.set_app_key(app_key)
        self.set_app_eui(app_eui)

    def get_otaa_config(
        self,
    ) -> tuple[str | bool | None, str | bool | None, str | bool | None]:
        """Retrieve the current OTAA configuration.

        :returns: A tuple containing (device_eui, app_key, app_eui).
        :rtype: tuple[str, str, str]

        MicroPython Code Block:

            .. code-block:: python

                print(lorawan_rui3.get_otaa_config())
        """
        return (self.get_device_eui(), self.get_app_key(), self.get_app_eui())
