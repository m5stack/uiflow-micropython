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
        self.spinbox1 = m5ui.M5Spinbox(
            x=0,
            y=0,
            w=200,
            h=40,
            value=50,
            min_value=0,
            max_value=100,
            digit_count=5,
            prec=2,  # 小数点位数 000.00
            parent=page0,
        )
        page0.screen_load()

    def test_set_get_value(self):
        self.spinbox1.set_value(75)
        self.assertEqual(self.spinbox1.get_value(), 75)

    def test_set_range(self):
        self.spinbox1.set_value(100)
        self.spinbox1.set_range(10, 90)
        self.assertEqual(self.spinbox1.get_value(), 90)

    def test_set_rollover(self):
        self.spinbox1.set_rollover(True)
        self.assertTrue(self.spinbox1.get_rollover())

    def test_step(self):
        self.spinbox1.set_value(50)
        self.spinbox1.set_range(0, 100)
        self.spinbox1.set_step(10)
        self.spinbox1.increment()
        self.assertEqual(self.spinbox1.get_value(), 60)
        self.spinbox1.decrement()
        self.assertEqual(self.spinbox1.get_value(), 50)

        self.spinbox1.set_step(1)
        self.spinbox1.increment()
        self.assertEqual(self.spinbox1.get_value(), 51)
        self.spinbox1.decrement()
        self.assertEqual(self.spinbox1.get_value(), 50)

        self.spinbox1.set_step(0.1)
        self.spinbox1.increment()
        self.assertEqual(self.spinbox1.get_value(), 50.1)
        self.spinbox1.decrement()
        self.assertEqual(self.spinbox1.get_value(), 50)

        self.spinbox1.set_step(0.01)
        self.spinbox1.increment()
        self.assertEqual(self.spinbox1.get_value(), 50.01)
        self.spinbox1.decrement()
        self.assertEqual(self.spinbox1.get_value(), 50)

    def test_set_size(self):
        self.spinbox1.set_size(150, 30)
        self.assertEqual((self.spinbox1.get_width(), self.spinbox1.get_height()), (150, 30))

    def test_set_width(self):
        self.spinbox1.set_width(180)
        self.assertEqual(self.spinbox1.get_width(), 180)

    def test_set_height(self):
        self.spinbox1.set_height(35)
        self.assertEqual(self.spinbox1.get_height(), 35)


if __name__ == "__main__":
    unittest.main()
