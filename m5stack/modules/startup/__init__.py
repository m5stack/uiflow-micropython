# -*- encoding: utf-8 -*-
# startup script
import M5
import time
import esp32
import network

BOOT_OPT_NOTHING = 0
BOOT_OPT_MENU_NET = 1
BOOT_OPT_NETWORK = 2


class Startup:

    def __init__(self) -> None:
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(False)
        self.wlan.active(True)

    def connect_network(self, ssid, pswd) -> bool:
        if (len(ssid) > 0) or (len(pswd) > 0):
            self.wlan.connect(ssid, pswd)
            return True
        else:
            return False

    def connect_status(self) -> int:
        return self.wlan.status()

    def local_ip(self) -> str:
        return self.wlan.ifconfig()[0]

def startup(boot_opt):
    # Read saved Wi-Fi information from NVS
    nvs = esp32.NVS("uiflow")
    ssid = nvs.get_str("ssid0")
    pswd = nvs.get_str("pswd0")

    # Do nothing
    if boot_opt is BOOT_OPT_NOTHING:
        pass
    # Show startup menu and connect to network
    elif boot_opt is BOOT_OPT_MENU_NET:
        if M5.BOARD.M5AtomS3 == M5.getBoard():
            from .atoms3 import AtomS3_Startup
            atoms3 = AtomS3_Startup()
            atoms3.startup(ssid, pswd)
        if M5.BOARD.unknown == M5.getBoard():
            print("Unknow Board Type")
    # Only connect to network, not show any menu
    elif boot_opt is BOOT_OPT_NETWORK:
        startup = Startup()
        startup.connect_network(ssid, pswd)
    else:
        print("Boot options not processed.")
