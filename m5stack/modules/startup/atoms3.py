# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
# AtomS3 startup script
import M5
import time
import network
import machine
import binascii
from . import Startup, print_access_info

try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False

# AtomS3 startup menu


class AtomS3_Startup(Startup):
    _BLACK = 0x000000
    _TEXT = 0x0F2B3A
    _ROW_LABEL_BG = 0x99CCCC
    _ROW_VALUE_BG = 0xCBDFE0
    _TITLE_WIFI = 0x336699
    _TITLE_SERVER = 0x006633
    _TITLE_TEXT = 0xFFFFFF
    _SCREEN_W = 128
    _ROW_LABEL_H = 16
    _PAGE_DEVELOP = 0
    _PAGE_WIFI = 1

    def __init__(self) -> None:
        super().__init__()
        self._page = self._PAGE_DEVELOP
        self._ssid = ""
        self._ip = ""
        self._mac = self._get_mac()
        self._access_code = ""
        self._nick_name = ""
        self._wifi_ok = False
        self._server_ok = False
        self._res_dir = self._get_res_dir()
        self._bg_img = self._res_dir + "/atom_bg.png"
        self._ng_img = self._res_dir + "/atom_ng.png"
        self._wifi_ok_img = self._res_dir + "/atom_wifi_ok.png"
        self._server_ok_img = self._res_dir + "/atom_server_ok.png"

    def show_ssid(self, ssid: str) -> None:
        self._ssid = ssid or ""
        self._render_current_page()

    def show_mac(self) -> None:
        self._mac = self._get_mac()
        self._render_current_page()

    def show_error(self, ssid: str, error: str) -> None:
        self._ssid = ssid or ""
        self._access_code = error or ""
        self._nick_name = ""
        self._wifi_ok = False
        self._server_ok = False
        self._render_current_page()
        print("SSID: " + ssid + "\r\nNotice: " + error)

    def show_nick_name(self, nick_name: str) -> None:
        self._nick_name = nick_name or ""
        self._render_current_page()

    def show_access_code(self, access_code: str) -> None:
        self._access_code = access_code or ""
        self._render_current_page()

    def show_status(self, is_online: bool) -> None:
        self._server_ok = is_online
        self._render_status()

    def show_layout(self, ssid: str) -> None:
        self._ssid = ssid or ""
        self._ip = ""
        self._mac = self._get_mac()
        self._access_code = ""
        self._nick_name = ""
        self._wifi_ok = False
        self._server_ok = False
        self._page = self._PAGE_DEVELOP
        self._render_current_page()

    def startup(
        self,
        ssid: str,
        pswd: str,
        protocol: str = "",
        ip: str = "",
        netmask: str = "",
        gateway: str = "",
        dns: str = "",
        timeout: int = 60,
    ) -> None:
        self.show_layout(ssid)

        if super().connect_network(
            ssid=ssid,
            pswd=pswd,
            protocol=protocol,
            ip=ip,
            netmask=netmask,
            gateway=gateway,
            dns=dns,
        ):
            count = 1
            status = super().connect_status()
            start = time.ticks_ms()
            while status is not network.STAT_GOT_IP:
                self._update_button()
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
                    self.show_access_code("." * count)
                    count = count + 1
                    if count > 5:
                        count = 1
                status = super().connect_status()
                # connect to network timeout
                if time.ticks_diff(time.ticks_ms(), start) > timeout * 1000:
                    self.show_error(ssid, "TIMEOUT")
                    break

            if status is network.STAT_GOT_IP:
                self._ip = super().local_ip()
                self._wifi_ok = True
                self._render_current_page()
                self._wait_server(ssid, start, timeout)
            else:
                self._run_idle()
        else:
            print("WiFi setup not found")
            self._run_idle()

    def _wait_server(self, ssid: str, start: int, timeout: int) -> None:
        count = 1
        while time.ticks_diff(time.ticks_ms(), start) <= timeout * 1000:
            self._update_button()
            access_code = self._get_access_code()
            if self._is_server_online() and access_code != "":
                self._access_code = access_code
                self._nick_name = self._get_nick_name()
                self._server_ok = True
                self._print_access_info()
                self._render_current_page()
                self._run_connected()
                return

            self.show_access_code("." * count)
            count = count + 1
            if count > 5:
                count = 1
            time.sleep_ms(1000)

        self.show_error(ssid, "TIMEOUT")
        if _HAS_SERVER:
            try:
                print("[MQTT]: " + self.m5things_status_str(M5Things.status()))
            except Exception:
                print("[MQTT]: UNKNOWN")
        else:
            print("[MQTT]: M5Things unavailable")

    def _run_idle(self) -> None:
        while True:
            self._update_button()
            time.sleep_ms(100)

    def _run_connected(self) -> None:
        last_update = time.ticks_ms()
        while True:
            self._update_button()
            if time.ticks_diff(time.ticks_ms(), last_update) >= 1500:
                access_code = self._get_access_code()
                nick_name = self._get_nick_name()
                server_ok = self._is_server_online()
                if (
                    access_code != self._access_code
                    or nick_name != self._nick_name
                    or server_ok != self._server_ok
                ):
                    self._access_code = access_code
                    self._nick_name = nick_name
                    self._server_ok = server_ok
                    self._print_access_info()
                    self._render_current_page()
                last_update = time.ticks_ms()
            time.sleep_ms(100)

    def _render_current_page(self) -> None:
        M5.Lcd.drawImage(self._bg_img, 0, 0)
        self._render_title()
        self._render_status()
        if self._page == self._PAGE_DEVELOP:
            self._draw_row("Access Code:", self._access_code, 39, 14)
            self._draw_row("Nickname:", self._nick_name, 77, 13)
        else:
            self._draw_row("IP Address:", self._ip, 39, 15)
            self._draw_row("MAC Address:", self._mac, 77, 17)

    def _render_title(self) -> None:
        self._draw_title_text(self._short_text(self._ssid, 11), 24, 0, 0, self._TITLE_WIFI)
        self._draw_title_text("UIFlow2", 24, 20, 22, self._TITLE_SERVER)

    def _render_status(self) -> None:
        M5.Lcd.drawImage(self._wifi_ok_img if self._wifi_ok else self._ng_img, 96, 0)
        M5.Lcd.drawImage(self._server_ok_img if self._server_ok else self._ng_img, 96, 20)

    def _draw_title_text(self, text: str, x: int, bg_y: int, text_y: int, bg: int) -> None:
        M5.Lcd.fillRect(x, bg_y, 78, 16, bg)
        self._set_text_color(self._TITLE_TEXT, bg)
        M5.Lcd.setFont(M5.Lcd.FONTS.Montserrat12)
        M5.Lcd.drawString(text, x, text_y)

    def _draw_row(self, label: str, value: str, y: int, max_len: int) -> None:
        M5.Lcd.fillRect(0, y + 1, self._SCREEN_W, self._ROW_LABEL_H, self._ROW_LABEL_BG)
        self._set_text_color(self._TEXT, self._ROW_LABEL_BG)
        M5.Lcd.setFont(M5.Lcd.FONTS.Montserrat12)
        M5.Lcd.drawString(label, 3, y + 1)
        self._set_text_color(self._TEXT, self._ROW_VALUE_BG)
        M5.Lcd.setFont(M5.Lcd.FONTS.Montserrat14)
        M5.Lcd.drawString(self._short_text(value, max_len), 3, y + 18)

    def _update_button(self) -> None:
        M5.update()
        if M5.BtnA.wasClicked():
            self._page = (
                self._PAGE_WIFI if self._page == self._PAGE_DEVELOP else self._PAGE_DEVELOP
            )
            self._render_current_page()

    def _print_access_info(self) -> None:
        print_access_info(self._nick_name, self._access_code)

    @staticmethod
    def _get_res_dir() -> str:
        try:
            if M5.getBoard() == M5.BOARD.M5AtomS3R:
                return "/system/atoms3r"
        except Exception:
            pass
        return "/system/atoms3"

    @staticmethod
    def _get_mac() -> str:
        text = binascii.hexlify(machine.unique_id()).decode("utf-8").upper()
        return ":".join(text[i : i + 2] for i in range(0, len(text), 2))

    @staticmethod
    def _get_nick_name() -> str:
        if _HAS_SERVER:
            try:
                return M5Things.nick_name() or ""
            except Exception:
                pass
        return ""

    @staticmethod
    def _get_access_code() -> str:
        if _HAS_SERVER:
            try:
                return M5Things.accesscode() or ""
            except Exception:
                pass
        return ""

    @staticmethod
    def _is_server_online() -> bool:
        if _HAS_SERVER:
            try:
                return M5Things.status() == 2
            except Exception:
                pass
        return False

    @staticmethod
    def _short_text(text: str, max_len: int) -> str:
        if text is None:
            return ""
        text = str(text)
        return text if len(text) <= max_len else text[: max_len - 3] + "..."

    @staticmethod
    def _set_text_color(fg: int, bg: int) -> None:
        try:
            M5.Lcd.setTextColor(fg, bg)
        except TypeError:
            M5.Lcd.setTextColor(fg)
