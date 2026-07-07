# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# StampS3 startup script
import M5
import time
import network
import machine
import binascii
import M5Things
from startup import Startup
from hardware import RGB


class NullRGB:
    def fill_color(self, color: int) -> None:
        pass

    def set_color(self, index: int, color: int) -> None:
        pass

    def set_brightness(self, brightness: int) -> None:
        pass


# Headless startup menu
class Headless_Startup:
    COLOR_RED = 0xFF0000  # WiFi not connected
    COLOR_BLUE = 0x0000FF  # WiFi connected, server not connected
    COLOR_GREEN = 0x00FF00  # WiFi connected, server connected
    COLOR_WHITE = 0xFFFFFF

    def __init__(self) -> None:
        self._board = M5.getBoard()
        has_rgb = self._board not in [M5.BOARD.M5AtomS3R_CAM, M5.BOARD.M5AtomEchoS3R]
        self.rgb = RGB() if has_rgb else NullRGB()
        if self._board is not M5.BOARD.M5PowerHub:
            self.rgb.set_brightness(50)
            self.rgb.fill_color(self.COLOR_BLUE)
        else:
            self.rgb.set_brightness(30)
            self.rgb.fill_color(self.COLOR_WHITE)
            self.rgb.set_color(5, self.COLOR_BLUE)

    def _set_status_color(self, color: int) -> None:
        if self._board is not M5.BOARD.M5PowerHub:
            self.rgb.set_brightness(100)
            self.rgb.fill_color(color)
        else:
            self.rgb.set_color(5, color)

    def show_hits(self, hits: str) -> None:
        pass

    def show_msg(self, msg: str) -> None:
        pass

    def show_ssid(self, ssid: str) -> None:
        pass

    def show_mac(self) -> None:
        mac = binascii.hexlify(machine.unique_id()).decode("utf-8").upper()
        print("MAC: " + mac[0:6] + "_" + mac[6:])

    def show_error(self, ssid: str, error: str) -> None:
        print("SSID: " + ssid + "\r\nNotice: " + error)

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
                        print(" ")
                        print("Local IP: " + self._net_if.local_ip())
                        print("=======================")
                        print("Nickname: " + M5Things.nick_name())
                        print("Access Code: " + access_code)
                        print("=======================")
                        self._set_status_color(self.COLOR_GREEN)
                        success = True
                        break
                    else:
                        print(".", end="")
                else:
                    print(".", end="")
                time.sleep(1)

            if not success:
                print(" ")
                self._set_status_color(self.COLOR_RED)
                self.show_error(ssid, "TIMEOUT")
                print(
                    f"[NET]: {self._net_if.wifi_status_str(status)} | "
                    f"[MQTT]: {self._net_if.m5things_status_str(M5Things.status())}"
                )
        else:
            self._set_status_color(self.COLOR_BLUE)
            self.show_error("Not Found", "Please use M5Burner setup :)")
