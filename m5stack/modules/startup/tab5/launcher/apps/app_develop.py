# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .app import AppBase
from ..hal import *
import lvgl as lv
import asyncio
from startup import print_access_info


_M5THINGS = None

_PANEL_PAD = 0
_DEFAULT_PANEL_PAD = 10
_PANEL_BG_COLOR = 0xFFFFFF
_DEFAULT_PANEL_BG_COLOR = 0xF6F6F6
_LABEL_COLOR = 0x8F8F8F
_VALUE_COLOR = 0x1F2933
_ONLINE_IMG = "utils/online.bin"
_OFFLINE_IMG = "utils/offline.bin"
_DEVELOP_BG_IMG = "utils/develop_bg.png"

_STATUS_IMG_X = 24
_STATUS_IMG_Y = 24
_DEVELOP_BG_X = 790
_DEVELOP_BG_Y = 60
_LEFT_X = 54
_RIGHT_X = 430
_LABEL_GAP = 42
_VALUE_W = 350
_VALUE_H = 56

_ROW_MAC_Y = 124
_ROW_CODE_Y = 248
_ROW_NICK_Y = 372
_ROW_WIFI_Y = 124
_ROW_IP_Y = 248
_ROW_FW_Y = 372

_REFRESH_DELAY_MS = 1500
_FIRST_REFRESH_DELAY_MS = 100
_DETAIL_REFRESH_INTERVAL = 4


