# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
# UnitC6L startup script
import M5
from M5 import Widgets
import time
import network
import machine
import binascii
import asyncio
import esp32
from . import Startup

try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False


_TEXT_FONT = Widgets.FONTS.Montserrat12


def _set_text_style(fg_color, bg_color):
    M5.Lcd.setFont(_TEXT_FONT)
    M5.Lcd.setTextColor(fg_color, bg_color)


def _measure_text(text):
    if not text:
        return 0
    M5.Lcd.setFont(_TEXT_FONT)
    return M5.Lcd.textWidth(text)


def _font_height():
    M5.Lcd.setFont(_TEXT_FONT)
    return M5.Lcd.fontHeight()


def _draw_textbox(x, y, w, h, r, text, invert=False, is_title=False):
    text = "" if text is None else str(text)
    max_chars = 8
    if len(text) > max_chars:
        if is_title:
            text = text[:3] + "..." + text[-3:]
        else:
            text = text[:3] + ".." + text[-3:]
    text_w = _measure_text(text)
    cursor_x = x + (w - text_w) // 2
    cursor_y = y + (h - _font_height()) // 2
    if invert:
        M5.Lcd.fillRoundRect(x, y, w, h, r, M5.Lcd.COLOR.WHITE)
        fg_color = M5.Lcd.COLOR.BLACK
        bg_color = M5.Lcd.COLOR.WHITE
    else:
        M5.Lcd.fillRoundRect(x, y, w, h, r, M5.Lcd.COLOR.BLACK)
        M5.Lcd.drawRoundRect(x, y, w, h, r, M5.Lcd.COLOR.WHITE)
        fg_color = M5.Lcd.COLOR.WHITE
        bg_color = M5.Lcd.COLOR.BLACK
    _set_text_style(fg_color, bg_color)
    M5.Lcd.drawString(text, cursor_x, cursor_y)


def title_set_text(text, invert=False):
    _draw_textbox(0, -3, 64, 18, 4, text, invert, is_title=True)


def label1_set_text(text, invert=False):
    _draw_textbox(3, 16, 58, 15, 4, text, invert, is_title=False)


def label2_set_text(text, invert=False):
    _draw_textbox(3, 32, 58, 15, 4, text, invert, is_title=False)


def _short_row_text(text):
    text = "" if text is None else str(text)
    if len(text) > 10:
        text = text[:4] + ".." + text[-4:]
    return text


def _draw_plain_row(text, y, h):
    text = _short_row_text(text)
    text_w = _measure_text(text)
    x = (64 - text_w) // 2
    text_y = y + (h - _font_height()) // 2
    _set_text_style(M5.Lcd.COLOR.WHITE, M5.Lcd.COLOR.BLACK)
    M5.Lcd.drawString(text, x, text_y)


def _draw_inverted_header(rows):
    box_x = 8
    box_y = -1
    box_w = 48
    box_h = 28
    radius = 8
    M5.Lcd.fillRect(box_x, box_y, box_w, box_h - radius, M5.Lcd.COLOR.WHITE)
    M5.Lcd.fillRoundRect(
        box_x, box_y + box_h - radius * 2, box_w, radius * 2, radius, M5.Lcd.COLOR.WHITE
    )
    for index, row in enumerate(rows[:2]):
        text = _short_row_text(row)
        text_w = _measure_text(text)
        x = box_x + (box_w - text_w) // 2
        text_y = box_y + 3 + index * 14 - (2 if index == 1 else 0)
        _set_text_style(M5.Lcd.COLOR.BLACK, M5.Lcd.COLOR.WHITE)
        M5.Lcd.drawString(text, x, text_y)


def _draw_split_rows(rows, inverted_header=False):
    M5.Lcd.fillRect(0, 0, 64, 48, M5.Lcd.COLOR.BLACK)
    count = len(rows)
    if count <= 0:
        return
    if inverted_header and count >= 2:
        _draw_inverted_header(rows)
        rest = rows[2:]
        rest_count = len(rest)
        if rest_count <= 0:
            return
        rest_y = 30
        row_h = (48 - rest_y) // rest_count
        for index, row in enumerate(rest):
            y = rest_y + index * row_h
            h = 48 - y if index == rest_count - 1 else row_h
            _draw_plain_row(row, y, h)
        return
    row_h = 48 // count
    for index, row in enumerate(rows):
        y = index * row_h
        h = 48 - y if index == count - 1 else row_h
        _draw_plain_row(row, y, h)


