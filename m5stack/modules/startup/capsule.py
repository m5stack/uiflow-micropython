# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from startup.headless import Headless_Startup
import network
import time
import M5
import M5Things
from startup import Startup


class Capsule_Startup(Headless_Startup):
    def __init__(self) -> None:
        super().__init__()

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
        M5.Speaker.setVolumePercentage(1.0)

        self._net_if = Startup(network_type=net_mode)  # type: ignore
        if self._net_if.connect_network(
            ssid=ssid,
            pswd=pswd,
            protocol=protocol,
            ip=ip,
            netmask=netmask,
            gateway=gateway,
            dns=dns,
        ):
            print("Connecting to " + ssid + " ", end="")
            start = time.ticks_ms()
            success = False
            while time.ticks_diff(time.ticks_ms(), start) < timeout * 1000:
                status = self._net_if.connect_status()
                if status is network.STAT_GOT_IP:
                    access_code = M5Things.accesscode()
                    if access_code != "":
                        M5.Speaker.tone(4500, 50)
                        time.sleep(0.1)
                        M5.Speaker.tone(4500, 50)
                        print(" ")
                        print("Local IP: " + self._net_if.local_ip())
                        print("=======================")
                        print("Nickname: " + M5Things.nick_name())
                        print("Access Code: " + access_code)
                        print("=======================")
                        self.rgb.fill_color(self.COLOR_GREEN)
                        success = True
                        break
                    else:
                        print(".", end="")
                else:
                    print(".", end="")
                time.sleep(1)

            if not success:
                M5.Speaker.tone(5000, 50)
                print(" ")
                self.show_error(ssid, "TIMEOUT")
                print(
                    f"[NET]: {self._net_if.wifi_status_str(status)} | "
                    f"[MQTT]: {self._net_if.m5things_status_str(M5Things.status())}"
                )
        else:
            self.rgb.fill_color(self.COLOR_RED)
            self.show_error("Not Found", "Please use M5Burner setup :)")
            print("Connecting to " + ssid + " ", end="")
