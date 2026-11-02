# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

"""Chain Captain startup view.

The layout follows the CoreP4X launcher language: a light surface, compact
status chips, and cards for the two values users need after boot. Chain
Captain has no touch configuration flow, so SSID/IP/password controls are
intentionally absent; the network is still connected by the existing startup
path and its state is shown as status only.
"""

from . import Startup, print_access_info
from .chain_captain_icons import WIFI_ICONS
import M5
import network
import time
import esp32

try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False


# White canvas with a blue primary card and a mint nickname card.
_BG = 0xFFFFFF
_CARD = 0xF2F4F7
_ACCESS_BG = 0x1769E0
_ACCESS_LABEL = 0xFFFFFF
_ACCESS_INK = 0xFFFFFF
_NICKNAME_BG = 0xE5F4EC
_NICKNAME_LABEL = 0x496D58
_NICKNAME_INK = 0x24543E
_MUTED = 0x6B7482
_ACCENT = 0x1769E0
_TINT = 0xE6EFFF
_WARNING = 0x9A5700
_DANGER = 0xC83D35

_SCREEN_W = 240
_MARGIN = 12
_CARD_W = _SCREEN_W - (_MARGIN * 2)
_CHIP_W = 112
_REFRESH_MS = 500


def _safe_text(value, limit=18):
    value = "" if value is None else str(value)
    if len(value) > limit:
        return value[: max(1, limit - 3)] + "..."
    return value


def _version():
    try:
        return str(esp32.firmware_info()[3]).lstrip("vV")
    except (OSError, IndexError, TypeError):
        return "--"


def _font(name):
    """Return a named font without making startup fail on older font sets."""
    try:
        return getattr(M5.Lcd.FONTS, name)
    except AttributeError:
        return M5.Lcd.FONTS.Montserrat12


def _center_text(text, x, y, color, font, background=_BG, gfx=None):
    gfx = M5.Lcd if gfx is None else gfx
    gfx.setFont(font)
    gfx.setTextColor(color, background)
    gfx.drawCenterString(str(text), x, y)


def _clock_text():
    try:
        value = time.localtime()
        return "%02d:%02d" % (value[3], value[4]) if value[0] >= 2024 else "--:--"
    except (AttributeError, IndexError, OSError, TypeError, ValueError):
        return "--:--"


def _battery_state():
    try:
        level = int(M5.Power.getBatteryLevel())
        if level < 0 or level > 100:
            return None, False
        return level, M5.Power.isCharging() == 1
    except (AttributeError, OSError, TypeError, ValueError):
        return None, False


