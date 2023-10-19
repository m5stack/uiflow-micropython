# -*- encoding: utf-8 -*-
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


def _is_psram():
    sum = 0
    infos = esp32.idf_heap_info(esp32.HEAP_DATA)
    for info in infos:
        sum += info[0]
    return True if sum > 520 * 1024 else False


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

    if boot_opt != BOOT_OPT_MENU_NET:
        M5.update()
        if M5.BtnA.isPressed():
            boot_opt = BOOT_OPT_MENU_NET
            nvs.set_u8("boot_option", boot_opt)
            # FIXME: remove this file is temporary solution
            os.remove("/flash/main.py")

    board_id = M5.getBoard()
    # Special operations for some devices
    if board_id == M5.BOARD.M5StickCPlus2:
        from machine import Pin

        pin4 = Pin(4, Pin.OUT)
        pin4.value(1)
    if board_id == M5.BOARD.M5Dial:
        from machine import Pin

        pin4 = Pin(46, Pin.OUT)
        pin4.value(1)

    if board_id in (
        M5.BOARD.M5AtomS3U,
        M5.BOARD.M5AtomS3Lite,
        M5.BOARD.M5StampS3,
        M5.BOARD.M5Capsule,
    ):
        # M5AtomS3U may fail to enter the AUTODETECT process, which will cause
        # m5things to fail to obtain the board id.
        nvs = esp32.NVS("M5GFX")
        nvs.set_u32("AUTODETECT", board_id)
        nvs.commit()

    # Do nothing
    if boot_opt is BOOT_OPT_NOTHING:
        pass
    # Show startup menu and connect to network
    elif boot_opt is BOOT_OPT_MENU_NET:
        if board_id == M5.BOARD.M5AtomS3:
            from .atoms3 import AtomS3_Startup

            atoms3 = AtomS3_Startup()
            atoms3.startup(ssid, pswd, timeout)
        elif board_id == M5.BOARD.M5AtomS3Lite:
            from .atoms3lite import AtomS3Lite_Startup

            atoms3 = AtomS3Lite_Startup()
            atoms3.startup(ssid, pswd, timeout)
        elif board_id == M5.BOARD.M5StampS3:
            from .stamps3 import StampS3_Startup

            stamps3 = StampS3_Startup()
            stamps3.startup(ssid, pswd, timeout)
        elif board_id == M5.BOARD.M5StackCoreS3:
            from .cores3 import CoreS3_Startup

            cores3 = CoreS3_Startup()
            cores3.startup(ssid, pswd, timeout)
        elif board_id in (M5.BOARD.M5StackCore2, M5.BOARD.M5Tough):
            from .core2 import Core2_Startup

            core2 = Core2_Startup()
            core2.startup(ssid, pswd, timeout)
        elif board_id == M5.BOARD.M5AtomS3U:
            from .atoms3u import AtomS3U_Startup

            atoms3u = AtomS3U_Startup()
            atoms3u.startup(ssid, pswd, timeout)
        elif board_id == M5.BOARD.M5StickCPlus2:
            from .stickcplus import StickCPlus_Startup

            stickcplus = StickCPlus_Startup()
            stickcplus.startup(ssid, pswd, timeout)
        elif board_id == M5.BOARD.M5StickCPlus:
            from .stickcplus import StickCPlus_Startup

            stickcplus2 = StickCPlus_Startup()
            stickcplus2.startup(ssid, pswd, timeout)
        elif board_id == M5.BOARD.M5Stack:
            if _is_psram():
                from .fire import Fire_Startup

                fire = Fire_Startup()
                fire.startup(ssid, pswd, timeout)
            else:
                from .basic import Basic_Startup

                basic = Basic_Startup()
                basic.startup(ssid, pswd, timeout)
        elif board_id == M5.BOARD.M5Capsule:
            from .capsule import Capsule_Startup

            capsule = Capsule_Startup()
            capsule.startup(ssid, pswd, timeout)
        elif board_id == M5.BOARD.M5Dial:
            from .dial import Dial_Startup

            dial = Dial_Startup()
            dial.startup(ssid, pswd, timeout)

    # Only connect to network, not show any menu
    elif boot_opt is BOOT_OPT_NETWORK:
        startup = Startup()
        startup.connect_network(ssid, pswd)
    else:
        print("Boot options not processed.")
