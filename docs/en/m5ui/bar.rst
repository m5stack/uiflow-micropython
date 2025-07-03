.. currentmodule:: m5ui

M5Bar
=====

.. include:: ../refs/m5ui.bar.ref

M5Bar is a widget that can be used to create progress bars in the user interface. It displays values within a specified range using a visual bar indicator. The bar can be customized with different colors, gradients, and can optionally display the current value as text.


UiFlow2 Example
---------------

Temperature meter
^^^^^^^^^^^^^^^^^

Open the |cores3_temperature_meter_example.m5f2| project in UiFlow2.

This example demonstrates how to create a temperature meter that shows the current temperature.

UiFlow2 Code Block:

    |cores3_temperature_meter_example.png|

Example output:

    None


MicroPython Example
-------------------

Temperature meter
^^^^^^^^^^^^^^^^^

This example demonstrates how to create a temperature meter that shows the current temperature.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/bar/cores3_temperature_meter_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

M5Bar
^^^^^

.. autoclass:: m5ui.bar.M5Bar
    :members:

    .. py:method:: set_value(value, anim_enable)

        Set the current value of the bar.

        :param int value: The value to set.
        :param bool anim_enable: Whether to enable animation when changing the value.
        :return: None

        UiFlow2 Code Block:

            |set_value.png|

        MicroPython Code Block:

            .. code-block:: python

                bar.set_value(75, True)

    .. py:method:: get_value()

        Get the current value of the bar.

        :return: The current value of the bar.
        :rtype: int

        UiFlow2 Code Block:

            |get_value.png|

        MicroPython Code Block:

            .. code-block:: python

                current_value = bar.get_value()

    .. py:method:: set_range(min_value, max_value)

        Set the value range of the bar.

        :param int min_value: The minimum value.
        :param int max_value: The maximum value.
        :return: None

        UiFlow2 Code Block:

            |set_range.png|

        MicroPython Code Block:

            .. code-block:: python

                bar.set_range(0, 200)

    .. py:method:: get_min_value()

        Get the minimum value of the bar range.

        :return: The minimum value.
        :rtype: int

        UiFlow2 Code Block:

            |get_min_value.png|

        MicroPython Code Block:

            .. code-block:: python

                min_val = bar.get_min_value()

    .. py:method:: get_max_value()

        Get the maximum value of the bar range.

        :return: The maximum value.
        :rtype: int

        UiFlow2 Code Block:

            |get_max_value.png|

        MicroPython Code Block:

            .. code-block:: python

                max_val = bar.get_max_value()

    .. py:method:: set_flag(flag, value)

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.
        :return: None

        UiFlow2 Code Block:

            |set_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                bar.set_flag(lv.obj.FLAG.HIDDEN, True)

    .. py:method:: toggle_flag(flag)

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

            |toggle_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                bar.toggle_flag(lv.obj.FLAG.HIDDEN)

    .. py:method:: set_state(state, value)

        Set the state of the bar. If ``value`` is True, the state is set; if False, the state is unset.

        :param int state: The state to set.
        :param bool value: If True, the state is set; if False, the state is unset.
        :return: None

        UiFlow2 Code Block:

            |set_state.png|

        MicroPython Code Block:

            .. code-block:: python

                bar.set_state(lv.STATE.PRESSED, True)

    .. py:method:: toggle_state(state)

        Toggle the state of the bar. If the state is set, it is unset; if not set, it is set.

        :param int state: The state to toggle.
        :return: None

        UiFlow2 Code Block:

            |toggle_state.png|

        MicroPython Code Block:

            .. code-block:: python

                bar.toggle_state(lv.STATE.PRESSED)

    .. py:method:: set_bg_color(color, opa, part)

        Set the background color of the bar.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |set_bg_color.png|

            |set_indicator_color.png|

        MicroPython Code Block:

            .. code-block:: python

                bar.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

                bar.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.INDICATOR | lv.STATE.DEFAULT)

    .. py:method:: set_bg_grad_color(color, opa, grad_color, grad_opd, grad_dir, part)

        Set the background gradient color of the bar.

        :param int color: The start color of the gradient, can be an integer (RGB).
        :param int opa: The opacity of the start color (0-255).
        :param int grad_color: The end color of the gradient, can be an integer (RGB).
        :param int grad_opd: The opacity of the end color (0-255).
        :param int grad_dir: The direction of the gradient (e.g., lv.GRAD_DIR.VER).
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |set_bg_grad_color.png|

            |set_indicator_grad_color.png|

        MicroPython Code Block:

            .. code-block:: python

                bar.set_bg_grad_color(0x00FF00, 255, 0xFF0000, 255, lv.GRAD_DIR.HOR, lv.PART.MAIN | lv.STATE.DEFAULT)
                bar.set_bg_grad_color(0x00FF00, 255, 0xFF0000, 255, lv.GRAD_DIR.HOR, lv.PART.INDICATOR | lv.STATE.DEFAULT)

    .. py:method:: set_pos(x, y)

        Set the position of the bar.

        :param int x: The x-coordinate of the bar.
        :param int y: The y-coordinate of the bar.
        :return: None

        UiFlow2 Code Block:

            |set_pos.png|

        MicroPython Code Block:

            .. code-block:: python

                bar.set_pos(100, 100)

    .. py:method:: set_x(x)

        Set the x-coordinate of the bar.

        :param int x: The x-coordinate of the bar.
        :return: None

        UiFlow2 Code Block:

            |set_x.png|

        MicroPython Code Block:

            .. code-block:: python

                bar.set_x(100)

    .. py:method:: set_y(y)

        Set the y-coordinate of the bar.

        :param int y: The y-coordinate of the bar.
        :return: None

        UiFlow2 Code Block:

            |set_y.png|

        MicroPython Code Block:

            .. code-block:: python

                bar.set_y(100)

    .. py:method:: set_size(width, height)

        Set the size of the bar.

        :param int width: The width of the bar.
        :param int height: The height of the bar.
        :return: None

        UiFlow2 Code Block:

            |set_size.png|

        MicroPython Code Block:

            .. code-block:: python

                bar.set_size(200, 30)

    .. py:method:: set_width(width)

        Set the width of the bar.

        :param int width: The width of the bar.
        :return: None

        UiFlow2 Code Block:

            |set_width.png|

        MicroPython Code Block:

            .. code-block:: python

                bar.set_width(200)

    .. py:method:: get_width()

        Get the width of the bar.

        :return: The width of the bar.
        :rtype: int

        UiFlow2 Code Block:

            |get_width.png|

        MicroPython Code Block:

            .. code-block:: python

                width = bar.get_width()

    .. py:method:: set_height(height)

        Set the height of the bar.

        :param int height: The height of the bar.
        :return: None

        UiFlow2 Code Block:

            |set_height.png|

        MicroPython Code Block:

            .. code-block:: python

                bar.set_height(30)

    .. py:method:: get_height()

        Get the height of the bar.

        :return: The height of the bar.
        :rtype: int

        UiFlow2 Code Block:

            |get_height.png|

        MicroPython Code Block:

            .. code-block:: python

                height = bar.get_height()

    .. py:method:: align_to(obj, align, x, y)

        Align the bar to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.
        :return: None

        UiFlow2 Code Block:

            |align_to.png|

        MicroPython Code Block:

            .. code-block:: python

                bar.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
