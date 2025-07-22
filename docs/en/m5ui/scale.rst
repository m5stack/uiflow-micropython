.. currentmodule:: m5ui

M5Scale
========

.. include:: ../refs/m5ui.scale.ref

M5Scale is a widget that can be used to create scales in the user interface. Scale Widgets show linear or circular scales with configurable ranges, tick counts, placement, labeling, and subsections (Sections) with custom styling.


UiFlow2 Example
---------------

scale example
^^^^^^^^^^^^^^

Open the |cores3_scroll_example.m5f2| project in UiFlow2.

This example demonstrates how to create a scale widget with a range of values and custom styling.

UiFlow2 Code Block:

    |cores3_scroll_example.png|

Example output:

    None


MicroPython Example
-------------------

scroll example
^^^^^^^^^^^^^^^

This example demonstrates how to create a scale widget with a range of values and custom styling.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/scale/cores3_scroll_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

M5Scale
^^^^^^^^

.. autoclass:: m5ui.scale.M5Scale
    :members:

    .. py:method:: set_flag(flag, value)

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.

        UiFlow2 Code Block:

            |set_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                scale_0.set_flag(lv.obj.FLAG.HIDDEN, True)

    .. py:method:: set_range(start_pos, end_pos)

        Set the range of the scale.

        :param int start_pos: The start position of the scale.
        :param int end_pos: The end position of the scale.

        UiFlow2 Code Block:

            |set_range.png|

        MicroPython Code Block:

            .. code-block:: python

                scale_0.set_range(0, 100)

    .. py:method:: set_major_tick_every(tick_every)

        Set the interval for major ticks on the scale.

        :param int tick_every: The interval for major ticks.

        UiFlow2 Code Block:

            |set_major_tick_every.png|

        MicroPython Code Block:

            .. code-block:: python

                scale_0.set_major_tick_every(10)

    .. py:method:: set_total_tick_count(tick_count)

        Set the total tick count of the scale.

        :param int tick_count: The total tick count.

        UiFlow2 Code Block:

            |set_total_tick_count.png|

        MicroPython Code Block:

            .. code-block:: python

                scale_0.set_total_tick_count(11)

    .. py:method:: set_label_show(label_show)

        Set the visibility of the scale labels.

        :param bool label_show: If True, the labels are shown; if False, they are hidden.

        UiFlow2 Code Block:

            |set_label_show.png|

        MicroPython Code Block:

            .. code-block:: python

                scale_0.set_label_show(True)


    .. py:method:: set_mode(show_mode)

        Set the display mode of the scale.

        :param int show_mode: The display mode.

            Optional: 

                - `lv.SCALE.MODE.HORIZONTAL_TOP`: Horizontal top scale.
                - `lv.SCALE.MODE.HORIZONTAL_BOTTOM`: Horizontal bottom scale.
                - `lv.SCALE.MODE.VERTICAL_LEFT`: Vertical left scale.
                - `lv.SCALE.MODE.VERTICAL_RIGHT`: Vertical right scale.
                - `lv.SCALE.MODE.ROUND_INNER`: Round inner scale.
                - `lv.SCALE.MODE.ROUND_OUTER`: Round outer scale.

        UiFlow2 Code Block:

            |set_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                scale_0.set_mode(lv.SCALE.MODE.HORIZONTAL_TOP)

    .. py:method:: set_text_src(text_src)

        Set the source of the scale label text.

        :param list text_src: The source of the scale label text.

        UiFlow2 Code Block:

            |set_text_src.png|

        MicroPython Code Block:

            .. code-block:: python

                scale_0.set_text_src(["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100", None])

    .. py:method:: set_line_color(color, opa, part)

        Set the color of the line.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).

        UiFlow2 Code Block:

            |set_line_color.png|

        MicroPython Code Block:

            .. code-block:: python

                scale_0.set_line_color(0xFF0000, 255, lv.PART.MAIN)
                scale_0.set_line_color(0x00FF00, 255, lv.PART.ITEMS)
                scale_0.set_line_color(0x0000FF, 255, lv.PART.INDICATOR)

    .. py:method:: set_style_line_width(width, part)

        Set the line width of the scale.

        :param int width: The line width to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).

        UiFlow2 Code Block:

            |set_style_line_width.png|

        MicroPython Code Block:

            .. code-block:: python

                scale_0.set_style_line_width(2, lv.PART.MAIN)
                scale_0.set_style_line_width(2, lv.PART.ITEMS)
                scale_0.set_style_line_width(2, lv.PART.INDICATOR)

    .. py:method:: set_text_color(color, opa, part)

        Set the color of the text.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to lv.PART.INDICATOR.

        UiFlow2 Code Block:

            |set_text_color.png|

        MicroPython Code Block:

            .. code-block:: python

                scale_0.set_text_color(0xFF0000, 255, lv.PART.INDICATOR)


    .. py:method:: set_style_text_font(font, part)

        Set the font of the scale label text.

        :param lv.lv_font_t font: The font to set.
        :param int part: The part of the object to apply the style to lv.PART.INDICATOR.

        UiFlow2 Code Block:

            |set_style_text_font.png|

        MicroPython Code Block:

            .. code-block:: python

                scale_0.set_style_text_font(lv.font_montserrat_14, lv.PART.INDICATOR)

    .. py:method:: set_pos(x, y)

        Set the position of the scale.

        :param int x: The x-coordinate of the scale.
        :param int y: The y-coordinate of the scale.

        UiFlow2 Code Block:

            |set_pos.png|

        MicroPython Code Block:

            .. code-block:: python

                scale_0.set_pos(100, 100)


    .. py:method:: set_x(x)

        Set the x-coordinate of the scale.

        :param int x: The x-coordinate of the scale.

        UiFlow2 Code Block:

            |set_x.png|

        MicroPython Code Block:

            .. code-block:: python

                scale_0.set_x(100)


    .. py:method:: set_y(y)

        Set the y-coordinate of the scale.

        :param int y: The y-coordinate of the scale.

        UiFlow2 Code Block:

            |set_y.png|

        MicroPython Code Block:

            .. code-block:: python

                scale_0.set_y(100)


    .. py:method:: set_size(width, height)

        Set the size of the scale.

        :param int width: The width of the scale.
        :param int height: The height of the scale.

        UiFlow2 Code Block:

            |set_size.png|

        MicroPython Code Block:

            .. code-block:: python

                scale_0.set_size(100, 50)


    .. py:method:: set_width(width)

        Set the width of the scale.

        :param int width: The width of the scale.

        UiFlow2 Code Block:

            |set_width.png|

            |set_width1.png|

        MicroPython Code Block:

            .. code-block:: python

                scale_0.set_width(100)

    .. py:method:: set_height(height)
        
        Set the height of the scale.

        :param int height: The height of the scale.

        UiFlow2 Code Block:

            |set_height.png|

        MicroPython Code Block:

            .. code-block:: python

                scale_0.set_height(50)

    .. py:method:: align_to(obj, align, x, y)

        Align the scale to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.

        UiFlow2 Code Block:

            |align_to.png|

        MicroPython Code Block:

            .. code-block:: python

                scale_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
