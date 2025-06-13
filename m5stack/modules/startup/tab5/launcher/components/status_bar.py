# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from ..hal import get_hal
from ..apps.app import AppManager
from ..common import *
import lvgl as lv
import time as t
import asyncio


class ItemPowerOff:
    def __init__(self, parent: lv.obj):
        self._press_start_time = 0
        self._press_count = 0

        self._img = lv.image(parent)
        self._img.add_flag(lv.obj.FLAG.CLICKABLE)
        self._img.add_event_cb(self._on_pressed, lv.EVENT.PRESSED, None)
        self._img.add_event_cb(self._on_long_pressed_repeat, lv.EVENT.LONG_PRESSED_REPEAT, None)
        self._img.add_event_cb(self._on_released, lv.EVENT.RELEASED, None)

        self._update_img()

    def _on_pressed(self, e: lv.event_t):
        get_hal().play_click_sfx()
        self._press_start_time = t.time()
        self._press_count = 1
        self._update_img()

    def _on_long_pressed_repeat(self, e: lv.event_t):
        delta_time = t.time() - self._press_start_time
        if delta_time > 0.5:
            get_hal().play_click_sfx()
            self._press_count += 1
            if self._press_count > 5:
                get_hal().power_off()
                return
            self._update_img()
            self._press_start_time = t.time()

    def _on_released(self, e: lv.event_t):
        self._press_count = 0
        self._update_img()

    def _update_img(self):
        self._img.set_src(
            get_hal().get_asset_path("status_bar/off_" + str(self._press_count) + IMAGE_SUFFIX)
        )


class ItemSleep:
    def __init__(self, parent: lv.obj):
        self._press_start_time = 0
        self._press_count = 0

        self._img = lv.image(parent)
        self._img.add_flag(lv.obj.FLAG.CLICKABLE)
        self._img.add_event_cb(self._on_pressed, lv.EVENT.PRESSED, None)
        self._img.add_event_cb(self._on_long_pressed_repeat, lv.EVENT.LONG_PRESSED_REPEAT, None)
        self._img.add_event_cb(self._on_released, lv.EVENT.RELEASED, None)

        self._update_img()

    def _on_pressed(self, e: lv.event_t):
        get_hal().play_click_sfx()
        self._press_start_time = t.time()
        self._press_count = 1
        self._update_img()

    def _on_long_pressed_repeat(self, e: lv.event_t):
        delta_time = t.time() - self._press_start_time
        if delta_time > 0.5:
            get_hal().play_click_sfx()
            self._press_count += 1
            if self._press_count > 4:
                get_hal().sleep()
                return
            self._update_img()
            self._press_start_time = t.time()

    def _on_released(self, e: lv.event_t):
        self._press_count = 0
        self._update_img()

    def _update_img(self):
        self._img.set_src(
            get_hal().get_asset_path("status_bar/z_" + str(self._press_count) + IMAGE_SUFFIX)
        )


class ItemBattery:
    def __init__(self, parent: lv.obj):
        self._img = lv.image(parent)

        self._label_bat_level = lv.label(self._img)
        self._label_bat_level.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
        self._label_bat_level.set_style_text_font(lv.font_montserrat_20, lv.PART.MAIN)
        self._label_bat_level.align(lv.ALIGN.CENTER, -9, -11)

        self._label_output_current = lv.label(self._img)
        self._label_output_current.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
        self._label_output_current.set_style_text_font(lv.font_montserrat_20, lv.PART.MAIN)
        self._label_output_current.align(lv.ALIGN.CENTER, -9, 19)

        self._update_img()
        self._update_labels()

        # TODO: Update task
        self._img.set_style_image_recolor_opa(123, lv.PART.MAIN)

    def _update_img(self):
        if get_hal().is_charging():
            self._img.set_src(get_hal().get_asset_path("status_bar/bat_2" + IMAGE_SUFFIX))
        elif get_hal().get_battery_level() <= 20:
            self._img.set_src(get_hal().get_asset_path("status_bar/bat_1" + IMAGE_SUFFIX))
        else:
            self._img.set_src(get_hal().get_asset_path("status_bar/bat_0" + IMAGE_SUFFIX))

    def _update_labels(self):
        self._label_bat_level.set_text(str(get_hal().get_battery_level()) + "%")
        self._label_output_current.set_text(str(round(get_hal().get_output_current(), 2)) + "A")


