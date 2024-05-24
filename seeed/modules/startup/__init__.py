# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# startup script
import os
import M5
import esp32
import network
import time

BOOT_OPT_NOTHING = 0  # Run main.py(after download code to device set to this)
BOOT_OPT_MENU_NET = 1  # Startup menu + Network setup
BOOT_OPT_NETWORK = 2  # Only Network setup


class Startup:
    def __init__(self) -> None:
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(False)
        self.wlan.active(True)

    def connect_network(self, ssid: str, pswd: str) -> bool:
        if len(ssid) > 0:
            self.wlan.connect(ssid, pswd)
            return True
        else:
            return False

    def connect_status(self) -> int:
        return self.wlan.status()

    def local_ip(self) -> str:
        return self.wlan.ifconfig()[0]

    def get_rssi(self) -> int:
        return self.wlan.status("rssi")


def startup(boot_opt, timeout: int = 60) -> None:
    M5.begin()
    # Read saved Wi-Fi information from NVS
    nvs = esp32.NVS("uiflow")
    ssid = nvs.get_str("ssid0")
    pswd = nvs.get_str("pswd0")
    try:
        tz = nvs.get_str("tz")
        time.timezone(tz)
    except:
        pass

    board_id = M5.getBoard()

    # Do nothing
    if boot_opt is BOOT_OPT_NOTHING:
        pass
    # Show startup menu and connect to network
    elif boot_opt is BOOT_OPT_MENU_NET:
        if board_id == M5.BOARD.SEEED_XIAO_ESP32S3:
            from .xiaos3 import XIAOS3_Startup

            xiaos3 = XIAOS3_Startup()
            xiaos3.startup(ssid, pswd, timeout)

    # Only connect to network, not show any menu
    elif boot_opt is BOOT_OPT_NETWORK:
        startup = Startup()
        startup.connect_network(ssid, pswd)
    else:
        print("Boot options not processed.")
