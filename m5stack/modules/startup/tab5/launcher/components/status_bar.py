# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from ..hal import get_hal
from ..apps.app import AppManager
from ..common import IMAGE_SUFFIX, IconIndicator
import lvgl as lv
import time as t
import asyncio


_STATUS_BAR_W = 110
_STATUS_BAR_H = 685
_STATUS_ITEM_H = 85
_STATUS_ACTION_ENABLE_DELAY_MS = 800


def _align_status_img(img, index):
    img.set_size(_STATUS_BAR_W, _STATUS_ITEM_H)
    img.align(lv.ALIGN.TOP_LEFT, 0, index * _STATUS_ITEM_H)


class ItemPowerOff:
    def __init__(self, parent: lv.obj, index: int):
        self._press_start_time = 0
        self._press_count = 0
        self._img_id = None

        self._img = lv.image(parent)
        _align_status_img(self._img, index)
        self._update_img()

        # Avoid stale touch state during boot animating the long-press icon.
        self._task = asyncio.create_task(self._enable_interaction())

    async def _enable_interaction(self):
        await asyncio.sleep_ms(_STATUS_ACTION_ENABLE_DELAY_MS)
        self._img.add_flag(lv.obj.FLAG.CLICKABLE)
        self._img.add_event_cb(self._on_pressed, lv.EVENT.PRESSED, None)
        self._img.add_event_cb(self._on_long_pressed_repeat, lv.EVENT.LONG_PRESSED_REPEAT, None)
        self._img.add_event_cb(self._on_released, lv.EVENT.RELEASED, None)

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
        if self._press_count == self._img_id:
            return
        self._img_id = self._press_count
        self._img.set_src(
            get_hal().get_asset_path("status_bar/off_" + str(self._press_count) + IMAGE_SUFFIX)
        )


class ItemSleep:
    def __init__(self, parent: lv.obj, index: int):
        self._press_start_time = 0
        self._press_count = 0
        self._img_id = None

        self._img = lv.image(parent)
        _align_status_img(self._img, index)
        self._update_img()

        self._task = asyncio.create_task(self._enable_interaction())

    async def _enable_interaction(self):
        await asyncio.sleep_ms(_STATUS_ACTION_ENABLE_DELAY_MS)
        self._img.add_flag(lv.obj.FLAG.CLICKABLE)
        self._img.add_event_cb(self._on_pressed, lv.EVENT.PRESSED, None)
        self._img.add_event_cb(self._on_long_pressed_repeat, lv.EVENT.LONG_PRESSED_REPEAT, None)
        self._img.add_event_cb(self._on_released, lv.EVENT.RELEASED, None)

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
        if self._press_count == self._img_id:
            return
        self._img_id = self._press_count
        self._img.set_src(
            get_hal().get_asset_path("status_bar/z_" + str(self._press_count) + IMAGE_SUFFIX)
        )


class ItemBattery:
    def __init__(self, parent: lv.obj, index: int):
        self._img = lv.image(parent)
        _align_status_img(self._img, index)
        self._img_id = None
        self._bat_level_text = None
        self._output_current_text = None

        self._label_bat_level = lv.label(self._img)
        self._label_bat_level.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
        self._label_bat_level.set_style_text_font(lv.font_montserrat_20, lv.PART.MAIN)
        self._label_bat_level.align(lv.ALIGN.CENTER, -9, -11)

        self._label_output_current = lv.label(self._img)
        self._label_output_current.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN)
        self._label_output_current.set_style_text_font(lv.font_montserrat_20, lv.PART.MAIN)
        self._label_output_current.align(lv.ALIGN.CENTER, -9, 19)

        self._update()

        self._task = asyncio.create_task(self.update_task())

    async def update_task(self):
        while True:
            self._update()
            await asyncio.sleep_ms(1000)

    def _update(self):
        bat_level = get_hal().get_battery_level()
        output_current = get_hal().get_output_current()
        self._update_img(bat_level, get_hal().is_charging())
        self._update_labels(bat_level, output_current)

    def _update_img(self, bat_level, is_charging):
        if is_charging:
            img_id = 2
        elif bat_level <= 20:
            img_id = 1
        else:
            img_id = 0

        if img_id != self._img_id:
            self._img_id = img_id
            self._img.set_src(
                get_hal().get_asset_path("status_bar/bat_" + str(img_id) + IMAGE_SUFFIX)
            )

    def _update_labels(self, bat_level, output_current):
        bat_level_text = str(bat_level) + "%"
        if bat_level_text != self._bat_level_text:
            self._bat_level_text = bat_level_text
            self._label_bat_level.set_text(bat_level_text)

        output_current_text = str(round(output_current, 1)) + "A"
        if output_current_text != self._output_current_text:
            self._output_current_text = output_current_text
            self._label_output_current.set_text(output_current_text)


class ItemCharge:
    def __init__(self, parent: lv.obj, index: int):
        self._img = lv.image(parent)
        _align_status_img(self._img, index)
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
    def __init__(self, parent: lv.obj, index: int):
        self._img = lv.image(parent)
        _align_status_img(self._img, index)
        self._network_status = None
        self._update_img()
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
        status = get_hal().get_network_status()
        if status != self._network_status:
            self._network_status = status
            self._img.set_src(
                get_hal().get_asset_path("status_bar/wifi_" + str(status) + IMAGE_SUFFIX)
            )

    def __del__(self):
        self._task.cancel()


class ItemServer:
    def __init__(self, parent: lv.obj, index: int):
        self._img = lv.image(parent)
        _align_status_img(self._img, index)
        self._cloud_status = None
        self._update_img()

        self._task = asyncio.create_task(self.update_task())

    async def update_task(self):
        while True:
            await asyncio.sleep_ms(2000)
            self._update_img()

    def _update_img(self):
        status = get_hal().get_cloud_status()
        if status != self._cloud_status:
            self._cloud_status = status
            self._img.set_src(
                get_hal().get_asset_path("status_bar/server_" + str(status) + IMAGE_SUFFIX)
            )

    def __del__(self):
        self._task.cancel()


class ItemVolume:
    def __init__(self, parent: lv.obj, index: int):
        self._img = lv.image(parent)
        _align_status_img(self._img, index)
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
    def __init__(self, parent: lv.obj, index: int):
        self._img = lv.image(parent)
        _align_status_img(self._img, index)
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
        self._panel.set_size(_STATUS_BAR_W, _STATUS_BAR_H)
        self._panel.set_style_bg_color(lv.color_hex(0x000000), lv.PART.MAIN)
        self._panel.set_style_radius(0, lv.PART.MAIN)
        self._panel.set_style_border_width(0, lv.PART.MAIN)
        self._panel.align(lv.ALIGN.TOP_RIGHT, 0, 0)
        self._panel.set_style_pad_all(0, lv.PART.MAIN)
        self._panel.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
        self._panel.remove_flag(lv.obj.FLAG.SCROLLABLE)

        self._items = (
            ItemPowerOff(self._panel, 0),
            ItemSleep(self._panel, 1),
            ItemBattery(self._panel, 2),
            ItemCharge(self._panel, 3),
            ItemWifi(self._panel, 4),
            ItemServer(self._panel, 5),
            ItemVolume(self._panel, 6),
            ItemBacklight(self._panel, 7),
        )
