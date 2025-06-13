# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from ..hal import get_hal
from ..apps.app import AppManager
from ..common import IconIndicator, Ezdata, EzdataAppState
import lvgl as lv
import asyncio
import time


class EzdataIcon:
    def __init__(self, parent: lv.obj, pos_x: int, group_id: str, name: str):
        self._group_id = group_id
        self._icon_pos_x = pos_x

        btn = lv.obj(parent)
        btn.set_size(99, 99)
        btn.set_style_border_width(0, lv.PART.MAIN)
        btn.align(lv.ALIGN.LEFT_MID, pos_x, 0)
        btn.add_flag(lv.obj.FLAG.CLICKABLE)
        btn.set_style_pad_all(0, lv.PART.MAIN)
        btn.add_event_cb(self._on_clicked, lv.EVENT.CLICKED, None)

        if not group_id:
            btn.remove_flag(lv.obj.FLAG.CLICKABLE)
            btn.set_style_bg_color(lv.color_hex(0x808080), lv.PART.MAIN)
        elif group_id == "settings":
            btn.set_style_bg_color(lv.color_hex(0x9E9E9E), lv.PART.MAIN)
        else:
            btn.set_style_bg_color(lv.color_hex(0xE6E6E6), lv.PART.MAIN)

        label = lv.label(btn)
        label.set_text(name)
        label.set_width(82)
        label.align(lv.ALIGN.CENTER, 0, 0)
        label.set_style_text_color(lv.color_hex(0x4A4949), lv.PART.MAIN)
        label.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)
        if group_id == "add":
            label.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN)
        else:
            label.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN)

    def _on_clicked(self, e: lv.event_t):
        get_hal().play_click_sfx()
        IconIndicator.create_indicator(e.get_target_obj())

        if self._group_id == "settings":
            AppManager.open_app("EzDataSettings")
        else:
            EzdataAppState.set_new_group_id(self._group_id)
            AppManager.open_app("EzData")


class EzdataDock:
    def __init__(self):
        self._last_ezdata_state = Ezdata.State.INIT
        self._icons = []
        self._last_update_group_list_time = 0
        self._last_group_list = []

        self._dock_panel = lv.obj(lv.screen_active())
        self._dock_panel.set_size(445, 115)
        self._dock_panel.align(lv.ALIGN.TOP_LEFT, 17, 27)
        self._dock_panel.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self._dock_panel.set_style_border_width(0, lv.PART.MAIN)
        self._dock_panel.set_style_pad_all(8, lv.PART.MAIN)
        self._dock_panel.set_scrollbar_mode(lv.SCROLLBAR_MODE.ACTIVE)

        self._create_init_dock()

        self._task = asyncio.create_task(self._update_task())

    async def _update_task(self):
        while True:
            await asyncio.sleep(0.5)

            state = Ezdata.get_state()

            # If state changed
            if not state == self._last_ezdata_state:
                self._handle_state_changed(state)
                self._last_ezdata_state = state

            # Check if group list is updated in every 10s
            if state == Ezdata.State.NORMAL:
                if time.time() - self._last_update_group_list_time > 10:
                    new_group_list = Ezdata.get_user_group_list()
                    if new_group_list != self._last_group_list:
                        self._create_data_dock(new_group_list)
                        self._last_group_list = new_group_list
                    self._last_update_group_list_time = time.time()

    def _handle_state_changed(self, new_state: Ezdata.State):
        # State init and wait token share the same dock
        if new_state == Ezdata.State.INIT:
            if self._last_ezdata_state == Ezdata.State.WAIT_USER_TOKEN:
                return
            self._create_init_dock()
        elif new_state == Ezdata.State.WAIT_USER_TOKEN:
            if self._last_ezdata_state == Ezdata.State.INIT:
                return
            self._create_init_dock()

        # Create data dock when ezdata in normal state
        elif new_state == Ezdata.State.NORMAL:
            new_group_list = Ezdata.get_user_group_list()
            self._create_data_dock(new_group_list)
            self._last_update_group_list_time = time.time()
            self._last_group_list = new_group_list

    def _create_init_dock(self):
        self._icons.clear()
        self._dock_panel.clean()

        for i in range(4):
            if i == 0:
                self._icons.append(EzdataIcon(self._dock_panel, 0, "add", "+"))
            else:
                self._icons.append(EzdataIcon(self._dock_panel, i * 110, "", ""))

    def _create_data_dock(self, group_list: list[dict]):
        self._icons.clear()
        self._dock_panel.clean()

        for i, group in enumerate(group_list):
            self._icons.append(
                EzdataIcon(self._dock_panel, i * 110, group.get("id"), group.get("domainName"))
            )

        self._icons.append(
            EzdataIcon(self._dock_panel, len(self._icons) * 110, "settings", "settings")
        )
