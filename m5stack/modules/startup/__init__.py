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

_WIFI_STATUS_MAP = {
    network.STAT_IDLE: "STAT_IDLE",  # 空闲 / 断开连接后
    network.STAT_CONNECTING: "STAT_CONNECTING",  # 连接中
    network.STAT_GOT_IP: "STAT_GOT_IP",  # 已连接并获取IP
    network.STAT_NO_AP_FOUND: "STAT_NO_AP_FOUND",  # 未找到AP
    network.STAT_NO_AP_FOUND_IN_RSSI_THRESHOLD: "STAT_NO_AP_FOUND_IN_RSSI_THRESHOLD",  # 未找到满足RSSI阈值的AP
    network.STAT_NO_AP_FOUND_IN_AUTHMODE_THRESHOLD: "STAT_NO_AP_FOUND_IN_AUTHMODE_THRESHOLD",  # 未找到满足认证模式阈值的AP
    network.STAT_NO_AP_FOUND_W_COMPATIBLE_SECURITY: "STAT_NO_AP_FOUND_W_COMPATIBLE_SECURITY",  # 未找到兼容安全模式的AP
    network.STAT_WRONG_PASSWORD: "STAT_WRONG_PASSWORD",  # 密码错误
    network.STAT_ASSOC_FAIL: "STAT_ASSOC_FAIL",  # 关联失败
    network.STAT_HANDSHAKE_TIMEOUT: "STAT_HANDSHAKE_TIMEOUT",  # 握手超时
    network.STAT_BEACON_TIMEOUT: "STAT_BEACON_TIMEOUT",  # Beacon 超时
}

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


class Startup:
    STAT_GOT_IP = 1010
    ETH_GOT_IP = 5

    def __init__(self, network_type: str = "WIFI") -> None:
        self.network_type = network_type
        print(f"Startup with network type: {network_type}")
        if network_type == "WIFI":
            try:
                self.network = network.WLAN(network.STA_IF)
                self.network.active(False)
                self.network.active(True)
                print("WiFi initialized")
            except RuntimeError:
                raise RuntimeError(
                    "External WiFi Co-processor not detected, unable to use WiFi features."
                )

    def connect_network(
        self,
        ssid: str = "",
        pswd: str = "",
        lan_if: "network.LAN" = None,
        protocol: str = "DHCP",
        ip: str = "",
        netmask: str = "",
        gateway: str = "",
        dns: str = "",
    ) -> bool:
        if self.network_type == "WIFI" and len(ssid) > 0:
            self.network.connect(ssid, pswd)
            if protocol == "STATIC":
                self.network.ifconfig((ip, netmask, gateway, dns))
            return True
        elif self.network_type == "ETH":
            self.network = lan_if
            self.network.active(True)
            if protocol == "STATIC":
                self.network.ifconfig((ip, netmask, gateway, dns))
            return True
        else:
            return False

    def active(self, is_active: bool) -> None:
        self.network.active(is_active)

    def connect_status(self) -> int:
        return self.network.status()

    def local_ip(self) -> str:
        return self.network.ifconfig()[0]

    def status(self, param: str) -> int:
        return self.network.status(param)

    def get_rssi(self) -> int:
        if hasattr(self.network, "status"):
            return self.network.status("rssi")
        else:
            return 0

    def wifi_status_str(self, status):
        return _WIFI_STATUS_MAP.get(status, f"UNKNOWN({status})")

    def eth_status_str(self, status):
        return _ETH_STATUS_MAP.get(status, f"UNKNOWN({status})")

    def m5things_status_str(self, status):
        return _M5THINGS_STATUS_MAP.get(status, f"UNKNOWN({status})")


_last_access_info = (None, None)


def print_access_info(nick_name, access_code):
    global _last_access_info
    nick_name = "" if nick_name is None else str(nick_name)
    access_code = "" if access_code is None else str(access_code)
    if nick_name == "" and access_code == "":
        return
    info = (nick_name, access_code)
    if info == _last_access_info:
        return
    _last_access_info = info
    print("Nickname: " + nick_name)
    print("Access Code: " + access_code)


def _is_psram():
    sum = 0
    infos = esp32.idf_heap_info(esp32.HEAP_DATA)
    for info in infos:
        sum += info[0]
    return True if sum > 520 * 1024 else False


def _apply_boot_button_override(boot_opt, nvs):
    if boot_opt != BOOT_OPT_MENU_NET:
        M5.update()
        if M5.BtnA.isPressed():
            boot_opt = BOOT_OPT_MENU_NET
            nvs.set_u8("boot_option", boot_opt)
            # FIXME: remove this file is temporary solution
            os.remove("/flash/main.py")
    return boot_opt


