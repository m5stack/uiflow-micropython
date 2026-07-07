# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# Unit_PoEP4 startup script
import M5
import time
import network
import machine
import binascii
import M5Things
from . import Startup


_ETH_STATUS_MAP = {
    network.ETH_STARTED: "ETH_STARTED",
    network.ETH_CONNECTED: "ETH_CONNECTED",
    network.ETH_DISCONNECTED: "ETH_DISCONNECTED",
    network.ETH_STOPPED: "ETH_STOPPED",
    network.ETH_GOT_IP: "ETH_GOT_IP",
}

_M5THINGS_STATUS_MAP = {
    -2: "SNTP_ERR",
    -1: "CONNECT_ERR",
    0: "STANDBY",
    1: "CONNECTING",
    2: "CONNECTED",
    3: "DISCONNECT",
}


# Unit PoEP4 startup menu
class Unit_PoEP4_Startup:
    def __init__(self) -> None:
        pass

    def show_mac(self) -> None:
        mac = binascii.hexlify(machine.unique_id()).decode("utf-8").upper()
        print("MAC: " + mac[0:6] + "_" + mac[6:])

    def startup(
        self,
        net_mode: str = "WIFI",
        ssid: str = "",
        pswd: str = "",
        protocol: str = "",
        ip: str = "",
        netmask: str = "",
        gateway: str = "",
        dns: str = "",
        timeout: int = 60,
    ) -> None:
        self.show_mac()

        if net_mode == "WIFI":
            self._unit_poep4_rgb_show("red")
            raise NotImplementedError("WIFI not supported on M5Unit-PoEP4")

        self._net_if = Startup(network_type=net_mode)  # type: ignore

        from driver.ip101gri import IP101GRI

        lan_if = IP101GRI(mdc_pin=31, mdio_pin=52, power_pin=51)
        if self._net_if.connect_network(
            ssid=ssid,
            pswd=pswd,
            lan_if=lan_if,
            protocol=protocol,
            ip=ip,
            netmask=netmask,
            gateway=gateway,
            dns=dns,
        ):
            success = False
            self._unit_poep4_rgb_show("yellow")
            for _ in range(10):
                time.sleep(1)
                eth_status = self._net_if.connect_status()
                if eth_status is network.ETH_GOT_IP:
                    access_code = M5Things.accesscode()
                    if access_code != "":
                        print("Local IP: " + self._net_if.local_ip())
                        print("=======================")
                        print("Nickname: " + M5Things.nick_name())
                        print("Access Code: " + access_code)
                        print("=======================")
                        self._unit_poep4_rgb_show("green")
                        success = True
                        break
            if not success:
                print(
                    f"[NET] ETH: {self.eth_status_str(eth_status)} | "
                    f"MQTT: {self.m5things_status_str(M5Things.status())}"
                )
        else:
            self._unit_poep4_rgb_show("blue")
            print("Not Found", "Please use M5Burner setup :)")

    def _unit_poep4_rgb_show(self, color: str):
        if not hasattr(self, "_poep4_led"):
            self._poep4_led = {
                "r": machine.Pin(17, machine.Pin.OUT, value=1),
                "g": machine.Pin(15, machine.Pin.OUT, value=1),
                "b": machine.Pin(16, machine.Pin.OUT, value=1),
            }

        _color_table = {
            "black": (1, 1, 1),
            "red": (0, 1, 1),
            "green": (1, 0, 1),
            "blue": (1, 1, 0),
            "yellow": (0, 0, 1),
        }

        color = color.lower()
        if color not in _color_table:
            raise ValueError("Unsupported color: " + color)

        r, g, b = _color_table[color]
        self._poep4_led["r"].value(r)
        self._poep4_led["g"].value(g)
        self._poep4_led["b"].value(b)

    def eth_status_str(self, status):
        return _ETH_STATUS_MAP.get(status, f"UNKNOWN({status})")

    def m5things_status_str(self, status):
        return _M5THINGS_STATUS_MAP.get(status, f"UNKNOWN({status})")
