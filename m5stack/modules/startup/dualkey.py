# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
# DualKey startup script
import M5
import time
import network
import machine
import binascii
from . import Startup
from hardware import RGB


# DualKey startup menu
class DualKey_Startup(Startup):
    COLOR_GREEN = 0x00FF00  # WiFi connected
    COLOR_BLUE = 0x0000FF  # Power on / WiFi connecting
    COLOR_RED = 0xFF0000  # WiFi connection failed

    def __init__(self) -> None:
        super().__init__()
        self.rgb = RGB()
        self.rgb.set_color(0, self.COLOR_BLUE)
        self.rgb.set_color(1, self.COLOR_BLUE)
        self.rgb.set_brightness(80)

    def show_hits(self, hits: str) -> None:
        print(hits)

    def show_msg(self, msg: str) -> None:
        print(msg)

    def show_ssid(self, ssid: str) -> None:
        if len(ssid) > 9:
            self.show_msg(ssid[:7] + "...")
        else:
            self.show_msg(ssid)

    def show_mac(self) -> None:
        mac = binascii.hexlify(machine.unique_id()).decode("utf-8").upper()
        print(mac[0:6] + "_" + mac[6:])

    def show_error(self, ssid: str, error: str) -> None:
        self.show_ssid(ssid)
        self.show_hits(error)
        self.show_mac()
        print("SSID: " + ssid + "\r\nNotice: " + error)

    def startup(self, ssid: str, pswd: str, timeout: int = 60) -> None:
        self.show_mac()

        if super().connect_network(ssid=ssid, pswd=pswd):
            self.show_ssid(ssid)
            count = 1
            status = super().connect_status()
            start = time.time()
            # 连接过程中保持蓝色
            self.rgb.set_color(0, self.COLOR_BLUE)
            self.rgb.set_color(1, self.COLOR_BLUE)
            self.rgb.set_brightness(80)

            while status is not network.STAT_GOT_IP:
                time.sleep_ms(300)

                if status is network.STAT_NO_AP_FOUND:
                    self.show_error(ssid, "NO AP FOUND")
                    break
                elif status is network.STAT_WRONG_PASSWORD:
                    self.show_error(ssid, "WRONG PASSWORD")
                    break
                elif status is network.STAT_HANDSHAKE_TIMEOUT:
                    self.show_error(ssid, "HANDSHAKE ERR")
                    break
                elif status is network.STAT_CONNECTING:
                    self.show_hits("." * count)
                    count = count + 1
                    if count > 5:
                        count = 1
                status = super().connect_status()
                # connect to network timeout
                if (time.time() - start) > timeout:
                    self.show_error(ssid, "TIMEOUT")
                    break

            if status is network.STAT_GOT_IP:
                # 连接成功，显示绿色
                self.rgb.set_color(0, self.COLOR_GREEN)
                self.rgb.set_color(1, self.COLOR_GREEN)
                self.rgb.set_brightness(80)
                self.show_hits(super().local_ip())
                print("Local IP: " + super().local_ip())
            else:
                # 连接失败，显示红色
                self.rgb.set_color(0, self.COLOR_RED)
                self.rgb.set_color(1, self.COLOR_RED)
                self.rgb.set_brightness(80)
        else:
            # 无法连接网络，显示红色
            self.rgb.set_color(0, self.COLOR_RED)
            self.rgb.set_color(1, self.COLOR_RED)
            self.rgb.set_brightness(80)
            self.show_error("Not Found", "Use Burner setup")
