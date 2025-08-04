# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import lvgl as lv
import time


class M5Base:
    @staticmethod
    def set_flag(self, flag: int, value: bool) -> None:
        """Set a flag on the object. If `value` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.
        :return: None
        """
        if value:
            self.add_flag(flag)
        else:
            self.remove_flag(flag)

    @staticmethod
    def toggle_flag(self, flag):
        """Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        """
        if self.has_flag(flag):
            self.remove_flag(flag)
        else:
            self.add_flag(flag)

    @staticmethod
    def set_state(self, state: int, value: bool) -> None:
        """Set a state on the object.

        :param int state: The state to set.
        :param bool value: If True, the state is added; if False, the state is removed.
        :return: None
        """
        if value:
            self.add_state(state)
        else:
            self.clear_state(state)

    @staticmethod
    def toggle_state(self, state: int) -> None:
        """Toggle a state on the object. If the state is set, it is removed; if not set, it is added.

        :param int state: The state to toggle.
        :return: None
        """
        if self.has_state(state):
            self.remove_state(state)
        else:
            self.add_state(state)
        return

    @staticmethod
    def set_text_color(self, color: int, opa: int, part: int) -> None:
        """Set the text color and opacity for a given part of the object.

        :param int color: The color to set, can be an integer (hex) or a lv.color object.
        :param int opa: The opacity level (0-255).
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None
        """
        if isinstance(color, int):
            color = lv.color_hex(color)

        self.set_style_text_color(color, part)
        time.sleep(0.01)
        self.set_style_text_opa(opa, part)

    @staticmethod
    def set_line_color(self, color: int, opa: int, part: int) -> None:
        """Set the line color and opacity for a given part of the object.

        :param int color: The color to set, can be an integer (hex) or a lv.color object.
        :param int opa: The opacity level (0-255).
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None
        """
        if isinstance(color, int):
            color = lv.color_hex(color)

        self.set_style_line_color(color, part)
        time.sleep(0.01)
        self.set_style_line_opa(opa, part)

    @staticmethod
    def set_bg_color(self, color: int, opa: int, part: int) -> None:
        """Set the background color and opacity for a given part of the object.

        :param int color: The color to set, can be an integer (hex) or a lv.color object.
        :param int opa: The opacity level (0-255).
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None
        """
        if isinstance(color, int):
            color = lv.color_hex(color)

        self.set_style_bg_color(color, part)
        time.sleep(0.01)
        self.set_style_bg_opa(opa, part)

    @staticmethod
    def set_bg_grad_color(self, color, opa, grad_color, grad_opd, grad_dir, part: int) -> None:
        """Set the background gradient color of the bar.

        :param int color: The start color of the gradient, can be an integer (RGB).
        :param int opa: The opacity of the start color (0-255).
        :param int grad_color: The end color of the gradient, can be an integer (RGB).
        :param int grad_opd: The opacity of the end color (0-255).
        :param int grad_dir: The direction of the gradient (e.g., lv.GRAD_DIR.VER).
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None
        """
        if isinstance(color, int):
            color = lv.color_hex(color)

        if isinstance(grad_color, int):
            grad_color = lv.color_hex(grad_color)

        # start color and opacity
        self.set_style_bg_color(color, part)
        time.sleep(0.01)
        self.set_style_bg_opa(opa, part)
        time.sleep(0.01)

        # end color and opacity
        self.set_style_bg_grad_color(grad_color, part)
        time.sleep(0.01)
        self.set_style_bg_grad_opa(grad_opd, part)
        time.sleep(0.01)
        self.set_style_bg_grad_dir(grad_dir, part)
        time.sleep(0.01)

    def set_border_color(self, color: int, opa: int, part: int):
        """Set the border color and opacity for a given part of the object.

        :param int color: The color to set, can be an integer (hex) or a lv.color object.
        :param int opa: The opacity level (0-255).
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None
        """
        if isinstance(color, int):
            color = lv.color_hex(color)

        self.set_style_border_color(color, part)
        time.sleep(0.01)
        self.set_style_border_opa(opa, part)
