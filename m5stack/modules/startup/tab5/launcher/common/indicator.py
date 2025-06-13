# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from ..hal import get_hal
from ..common import IMAGE_SUFFIX
import lvgl as lv


class IconIndicator:
    _img: lv.image = None

    @staticmethod
    def create_indicator(target: lv.obj):
        if not IconIndicator._img:
            IconIndicator._img = lv.image(lv.screen_active())
            IconIndicator._img.set_src(get_hal().get_asset_path("icons/indicator" + IMAGE_SUFFIX))
        IconIndicator._img.align_to(target, lv.ALIGN.OUT_BOTTOM_MID, 0, 3)

    @staticmethod
    def destroy_indicator():
        if IconIndicator._img:
            IconIndicator._img.delete()
            IconIndicator._img = None
