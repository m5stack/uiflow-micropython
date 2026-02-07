.. currentmodule:: m5ui

M5Canvas
========

.. include:: ../refs/m5ui.canvas.ref

M5Canvas is a powerful graphics widget that provides a drawable surface for creating custom graphics, animations, and visual effects in the user interface. It supports drawing operations, sprite management, and advanced graphics rendering.


UiFlow2 Example
---------------

draw basic shapes
^^^^^^^^^^^^^^^^^

Open the |cores3_canvas_basic_example.m5f2| project in UiFlow2.

This example demonstrates how to create a canvas and draw basic shapes like rectangles, circles, and lines.

UiFlow2 Code Block:

    |cores3_canvas_basic_example.png|

Example output:

    A canvas with various colored shapes including rectangles, circles, and lines.


MicroPython Example
-------------------

draw basic shapes
^^^^^^^^^^^^^^^^^

This example demonstrates how to create a canvas and draw basic shapes programmatically.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/canvas/cores3_canvas_basic_example.py
        :language: python
        :linenos:

Example output:

    A canvas displaying various geometric shapes with different colors.


**API**
-------

M5Canvas
^^^^^^^^

.. autoclass:: m5ui.canvas.M5Canvas
    :members:
    :member-order: bysource

    .. py:method:: set_flag(flag, value)

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.
        :return: None

        UiFlow2 Code Block:

            |set_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                canvas_0.set_flag(lv.obj.FLAG.HIDDEN, True)

    .. py:method:: toggle_flag(flag)

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

            |toggle_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                canvas_0.toggle_flag(lv.obj.FLAG.HIDDEN)


    .. py:method:: set_pos(x, y)

        Set the position of the canvas.

        :param int x: The x-coordinate of the canvas.
        :param int y: The y-coordinate of the canvas.
        :return: None

        UiFlow2 Code Block:

            |set_pos.png|

        MicroPython Code Block:

            .. code-block:: python

                canvas_0.set_pos(100, 100)

    .. py:method:: set_x(x)

        Set the x-coordinate of the canvas.

        :param int x: The x-coordinate of the canvas.
        :return: None

        UiFlow2 Code Block:

            |set_x.png|

        MicroPython Code Block:

            .. code-block:: python

                canvas_0.set_x(100)

    .. py:method:: set_y(y)

        Set the y-coordinate of the canvas.

        :param int y: The y-coordinate of the canvas.
        :return: None

        UiFlow2 Code Block:

            |set_y.png|

        MicroPython Code Block:

            .. code-block:: python

                canvas_0.set_y(100)

    .. py:method:: align_to(obj, align, x, y)

        Align the canvas to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.
        :return: None

        UiFlow2 Code Block:

            |align_to.png|

        MicroPython Code Block:

            .. code-block:: python

                canvas_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)

    .. py:method:: set_size(width, height)

        Set the size of the canvas.

        :param int width: The width of the canvas.
        :param int height: The height of the canvas.
        :return: None

        UiFlow2 Code Block:

            |set_size.png|

        MicroPython Code Block:

            .. code-block:: python

                canvas_0.set_size(200, 100)

    .. py:method:: set_width(width)

        Set the width of the canvas.

        :param int width: The width of the canvas.
        :return: None

        UiFlow2 Code Block:

            |set_width.png|

        MicroPython Code Block:

            .. code-block:: python

                canvas_0.set_width(200)

    .. py:method:: set_height(height)

        Set the height of the canvas.

        :param int height: The height of the canvas.
        :return: None

        UiFlow2 Code Block:

            |set_height.png|

        MicroPython Code Block:

            .. code-block:: python

                canvas_0.set_height(100)

    .. py:method:: get_width()

        Get the width of the canvas.

        :return: The width of the canvas.
        :rtype: int

        UiFlow2 Code Block:

            |get_width.png|

        MicroPython Code Block:

            .. code-block:: python

                width = canvas_0.get_width()

    .. py:method:: get_height()

        Get the height of the canvas.

        :return: The height of the canvas.
        :rtype: int

        UiFlow2 Code Block:

            |get_height.png|

        MicroPython Code Block:

            .. code-block:: python

                height = canvas_0.get_height()
