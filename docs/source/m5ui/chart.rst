.. currentmodule:: m5ui

M5Chart
=======

.. include:: ../refs/m5ui.chart.ref

M5Chart is a versatile charting widget that allows users to create various types of charts, including line charts and bar charts. It provides features for data visualization, customization, and interactivity within the user interface.

UiFlow2 Example
---------------

Temperature Line Chart
^^^^^^^^^^^^^^^^^^^^^^

Open the |cores3_chart_line_example.m5f2| project in UiFlow2.

This example demonstrates how to create a line chart to visualize temperature data over time.

UiFlow2 Code Block:

    |cores3_chart_line_example.png|

Example output:

    A line chart displaying temperature data with labeled axes and grid lines.


MicroPython Example
-------------------

Temperature Line Chart
^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to create a line chart programmatically to visualize temperature data.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/chart/cores3_chart_line_example.py

Example output:

    A line chart displaying temperature data with labeled axes and grid lines.

**API**
-------

M5Chart
^^^^^^^^

.. autoclass:: m5ui.chart.M5Chart
    :members:

    .. py:method:: set_flag(flag, value)

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.
        :return: None

        UiFlow2 Code Block:

            |set_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.set_flag(lv.obj.FLAG.HIDDEN, True)


    .. py:method:: toggle_flag(flag)

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

            |toggle_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.toggle_flag(lv.obj.FLAG.HIDDEN)


    .. py:method:: add_event_cb(handler, event, user_data)

        Add an event callback to the chart. The callback will be called when the specified event occurs.

        :param function handler: The callback function to call.
        :param int event: The event to listen for.
        :param Any user_data: Optional user data to pass to the callback.
        :return: None

        UiFlow2 Code Block:

            |event.png|

        MicroPython Code Block:

            .. code-block:: python

                def chart_0_value_changed_event(event_struct):
                    global page0, button0
                    print("value changed)

                def chart_0_event_handler(event_struct):
                    global page0, button0
                    event = event_struct.code
                    obj = event_struct.get_target_obj()
                    if event == lv.EVENT.VALUE_CHANGED:
                        chart_0_value_changed_event(event_struct)
                    return

                chart_0.add_event_cb(chart_0_event_handler, lv.EVENT.ALL, None)


    .. py:method:: set_bg_color(color, opa, part)

        Set the background color of the chart.

        :param int color: The color to set.
        :param int opa: The opacity of the color. The value should be between 0 (transparent) and 255 (opaque).
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |set_bg_color.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.set_bg_color(lv.color_hex(0xFFFFFF), 255, lv.PART.MAIN | lv.STATE.DEFAULT)


    .. py:method:: set_border_color(color, opa, part)

        Set the border color of the chart.

        :param int color: The color to set.
        :param int opa: The opacity of the color. The value should be between 0 (transparent) and 255 (opaque).
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |set_border_color.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.set_border_color(lv.color_hex(0x2196F3), 255, lv.PART.MAIN | lv.STATE.DEFAULT)


    .. py:method:: set_style_border_width(width, part)

        Set the border width of the chart.

        :param int width: The width to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |set_style_border_width.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.set_style_border_width(2, lv.PART.MAIN | lv.STATE.DEFAULT)


    .. py:method:: set_type(chart_type)

        Set the type of the chart.

        :param int chart_type: The type of the chart (e.g., lv.chart.TYPE.LINE, lv.chart.TYPE.BAR).
        :return: None

        UiFlow2 Code Block:

            |set_type.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.set_type(lv.chart.TYPE.LINE)


    .. py:method:: set_point_count(count)

        Set the number of points in the chart.

        :param int count: The number of points.
        :return: None

        UiFlow2 Code Block:

            |set_point_count.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.set_point_count(10)


    .. py:method:: set_update_mode(mode)

        Set the update mode of the chart.

        :param int mode: The update mode (e.g., lv.chart.UPDATE_MODE.CIRCULAR, lv.chart.UPDATE_MODE.SHIFT).
        :return: None

        UiFlow2 Code Block:

            |set_update_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.set_update_mode(lv.chart.UPDATE_MODE.CIRCULAR)


    .. py:method:: set_div_line_count(hdiv, vdiv)

        Set the number of division lines on the chart.

        :param int hdiv: The number of horizontal division lines.
        :param int vdiv: The number of vertical division lines.
        :return: None

        UiFlow2 Code Block:

            |set_div_line_count.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.set_div_line_count(5, 5)


    .. py:method:: get_type()

        Get the type of the chart.

        :return: The type of the chart.

        UiFlow2 Code Block:

            |get_type.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_type = chart_0.get_type()


    .. py:method:: get_point_count()

        Get the number of points in the chart.

        :return: The number of points.
        :rtype: int

        UiFlow2 Code Block:

            |get_point_count.png|

        MicroPython Code Block:

            .. code-block:: python

                point_count = chart_0.get_point_count()


    .. py:method:: remove_series(series)

        Remove a data series from the chart.

        :param lv.chart.Series series: The data series to remove.
        :return: None

        UiFlow2 Code Block:

            |remove_series.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.remove_series(series_0)


    .. py:method:: hide_series(series)

        Hide a data series on the chart.

        :param lv.chart.Series series: The data series to hide.
        :return: None

        UiFlow2 Code Block:

            |hide_series.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.hide_series(series_0)


    .. py:method:: set_next_value(series, value)

        Set the next point's Y value according to the update mode policy.

        :param lv.chart.Series series: The data series to update.
        :param int value: The Y value to set.
        :return: None

        UiFlow2 Code Block:

            |set_next_value.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.set_next_value(series_0, 50)


    .. py:method:: get_pressed_point()

        Get the index of the pressed point on the chart.

        :return: The index of the pressed point.
        :rtype: int

        UiFlow2 Code Block:

            |get_pressed_point.png|

        MicroPython Code Block:

            .. code-block:: python

                pressed_point_index = chart_0.get_pressed_point()


    .. py:method:: set_style_radius(radius, part)

        Set the corner radius of the chart.

        :param int radius: The radius to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.INDICATOR).
        :return: None

        UiFlow2 Code Block:

            |set_style_radius.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.set_style_radius(10, lv.PART.INDICATOR | lv.STATE.DEFAULT)

    .. py:method:: set_style_size(w, h, part)

        Set the size of the chart.

        :param int w: The width to set.
        :param int h: The height to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.INDICATOR).
        :return: None

        UiFlow2 Code Block:

            |set_style_size.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.set_style_size(0, 0, lv.PART.INDICATOR | lv.STATE.DEFAULT)


    .. py:method:: set_pos(x, y)

        Set the position of the chart.

        :param int x: The x-coordinate of the chart.
        :param int y: The y-coordinate of the chart.
        :return: None

        UiFlow2 Code Block:

            |set_pos.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.set_pos(100, 100)


    .. py:method:: set_x(x)

        Set the x-coordinate of the chart.

        :param int x: The x-coordinate of the chart.
        :return: None

        UiFlow2 Code Block:

            |set_x.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.set_x(100)


    .. py:method:: set_y(y)

        Set the y-coordinate of the chart.

        :param int y: The y-coordinate of the chart.
        :return: None

        UiFlow2 Code Block:

            |set_y.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.set_y(100)


    .. py:method:: align_to(obj, align, x, y)

        Align the chart to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.
        :return: None

        UiFlow2 Code Block:

            |align_to.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)


    .. py:method:: set_size(width, height)

        Set the size of the chart.

        :param int width: The width of the chart.
        :param int height: The height of the chart.
        :return: None

        UiFlow2 Code Block:

            |set_size.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.set_size(200, 30)


    .. py:method:: set_width(width)

        Set the width of the chart.

        :param int width: The width of the chart.
        :return: None

        UiFlow2 Code Block:

            |set_width.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.set_width(200)


    .. py:method:: get_width()

        Get the width of the chart.

        :return: The width of the chart.
        :rtype: int

        UiFlow2 Code Block:

            |get_width.png|

        MicroPython Code Block:

            .. code-block:: python

                width = chart_0.get_width()


    .. py:method:: set_height(height)

        Set the height of the chart.

        :param int height: The height of the chart.
        :return: None

        UiFlow2 Code Block:

            |set_height.png|

        MicroPython Code Block:

            .. code-block:: python

                chart_0.set_height(30)

    .. py:method:: get_height()

        Get the height of the chart.

        :return: The height of the chart.
        :rtype: int

        UiFlow2 Code Block:

            |get_height.png|

        MicroPython Code Block:

            .. code-block:: python

                height = chart_0.get_height()
