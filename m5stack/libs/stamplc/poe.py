# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import network
import machine
import builtins


class PoEStamPLC:
    """Create an PoEStamPLC object

    :param int cs_pin: The chip select pin number.
    :param int rst_pin: The reset pin number.
    :param int int_pin: The interrupt pin number.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from stamplc import PoEStamPLC

            stamplc_poe_0 = PoEStamPLC()
    """

    def __new__(cls, cs_pin=11, rst_pin=3, int_pin=14):
        _spi_handle = machine.SPI(
            1,
            sck=machine.Pin(7),
            mosi=machine.Pin(8),
            miso=machine.Pin(9),
        )
        nic = network.LAN(
            0,
            phy_addr=0,
            phy_type=network.PHY_W5500,
            spi=_spi_handle,
            cs=machine.Pin(cs_pin),
            int=machine.Pin(int_pin),
        )
        mac = builtins.int.from_bytes(machine.unique_id(), "big")
        mac = mac + 3
        # esp32-s3 no eth mac, so use sta mac + 3
        nic.config(mac=mac.to_bytes(6, "big"))
        nic.active(True)
        return nic
