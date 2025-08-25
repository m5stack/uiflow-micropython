# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from . import mbus
import network
import machine
import builtins


class LANModule:
    def __new__(cls, cs=-1, rst=-1, int=-1):
        nic = network.LAN(
            0,
            phy_addr=0,
            phy_type=network.PHY_W5500,
            spi=mbus.spi,
            cs=machine.Pin(cs),
            int=machine.Pin(int),
            power=machine.Pin(rst),
        )
        mac = builtins.int.from_bytes(machine.unique_id(), "big")
        mac = mac + 3
        # esp32-s3 no eth mac, so use sta mac + 3
        nic.config(mac=mac.to_bytes(6, "big"))
        nic.active(True)
        return nic
