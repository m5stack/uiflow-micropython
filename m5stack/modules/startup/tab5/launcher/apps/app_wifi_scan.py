# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .app import AppBase
from ..hal import *
import lvgl as lv
import asyncio


class NetworkInfo:
    def __init__(self, parent: lv.obj, network_info: tuple, pos_y: int):
        self._panel = lv.obj(parent)
        self._panel.align(lv.ALIGN.TOP_LEFT, 0, pos_y)
        self._panel.set_size(880, 40)
        self._panel.set_style_pad_all(0, lv.PART.MAIN)
        self._panel.set_style_border_width(0, lv.PART.MAIN)
        self._panel.set_style_radius(10, lv.PART.MAIN)

        self._label = lv.label(self._panel)
        self._label.align(lv.ALIGN.LEFT_MID, 10, 0)
        self._label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)
        self._label.set_style_text_color(lv.color_hex(0x4A4A4A), lv.PART.MAIN)

        self._parse_network_info(network_info)

    def _parse_network_info(self, network_info: tuple):
        ssid = network_info[0].decode()  # SSID 是 bytes，要 decode
        bssid = ":".join("{:02x}".format(b) for b in network_info[1])  # BSSID 转换为 MAC 地址格式
        channel = network_info[2]
        rssi = network_info[3]
        auth = network_info[4]
        hidden = network_info[5]

        auth_dict = {0: "OPEN", 1: "WEP", 2: "WPA-PSK", 3: "WPA2-PSK", 4: "WPA/WPA2-PSK"}
        auth_str = auth_dict.get(auth, "UNKNOWN")

        self._label.set_text(
            f"SSID: {ssid}   |   RSSI: {rssi:3} dBm   |   CH: {channel}   |   Auth: {auth_str}   |   Hidden: {hidden}   |   BSSID: {bssid}"
        )
        self._panel.set_style_bg_color(
            lv.color_hex(0xC8F3D1 if rssi >= -60 else 0xFFE7D7), lv.PART.MAIN
        )

    def cleanup(self):
        self._label.delete()
        self._label = None

        self._panel.delete()
        self._panel = None


class AppWifiScan(AppBase):
    class ScanState:
        IDLE = 0
        SCANNING = 1

    async def main(self):
        self._task = None
        self._current_state = self.ScanState.IDLE
        self._results = []

        self._btn_scan = lv.button(self.get_app_panel())
        self._btn_scan.set_size(150, 100)
        self._btn_scan.align(lv.ALIGN.TOP_RIGHT, -18, 350)
        self._btn_scan.set_style_bg_color(lv.color_hex(0x119FE6), lv.PART.MAIN)
        self._btn_scan.set_style_radius(10, lv.PART.MAIN)
        self._btn_scan.set_style_shadow_width(0, lv.PART.MAIN)
        self._btn_scan.add_event_cb(self._on_scan_btn_clicked, lv.EVENT.CLICKED, None)

        self._label_scan = lv.label(self._btn_scan)
        self._label_scan.set_text("SCAN")
        self._label_scan.set_align(lv.ALIGN.CENTER)
        self._label_scan.set_style_text_font(lv.font_montserrat_20, lv.PART.MAIN)

        self._wifi_panel = lv.obj(self.get_app_panel())
        self._wifi_panel.set_size(920, 440)
        self._wifi_panel.align(lv.ALIGN.LEFT_MID, 15, 0)
        self._wifi_panel.set_style_radius(10, lv.PART.MAIN)
        self._wifi_panel.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self._wifi_panel.set_style_border_width(0, lv.PART.MAIN)

        self._spinner = lv.spinner(self._wifi_panel)
        self._spinner.align(lv.ALIGN.CENTER, 0, 0)
        self._spinner.set_size(60, 60)
        self._spinner.set_style_arc_width(5, lv.PART.MAIN)
        self._spinner.set_style_arc_width(5, lv.PART.INDICATOR)

        self._update_state(self.ScanState.IDLE)

    def _update_state(self, state: ScanState):
        self._current_state = state
        self._update_ui()

    def _update_ui(self):
        if self._current_state == self.ScanState.IDLE:
            self._btn_scan.add_flag(lv.obj.FLAG.CLICKABLE)
            self._label_scan.set_text("SCAN")
            self._spinner.set_style_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        elif self._current_state == self.ScanState.SCANNING:
            self._btn_scan.remove_flag(lv.obj.FLAG.CLICKABLE)
            self._label_scan.set_text("SCANNING...")
            self._spinner.set_style_opa(lv.OPA.COVER, lv.PART.MAIN)

    def _on_scan_btn_clicked(self, e: lv.event_t):
        get_hal().play_click_sfx()
        if self._current_state == self.ScanState.SCANNING:
            return
        self._update_state(self.ScanState.SCANNING)
        self._task = asyncio.create_task(self._wifi_scan_task())

    def _clear_result_labels(self):
        for result in self._results:
            result.cleanup()
        self._results.clear()

    def _create_result_labels(self, new_result: list[tuple]):
        for i, network_info in enumerate(new_result):
            self._results.append(NetworkInfo(self._wifi_panel, network_info, 10 + i * 70))

    async def _wifi_scan_task(self):
        self._clear_result_labels()
        result = await get_hal().scan_wifi()
        self._create_result_labels(result)
        self._update_state(self.ScanState.IDLE)

    def on_cleanup(self):
        self._label_scan.delete()
        self._label_scan = None
        self._btn_scan.delete()
        self._btn_scan = None

        self._clear_result_labels()

        self._wifi_panel.delete()
        self._wifi_panel = None
