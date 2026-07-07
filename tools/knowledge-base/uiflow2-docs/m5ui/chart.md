<!-- .. currentmodule:: m5ui -->

# M5Chart

<!-- .. include:: ../refs/m5ui.chart.ref -->

M5Chart is a versatile charting widget that allows users to create various types of charts, including line charts and bar charts. It provides features for data visualization, customization, and interactivity within the user interface.

## UiFlow2 Example

#### Temperature Line Chart

Open the |cores3_chart_line_example.m5f2| project in UiFlow2.

This example demonstrates how to create a line chart to visualize temperature data over time.

UiFlow2 Code Block:

Example output:

    A line chart displaying temperature data with labeled axes and grid lines.

## MicroPython Example

#### Temperature Line Chart

This example demonstrates how to create a line chart programmatically to visualize temperature data.

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
from hardware import Pin
from hardware import I2C
from unit import ENVUnit
import time

page0 = None
chart0 = None
i2c0 = None
series_temp = None
series_humi = None
env3_0 = None

def setup():
    global page0, chart0, i2c0, series_temp, series_humi, env3_0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    chart0 = m5ui.M5Chart(
        x=43,
        y=40,
        w=240,
        h=160,
        chart_type=lv.chart.TYPE.LINE,
        point_num=10,
        hdiv=3,
        vdiv=5,
        bg_radius=7,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        border_w=2,
        parent=page0,
    )
    chart0.y_axis1_init(
        min_value=0,
        max_value=50,
        major_ticks=3,
        major_tick_len=10,
        minor_ticks=2,
        minor_tick_len=5,
        label_show=True,
    )
    chart0.y_axis2_init(
        min_value=0,
        max_value=100,
        major_ticks=3,
        major_tick_len=10,
        minor_ticks=2,
        minor_tick_len=5,
        label_show=True,
    )

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    env3_0 = ENVUnit(i2c=i2c0, type=3)
    page0.screen_load()
    series_temp = chart0.add_series(0xFF0000, lv.chart.AXIS.PRIMARY_Y)
    series_humi = chart0.add_series(0x009900, lv.chart.AXIS.SECONDARY_Y)
    chart0.set_update_mode(lv.chart.UPDATE_MODE.SHIFT)
    chart0.align_to(page0, lv.ALIGN.CENTER, 0, 0)
    chart0.set_style_size(0, 0, lv.PART.INDICATOR | lv.STATE.DEFAULT)

def loop():
    global page0, chart0, i2c0, series_temp, series_humi, env3_0
    M5.update()
    chart0.set_next_value(series_temp, int(env3_0.read_temperature()))
    chart0.set_next_value(series_humi, int(env3_0.read_humidity()))
    time.sleep(1)

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

    A line chart displaying temperature data with labeled axes and grid lines.

## **API**

#### M5Chart

## M5Chart
Create a Chart object.

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

### `x_axis_init`
Initialize the X axis.

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

### `y_axis1_init`
Initialize the primary Y axis.

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

### `y_axis2_init`
Initialize the secondary Y axis.

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

### `set_axis_range`
Set the range of the specified axis.

:param int axis: Axis to set the range for. lv.chart.AXIS.PRIMARY_X, lv.chart.AXIS.PRIMARY_Y, or lv.chart.AXIS.SECONDARY_Y.
:param int min_value: Minimum value of the axis.
:param int max_value: Maximum value of the axis.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        chart_0.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 0, 200)

### `add_series`
Add a data series to the chart.

:param int color: Color of the series in hex format.
:param int axis: Axis to associate the series with. lv.chart.AXIS.PRIMARY_Y or lv.chart.AXIS.SECONDARY_Y.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        series_0 = chart_0.add_series(0xFF0000, lv.chart.AXIS.PRIMARY_Y)

### `set_series_color`
Set the color of a data series.

:param series: Series to set the color for.
:param int color: Color of the series in hex format.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        chart_0.set_series_color(series_0, 0x00FF00)

### `get_series_color`
Get the color of a data series.

:param series: Series to get the color for.
:return: Color of the series in hex format.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        color = chart_0.get_series_color(series_0)

### `set_series_values`
Set the values of a data series.

:param series: Series to set the values for.
:param list values: List of values to set.
:param int size: Number of values to set. Default is -1 (set all values).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        chart_0.set_series_values(series_0, [10, 20, 30, 40, 50])

<!-- .. py:method:: set_flag(flag, value) -->

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                chart_0.set_flag(lv.obj.FLAG.HIDDEN, True)

<!-- .. py:method:: toggle_flag(flag) -->

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                chart_0.toggle_flag(lv.obj.FLAG.HIDDEN)

<!-- .. py:method:: add_event_cb(handler, event, user_data) -->

        Add an event callback to the chart. The callback will be called when the specified event occurs.

        :param function handler: The callback function to call.
        :param int event: The event to listen for.
        :param Any user_data: Optional user data to pass to the callback.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

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

