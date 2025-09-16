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
        self.slider0 = m5ui.M5Slider(value=25, parent=page0)
        self.slider0.set_pos(50, 50)
        page0.screen_load()

    def test_set_range(self):
        self.slider0.set_range(40, 50)
        self.assertEqual(self.slider0.get_value(), 40)

    def test_set_value(self):
        self.slider0.set_value(60)
        self.assertEqual(self.slider0.get_value(), 50)
        self.slider0.set_value(30)
        self.assertEqual(self.slider0.get_value(), 40)

    def tearDown(self):
        time.sleep(3)


if __name__ == "__main__":
    unittest.main()
