.. currentmodule:: m5ui

M5Calendar
==========

.. include:: ../refs/m5ui.calendar.ref

M5Calendar is a widget that can be used to create a calendar in the user interface. It can be used to display and select dates.

UiFlow2 Example
---------------

event calendar
^^^^^^^^^^^^^^

Open the |cores3_calendar_event_example.m5f2| project in UiFlow2.

This example creates a calendar that triggers an event when the date is changed.

UiFlow2 Code Block:

    |cores3_calendar_event_example.png|

Example output:

    None


MicroPython Example
-------------------

event calendar
^^^^^^^^^^^^^^

This example creates a calendar that triggers an event when the date is changed.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/calendar/cores3_calendar_event_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

M5Calendar
^^^^^^^^^^

.. autoclass:: m5ui.calendar.M5Calendar
    :members:
    :member-order: bysource

    .. py:method:: set_month_shown(year, month)

        Set the month and year shown in the calendar.

        :param int year: The year to show.
        :param int month: The month to show.

        UiFlow2 Code Block:

            |set_month_shown.png|

        MicroPython Code Block:

            .. code-block:: python

                calendar_0.set_month_shown(2023, 3)

    .. py:method:: set_pos(x, y)

        Set the position of the calendar.

        :param int x: The x-coordinate of the calendar.
        :param int y: The y-coordinate of the calendar.

        UiFlow2 Code Block:

            |set_pos.png|

        MicroPython Code Block:

            .. code-block:: python

                calendar_0.set_pos(100, 100)

    .. py:method:: set_x(x)

        Set the x-coordinate of the calendar.

        :param int x: The x-coordinate of the calendar.

        UiFlow2 Code Block:

            |set_x.png|

        MicroPython Code Block:

            .. code-block:: python

                calendar_0.set_x(100)

    .. py:method:: set_y(y)

        Set the y-coordinate of the calendar.

        :param int y: The y-coordinate of the calendar.

        UiFlow2 Code Block:

            |set_y.png|

        MicroPython Code Block:

            .. code-block:: python

                calendar_0.set_y(100)

    .. py:method:: set_size(width, height)

        Set the size of the calendar.

        :param int width: The width of the calendar.
        :param int height: The height of the calendar.

        UiFlow2 Code Block:

            |set_size.png|

        MicroPython Code Block:

            .. code-block:: python

                calendar_0.set_size(100, 50)

    .. py:method:: set_width(width)

        Set the width of the calendar.

        :param int width: The width of the calendar.

        UiFlow2 Code Block:

            |set_width.png|

        MicroPython Code Block:

            .. code-block:: python

                calendar_0.set_width(100)

    .. py:method:: set_height(height)

        Set the height of the calendar.

        :param int height: The height of the calendar.

        UiFlow2 Code Block:

            |set_height.png|

        MicroPython Code Block:

            .. code-block:: python

                calendar_0.set_height(50)

    .. py:method:: align_to(obj, align, x, y)

        Align the calendar to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.

        UiFlow2 Code Block:

            |align_to.png|

        MicroPython Code Block:

            .. code-block:: python

                calendar_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)

    .. py:method:: add_event_cb(handler, event, user_data)

        Add an event callback to the calendar. The callback will be called when the specified event occurs.

        :param function handler: The callback function to call.
        :param int event: The event to listen for.
        :param Any user_data: Optional user data to pass to the callback.

        UiFlow2 Code Block:

            |event.png|

        MicroPython Code Block:

            .. code-block:: python

                def calendar_event_handler(event_struct):
                    if event_struct.get_code() == lv.EVENT.VALUE_CHANGED:
                        date = lv.calendar_date_t()
                        if calendar_0.get_pressed_date(date) == lv.RESULT.OK:
                            calendar_0.set_today_date(date.year, date.month, date.day)
                            print("Clicked date: %02d.%02d.%02d" % (date.year, date.month, date.day))

                calendar_0.add_event_cb(calendar_event_handler, lv.EVENT.ALL, None)
