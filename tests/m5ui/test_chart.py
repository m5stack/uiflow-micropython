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
        self.chart0 = m5ui.M5Chart(
            x=10, y=10, w=200, h=100, chart_type=lv.chart.TYPE.LINE, parent=page0
        )
        self.chart0.x_axis_init()
        self.chart0.y_axis1_init()
        self.chart0.y_axis2_init()
        self.series_lbv = self.chart0.add_series(0xFF0000, lv.chart.AXIS.PRIMARY_Y)
        page0.screen_load()

    def test_series_color(self):
        self.assertEqual(self.chart0.get_series_color(self.series_lbv), 0xFF0000)


if __name__ == "__main__":
    unittest.main()