def _prepare_board(board_id):
    if board_id == M5.BOARD.M5Tab5:
        M5.Lcd.clear(0xFFFFFF)
    elif board_id != M5.BOARD.M5PaperColor:
        M5.Lcd.clear()
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


def _connect_network_only(board_id, net_mode, ssid, pswd):
    startup = Startup(network_type=net_mode)
    lan_if = None
    if board_id == M5.BOARD.M5Unit_PoEP4:
        from driver.ip101gri import IP101GRI

        lan_if = IP101GRI(mdc_pin=31, mdio_pin=52, power_pin=51)
    elif board_id == M5.BOARD.M5StamPLC:
        from stamplc import PoEStamPLC

        lan_if = PoEStamPLC()
    startup.connect_network(ssid, pswd, lan_if)


def startup(boot_opt, timeout: int = 60) -> None:
    M5.begin()
    # Read saved Wi-Fi information from NVS
    nvs = esp32.NVS("uiflow")
    net_mode = nvs.get_str("net_mode")
    ssid = nvs.get_str("ssid0")
    pswd = nvs.get_str("pswd0")
    protocol = nvs.get_str("protocol")
    ip = nvs.get_str("ip_addr")
    netmask = nvs.get_str("netmask")
    gateway = nvs.get_str("gateway")
    dns = nvs.get_str("dns")
    try:
        tz = nvs.get_str("tz")
        time.timezone(tz)
    except:
        pass

    boot_opt = _apply_boot_button_override(boot_opt, nvs)

    board_id = M5.getBoard()
    _prepare_board(board_id)

    # Do nothing
    if boot_opt is BOOT_OPT_NOTHING:
        pass
    # Show startup menu and connect to network
    elif boot_opt is BOOT_OPT_MENU_NET:
        if board_id in (M5.BOARD.M5AtomS3, M5.BOARD.M5AtomS3R):
            from .atoms3 import AtomS3_Startup

            atoms3 = AtomS3_Startup()
            atoms3.startup(ssid, pswd, timeout=timeout)
        elif board_id in (
            M5.BOARD.M5Atom,
            M5.BOARD.M5AtomU,
            M5.BOARD.M5AtomEcho,
            M5.BOARD.M5AtomMatrix,
            M5.BOARD.M5AtomEchoS3R,
            M5.BOARD.M5AtomS3U,
            M5.BOARD.M5AtomS3Lite,
            M5.BOARD.M5AtomS3R_CAM,
            M5.BOARD.M5StampPico,
            M5.BOARD.M5StampS3Bat,
            M5.BOARD.M5StampS3,
            M5.BOARD.M5StampP4,
            M5.BOARD.M5NanoC6,
            M5.BOARD.M5DualKey,
            M5.BOARD.M5PowerHub,
        ):
            from .headless import Headless_Startup

            headless = Headless_Startup()
            headless.startup(net_mode, ssid, pswd, timeout=timeout)
        elif board_id == M5.BOARD.M5StackCoreS3:
            from .cores3 import CoreS3_Startup

            cores3 = CoreS3_Startup()
            cores3.startup(ssid, pswd, timeout=timeout)
        elif board_id == M5.BOARD.M5StackCore2:
            from .core2 import Core2_Startup

            core2 = Core2_Startup()
            core2.startup(ssid, pswd, timeout=timeout)
        elif board_id == M5.BOARD.M5StickCPlus2:
            from .stickcplus2 import StickCPlus2_Startup

            stickcplus = StickCPlus2_Startup()
            stickcplus.startup(ssid, pswd, timeout=timeout)
        elif board_id == M5.BOARD.M5StickCPlus:
            from .stickcplus import StickCPlus_Startup

            stickcplus2 = StickCPlus_Startup()
            stickcplus2.startup(ssid, pswd, timeout=timeout)
        elif board_id == M5.BOARD.M5Stack:
            if _is_psram():
                from .fire import Fire_Startup

                fire = Fire_Startup()
                fire.startup(ssid, pswd, timeout=timeout)
            else:
                from .basic import Basic_Startup

                basic = Basic_Startup()
                basic.startup(ssid, pswd, timeout=timeout)
        elif board_id == M5.BOARD.M5Capsule:
            from .capsule import Capsule_Startup

            capsule = Capsule_Startup()
            capsule.startup(net_mode, ssid, pswd, timeout=timeout)
        elif board_id == M5.BOARD.M5Dial:
            from .dial import Dial_Startup

            dial = Dial_Startup()
            dial.startup(ssid, pswd, timeout=timeout)

        elif board_id == M5.BOARD.M5StackCoreInk:
            from .coreink import CoreInk_Startup

            coreink = CoreInk_Startup()
            coreink.startup(ssid, pswd, timeout=timeout)
        elif board_id == M5.BOARD.M5AirQ:
            from .airq import AirQ_Startup

            airq = AirQ_Startup()
            airq.startup(ssid, pswd, timeout=timeout)
        elif board_id == M5.BOARD.M5Cardputer:
            from .cardputer import Cardputer_Startup

            cardputer = Cardputer_Startup()
            cardputer.startup(ssid, pswd, timeout=timeout)
        elif board_id == M5.BOARD.M5CardputerADV:
            from .cardputeradv import CardputerADV_Startup

            cardputeradv = CardputerADV_Startup()
            cardputeradv.startup(ssid, pswd, timeout=timeout)
        elif board_id == M5.BOARD.M5Paper:
            from .paper import Paper_Startup

            paper = Paper_Startup()
            paper.startup(ssid, pswd, timeout=timeout)
        elif board_id == M5.BOARD.M5DinMeter:
            from .dinmeter import DinMeter_Startup

            dinmeter = DinMeter_Startup()
            dinmeter.startup(ssid, pswd, timeout=timeout)
        elif board_id == M5.BOARD.M5StickC:
            from .stickc import StickC_Startup

            stickc = StickC_Startup()
            stickc.startup(ssid, pswd, timeout=timeout)

        elif board_id == M5.BOARD.M5Station:
            from .station import Station_Startup

            station = Station_Startup()
            station.startup(ssid, pswd, timeout=timeout)

        elif board_id == M5.BOARD.M5Tough:
            from .tough import Tough_Startup

            tough = Tough_Startup()
            tough.startup(ssid, pswd, timeout=timeout)

        elif board_id == M5.BOARD.M5PaperS3:
            from .papers3 import PaperS3_Startup

            papers3 = PaperS3_Startup()
            papers3.startup(ssid, pswd, timeout=timeout)

        elif board_id == M5.BOARD.M5StamPLC:
            from .stamplc import StampPLC_Startup

            plc = StampPLC_Startup()
            plc.startup(net_mode, ssid, pswd, protocol, ip, netmask, gateway, dns, timeout)

        elif board_id == M5.BOARD.M5Tab5:
            from .tab5 import Tab5_Startup

            tab5 = Tab5_Startup()
            tab5.startup(ssid, pswd, timeout=timeout)

        elif board_id == M5.BOARD.M5UnitC6L:
            from .unit_c6l import UnitC6L_Startup

            unit_c6l = UnitC6L_Startup()
            unit_c6l.startup(ssid, pswd, timeout=timeout)
        elif board_id == M5.BOARD.ArduinoNessoN1:
            from .nesson1 import NessoN1_Startup

            nesson1 = NessoN1_Startup()
            nesson1.startup(ssid, pswd, timeout=timeout)
        elif board_id == M5.BOARD.M5StickS3:
            from .sticks3 import StickS3_Startup

            sticks3 = StickS3_Startup()
            sticks3.startup(ssid, pswd, timeout=timeout)
        elif board_id == M5.BOARD.M5StopWatch:
            from .stopwatch import StopWatch_Startup

            stopwatch = StopWatch_Startup()
            stopwatch.startup(ssid, pswd, timeout=timeout)
        elif board_id == M5.BOARD.M5Unit_PoEP4:
            from .unit_poep4 import Unit_PoEP4_Startup

            unit_poep4 = Unit_PoEP4_Startup()
            unit_poep4.startup(net_mode, ssid, pswd, protocol, ip, netmask, gateway, dns, timeout)
        elif board_id == M5.BOARD.M5StackChan:
            from .stackchan import StackChan_Startup

            stackchan = StackChan_Startup()
            stackchan.startup(ssid, pswd, timeout=timeout)
        elif board_id == M5.BOARD.M5PaperColor:
            from .papercolor import PaperColor_Startup

            papercolor = PaperColor_Startup()
            papercolor.startup(ssid, pswd, timeout=timeout)

    # Only connect to network, not show any menu
    elif boot_opt is BOOT_OPT_NETWORK:
        _connect_network_only(board_id, net_mode, ssid, pswd)
    else:
        print("Boot options not processed.")