class AppDevelop(AppBase):
    async def main(self):
        self._state = self._get_initial_state()
        self._labels = []
        self._images = []
        self._refresh_count = 0

        self._setup_panel()
        self._create_view()

        await asyncio.sleep_ms(_FIRST_REFRESH_DELAY_MS)

        while True:
            self._refresh_count += 1
            self._update_view(self._should_refresh_details())
            await asyncio.sleep_ms(_REFRESH_DELAY_MS)

    def _setup_panel(self):
        panel = self.get_app_panel()
        panel.set_style_pad_all(_PANEL_PAD, lv.PART.MAIN)
        panel.set_style_bg_color(lv.color_hex(_PANEL_BG_COLOR), lv.PART.MAIN)
        panel.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
        panel.remove_flag(lv.obj.FLAG.SCROLLABLE)

    def _create_view(self):
        self._status_img = lv.image(self.get_app_panel())
        self._status_img.align(lv.ALIGN.TOP_LEFT, _STATUS_IMG_X, _STATUS_IMG_Y)
        self._images.append(self._status_img)

        self._develop_bg_img = lv.image(self.get_app_panel())
        self._develop_bg_img.set_src(get_hal().get_asset_path(_DEVELOP_BG_IMG))
        self._develop_bg_img.align(lv.ALIGN.TOP_LEFT, _DEVELOP_BG_X, _DEVELOP_BG_Y)
        self._images.append(self._develop_bg_img)

        self._mac_value = self._create_row("Device MAC:", _LEFT_X, _ROW_MAC_Y)
        self._code_value = self._create_row(
            "Access Code:", _LEFT_X, _ROW_CODE_Y, lv.font_montserrat_48
        )
        self._nick_value = self._create_row("Nickname:", _LEFT_X, _ROW_NICK_Y)
        self._wifi_value = self._create_row("Wi-Fi SSID:", _RIGHT_X, _ROW_WIFI_Y)
        self._ip_value = self._create_row("IP Address:", _RIGHT_X, _ROW_IP_Y)
        self._fw_value = self._create_row("UIFlow2 firmware:", _RIGHT_X, _ROW_FW_Y)

        self._set_status(self._state.get("is_cloud_connected", False))
        self._set_value(self._mac_value, self._state.get("mac", "-"))
        self._set_value(self._code_value, self._state.get("access_code", ""), fallback="")
        self._set_value(self._nick_value, self._state.get("nick_name", ""), fallback="")
        self._set_value(self._wifi_value, self._state.get("wifi_ssid", ""), fallback="")
        self._set_value(self._ip_value, self._state.get("ip_address", ""), fallback="")
        self._set_value(self._fw_value, self._state.get("firmware", ""), fallback="")
        print_access_info(self._state.get("nick_name", ""), self._state.get("access_code", ""))

    def _update_view(self, refresh_details=False):
        new_state = self._collect_state(refresh_details)

        if new_state["is_cloud_connected"] != self._state.get("is_cloud_connected"):
            self._state["is_cloud_connected"] = new_state["is_cloud_connected"]
            self._set_status(new_state["is_cloud_connected"])

        self._update_label("access_code", self._code_value, new_state, fallback="")
        self._update_label("nick_name", self._nick_value, new_state, fallback="")
        self._update_label("wifi_ssid", self._wifi_value, new_state, fallback="")
        self._update_label("ip_address", self._ip_value, new_state, fallback="")
        self._update_label("firmware", self._fw_value, new_state, fallback="")
        print_access_info(self._state.get("nick_name", ""), self._state.get("access_code", ""))

    def _update_label(self, key, label, new_state, fallback="-"):
        if new_state[key] != self._state.get(key):
            self._state[key] = new_state[key]
            self._set_value(label, new_state[key], fallback=fallback)

    def on_cleanup(self):
        for label in self._labels:
            label.delete()
        self._labels.clear()

        for img in self._images:
            img.delete()
        self._images.clear()

        panel = self.get_app_panel()
        panel.set_style_pad_all(_DEFAULT_PANEL_PAD, lv.PART.MAIN)
        panel.set_style_bg_color(lv.color_hex(_DEFAULT_PANEL_BG_COLOR), lv.PART.MAIN)
        panel.add_flag(lv.obj.FLAG.SCROLLABLE)

    def _create_row(self, caption, x, y, value_font=lv.font_montserrat_36):
        self._create_caption(caption, x, y)
        return self._create_value_label(x, y + _LABEL_GAP, _VALUE_W, value_font)

    def _create_caption(self, text, x, y):
        label = self._create_text_label(x, y, _VALUE_W, 32)
        label.set_text(text)
        label.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN)
        label.set_style_text_color(lv.color_hex(_LABEL_COLOR), lv.PART.MAIN)
        return label

    def _create_value_label(self, x, y, width, font):
        label = self._create_text_label(x, y, width, _VALUE_H)
        label.set_style_text_font(font, lv.PART.MAIN)
        label.set_style_text_color(lv.color_hex(_VALUE_COLOR), lv.PART.MAIN)
        return label

    def _create_text_label(self, x, y, width, height):
        label = lv.label(self.get_app_panel())
        label.set_size(width, height)
        label.align(lv.ALIGN.TOP_LEFT, x, y)
        label.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN)
        self._labels.append(label)
        return label

    def _set_status(self, is_cloud_connected):
        if is_cloud_connected:
            self._status_img.set_src(get_hal().get_asset_path(_ONLINE_IMG))
        else:
            self._status_img.set_src(get_hal().get_asset_path(_OFFLINE_IMG))

    @staticmethod
    def _set_value(label, text, fallback="-"):
        text = fallback if text is None or text == "" else str(text)
        label.set_text(text)

    @staticmethod
    def _is_cloud_connected():
        try:
            return get_hal().get_cloud_status() == CloudStatus.CONNECTED
        except Exception:
            return False

    @staticmethod
    def _get_m5things():
        global _M5THINGS
        if _M5THINGS is None:
            try:
                import M5Things

                _M5THINGS = M5Things
            except ImportError:
                return None
        return _M5THINGS

    @staticmethod
    def _get_access_code(m5things, is_cloud_connected):
        if m5things and is_cloud_connected:
            try:
                return m5things.accesscode() or ""
            except Exception:
                pass
        return ""

    @staticmethod
    def _get_nick_name(m5things, is_cloud_connected):
        if m5things and is_cloud_connected:
            try:
                return m5things.nick_name() or ""
            except Exception:
                pass
        return ""

    @staticmethod
    def _get_mac():
        import binascii

        return binascii.hexlify(get_hal().get_mac()).decode("utf-8").upper()

    @staticmethod
    def _get_wifi_ssid():
        try:
            return get_hal().get_network_config().ssid or ""
        except Exception:
            return ""

    @staticmethod
    def _get_ip_address():
        try:
            import network

            wlan = network.WLAN(network.STA_IF)
            if wlan.isconnected():
                return wlan.ifconfig()[0]
        except Exception:
            pass
        return ""

    @staticmethod
    def _get_firmware_version():
        try:
            import esp32

            return esp32.firmware_info()[3]
        except Exception:
            return ""

    def _get_initial_state(self):
        return {
            "mac": self._get_mac(),
            "is_cloud_connected": False,
            "access_code": "",
            "nick_name": "",
            "wifi_ssid": "",
            "ip_address": "",
            "firmware": self._get_firmware_version(),
        }

    def _should_refresh_details(self):
        return self._refresh_count % _DETAIL_REFRESH_INTERVAL == 1

    def _collect_state(self, refresh_details=False):
        is_cloud_connected = self._is_cloud_connected()
        state = {
            "mac": self._state.get("mac", ""),
            "is_cloud_connected": is_cloud_connected,
            "access_code": self._state.get("access_code", ""),
            "nick_name": self._state.get("nick_name", ""),
            "wifi_ssid": self._state.get("wifi_ssid", ""),
            "ip_address": self._state.get("ip_address", ""),
            "firmware": self._state.get("firmware", ""),
        }

        if not is_cloud_connected:
            state["access_code"] = ""
            state["nick_name"] = ""

        if refresh_details:
            m5things = self._get_m5things() if is_cloud_connected else None
            state["access_code"] = self._get_access_code(m5things, is_cloud_connected)
            state["nick_name"] = self._get_nick_name(m5things, is_cloud_connected)
            state["wifi_ssid"] = self._get_wifi_ssid()
            state["ip_address"] = self._get_ip_address()

        return state