class ItemCharge:
    def __init__(self, parent: lv.obj):
        self._img = lv.image(parent)
        self._img.add_flag(lv.obj.FLAG.CLICKABLE)
        self._img.add_event_cb(self._on_clicked, lv.EVENT.CLICKED, None)

        self._label_chg = lv.label(self._img)
        self._label_chg.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
        self._label_chg.set_style_text_font(lv.font_montserrat_20, lv.PART.MAIN)
        self._label_chg.align(lv.ALIGN.CENTER, -10, 19)

        self._update_img()
        self._update_label()

    def _update_img(self):
        self._img.set_src(
            get_hal().get_asset_path(
                "status_bar/chg_" + str(get_hal().get_charge_mode()) + IMAGE_SUFFIX
            )
        )

    def _update_label(self):
        texts = ["0.5A", "1A", "NO"]
        self._label_chg.set_text(texts[get_hal().get_charge_mode()])

    def _on_clicked(self, e: lv.event_t):
        get_hal().play_click_sfx()
        get_hal().set_charge_mode((get_hal().get_charge_mode() + 1) % 3)
        self._update_img()
        self._update_label()


class ItemWifi:
    def __init__(self, parent: lv.obj):
        self._img = lv.image(parent)
        self._img.set_src(get_hal().get_asset_path("status_bar/wifi_0" + IMAGE_SUFFIX))
        self._img.add_flag(lv.obj.FLAG.CLICKABLE)
        self._img.add_event_cb(self._on_clicked, lv.EVENT.CLICKED, None)

        self._task = asyncio.create_task(self.update_task())

    def _on_clicked(self, e: lv.event_t):
        get_hal().play_click_sfx()
        IconIndicator.destroy_indicator()
        AppManager.open_app("Wifi")

    async def update_task(self):
        while True:
            await asyncio.sleep_ms(2000)
            self._update_img()

    def _update_img(self):
        self._img.set_src(
            get_hal().get_asset_path(
                "status_bar/wifi_" + str(get_hal().get_network_status()) + IMAGE_SUFFIX
            )
        )

    def __del__(self):
        self._task.cancel()


class ItemServer:
    def __init__(self, parent: lv.obj):
        self._img = lv.image(parent)
        self._img.set_src(get_hal().get_asset_path("status_bar/server_0" + IMAGE_SUFFIX))

        self._task = asyncio.create_task(self.update_task())

    async def update_task(self):
        while True:
            await asyncio.sleep_ms(2000)
            self._update_img()

    def _update_img(self):
        self._img.set_src(
            get_hal().get_asset_path(
                "status_bar/server_" + str(get_hal().get_cloud_status()) + IMAGE_SUFFIX
            )
        )

    def __del__(self):
        self._task.cancel()


class ItemVolume:
    def __init__(self, parent: lv.obj):
        self._img = lv.image(parent)
        self._img.add_flag(lv.obj.FLAG.CLICKABLE)
        self._img.add_event_cb(self._on_clicked, lv.EVENT.CLICKED, None)

        self._update_img()

    def _on_clicked(self, e: lv.event_t):
        new_volume = get_hal().get_volume() + 20
        if new_volume > 100:
            new_volume = 0
        get_hal().set_volume(new_volume)

        self._update_img()

        get_hal().play_click_sfx()

    def _update_img(self):
        self._img.set_src(
            get_hal().get_asset_path(
                "status_bar/vol_" + str(get_hal().get_volume()) + IMAGE_SUFFIX
            )
        )


class ItemBacklight:
    def __init__(self, parent: lv.obj):
        self._img = lv.image(parent)
        self._img.add_flag(lv.obj.FLAG.CLICKABLE)
        self._img.add_event_cb(self._on_clicked, lv.EVENT.CLICKED, None)

        self._update_img()

    def _on_clicked(self, e: lv.event_t):
        get_hal().play_click_sfx()

        new_volume = get_hal().get_backlight() + 10
        if new_volume > 100:
            new_volume = 30
        get_hal().set_backlight(new_volume)

        self._update_img()

    def _update_img(self):
        self._img.set_src(
            get_hal().get_asset_path(
                "status_bar/light_" + str(get_hal().get_backlight()) + IMAGE_SUFFIX
            )
        )


class StatusBar:
    def __init__(self):
        self._panel = lv.obj(lv.screen_active())
        self._panel.set_size(110, 685)
        self._panel.set_style_bg_color(lv.color_hex(0x000000), lv.PART.MAIN)
        self._panel.set_style_radius(0, lv.PART.MAIN)
        self._panel.set_style_border_width(0, lv.PART.MAIN)
        self._panel.align(lv.ALIGN.TOP_RIGHT, 0, 0)
        self._panel.set_style_pad_all(0, lv.PART.MAIN)
        self._panel.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self._panel.set_flex_align(
            lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER
        )
        self._panel.set_style_pad_gap(0, lv.PART.MAIN)

        self._item_power_off = ItemPowerOff(self._panel)
        self._item_sleep = ItemSleep(self._panel)
        self._item_battery = ItemBattery(self._panel)
        self._item_charge = ItemCharge(self._panel)
        self._item_wifi = ItemWifi(self._panel)
        self._item_server = ItemServer(self._panel)
        self._item_volume = ItemVolume(self._panel)
        self._item_backlight = ItemBacklight(self._panel)
