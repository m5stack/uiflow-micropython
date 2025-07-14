# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .app import AppBase
from ..common import Ezdata, debug_print
from ..hal import get_hal
import lvgl as lv


class AppEzdataSettings(AppBase):
    def create_panel(self, parent: lv.obj, pos: tuple[int, int], size: tuple[int, int]):
        panel = lv.obj(parent)
        panel.set_size(size[0], size[1])
        panel.align(lv.ALIGN.TOP_LEFT, pos[0], pos[1])
        panel.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        panel.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
        panel.set_style_border_width(0, lv.PART.MAIN)
        panel.set_style_radius(15, lv.PART.MAIN)
        panel.remove_flag(lv.obj.FLAG.SCROLLABLE)

    def create_badge(self, parent: lv.obj, text: str, pos: tuple[int, int]):
        panel = lv.obj(parent)
        panel.set_size(53, 53)
        panel.align(lv.ALIGN.TOP_LEFT, pos[0], pos[1])
        panel.set_style_bg_color(lv.color_hex(0x68A4F7), lv.PART.MAIN)
        panel.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
        panel.set_style_border_width(0, lv.PART.MAIN)
        panel.set_style_radius(233, lv.PART.MAIN)
        panel.remove_flag(lv.obj.FLAG.SCROLLABLE)

        label = lv.label(panel)
        label.set_text(text)
        label.align(lv.ALIGN.CENTER, 0, 0)
        label.set_style_text_font(lv.font_montserrat_30, lv.PART.MAIN)
        label.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

    async def main(self):
        parent = self.get_app_panel()

        # Step 1
        self.create_panel(parent, (33, 20), (518, 287))
        self.create_badge(parent, "1", (65, 52))

        label_1 = lv.label(parent)
        label_1.set_text('Install "Ez Data" from App Store')
        label_1.align(lv.ALIGN.LEFT_MID, 132, -171)
        label_1.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN)

        img_icon_pohone = lv.image(parent)
        img_icon_pohone.set_src(get_hal().get_asset_path("icons/guide_phone.bin"))
        img_icon_pohone.align(lv.ALIGN.TOP_LEFT, 132, 150)

        install_url = "https://apps.apple.com/us/app/ezdata/id6738713869"
        qr_install = lv.qrcode(parent)
        qr_install.align(lv.ALIGN.CENTER, -190, -50)
        qr_install.set_size(135)
        qr_install.set_dark_color(lv.color_hex(0x3F3F3F))
        qr_install.update(install_url, len(install_url))

        # Step 2
        self.create_panel(parent, (579, 20), (518, 287))
        self.create_badge(parent, "2", (617, 52))

        img_icon_camera = lv.image(parent)
        img_icon_camera.set_src(get_hal().get_asset_path("icons/guide_camera.bin"))
        img_icon_camera.align(lv.ALIGN.TOP_LEFT, 688, 150)

        label_2 = lv.label(parent)
        label_2.set_text('Scan with the "Ez Data" app\nto Add device')
        label_2.align(lv.ALIGN.LEFT_MID, 688, -171)
        label_2.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN)

        add_user_qr_code = Ezdata.get_add_user_qr_code()
        qr_add = lv.qrcode(parent)
        qr_add.align(lv.ALIGN.CENTER, 369, -50)
        qr_add.set_size(135)
        qr_add.set_dark_color(lv.color_hex(0x3F3F3F))
        qr_add.update(add_user_qr_code, len(add_user_qr_code))

        # Step 3
        self.create_panel(parent, (33, 334), (1064, 145))
        self.create_badge(parent, "3", (65, 380))

        img_icon_folder = lv.image(parent)
        img_icon_folder.set_src(get_hal().get_asset_path("icons/guide_folder.bin"))
        img_icon_folder.align(lv.ALIGN.TOP_LEFT, 894, 353)

        mac = "".join(f"{byte:02x}" for byte in get_hal().get_mac())
        label_3 = lv.label(parent)
        label_3.set_text(f"Add or modify data in the tab5-{mac} folder")
        label_3.align(lv.ALIGN.LEFT_MID, 132, 157)
        label_3.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN)

        label_folder_name = lv.label(parent)
        label_folder_name.set_text(f"tab5-{mac}")
        label_folder_name.align(lv.ALIGN.CENTER, 369, 195)
        label_folder_name.set_style_text_color(lv.color_hex(0x3F3F3F), lv.PART.MAIN)
        label_folder_name.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)
