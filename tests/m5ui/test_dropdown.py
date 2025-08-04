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
        self.dropdown0 = m5ui.M5Dropdown(options=["a", "b", "c"], x=81, y=93, w=200, parent=page0)
        page0.screen_load()

    def test_get_options(self):
        self.assertEqual(self.dropdown0.get_options(), ["a", "b", "c"])

    def test_get_selected_str(self):
        self.dropdown0.set_selected(0, True)
        self.assertEqual(self.dropdown0.get_selected_str(), "a")
        self.dropdown0.set_selected(1, True)
        self.assertEqual(self.dropdown0.get_selected_str(), "b")

    def test_clear_options(self):
        self.dropdown0.clear_options()
        self.assertEqual(self.dropdown0.get_options(), [])

    def test_set_options(self):
        self.dropdown0.set_options(["a", "b", "c"])
        self.assertEqual(self.dropdown0.get_options(), ["a", "b", "c"])

    def test_get_option_index(self):
        self.dropdown0.set_options(["a", "b", "c"])
        self.assertEqual(self.dropdown0.get_option_index("a"), 0)
        self.assertEqual(self.dropdown0.get_option_index("b"), 1)
        self.assertEqual(self.dropdown0.get_option_index("c"), 2)
        self.assertEqual(self.dropdown0.get_option_index("d"), -1)

    def test_get_text(self):
        self.dropdown0.set_text("abc")
        self.assertEqual(self.dropdown0.get_text(), "abc")

    def test_add_option(self):
        self.dropdown0.add_option("d", 0)
        self.assertEqual(self.dropdown0.get_options(), ["d", "a", "b", "c"])
        self.assertEqual(self.dropdown0.get_option_index("d"), 0)


if __name__ == "__main__":
    unittest.main()
