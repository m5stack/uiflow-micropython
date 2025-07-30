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
        self.textarea0 = m5ui.M5TextArea(x=10, y=10, w=200, h=60, parent=page0)
        self.buttonmatrix0 = m5ui.M5ButtonMatrix(
            ["0", "1", "2", "4", "\n", "5", "6", "7", "8", "9"],
            x=25,
            y=100,
            w=260,
            h=130,
            target_textarea=self.textarea0,
            parent=page0,
        )
        page0.screen_load()

    def test_get_textarea(self):
        self.buttonmatrix0.set_textarea(None)
        self.assertIsNone(self.buttonmatrix0.textarea)
        self.buttonmatrix0.set_textarea(self.textarea0)
        self.assertIsInstance(self.buttonmatrix0.textarea, m5ui.M5TextArea)

    def test_toggle_button_ctrl(self):
        self.buttonmatrix0.toggle_button_ctrl(0, lv.buttonmatrix.CTRL.NO_REPEAT)
        self.assertTrue(self.buttonmatrix0.has_button_ctrl(0, lv.buttonmatrix.CTRL.NO_REPEAT))

    def test_text_area_update(self):
        self.textarea0.set_text("")
        self.buttonmatrix0.set_selected_button(0)
        self.buttonmatrix0.send_event(lv.EVENT.VALUE_CHANGED, None)
        self.assertEqual(self.textarea0.get_text(), "0")

        self.buttonmatrix0.set_selected_button(1)
        self.buttonmatrix0.send_event(lv.EVENT.VALUE_CHANGED, None)
        self.assertEqual(self.textarea0.get_text(), "01")

        self.buttonmatrix0.set_selected_button(2)
        self.buttonmatrix0.send_event(lv.EVENT.VALUE_CHANGED, None)
        self.assertEqual(self.textarea0.get_text(), "012")


if __name__ == "__main__":
    unittest.main()
