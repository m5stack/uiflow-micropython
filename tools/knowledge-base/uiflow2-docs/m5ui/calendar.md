<!-- .. currentmodule:: m5ui -->

# M5Calendar

<!-- .. include:: ../refs/m5ui.calendar.ref -->

M5Calendar is a widget that can be used to create a calendar in the user interface. It can be used to display and select dates.

## UiFlow2 Example

#### event calendar

Open the |calendar_core2_example.m5f2| project in UiFlow2.

This example creates a calendar that triggers an event when the date is changed.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### event calendar

This example creates a calendar that triggers an event when the date is changed.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv

page0 = None
calendar0 = None

year = None
month = None
day = None

def calendar0_value_changed_event(date):
    global page0, calendar0, year, month, day
    year = date.year
    month = date.month
    day = date.day
    calendar0.set_today_date(year, month, day)
    print((str("Today is:") + str((str(year) + str((str(month) + str(day)))))))

def calendar0_event_handler(event_struct):
    global page0, calendar0, year, month, day
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED:
        date = lv.calendar_date_t()
        if calendar0.get_pressed_date(date) == lv.RESULT.OK:
            calendar0_value_changed_event(date)
    return

def setup():
    global page0, calendar0, year, month, day

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    calendar0 = m5ui.M5Calendar(
        x=0,
        y=0,
        w=320,
        h=240,
        style="arrow",
        today_date=[2025, 8, 7],
        show_month=[2025, 8],
        parent=page0,
    )

    calendar0.add_event_cb(calendar0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()

def loop():
    global page0, calendar0, year, month, day
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

```

Example output:

    None

## **API**

#### M5Calendar

## M5Calendar
Create a calendar object.

:param int x: The x position of the calendar.
:param int y: The y position of the calendar.
:param int w: The width of the calendar.
:param int h: The height of the calendar.
:param str style: The style of the calendar, can be "arrow" or "dropdown" and None.
:param list today_date: The date to highlight as today in the format [year, month, day].
:param list show_month: The month to show in the format [year, month].
:param lv.obj parent: The parent object to attach the calendar to. If not specified, the calendar will be attached to the default screen.

MicroPython Code Block:

    .. code-block:: python

        from m5ui import M5Calendar
        import lvgl as lv

        m5ui.init()
        calendar_0 = M5Calendar(x=0, y=0, w=200, h=200, style=None, today_date=[2024, 1, 1], show_month=[2024, 1], parent=page0)

### `set_calendar_style`
Set the style of the calendar header.

:param str style: The style of the calendar header, can be "arrow", "dropdown", or None.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        calendar_0.set_calendar_style("arrow")
        calendar_0.set_calendar_style("dropdown")
        calendar_0.set_calendar_style(None)

### `set_highlighted_dates`
Set the highlighted dates in the calendar.

:param list dates: A list of dates to highlight in the format [year, month, day, year, month, day, ...]

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        calendar_0.set_highlighted_dates([2024, 1, 1, 2024, 1, 2, 2024, 1, 3])

### `set_style_radius`

<!-- .. py:method:: set_month_shown(year, month) -->

        Set the month and year shown in the calendar.

        :param int year: The year to show.
        :param int month: The month to show.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                calendar_0.set_month_shown(2023, 3)

<!-- .. py:method:: set_pos(x, y) -->

        Set the position of the calendar.

        :param int x: The x-coordinate of the calendar.
        :param int y: The y-coordinate of the calendar.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                calendar_0.set_pos(100, 100)

<!-- .. py:method:: set_x(x) -->

        Set the x-coordinate of the calendar.

        :param int x: The x-coordinate of the calendar.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                calendar_0.set_x(100)

<!-- .. py:method:: set_y(y) -->

        Set the y-coordinate of the calendar.

        :param int y: The y-coordinate of the calendar.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                calendar_0.set_y(100)

<!-- .. py:method:: set_size(width, height) -->

        Set the size of the calendar.

        :param int width: The width of the calendar.
        :param int height: The height of the calendar.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                calendar_0.set_size(100, 50)

<!-- .. py:method:: align_to(obj, align, x, y) -->

        Align the calendar to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                calendar_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)

<!-- .. py:method:: add_event_cb(handler, event, user_data) -->

        Add an event callback to the calendar. The callback will be called when the specified event occurs.

        :param function handler: The callback function to call.
        :param int event: The event to listen for.
        :param Any user_data: Optional user data to pass to the callback.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                def calendar_event_handler(event_struct):
                    if event_struct.get_code() == lv.EVENT.VALUE_CHANGED:
                        date = lv.calendar_date_t()
                        if calendar_0.get_pressed_date(date) == lv.RESULT.OK:
                            calendar_0.set_today_date(date.year, date.month, date.day)
                            print("Clicked date: %02d.%02d.%02d" % (date.year, date.month, date.day))

                calendar_0.add_event_cb(calendar_event_handler, lv.EVENT.ALL, None)
