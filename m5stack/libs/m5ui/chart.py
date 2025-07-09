# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .base import M5Base
import lvgl as lv
import warnings


class M5Chart(lv.chart):
    """Create a Chart object.

    :param int x: X coordinate of the chart's position. Default is 0.
    :param int y: Y coordinate of the chart's position. Default is 0.
    :param int w: Width of the chart. Default is 200.
    :param int h: Height of the chart. Default is 100.
    :param int chart_type: Type of the chart. lv.chart.TYPE.LINE, lv.chart.TYPE.BAR, etc. Default is lv.chart.TYPE.LINE.
    :param int point_num: Number of points in the chart. Default is 10.
    :param int hdiv: Number of horizontal division lines. Default is 0 (no lines).
    :param int vdiv: Number of vertical division lines. Default is 0 (no lines).
    :param int bg_radius: Background corner radius. Default is 7.
    :param int bg_c: Background color in hex format. Default is 0xFFFFFF (white).
    :param int border_c: Border color in hex format. Default is 0xE0E0E0 (light gray).
    :param int border_w: Border width. Default is 2.
    :param lv.obj parent: Parent LVGL object. Default is the active screen.
    """

    def __init__(
        self,
        x=0,
        y=0,
        w=200,
        h=100,
        chart_type=lv.chart.TYPE.LINE,
        point_num=10,
        hdiv=0,
        vdiv=0,
        bg_radius=7,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        border_w=2,
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)
        self.set_pos(x, y)
        self.set_size(w, h)
        self.set_type(chart_type)
        self.set_flag(lv.obj.FLAG.OVERFLOW_VISIBLE, True)
        self.set_flag(lv.obj.FLAG.SCROLLABLE, False)
        self.set_style_outline_pad(max(50, 50, 25), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_style_outline_width(-1, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.set_point_count(point_num)
        self.set_div_line_count(hdiv, vdiv)
        self.set_style_radius(bg_radius, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_style_bg_color(lv.color_hex(bg_c), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_border_color(
            lv.color_hex(border_c), lv.OPA.COVER, lv.PART.MAIN | lv.STATE.DEFAULT
        )
        self.set_style_border_width(border_w, lv.PART.MAIN | lv.STATE.DEFAULT)

    def x_axis_init(
        self,
        width=lv.pct(100),
        height=50,
        mode=lv.scale.MODE.HORIZONTAL_BOTTOM,
        min_value=0,
        max_value=100,
        major_ticks=5,
        major_tick_len=10,
        minor_ticks=2,
        minor_tick_len=5,
        label_show=True,
    ):
        """Initialize the X axis.

        :param int width: Width of the X axis. Default is lv.pct(100).
        :param int height: Height of the X axis. Default is 50.
        :param int mode: Mode of the X axis. Default is lv.scale.MODE.HORIZONTAL_BOTTOM.
        :param int min_value: Minimum value of the X axis. Default is 0.
        :param int max_value: Maximum value of the X axis. Default is 100.
        :param int major_ticks: Number of major ticks on the X axis. Default is 5.
        :param int major_tick_len: Length of major ticks. Default is 10.
        :param int minor_ticks: Number of minor ticks between major ticks. Default is 2.
        :param int minor_tick_len: Length of minor ticks. Default is 5.
        :param bool label_show: Whether to show labels on the X axis. Default is True.
        """
        if not hasattr(self, "x_axis"):
            self.x_axis = lv.scale(self)
        self.x_axis.set_mode(mode)
        self.x_axis.set_size(width, height)
        self.x_axis.set_align(lv.ALIGN.BOTTOM_MID)
        self.x_axis.set_y(
            height
            + self.get_style_pad_bottom(lv.PART.MAIN)
            + self.get_style_border_width(lv.PART.MAIN)
        )
        self.x_axis.set_range(min_value, max_value)
        super().set_axis_range(lv.chart.AXIS.PRIMARY_X, min_value, max_value)
        self.x_axis.set_total_tick_count(major_ticks * minor_ticks + 1)
        self.x_axis.set_major_tick_every(minor_ticks if minor_ticks >= 1 else 1)
        self.x_axis.set_style_line_width(0, lv.PART.MAIN)
        self.x_axis.set_style_line_width(1, lv.PART.ITEMS)
        self.x_axis.set_style_line_width(1, lv.PART.INDICATOR)
        self.x_axis.set_style_length(major_tick_len, lv.PART.INDICATOR)
        self.x_axis.set_style_length(minor_tick_len, lv.PART.ITEMS)
        self.x_axis.set_label_show(label_show)

    def y_axis1_init(
        self,
        width=50,
        height=lv.pct(100),
        mode=lv.scale.MODE.VERTICAL_LEFT,
        min_value=0,
        max_value=100,
        major_ticks=5,
        major_tick_len=10,
        minor_ticks=2,
        minor_tick_len=5,
        label_show=True,
    ):
        """Initialize the primary Y axis.

        :param int width: Width of the Y axis. Default is 50.
        :param int height: Height of the Y axis. Default is lv.pct(100).
        :param int mode: Mode of the Y axis. Default is lv.scale.MODE.VERTICAL_LEFT.
        :param int min_value: Minimum value of the Y axis. Default is 0.
        :param int max_value: Maximum value of the Y axis. Default is 100.
        :param int major_ticks: Number of major ticks on the Y axis. Default is 5.
        :param int major_tick_len: Length of major ticks. Default is 10.
        :param int minor_ticks: Number of minor ticks between major ticks. Default is 2.
        :param int minor_tick_len: Length of minor ticks. Default is 5.
        :param bool label_show: Whether to show labels on the Y axis. Default is True.

        """
        if not hasattr(self, "y_axis1"):
            self.y_axis1 = lv.scale(self)
        self.y_axis1.set_mode(mode)
        self.y_axis1.set_size(width, height)
        self.y_axis1.set_align(lv.ALIGN.LEFT_MID)
        self.y_axis1.set_x(
            -width
            - self.get_style_pad_left(lv.PART.MAIN)
            - self.get_style_border_width(lv.PART.MAIN)
            + 2
        )
        self.y_axis1.set_range(min_value, max_value)
        super().set_axis_range(lv.chart.AXIS.PRIMARY_Y, min_value, max_value)
        self.y_axis1.set_total_tick_count(major_ticks * minor_ticks + 1)
        self.y_axis1.set_major_tick_every(minor_ticks if minor_ticks >= 1 else 1)
        self.y_axis1.set_style_line_width(0, lv.PART.MAIN)
        self.y_axis1.set_style_line_width(1, lv.PART.ITEMS)
        self.y_axis1.set_style_line_width(1, lv.PART.INDICATOR)
        self.y_axis1.set_style_length(major_tick_len, lv.PART.INDICATOR)
        self.y_axis1.set_style_length(minor_tick_len, lv.PART.ITEMS)
        self.y_axis1.set_label_show(label_show)

    def y_axis2_init(
        self,
        width=50,
        height=lv.pct(100),
        mode=lv.scale.MODE.VERTICAL_RIGHT,
        min_value=0,
        max_value=100,
        major_ticks=5,
        major_tick_len=10,
        minor_ticks=2,
        minor_tick_len=5,
        label_show=True,
    ):
        """Initialize the secondary Y axis.

        :param int width: Width of the Y axis. Default is 50.
        :param int height: Height of the Y axis. Default is lv.pct(100).
        :param int mode: Mode of the Y axis. Default is lv.scale.MODE.VERTICAL_RIGHT.
        :param int min_value: Minimum value of the Y axis. Default is 0.
        :param int max_value: Maximum value of the Y axis. Default is 100.
        :param int major_ticks: Number of major ticks on the Y axis. Default is 5.
        :param int major_tick_len: Length of major ticks. Default is 10.
        :param int minor_ticks: Number of minor ticks between major ticks. Default is 2.
        :param int minor_tick_len: Length of minor ticks. Default is 5.
        :param bool label_show: Whether to show labels on the Y axis. Default is True

        """
        if not hasattr(self, "y_axis2"):
            self.y_axis2 = lv.scale(self)
        self.y_axis2.set_mode(mode)
        self.y_axis2.set_size(width, height)
        self.y_axis2.set_align(lv.ALIGN.RIGHT_MID)
        self.y_axis2.set_x(
            width
            + self.get_style_pad_right(lv.PART.MAIN)
            + self.get_style_border_width(lv.PART.MAIN)
            + 1
        )
        self.y_axis2.set_range(min_value, max_value)
        super().set_axis_range(lv.chart.AXIS.SECONDARY_Y, min_value, max_value)
        self.y_axis2.set_total_tick_count(major_ticks * minor_ticks + 1)
        self.y_axis2.set_major_tick_every(minor_ticks if minor_ticks >= 1 else 1)
        self.y_axis2.set_style_line_width(0, lv.PART.MAIN)
        self.y_axis2.set_style_line_width(1, lv.PART.ITEMS)
        self.y_axis2.set_style_line_width(1, lv.PART.INDICATOR)
        self.y_axis2.set_style_length(major_tick_len, lv.PART.INDICATOR)
        self.y_axis2.set_style_length(minor_tick_len, lv.PART.ITEMS)
        self.y_axis2.set_label_show(label_show)

    def set_axis_range(self, axis, min_value, max_value):
        """Set the range of the specified axis.

        :param int axis: Axis to set the range for. lv.chart.AXIS.PRIMARY_X, lv.chart.AXIS.PRIMARY_Y, or lv.chart.AXIS.SECONDARY_Y.
        :param int min_value: Minimum value of the axis.
        :param int max_value: Maximum value of the axis.

        UiFlow2 Code Block:

            |set_axis_range.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 200)
        """
        if axis == lv.chart.AXIS.PRIMARY_X:
            if hasattr(self, "x_axis"):
                self.x_axis.set_range(min_value, max_value)
            else:
                warnings.warn("x_axis is not initialized")
        if axis == lv.chart.AXIS.PRIMARY_Y:
            if hasattr(self, "y_axis1"):
                self.y_axis1.set_range(min_value, max_value)
            else:
                warnings.warn("y_axis1 is not initialized")
        elif axis == lv.chart.AXIS.SECONDARY_Y:
            if hasattr(self, "y_axis2"):
                self.y_axis2.set_range(min_value, max_value)
            else:
                warnings.warn("y_axis2 is not initialized")
        super().set_axis_range(axis, min_value, max_value)

    def add_series(self, color, axis):
        """Add a data series to the chart.

        :param int color: Color of the series in hex format.
        :param int axis: Axis to associate the series with. lv.chart.AXIS.PRIMARY_Y or lv.chart.AXIS.SECONDARY_Y.

        UiFlow2 Code Block:

            |add_series.png|

        MicroPython Code Block:

            .. code-block:: python

                series_0 = chart_0.add_series(0xFF0000, lv.chart.AXIS.PRIMARY_Y)
        """
        if isinstance(color, int):
            color = lv.color_hex(color)

        return super().add_series(color, axis)

    def set_series_color(self, series, color):
        """Set the color of a data series.

        :param series: Series to set the color for.
        :param int color: Color of the series in hex format.

        UiFlow2 Code Block:

            |set_series_color.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.set_series_color(series_0, 0x00FF00)
        """
        if isinstance(color, int):
            color = lv.color_hex(color)

        return super().set_series_color(series, color)

    def get_series_color(self, series) -> int:
        """Get the color of a data series.

        :param series: Series to get the color for.
        :return: Color of the series in hex format.

        UiFlow2 Code Block:

            |get_series_color.png|

        MicroPython Code Block:

            .. code-block:: python

                color = chart_0.get_series_color(series_0)
        """
        color = super().get_series_color(series)
        return color.to_int()

    def set_series_values(self, series, values, size=-1):
        """Set the values of a data series.

        :param series: Series to set the values for.
        :param list values: List of values to set.
        :param int size: Number of values to set. Default is -1 (set all values).

        UiFlow2 Code Block:

            |set_series_values.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.set_series_values(series_0, [10, 20, 30, 40, 50])
        """
        if size < 0:
            size = len(values)
        super().set_series_values(series, values, size)

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
