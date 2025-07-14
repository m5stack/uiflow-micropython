# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from ..hal import get_hal
from ..apps.app import AppManager
from ..common import IconIndicator, Ezdata
from ..common import debug_print
import lvgl as lv
import asyncio


class EzdataIcon:
    def __init__(self, parent: lv.obj, pos_x: int, data_id: str, name: str, pin_color=None):
        self._data_id = data_id
        self._icon_pos_x = pos_x

        btn = lv.obj(parent)
        btn.set_size(99, 99)
        btn.set_style_border_width(0, lv.PART.MAIN)
        btn.align(lv.ALIGN.LEFT_MID, pos_x, 0)
        btn.add_flag(lv.obj.FLAG.CLICKABLE)
        btn.set_style_pad_all(0, lv.PART.MAIN)
        btn.add_event_cb(self._on_clicked, lv.EVENT.CLICKED, None)
        btn.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

        if data_id == "settings":
            btn.set_style_bg_color(lv.color_hex(0xE0EDFF), lv.PART.MAIN)

            img_icon = lv.image(btn)
            img_icon.set_src(get_hal().get_asset_path("icons/settings.png"))
            img_icon.align(lv.ALIGN.CENTER, 0, 0)
        else:
            label = lv.label(btn)
            label.set_text(name)
            label.set_width(82)
            label.align(lv.ALIGN.CENTER, 0, 0)
            label.set_style_text_color(lv.color_hex(0x4A4949), lv.PART.MAIN)
            label.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)
            label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

        if pin_color:
            pin = lv.obj(btn)
            pin.set_size(16, 16)
            pin.align(lv.ALIGN.TOP_RIGHT, -6, 6)
            pin.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
            pin.set_style_border_width(0, lv.PART.MAIN)
            pin.set_style_bg_color(lv.color_hex(pin_color), lv.PART.MAIN)

    def _on_clicked(self, e: lv.event_t):
        get_hal().play_click_sfx()
        IconIndicator.create_indicator(e.get_target_obj())

        if self._data_id == "settings":
            AppManager.open_app("EzDataSettings")
        else:
            Ezdata.set_selected_data_id(self._data_id)
            AppManager.open_app("EzData")


class EzdataDock:
    def __init__(self):
        self._icons = []

        self._dock_panel = lv.obj(lv.screen_active())
        self._dock_panel.set_size(445, 115)
        self._dock_panel.align(lv.ALIGN.TOP_LEFT, 17, 27)
        self._dock_panel.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self._dock_panel.set_style_border_width(0, lv.PART.MAIN)
        self._dock_panel.set_style_pad_all(8, lv.PART.MAIN)
        self._dock_panel.set_scrollbar_mode(lv.SCROLLBAR_MODE.ACTIVE)

        label_init = lv.label(self._dock_panel)
        label_init.set_text("Connecting...")
        label_init.align(lv.ALIGN.CENTER, 0, 0)
        label_init.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        label_init.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN)

        self._task = asyncio.create_task(self._task())

    async def _task(self):
        # Wait ezdata ready
        while Ezdata.get_state() == Ezdata.State.INIT:
            await asyncio.sleep(0.5)
            continue

        # Connect on change signal and create initial data dock
        Ezdata.on_data_list_changed.connect(self._handle_data_list_changed)
        self._create_data_dock()

    def _create_data_dock(self):
        all_data = Ezdata.get_all_data()
        # debug_print("data:", all_data)

        self._icons.clear()
        self._dock_panel.clean()

        # Setting icon
        self._icons.append(EzdataIcon(self._dock_panel, 0, "settings", "settings"))

        # If no data
        if len(all_data) == 0:
            label_no_data = lv.label(self._dock_panel)
            label_no_data.set_text("No data.")
            label_no_data.align(lv.ALIGN.CENTER, 50, 0)
            label_no_data.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
            label_no_data.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN)

        for i, data in enumerate(all_data):
            self._icons.append(
                EzdataIcon(
                    self._dock_panel,
                    (i + 1) * 110,
                    data.get("id"),
                    data.get("name"),
                )
            )

    def _handle_data_list_changed(self):
        debug_print("[EzdataDock] data list changed")
        self._create_data_dock()
