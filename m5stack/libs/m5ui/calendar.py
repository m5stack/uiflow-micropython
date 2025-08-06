# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from m5ui.base import M5Base
import lvgl as lv


class M5Calendar(lv.calendar):
    """Create a calendar object.

    :param int x: The x position of the calendar.
    :param int y: The y position of the calendar.
    :param int w: The width of the calendar.
    :param int h: The height of the calendar.
    :param str style: The style of the calendar, can be "arrow" or "dropdown" and None.
    :param list today_date: The date to highlight as today in the format [year, month, day].
    :param list show_month: The month to show in the format [year, month].
    :param lv.obj parent: The parent object to attach the calendar to. If not specified, the calendar will be attached to the default screen.

    UiFlow2 Code Block:

        None

    MicroPython Code Block:

        .. code-block:: python

            from m5ui import M5Calendar
            import lvgl as lv

            m5ui.init()
            calendar_0 = M5Calendar(x=0, y=0, w=200, h=200, style=None, today_date=[2024, 1, 1], show_month=[2024, 1], parent=page0)
    """

    def __init__(
        self,
        x=0,
        y=0,
        w=200,
        h=200,
        style="arrow",
        today_date=[2024, 1, 1],
        show_month=[2024, 1],
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)
        self.header = None
        self.set_pos(x, y)
        self.set_size(w, h)
        self.set_calendar_style(style)
        self.set_today_date(*today_date)
        self.set_month_shown(*show_month)

    def set_calendar_style(self, style):
        """Set the style of the calendar header.

        :param str style: The style of the calendar header, can be "arrow", "dropdown", or None.

        UiFlow2 Code Block:

            |set_calendar_style.png|

        MicroPython Code Block:

            .. code-block:: python

                calendar_0.set_calendar_style("arrow")
                calendar_0.set_calendar_style("dropdown")
                calendar_0.set_calendar_style(None)
        """
        if self.header:
            self.header.delete()
            self.header = None

        if style == "arrow":
            self.header = lv.calendar_header_arrow(self)
        elif style == "dropdown":
            self.header = lv.calendar_header_dropdown(self)

    def set_highlighted_dates(self, dates):
        """Set the highlighted dates in the calendar.

        :param list dates: A list of dates to highlight in the format [year, month, day, year, month, day, ...]

        UiFlow2 Code Block:

            |set_highlighted_dates.png|

        MicroPython Code Block:

            .. code-block:: python

                calendar_0.set_highlighted_dates([2024, 1, 1, 2024, 1, 2, 2024, 1, 3])
        """
        self.highlighted_days = []
        for i in range(0, len(dates), 3):
            self.highlighted_days.append(
                {"year": dates[i], "month": dates[i + 1], "day": dates[i + 2]}
            )
        super().set_highlighted_dates(self.highlighted_days, len(self.highlighted_days))

    def set_style_radius(self, radius: int, part: int) -> None:
        if radius < 0:
            raise ValueError("Radius must be a non-negative integer.")
        super().set_style_radius(radius, part)

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
