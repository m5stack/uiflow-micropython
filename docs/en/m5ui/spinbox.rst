.. currentmodule:: m5ui

M5Spinbox
=========

.. include:: ../refs/m5ui.spinbox.ref

M5Spinbox is a widget that provides a numeric input interface with increment and decrement buttons.
It displays a numeric value that can be adjusted by clicking the + and - buttons or by typing directly.
The spinbox supports both integer and floating-point numbers with customizable digit count and decimal precision.


UiFlow2 Example
---------------

basic spinbox
^^^^^^^^^^^^^

Open the |cores3_spinbox_basic_example.m5f2| project in UiFlow2.

This example demonstrates how to create a spinbox with customizable range and precision settings.

UiFlow2 Code Block:

    |cores3_spinbox_basic_example.png|

Example output:

    None


MicroPython Example
-------------------

basic spinbox
^^^^^^^^^^^^^

This example demonstrates how to create a spinbox with customizable range and precision settings.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/spinbox/cores3_spinbox_basic_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

M5Spinbox
^^^^^^^^^

.. autoclass:: m5ui.spinbox.M5Spinbox
    :members:
    :exclude-members: set_digit_format, value2raw, raw2value

    .. py:method:: set_flag(flag, value)

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.
        :return: None

        UiFlow2 Code Block:

            |set_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                spinbox_0.set_flag(lv.obj.FLAG.HIDDEN, True)

    .. py:method:: toggle_flag(flag)

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

            |toggle_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                spinbox_0.toggle_flag(lv.obj.FLAG.HIDDEN)

    .. py:method:: set_state(state, value)

        Set the state of the spinbox. If ``value`` is True, the state is set; if False, the state is unset.

        :param int state: The state to set.
        :param bool value: If True, the state is set; if False, the state is unset.
        :return: None

        UiFlow2 Code Block:

            |set_state.png|

        MicroPython Code Block:

            .. code-block:: python

                spinbox_0.set_state(lv.STATE.DISABLED, True)

    .. py:method:: toggle_state(state)

        Toggle the state of the spinbox. If the state is set, it is unset; if not set, it is set.

        :param int state: The state to toggle.
        :return: None

        UiFlow2 Code Block:

            |toggle_state.png|

        MicroPython Code Block:

            .. code-block:: python

                spinbox_0.toggle_state(lv.STATE.CHECKED)

    .. py:method:: set_pos(x, y)

        Set the position of the spinbox.

        :param int x: The x-coordinate of the spinbox.
        :param int y: The y-coordinate of the spinbox.
        :return: None

        UiFlow2 Code Block:

            |set_pos.png|

        MicroPython Code Block:

            .. code-block:: python

                spinbox_0.set_pos(100, 200)

    .. py:method:: set_x(x)

        Set the x-coordinate of the spinbox.

        :param int x: The x-coordinate of the spinbox.
        :return: None

        UiFlow2 Code Block:

            |set_x.png|

        MicroPython Code Block:

            .. code-block:: python

                spinbox_0.set_x(150)

    .. py:method:: set_y(y)

        Set the y-coordinate of the spinbox.

        :param int y: The y-coordinate of the spinbox.
        :return: None

        UiFlow2 Code Block:

            |set_y.png|

        MicroPython Code Block:

            .. code-block:: python

                spinbox_0.set_y(250)

    .. py:method:: set_size(width, height)

        Set the size of the spinbox.

        :param int width: The width of the spinbox.
        :param int height: The height of the spinbox.
        :return: None

        UiFlow2 Code Block:

            |set_size.png|

        MicroPython Code Block:

            .. code-block:: python

                spinbox_0.set_size(150, 40)

    .. py:method:: set_width(width)

        Set the width of the spinbox.

        :param int width: The width of the spinbox.
        :return: None

        UiFlow2 Code Block:

            |set_width.png|

        MicroPython Code Block:

            .. code-block:: python

                spinbox_0.set_width(180)

    .. py:method:: get_width()

        Get the width of the spinbox.

        :return: The width of the spinbox.
        :rtype: int

        UiFlow2 Code Block:

            |get_width.png|

        MicroPython Code Block:

            .. code-block:: python

                width = spinbox_0.get_width()

    .. py:method:: set_height(height)

        Set the height of the spinbox.

        :param int height: The height of the spinbox.
        :return: None

        UiFlow2 Code Block:

            |set_height.png|

        MicroPython Code Block:

            .. code-block:: python

                spinbox_0.set_height(50)

    .. py:method:: get_height()

        Get the height of the spinbox.

        :return: The height of the spinbox.
        :rtype: int

        UiFlow2 Code Block:

            |get_height.png|

        MicroPython Code Block:

            .. code-block:: python

                height = spinbox_0.get_height()

    .. py:method:: align_to(obj, align, x, y)

        Align the spinbox to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.
        :return: None

        UiFlow2 Code Block:

            |align_to.png|

        MicroPython Code Block:

            .. code-block:: python

                spinbox_0.align_to(label_0, lv.ALIGN.OUT_BOTTOM_MID, 0, 10)
