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
    
    .. py:method:: set_pos(x, y)

        Set the position of the switch.

        :param int x: The x-coordinate of the switch.
        :param int y: The y-coordinate of the switch.

        UiFlow2 Code Block:

            |set_pos.png|

        MicroPython Code Block:

            .. code-block:: python

                switch_0.set_pos(100, 100)

    .. py:method:: set_x(x)

        Set the x-coordinate of the switch.

        :param int x: The x-coordinate of the switch.

        UiFlow2 Code Block:

            |set_x.png|

        MicroPython Code Block:

            .. code-block:: python

                switch_0.set_x(100)

    .. py:method:: set_y(y)

        Set the y-coordinate of the switch.

        :param int y: The y-coordinate of the switch.

        UiFlow2 Code Block:

            |set_y.png|

        MicroPython Code Block:

            .. code-block:: python

                switch_0.set_y(100)


    .. py:method:: align_to(obj, align, x, y)

        Align the switch to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.

        UiFlow2 Code Block:

            |align_to.png|

        MicroPython Code Block:

            .. code-block:: python

                switch_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