<!-- .. py:method:: set_bg_color(color, opa, part) -->

        Set the background color of the chart.

        :param int color: The color to set.
        :param int opa: The opacity of the color. The value should be between 0 (transparent) and 255 (opaque).
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                chart_0.set_bg_color(lv.color_hex(0xFFFFFF), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

<!-- .. py:method:: set_border_color(color, opa, part) -->

        Set the border color of the chart.

        :param int color: The color to set.
        :param int opa: The opacity of the color. The value should be between 0 (transparent) and 255 (opaque).
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                chart_0.set_border_color(lv.color_hex(0x2196F3), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

<!-- .. py:method:: set_style_border_width(width, part) -->

        Set the border width of the chart.

        :param int width: The width to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                chart_0.set_style_border_width(2, lv.PART.MAIN | lv.STATE.DEFAULT)

<!-- .. py:method:: set_type(chart_type) -->

        Set the type of the chart.

        :param int chart_type: The type of the chart (e.g., lv.chart.TYPE.LINE, lv.chart.TYPE.BAR).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                chart_0.set_type(lv.chart.TYPE.LINE)

<!-- .. py:method:: set_point_count(count) -->

        Set the number of points in the chart.

        :param int count: The number of points.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                chart_0.set_point_count(10)

<!-- .. py:method:: set_update_mode(mode) -->

        Set the update mode of the chart.

        :param int mode: The update mode (e.g., lv.chart.UPDATE_MODE.CIRCULAR, lv.chart.UPDATE_MODE.SHIFT).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                chart_0.set_update_mode(lv.chart.UPDATE_MODE.CIRCULAR)

<!-- .. py:method:: set_div_line_count(hdiv, vdiv) -->

        Set the number of division lines on the chart.

        :param int hdiv: The number of horizontal division lines.
        :param int vdiv: The number of vertical division lines.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                chart_0.set_div_line_count(5, 5)

<!-- .. py:method:: get_type() -->

        Get the type of the chart.

        :return: The type of the chart.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                chart_type = chart_0.get_type()

<!-- .. py:method:: get_point_count() -->

        Get the number of points in the chart.

        :return: The number of points.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                point_count = chart_0.get_point_count()

<!-- .. py:method:: remove_series(series) -->

        Remove a data series from the chart.

        :param lv.chart.Series series: The data series to remove.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                chart_0.remove_series(series_0)

<!-- .. py:method:: hide_series(series) -->

        Hide a data series on the chart.

        :param lv.chart.Series series: The data series to hide.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                chart_0.hide_series(series_0)

<!-- .. py:method:: set_next_value(series, value) -->

        Set the next point's Y value according to the update mode policy.

        :param lv.chart.Series series: The data series to update.
        :param int value: The Y value to set.
        :return: None

<!-- .. tip:: -->

            For real-time data (sensors, audio, etc.), combine
            ``set_next_value()`` with ``set_update_mode(lv.chart.UPDATE_MODE.SHIFT)``
            for incremental scrolling. This is much more efficient than
            replacing the entire series with ``set_series_values()`` every
            frame, which triggers a full chart redraw and becomes slow with
            400+ data points.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                chart_0.set_next_value(series_0, 50)

<!-- .. py:method:: get_pressed_point() -->

        Get the index of the pressed point on the chart.

        :return: The index of the pressed point.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                pressed_point_index = chart_0.get_pressed_point()

<!-- .. py:method:: set_style_radius(radius, part) -->

        Set the corner radius of the chart.

        :param int radius: The radius to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.INDICATOR).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                chart_0.set_style_radius(10, lv.PART.INDICATOR | lv.STATE.DEFAULT)

<!-- .. py:method:: set_style_size(w, h, part) -->

        Set the size of the chart.

        :param int w: The width to set.
        :param int h: The height to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.INDICATOR).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                chart_0.set_style_size(0, 0, lv.PART.INDICATOR | lv.STATE.DEFAULT)

<!-- .. py:method:: set_pos(x, y) -->

        Set the position of the chart.

        :param int x: The x-coordinate of the chart.
        :param int y: The y-coordinate of the chart.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                chart_0.set_pos(100, 100)

<!-- .. py:method:: set_x(x) -->

        Set the x-coordinate of the chart.

        :param int x: The x-coordinate of the chart.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                chart_0.set_x(100)

<!-- .. py:method:: set_y(y) -->

        Set the y-coordinate of the chart.

        :param int y: The y-coordinate of the chart.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                chart_0.set_y(100)

<!-- .. py:method:: align_to(obj, align, x, y) -->

        Align the chart to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                chart_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)

<!-- .. py:method:: set_size(width, height) -->

        Set the size of the chart.

        :param int width: The width of the chart.
        :param int height: The height of the chart.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                chart_0.set_size(200, 30)

<!-- .. py:method:: set_width(width) -->

        Set the width of the chart.

        :param int width: The width of the chart.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                chart_0.set_width(200)

<!-- .. py:method:: get_width() -->

        Get the width of the chart.

        :return: The width of the chart.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                width = chart_0.get_width()

<!-- .. py:method:: set_height(height) -->

        Set the height of the chart.

        :param int height: The height of the chart.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                chart_0.set_height(30)

<!-- .. py:method:: get_height() -->

        Get the height of the chart.

        :return: The height of the chart.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                height = chart_0.get_height()