class ChainCaptain_Startup(Startup):
    def __init__(self) -> None:
        super().__init__()
        self._last_payload = None
        self._error = ""
        self._last_status = (None, None, None)
        # Persistent small sprites keep erase/draw operations off the LCD.
        self._wifi_canvas = M5.Lcd.newCanvas(34, 26, 16)
        self._clock_canvas = M5.Lcd.newCanvas(70, 26, 16)
        self._battery_canvas = M5.Lcd.newCanvas(27, 26, 16)

    def _draw_static(self):
        """Draw the stable launcher frame and placeholder content."""
        M5.Lcd.setRotation(0)
        M5.Lcd.clear(_BG)

        self._last_status = (None, None, None)
        self._draw_status_bar("checking")
        _center_text(
            "UIFlow2 v" + _safe_text(_version(), 12),
            120,
            218,
            _MUTED,
            _font("Montserrat12"),
        )

        self._draw_chip(12, 42, "Wi-Fi", "Connecting", _WARNING, 0xFFF0D6)
        self._draw_chip(132, 42, "Service", "Offline", _MUTED, _CARD, width=96)

        self._draw_card(12, 80, _CARD_W, 66, 14, _ACCESS_BG)
        _center_text("Access Code", 120, 90, _ACCESS_LABEL, _font("Montserrat12"), _ACCESS_BG)

        self._draw_card(12, 156, _CARD_W, 48, 14, _NICKNAME_BG)
        _center_text("Nickname", 120, 163, _NICKNAME_LABEL, _font("Montserrat12"), _NICKNAME_BG)

    @staticmethod
    def _draw_card(x, y, width, height, radius, color):
        M5.Lcd.fillRoundRect(x, y, width, height, radius, color)

    def _draw_chip(self, x, y, label, state, color, background, width=_CHIP_W):
        M5.Lcd.fillRoundRect(x, y, width, 25, 10, background)
        _center_text(
            label + " " + state,
            x + width // 2,
            y + 6,
            color,
            _font("Montserrat12"),
            background,
        )

    def _draw_status_bar(self, wifi_state):
        level = 0
        if wifi_state == "connected":
            try:
                rssi = self.get_rssi()
                level = 3 if rssi >= -60 else (2 if rssi >= -75 else 1)
            except (OSError, RuntimeError, TypeError, ValueError):
                level = 0
        disconnected = wifi_state not in ("connected", "checking", "connecting")
        wifi_visual = (level, disconnected)
        clock = _clock_text()
        battery, charging = _battery_state()
        battery_color = (
            0x1D9A62
            if charging
            else (_DANGER if battery is not None and battery <= 20 else _ACCENT)
        )
        fill = 0 if battery is None else max(0, min(17, (battery * 17 + 50) // 100))
        battery_visual = (fill, battery_color)

        if wifi_visual != self._last_status[0]:
            gfx = self._wifi_canvas
            gfx.clear(_BG)
            # Pre-antialiased at native size, aligned with the other status items.
            gfx.drawPng(WIFI_ICONS[4 if disconnected else level], 7, 7)
            gfx.push(10, 0)

        if clock != self._last_status[1]:
            gfx = self._clock_canvas
            gfx.clear(_BG)
            _center_text(clock, 35, 6, _ACCENT, _font("Montserrat16"), gfx=gfx)
            gfx.push(85, 0)

        if battery_visual != self._last_status[2]:
            gfx = self._battery_canvas
            gfx.clear(_BG)
            gfx.drawRoundRect(4, 8, 21, 12, 3, battery_color)
            gfx.fillRect(25, 12, 2, 4, battery_color)
            if fill:
                gfx.fillRect(6, 10, fill, 8, battery_color)
            gfx.push(201, 0)

        self._last_status = (wifi_visual, clock, battery_visual)

    def _draw_dynamic(self, wifi_state, service_state, access_code, nick_name):
        wifi_label, wifi_color, wifi_bg = self._status_style(wifi_state, "connected")
        service_label, service_color, service_bg = self._status_style(
            service_state, "online"
        )
        self._draw_chip(12, 42, "Wi-Fi", wifi_label, wifi_color, wifi_bg)
        self._draw_chip(
            132, 42, "Service", service_label, service_color, service_bg, width=96
        )

        self._draw_card(12, 80, _CARD_W, 66, 14, _ACCESS_BG)
        _center_text("Access Code", 120, 90, _ACCESS_LABEL, _font("Montserrat12"), _ACCESS_BG)
        code = _safe_text(access_code, 10) if access_code else ""
        code_font = _font("Montserrat24") if len(code) <= 8 else _font("Montserrat18")
        _center_text(code, 120, 112, _ACCESS_INK, code_font, _ACCESS_BG)

        self._draw_card(12, 156, _CARD_W, 48, 14, _NICKNAME_BG)
        _center_text("Nickname", 120, 163, _NICKNAME_LABEL, _font("Montserrat12"), _NICKNAME_BG)
        nickname = _safe_text(nick_name, 19) if nick_name else ""
        _center_text(
            nickname,
            120,
            181,
            _NICKNAME_INK,
            _font("Montserrat16"),
            _NICKNAME_BG,
        )

    @staticmethod
    def _status_style(state, good_state):
        if state == good_state:
            return "Online" if good_state == "online" else "Connected", _ACCENT, _TINT
        if state in ("connecting", "checking"):
            return "Connecting", _WARNING, 0xFFF0D6
        if state in ("error", "offline", "disconnected"):
            return "Offline", _DANGER if state == "error" else _MUTED, _CARD
        return "Offline", _MUTED, _CARD

    def _access_code(self):
        if _HAS_SERVER:
            try:
                if M5Things.status() == 2:
                    return M5Things.accesscode() or ""
            except Exception:
                pass
        return ""

    def _nick_name(self):
        if _HAS_SERVER:
            try:
                if M5Things.status() == 2:
                    return M5Things.nick_name() or ""
            except Exception:
                pass
        return ""

    def _refresh(self, error=None):
        if error is not None:
            self._error = error
        status = self.connect_status()
        if status == network.STAT_GOT_IP:
            wifi_state = "connected"
            self._error = ""
        elif status == network.STAT_CONNECTING:
            wifi_state = "connecting"
        elif self._error:
            wifi_state = "error"
        else:
            wifi_state = "offline"
        error = self._error

        service_state = "offline"
        if _HAS_SERVER:
            try:
                service_state = "online" if M5Things.status() == 2 else "offline"
            except Exception:
                service_state = "offline"

        access_code = self._access_code()
        nick_name = self._nick_name()
        payload = (wifi_state, service_state, access_code, nick_name, error)
        self._draw_status_bar(wifi_state)
        if payload == self._last_payload:
            return
        self._last_payload = payload
        self._draw_dynamic(wifi_state, service_state, access_code, nick_name)
        print_access_info(nick_name, access_code)

    def startup(self, ssid: str, pswd: str, timeout: int = 60) -> None:
        self._draw_static()
        self._refresh()
        if super().connect_network(ssid=ssid, pswd=pswd):
            start = time.time()
            error = ""
            while True:
                M5.update()
                status = super().connect_status()
                if status == network.STAT_GOT_IP:
                    print("Local IP: " + super().local_ip())
                    break
                if status == network.STAT_NO_AP_FOUND:
                    error = "Network not found"
                    break
                if status == network.STAT_WRONG_PASSWORD:
                    error = "Wrong password"
                    break
                if status == network.STAT_HANDSHAKE_TIMEOUT:
                    error = "Connection timed out"
                    break
                if (time.time() - start) > timeout:
                    error = "Connection timed out"
                    break
                self._refresh()
                time.sleep_ms(_REFRESH_MS)
            self._refresh(error)
        else:
            self._refresh("Use Burner setup")

        while True:
            M5.update()
            self._refresh()
            time.sleep_ms(_REFRESH_MS)
