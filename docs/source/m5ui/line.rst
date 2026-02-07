.. currentmodule:: m5ui

M5Line
========

.. include:: ../refs/m5ui.line.ref

M5Line is a widget that can be used to create lines in the user interface. It can be used to draw shapes and connect points.

UiFlow2 Example
---------------

points connect
^^^^^^^^^^^^^^

Open the |cores3_line_example.m5f2| project in UiFlow2.

This example creates a line that connects multiple points.

UiFlow2 Code Block:

    |cores3_line_example.png|

Example output:

    None


MicroPython Example
-------------------

points connect
^^^^^^^^^^^^^^

This example creates a line that connects multiple points.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/line/cores3_line_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

M5Line
^^^^^^^

.. autoclass:: m5ui.line.M5Line
    :members:

    .. py:method:: set_line_color(color, opa, part)

        Set the color of the line.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).

        UiFlow2 Code Block:

            |set_line_color.png|

        MicroPython Code Block:

            .. code-block:: python

                line_0.set_line_color(0xFF0000, 255, lv.PART.MAIN)

    .. py:method:: set_style_line_width(width,  part)

        Set the width of the line.

        :param int width: The width to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).

        UiFlow2 Code Block:

            |set_style_line_width.png|

        MicroPython Code Block:

            .. code-block:: python

                line_0.set_style_line_width(2, lv.PART.MAIN)

    .. py:method:: set_flag(flag, value)

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.
        :return: None

        UiFlow2 Code Block:

            |set_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                button_0.set_flag(lv.obj.FLAG.HIDDEN, True)

    .. py:method:: set_pos(x, y)

        Set the position of the line.

        :param int x: The x-coordinate of the line.
        :param int y: The y-coordinate of the line.

        UiFlow2 Code Block:

            |set_pos.png|

        MicroPython Code Block:

            .. code-block:: python

                line_0.set_pos(100, 100)

    .. py:method:: set_x(x)

        Set the x-coordinate of the line.

        :param int x: The x-coordinate of the line.

        UiFlow2 Code Block:

            |set_x.png|

        MicroPython Code Block:

            .. code-block:: python

                line_0.set_x(100)

    .. py:method:: set_y(y)

        Set the y-coordinate of the line.

        :param int y: The y-coordinate of the line.

        UiFlow2 Code Block:

            |set_y.png|

        MicroPython Code Block:

            .. code-block:: python

                line_0.set_y(100)


    .. py:method:: align_to(obj, align, x, y)

        Align the line to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.

        UiFlow2 Code Block:

            |align_to.png|

        MicroPython Code Block:

            .. code-block:: python

                line_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
