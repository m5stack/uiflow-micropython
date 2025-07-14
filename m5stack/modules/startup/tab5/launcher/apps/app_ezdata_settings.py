# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .app import AppBase
from ..common import Ezdata, debug_print
from ..hal import get_hal
import lvgl as lv


class AppEzdataSettings(AppBase):
    async def main(self):
        parent = self.get_app_panel()
        # qrcode_data = Ezdata.get_add_user_qr_code()

        # qr_add = lv.qrcode(parent)
        # qr_add.align(lv.ALIGN.CENTER, -167, -62)
        # qr_add.set_size(280)
        # qr_add.set_dark_color(lv.color_hex(0x0075B0))
        # qr_add.update(qrcode_data, len(qrcode_data))

        # label_qr_add = lv.label(parent)
        # label_qr_add.set_text('Scan with the "Ez Data" app to begin.')
        # label_qr_add.align(lv.ALIGN.CENTER, -167, 127)
        # label_qr_add.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN)

        # install_url = "https://apps.apple.com/us/app/ezdata/id6738713869"
        # qr_install = lv.qrcode(parent)
        # qr_install.align(lv.ALIGN.CENTER, 413, -46)
        # qr_install.set_size(170)
        # qr_install.set_dark_color(lv.color_hex(0x0075B0))
        # qr_install.update(install_url, len(install_url))

        # label_qr_install = lv.label(parent)
        # label_qr_install.set_width(300)
        # label_qr_install.set_text('Install "Ez Data" from App Store')
        # label_qr_install.align(lv.ALIGN.CENTER, 413, 110)
        # label_qr_install.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN)
        # label_qr_install.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)

        # divider = lv.obj(parent)
        # divider.set_size(6, 345)
        # divider.set_style_border_width(0, lv.PART.MAIN)
        # divider.align(lv.ALIGN.CENTER, 249, 0)
        # divider.set_style_radius(2, lv.PART.MAIN)
        # divider.set_style_bg_color(lv.color_hex(0xE5E5E5), lv.PART.MAIN)

        # Step 1
        img_bg_1 = lv.image(parent)
        img_bg_1.set_src(get_hal().get_asset_path("utils/ezdata_guide_bg_1.png"))
        img_bg_1.align(lv.ALIGN.TOP_LEFT, 33, 20)

        label_1 = lv.label(parent)
        label_1.set_text('Install "Ez Data" from App Store')
        label_1.align(lv.ALIGN.LEFT_MID, 132, -171)
        label_1.set_style_text_font(lv.font_montserrat_24, lv.PART.MAIN)

        install_url = "https://apps.apple.com/us/app/ezdata/id6738713869"
        qr_install = lv.qrcode(parent)
        qr_install.align(lv.ALIGN.CENTER, -190, -50)
        qr_install.set_size(135)
        qr_install.set_dark_color(lv.color_hex(0x3F3F3F))
        qr_install.update(install_url, len(install_url))

        # Step 2
        img_bg_2 = lv.image(parent)
        img_bg_2.set_src(get_hal().get_asset_path("utils/ezdata_guide_bg_2.png"))
        img_bg_2.align(lv.ALIGN.TOP_LEFT, 579, 20)

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
        img_bg_3 = lv.image(parent)
        img_bg_3.set_src(get_hal().get_asset_path("utils/ezdata_guide_bg_3.png"))
        img_bg_3.align(lv.ALIGN.TOP_LEFT, 33, 334)

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
