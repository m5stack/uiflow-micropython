# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from m5ui.base import M5Base
import lvgl as lv


class M5Line(lv.line):
    """Create a line object.

    :param list points: A list of points where each point is a pair of x and y coordinates.
    :param int width: The width of the line.
    :param int color: The color of the line in hexadecimal format.
    :param bool rounded: If True, the line will have rounded ends; otherwise, it will have square ends.
    :param lv.obj parent: The parent object to attach the line to. If not specified, the line will be attached to the default screen.

    MicroPython Code Block:

        .. code-block:: python

            from m5ui import M5Image
            import lvgl as lv

            m5ui.init()
            line_0 = M5Line(
                points=[5, 5, 70, 70, 120, 10, 180, 60, 240, 20],
                width=2,
                color=0x2196F3,
                rounded=True,
                parent=page0,
            )
    """

    def __init__(
        self,
        points=list([]),
        width=1,
        color=0x3F51B5,
        rounded=True,
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)

        self.set_points(points)
        self.set_line_color(color, 255)
        self.set_style_line_width(width, lv.PART.MAIN)
        self.set_style_line_rounded(rounded, lv.PART.MAIN)

    def set_points(self, points: list):
        """Set the points of the line.

        :param list points: A list of points where each point is a pair of x and y coordinates.

        UiFlow2 Code Block:

            |set_points.png|

        MicroPython Code Block:

            .. code-block:: python

                line_0.set_points([0, 0, 100, 100, 200, 50])
        """
        self.lv_points = []
        for i in range(0, len(points), 2):
            self.lv_points.append({"x": points[i], "y": points[i + 1]})
        super().set_points(self.lv_points, len(self.lv_points))

    def add_point(self, x, y):
        """Add a point to the line end.

        :param int x: The x position of the point.
        :param int y: The y position of the point.

        UiFlow2 Code Block:

            |add_point.png|

        MicroPython Code Block:

            .. code-block:: python

                line_0.add_point(100, 100)
        """
        self.lv_points.append({"x": x, "y": y})
        super().set_points(self.lv_points, len(self.lv_points))

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
