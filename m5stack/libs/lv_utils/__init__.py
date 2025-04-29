# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import lvgl as lv
import _lv_utils


def fs_register(fs_drv, letter, cache_size=500):
    fs_drv.init()
    fs_drv.letter = ord(letter)
    fs_drv.open_cb = _lv_utils.fs_open_cb
    fs_drv.read_cb = _lv_utils.fs_read_cb
    fs_drv.write_cb = _lv_utils.fs_write_cb
    fs_drv.seek_cb = _lv_utils.fs_seek_cb
    fs_drv.tell_cb = _lv_utils.fs_tell_cb
    fs_drv.close_cb = _lv_utils.fs_close_cb

    if cache_size >= 0:
        fs_drv.cache_size = cache_size

    fs_drv.register()
