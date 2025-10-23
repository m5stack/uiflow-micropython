# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import lvgl as lv
import sys
import time

sys.path.append("../../m5stack/libs")
import m5ui
import unittest


class Test(unittest.TestCase):
    def __init__(self) -> None:
        super().__init__()
        m5ui.init()
        page0 = m5ui.M5Page()
        self.led0 = m5ui.M5LED(x=123, y=109, size=20, color=0x00FF00, on=False, parent=page0)
        page0.screen_load()

    def test_brightness(self):
        for br in range(0, 101):
            self.led0.set_brightness(br)
            self.assertEqual(self.led0.get_brightness(), br)

    def tearDown(self):
        time.sleep(3)


if __name__ == "__main__":
    unittest.main()
