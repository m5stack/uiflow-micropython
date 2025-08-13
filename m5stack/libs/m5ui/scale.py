# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from m5ui.base import M5Base
import lvgl as lv


class M5Scale(lv.scale):
    """Create a scale object.

    :param int x: The x position of the scale.
    :param int y: The y position of the scale.
    :param int w: The width of the scale. If not specified, it will be set based on the mode.
    :param int h: The height of the scale. If not specified, it will be set based on the mode.
    :param int start_pos: The starting position of the scale.
    :param int end_pos: The ending position of the scale.
    :param int tick_count: The total number of ticks on the scale.
    :param int tick_every: The interval between major ticks on the scale.
    :param int mode: The mode of the scale. It can be one of the following:

        Options:

            - `lv.scale.MODE.HORIZONTAL_TOP`: Horizontal top scale.
            - `lv.scale.MODE.HORIZONTAL_BOTTOM`: Horizontal bottom scale.
            - `lv.scale.MODE.VERTICAL_LEFT`: Vertical left scale.
            - `lv.scale.MODE.VERTICAL_RIGHT`: Vertical right scale.
            - `lv.scale.MODE.ROUND_INNER`: Round inner scale.
            - `lv.scale.MODE.ROUND_OUTER`: Round outer scale.

    :param lv.obj parent: The parent object to attach the scale to. If not specified, the scale will be attached to the default screen.

    MicroPython Code Block:

        .. code-block:: python

            from m5ui import M5Scale
            import lvgl as lv

            m5ui.init()
            scale_0 = M5Scale(x=10, y=10, w=200, h=20, start_pos=0, end_pos=100, tick_count=11, tick_every=2, mode=lv.scale.MODE.HORIZONTAL_TOP, parent=page0)
    """

    def __init__(
        self,
        x=0,
        y=0,
        w=0,
        h=0,
        start_pos=0,
        end_pos=100,
        tick_count=11,
        tick_every=2,
        show_mode=lv.scale.MODE.HORIZONTAL_BOTTOM,
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)
        self.set_pos(x, y)
        self.set_range(start_pos, end_pos)
        self.set_total_tick_count(tick_count)
        self.set_major_tick_every(tick_every)
        self.set_mode(show_mode)
        if show_mode in [
            lv.scale.MODE.HORIZONTAL_TOP,
            lv.scale.MODE.HORIZONTAL_BOTTOM,
        ]:
            self.set_size(w, 20)
        elif show_mode in [
            lv.scale.MODE.VERTICAL_LEFT,
            lv.scale.MODE.VERTICAL_RIGHT,
        ]:
            self.set_size(20, h)
        else:
            r = max(w, h)
            self.set_size(r, r)

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