class InfoPages:
    PAGE_ACCESS = 0
    PAGE_NICKNAME = 1
    PAGE_WIFI = 2
    PAGE_MAC = 3
    PAGE_COUNT = 4

    def __init__(self, wifi, ssid) -> None:
        self._wifi = wifi
        self._ssid = ssid or ""
        self._page = self.PAGE_ACCESS
        self._last_payload = None
        self._last_refresh_ms = 0

    def draw_start_page(self):
        self._page = self.PAGE_ACCESS
        self._draw_current_page(force=True)

    async def start(self):
        self._draw_current_page(force=True)
        while True:
            M5.update()
            if M5.BtnA.wasClicked():
                try:
                    M5.Speaker.tone(666, 100)
                except Exception:
                    pass
                self._page = (self._page + 1) % self.PAGE_COUNT
                self._draw_current_page(force=True)
            else:
                self._refresh_current_page()
            await asyncio.sleep_ms(100)

    def _refresh_current_page(self):
        now = time.ticks_ms()
        if time.ticks_diff(now, self._last_refresh_ms) < 1500:
            return
        self._last_refresh_ms = now
        self._draw_current_page(force=False)

    def _draw_current_page(self, force=False):
        payload = self._get_page_payload()
        if not force and payload == self._last_payload:
            return
        self._last_payload = payload
        _draw_split_rows(payload, True)

    def _get_page_payload(self):
        if self._page == self.PAGE_ACCESS:
            return ("Access", "code", self._get_access_code() or "None")
        if self._page == self.PAGE_NICKNAME:
            return ("Nick", "name", self._get_nick_name() or "None")
        if self._page == self.PAGE_WIFI:
            return ("Wi-Fi", self._get_wifi_status_text(), self._ssid or "None")
        return self._get_mac_rows()

    def _get_wifi_status_text(self):
        if self._wifi.connect_status() == network.STAT_GOT_IP:
            return "OK"
        return "FAIL"

    @staticmethod
    def _get_version():
        try:
            return str(esp32.firmware_info()[3]).lstrip("v")
        except Exception:
            return "-.-.-"

    @staticmethod
    def _get_mac_rows():
        text = binascii.hexlify(machine.unique_id()).decode("utf-8").upper()
        mac = ":".join(text[i : i + 2] for i in range(0, len(text), 2))
        return ("MAC", "Address", mac[:8], mac[9:])

    @staticmethod
    def _get_access_code():
        if _HAS_SERVER is True:
            try:
                if M5Things.status() == 2:
                    return M5Things.accesscode() or ""
            except Exception:
                pass
        return ""

    @staticmethod
    def _get_nick_name():
        if _HAS_SERVER is True:
            try:
                if M5Things.status() == 2:
                    return M5Things.nick_name() or ""
            except Exception:
                pass
        return ""


# UnitC6L startup menu
class UnitC6L_Startup(Startup):
    def __init__(self) -> None:
        super().__init__()

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
        M5.Speaker.begin()
        M5.Speaker.setVolumePercentage(1)
        # 显示启动画面
        _draw_split_rows(("UiFlow2", InfoPages._get_version()))
        time.sleep_ms(1500)
        pages = InfoPages(self, ssid)
        pages.draw_start_page()
        M5.Speaker.tone(888, 200)
        self.show_mac()
        # 连接网络
        if super().connect_network(
            ssid=ssid,
            pswd=pswd,
            protocol=protocol,
            ip=ip,
            netmask=netmask,
            gateway=gateway,
            dns=dns,
        ):
            self.show_ssid(ssid)
            count = 1
            status = super().connect_status()
            start = time.time()
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
                self.show_hits(super().local_ip())
                print("Local IP: " + super().local_ip())
        else:
            self.show_error("Not Found", "Use Burner setup")
        self._start_menu_system(pages)

    def _start_menu_system(self, pages):
        """Start the simple info page switcher."""
        try:
            asyncio.run(pages.start())
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Info page error: {e}")
