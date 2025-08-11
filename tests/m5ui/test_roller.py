# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import lvgl as lv
import sys

sys.path.append("../../m5stack/libs")
import m5ui
import unittest


class Test(unittest.TestCase):
    def __init__(self) -> None:
        super().__init__()
        m5ui.init()
        page0 = m5ui.M5Page()
        self.roller0 = m5ui.M5Roller(options=["a", "b", "c"], x=81, y=93, w=200, parent=page0)
        page0.screen_load()

    def test_get_options(self):
        self.roller0.set_options(["a", "b", "c"], lv.roller.MODE.NORMAL)
        self.assertEqual(self.roller0.get_options(), ["a", "b", "c"])

    def test_get_selected_str(self):
        self.roller0.set_selected(0, True)
        self.assertEqual(self.roller0.get_selected_str(), "a")
        self.roller0.set_selected(1, True)
        self.assertEqual(self.roller0.get_selected_str(), "b")

    def test_get_selected(self):
        self.roller0.set_selected(0, True)
        self.assertEqual(self.roller0.get_selected(), 0)
        self.roller0.set_selected(1, True)
        self.assertEqual(self.roller0.get_selected(), 1)


if __name__ == "__main__":
    unittest.main()
