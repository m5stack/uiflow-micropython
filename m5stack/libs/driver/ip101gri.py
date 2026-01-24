# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import network
import machine
import builtins


class IP101GRI:
    def __new__(cls, mdc_pin, mdio_pin, power_pin):
        nic = network.LAN(
            0,
            phy_addr=1,
            phy_type=network.PHY_IP101,
            mdc=machine.Pin(mdc_pin),
            mdio=machine.Pin(mdio_pin),
            power=machine.Pin(power_pin),
        )
        mac = builtins.int.from_bytes(machine.unique_id(), "big")
        nic.config(mac=mac.to_bytes(6, "big"))
        nic.active(True)
        return nic
