.. currentmodule:: m5ui

N5Label
=======

.. include:: ../refs/m5ui.label.ref

M5Label is a widget that can be used to create labels in the user interface. It can display text and can be styled with different fonts, colors, and sizes.


UiFlow2 Example
---------------

scroll label
^^^^^^^^^^^^

Open the |cores3_scroll_label_example.m5f2| project in UiFlow2.

This example demonstrates how to create a label that scrolls text in a circular manner.

UiFlow2 Code Block:

    |cores3_scroll_label_example.png|

Example output:

    None


MicroPython Example
-------------------

scroll label
^^^^^^^^^^^^

This example demonstrates how to create a label that scrolls text in a circular manner.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/label/cores3_scroll_label_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

M5Label
^^^^^^^^

.. autoclass:: m5ui.label.M5Label
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

                label_0.set_flag(lv.obj.FLAG.HIDDEN, True)

    .. py:method:: toggle_flag(flag)

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

            |toggle_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.toggle_flag(lv.obj.FLAG.HIDDEN)

    .. py:method:: set_state(state, value)

        Set the state of the label. If ``value`` is True, the state is set; if False, the state is unset.

        :param int state: The state to set.
        :param bool value: If True, the state is set; if False, the state is unset.
        :return: None

        UiFlow2 Code Block:

            |set_state.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.set_state(lv.STATE.PRESSED, True)

    .. py:method:: toggle_state(state)

        Toggle the state of the label. If the state is set, it is unset; if not set, it is set.

        :param int state: The state to toggle.
        :return: None

        UiFlow2 Code Block:

            |toggle_state.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.toggle_state(lv.STATE.PRESSED)

    .. py:method:: set_style_text_font(font, part)

        Set the font of the label text.

        :param lv.lv_font_t font: The font to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |set_style_text_font.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN | lv.STATE.DEFAULT)


    .. py:method:: set_text_color(color, opa, part)

        Set the color of the text.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |set_text_color.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)


    .. py:method:: set_bg_color(color, opa, part)

        Set the background color of the label.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |set_text_color.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)


    .. py:method:: set_pos(x, y)

        Set the position of the label.

        :param int x: The x-coordinate of the label.
        :param int y: The y-coordinate of the label.
        :return: None

        UiFlow2 Code Block:

            |set_pos.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.set_pos(100, 100)


    .. py:method:: set_x(x)

        Set the x-coordinate of the label.

        :param int x: The x-coordinate of the label.
        :return: None

        UiFlow2 Code Block:

            |set_x.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.set_x(100)


    .. py:method:: set_y(y)

        Set the y-coordinate of the label.

        :param int y: The y-coordinate of the label.
        :return: None

        UiFlow2 Code Block:

            |set_y.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.set_y(100)


    .. py:method:: set_size(width, height)

        Set the size of the label.

        :param int width: The width of the label.
        :param int height: The height of the label.
        :return: None

        UiFlow2 Code Block:

            |set_size.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.set_size(100, 50)


    .. py:method:: set_width(width)

        Set the width of the label.

        :param int width: The width of the label.
        :return: None

        UiFlow2 Code Block:

            |set_width.png|

            |set_width1.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.set_width(100)


    .. py::method:: get_width()

        Get the width of the label.

        :return: The width of the label.
        :rtype: int

        UiFlow2 Code Block:

            |get_width.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.get_width()


    .. py:method:: align_to(obj, align, x, y)

        Align the label to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.
        :return: None

        UiFlow2 Code Block:

            |align_to.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
