.. currentmodule:: m5ui

M5LED
=====

.. include:: ../refs/m5ui.led.ref

M5LED is a lightweight widget that simulates a light-emitting diode indicator in the user interface.

UiFlow2 Example
---------------

LED Basic Usage Example
^^^^^^^^^^^^^^^^^^^^^^^

Open the |m5cores3_m5ui_led_example.m5f2| project in UiFlow2.

This example demonstrates how to create and control an LED widget.
It shows how to turn the LED on and off, change its color, adjust brightness.

UiFlow2 Code Block:

    |m5cores3_m5ui_led_example.png|

Example output:

    None.

MicroPython Example
-------------------

LED Basic Usage Example
^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to create and control an LED widget.
It shows how to turn the LED on and off, change its color, adjust brightness.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/led/m5cores3_m5ui_led_example.py
        :language: python
        :linenos:

Example output:

    None.

**API**
-------

M5LED
^^^^^

.. autoclass:: m5ui.led.M5LED
    :members:

    .. py:method:: on()

        Turn on the LED.

        :return: None

        UiFlow2 Code Block:

            |on.png|

        MicroPython Code Block:

            .. code-block:: python

                led_0.on()

    .. py:method:: off()

        Turn off the LED.

        :return: None

        UiFlow2 Code Block:

            |set_state.png|

        MicroPython Code Block:

            .. code-block:: python

                led_0.off()

    .. py:method:: toggle()

        Toggle the state of a LED.

        :return: None

        UiFlow2 Code Block:

            |toggle.png|

        MicroPython Code Block:

            .. code-block:: python

                led_0.toggle()

    .. py:method:: set_color(color)

        Set the color of the LED.

        :param int color: The color of the LED (RGB888 format).
        :return: None

        UiFlow2 Code Block:

            |set_color.png|

        MicroPython Code Block:

            .. code-block:: python

                led_0.set_color(color)

    .. py:method:: set_pos(x, y)

        Set the position of the LED.

        :param int x: The x position of the LED.
        :param int y: The y position of the LED.
        :return: None

        UiFlow2 Code Block:

            |set_pos.png|

        MicroPython Code Block:

            .. code-block:: python

                led_0.set_pos(x, y)

    .. py:method:: set_x(x)

        Set the x position of the LED.

        :param int x: The x position of the LED.
        :return: None

        UiFlow2 Code Block:

            |set_x.png|

        MicroPython Code Block:

            .. code-block:: python

                led_0.set_x(x)

    .. py:method:: set_y(y)

        Set the y position of the LED.

        :param int y: The y position of the LED.
        :return: None

        UiFlow2 Code Block:

            |set_y.png|

        MicroPython Code Block:

            .. code-block:: python

                led_0.set_y(y)

    .. py:method:: get_x()

        Get the x position of the LED.

        :return: The x position of the LED.
        :rtype: int

        UiFlow2 Code Block:

            |get_x.png|

        MicroPython Code Block:

            .. code-block:: python

                x = led_0.get_x()

    .. py:method:: get_y()

        Get the y position of the LED.

        :return: The y position of the LED.
        :rtype: int

        UiFlow2 Code Block:

            |get_y.png|

        MicroPython Code Block:

            .. code-block:: python

                y = led_0.get_y()

    .. py:method:: set_size(width, height)

        Set the size of the LED.

        :param int width: The width of the LED.
        :param int height: The height of the LED.
        :return: None

        UiFlow2 Code Block:

            |set_size.png|

        MicroPython Code Block:

            .. code-block:: python

                led_0.set_size(width, height)

    .. py:method:: set_width(width)

        Set the width of the LED.

        :param int width: The width of the LED.
        :return: None

        UiFlow2 Code Block:

            |set_width.png|

        MicroPython Code Block:

            .. code-block:: python

                led_0.set_width(width)

    .. py:method:: set_height(height)

        Set the height of the LED.

        :param int height: The height of the LED.
        :return: None

        UiFlow2 Code Block:

            |set_height.png|

        MicroPython Code Block:

            .. code-block:: python

                led_0.set_height(height)

    .. py:method:: align_to(obj, align, x, y)

        Align the LED relative to another object.

        :param obj: The reference object (e.g. page0).
        :param int align: Alignment option (see lv.ALIGN constants below).
        :param int x: X offset after alignment.
        :param int y: Y offset after alignment.
        :return: None

        UiFlow2 Code Block:

            |align_to.png|

        MicroPython Code Block:

            .. code-block:: python

                led_0.align_to(page0, lv.ALIGN.CENTER, 0, 0)

    .. py:data:: lv.ALIGN

        Alignment options for positioning objects.

        - lv.ALIGN.DEFAULT
        - lv.ALIGN.TOP_LEFT
        - lv.ALIGN.TOP_MID
        - lv.ALIGN.TOP_RIGHT
        - lv.ALIGN.BOTTOM_LEFT
        - lv.ALIGN.BOTTOM_MID
        - lv.ALIGN.BOTTOM_RIGHT
        - lv.ALIGN.LEFT_MID
        - lv.ALIGN.RIGHT_MID
        - lv.ALIGN.CENTER
        - lv.ALIGN.OUT_TOP_LEFT
        - lv.ALIGN.OUT_TOP_MID
        - lv.ALIGN.OUT_TOP_RIGHT
        - lv.ALIGN.OUT_BOTTOM_LEFT
        - lv.ALIGN.OUT_BOTTOM_MID
        - lv.ALIGN.OUT_BOTTOM_RIGHT
        - lv.ALIGN.OUT_LEFT_TOP
        - lv.ALIGN.OUT_LEFT_MID
        - lv.ALIGN.OUT_LEFT_BOTTOM
        - lv.ALIGN.OUT_RIGHT_TOP
        - lv.ALIGN.OUT_RIGHT_MID
        - lv.ALIGN.OUT_RIGHT_BOTTOM
