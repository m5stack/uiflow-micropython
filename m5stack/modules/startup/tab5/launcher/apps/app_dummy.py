# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .app import AppBase
import lvgl as lv
import asyncio


class AppDummy(AppBase):
    async def main(self):
        label = lv.label(self.get_app_panel())
        label.align(lv.ALIGN.CENTER, 0, 0)
        label.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN)
        label.set_text(self.get_app_name() + ": TODO")

        while True:
            await asyncio.sleep(1)

    def on_cleanup(self):
        pass
