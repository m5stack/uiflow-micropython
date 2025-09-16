.. currentmodule:: m5ui

M5Slider
========

.. include:: ../refs/m5ui.slider.ref

M5Slider is a widget that can be used to create sliders in the user interface. It allows users to select a value from a range by dragging a handle along a track.

UiFlow2 Example
---------------

basic slider
^^^^^^^^^^^^

Open the |cores3_slider_basic_example.m5f2| project in UiFlow2.

This example creates a basic slider that can be used to select values from 0 to 100.

UiFlow2 Code Block:

    |cores3_slider_basic_example.png|

Example output:

    None


MicroPython Example
-------------------

basic slider
^^^^^^^^^^^^

This example creates a basic slider that can be used to select values from 0 to 100.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/slider/cores3_slider_basic_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

M5Slider
^^^^^^^^

.. autoclass:: m5ui.slider.M5Slider
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

                slider_0.set_flag(lv.obj.FLAG.HIDDEN, True)

    .. py:method:: toggle_flag(flag)

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

            |toggle_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                slider_0.toggle_flag(lv.obj.FLAG.HIDDEN)

    .. py:method:: set_state(state, value)

        Set the state of the slider. If ``value`` is True, the state is set; if False, the state is unset.

        :param int state: The state to set.
        :param bool value: If True, the state is set; if False, the state is unset.
        :return: None

        UiFlow2 Code Block:

            |set_state.png|

        MicroPython Code Block:

            .. code-block:: python

                slider_0.set_state(lv.STATE.PRESSED, True)

    .. py:method:: toggle_state(state)

        Toggle the state of the slider. If the state is set, it is unset; if not set, it is set.

        :param int state: The state to toggle.
        :return: None

        UiFlow2 Code Block:

            |toggle_state.png|

        MicroPython Code Block:

            .. code-block:: python

                slider_0.toggle_state(lv.STATE.PRESSED)

    .. py:method:: add_event_cb(handler, event, user_data)

        Add an event callback to the slider. The callback will be called when the specified event occurs.

        :param function handler: The callback function to call.
        :param int event: The event to listen for.
        :param Any user_data: Optional user data to pass to the callback.
        :return: None

        UiFlow2 Code Block:

            |event.png|

        MicroPython Code Block:

            .. code-block:: python

                def slider_0_value_changed_event(event_struct):
                    global slider_0
                    value = slider_0.get_value()
                    print(f"Slider value changed to: {value}")

                def slider_0_event_handler(event_struct):
                    global slider_0
                    event = event_struct.code
                    if event == lv.EVENT.VALUE_CHANGED:
                        slider_0_value_changed_event(event_struct)
                    return

                slider_0.add_event_cb(slider_0_event_handler, lv.EVENT.ALL, None)

    .. py:method:: set_bg_color(color, opa, part)

        Set the background color of the slider.

        :param int color: The color to set.
        :param int opa: The opacity of the color. The value should be between 0 (transparent) and 255 (opaque).
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN, lv.PART.INDICATOR).
        :return: None

        UiFlow2 Code Block:

            |set_bg_color.png|

        MicroPython Code Block:

            .. code-block:: python

                slider_0.set_bg_color(lv.color_hex(0x2196F3), 255, lv.PART.INDICATOR | lv.STATE.DEFAULT)

    .. py:method:: set_style_radius(radius, part)

        Set the corner radius of the slider components.

        :param int radius: The radius to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN, lv.PART.KNOB).
        :return: None

        UiFlow2 Code Block:

            |set_bg_radius.png|

            |set_indicator_radius.png|

            |set_knob_radius.png|

        MicroPython Code Block:

            .. code-block:: python

                slider_0.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)

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

            |set_knob_grad_color.png|

        MicroPython Code Block:

            .. code-block:: python

                bar.set_bg_grad_color(0x00FF00, 255, 0xFF0000, 255, lv.GRAD_DIR.HOR, lv.PART.MAIN | lv.STATE.DEFAULT)
                bar.set_bg_grad_color(0x00FF00, 255, 0xFF0000, 255, lv.GRAD_DIR.HOR, lv.PART.INDICATOR | lv.STATE.DEFAULT)

    .. py:method:: get_value()

        Get the current value of the slider.

        :return: The current value of the slider.
        :rtype: int

        UiFlow2 Code Block:

            |get_value.png|

        MicroPython Code Block:

            .. code-block:: python

                value = slider_0.get_value()

    .. py:method:: set_mode(mode)

        Set the mode of the slider.

    .. py:method:: get_min_value()

        Get the minimum value of the slider range.

        :return: The minimum value of the slider range.
        :rtype: int

        UiFlow2 Code Block:

            |get_min_value.png|

        MicroPython Code Block:

            .. code-block:: python

                min_value = slider_0.get_min_value()

    .. py:method:: get_max_value()

        Get the maximum value of the slider range.

        :return: The maximum value of the slider range.
        :rtype: int

        UiFlow2 Code Block:

            |get_max_value.png|

        MicroPython Code Block:

            .. code-block:: python

                max_value = slider_0.get_max_value()

    .. py:method:: set_pos(x, y)

        Set the position of the slider.

        :param int x: The x-coordinate of the slider.
        :param int y: The y-coordinate of the slider.
        :return: None

        UiFlow2 Code Block:

            |set_pos.png|

        MicroPython Code Block:

            .. code-block:: python

                slider_0.set_pos(100, 100)

    .. py:method:: set_x(x)

        Set the x-coordinate of the slider.

        :param int x: The x-coordinate of the slider.
        :return: None

        UiFlow2 Code Block:

            |set_x.png|

        MicroPython Code Block:

            .. code-block:: python

                slider_0.set_x(100)

    .. py:method:: set_y(y)

        Set the y-coordinate of the slider.

        :param int y: The y-coordinate of the slider.
        :return: None

        UiFlow2 Code Block:

            |set_y.png|

        MicroPython Code Block:

            .. code-block:: python

                slider_0.set_y(100)

    .. py:method:: align_to(obj, align, x, y)

        Align the slider to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.
        :return: None

        UiFlow2 Code Block:

            |align_to.png|

        MicroPython Code Block:

            .. code-block:: python

                slider_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)

    .. py:method:: set_size(width, height)

        Set the size of the slider.

        :param int width: The width of the slider.
        :param int height: The height of the slider.
        :return: None

        UiFlow2 Code Block:

            |set_size.png|

        MicroPython Code Block:

            .. code-block:: python

                slider_0.set_size(200, 20)

    .. py:method:: set_width(width)

        Set the width of the slider.

        :param int width: The width of the slider.
        :return: None

        UiFlow2 Code Block:

            |set_width.png|

        MicroPython Code Block:

            .. code-block:: python

                slider_0.set_width(200)

    .. py:method:: get_width()

        Get the width of the slider.

        :return: The width of the slider.
        :rtype: int

        UiFlow2 Code Block:

            |get_width.png|

        MicroPython Code Block:

            .. code-block:: python

                slider_0.get_width()

    .. py:method:: set_height(height)

        Set the height of the slider.

        :param int height: The height of the slider.
        :return: None

        UiFlow2 Code Block:

            |set_height.png|

        MicroPython Code Block:

            .. code-block:: python

                slider_0.set_height(20)

    .. py:method:: get_height()

        Get the height of the slider.

        :return: The height of the slider.
        :rtype: int

        UiFlow2 Code Block:

            |get_height.png|

        MicroPython Code Block:

            .. code-block:: python

                slider_0.get_height()
