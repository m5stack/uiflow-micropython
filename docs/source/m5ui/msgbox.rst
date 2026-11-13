.. currentmodule:: m5ui

M5Msgbox
========

.. include:: ../refs/m5ui.msgbox.ref

M5Msgbox provides a container for labels and buttons.

Use the label and button returned by ``add_text()`` and ``add_button()``
to update their contents:

.. code-block:: python

    import M5
    import m5ui
    import lvgl as lv

    M5.begin()
    m5ui.init()
    page0 = m5ui.M5Page()
    msgbox_0 = m5ui.M5Msgbox(title="Message", w=240, h=180, parent=page0)
    label_0 = msgbox_0.add_text("Ready")
    label_0.set_text("Complete")
    label_0.set_long_mode(lv.label.LONG_MODE.WRAP)
    button_0 = msgbox_0.add_button(text="OK")
    button_0.set_btn_text("Close")
    page0.screen_load()

UiFlow2 Example
---------------

msgbox event
^^^^^^^^^^^^^^

Open the |msgbox_core2_example.m5f2| project in UiFlow2.

This example creates msgbox and associated with events.

UiFlow2 Code Block:

    |msgbox_core2_example.png|

Example output:

    None

MicroPython Example
-------------------

msgbox event
^^^^^^^^^^^^^^

This example creates msgbox and associated with events.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/msgbox/msgbox_core2_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------
M5Msgbox
^^^^^^^^

.. autoclass:: m5ui.msgbox.M5Msgbox
    :members:

    .. py:method:: add_close_button()

        Add a close button to the msgbox header.

        :return: The close button.
        :rtype: lv.obj

        UiFlow2 Code Block:

            |add_close_button.png|

        MicroPython Code Block:

            .. code-block:: python

                msgbox_0.add_close_button()

    .. py:method:: delete()

        Delete the msgbox and its child widgets.

        UiFlow2 Code Block:

            |label_delete.png|

            |button_delete.png|

        MicroPython Code Block:

            .. code-block:: python

                msgbox_0.delete()

    .. py:method:: set_style_text_font(font, part)

        Set the default text font for the msgbox.

        :param lv.lv_font_t font: The font to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |button_set_font.png|

            |label_set_font.png|

        MicroPython Code Block:

            .. code-block:: python

                msgbox_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN | lv.STATE.DEFAULT)

    .. py:method:: set_text_color(color, opa, part)

        Set the default text color for the msgbox.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |button_set_text_color.png|

            |label_set_text_color.png|

        MicroPython Code Block:

            .. code-block:: python

                msgbox_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

    .. py:method:: set_bg_color(color, opa, part)

        Set the background color of the msgbox.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |button_set_bg_color.png|

            |label_set_bg_color.png|

        MicroPython Code Block:

            .. code-block:: python

                msgbox_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

    .. py:method:: set_flag(flag, value)

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.

        UiFlow2 Code Block:

            |set_flag.png|

            |label_set_flag.png|

            |button_set_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                msgbox_0.set_flag(lv.obj.FLAG.HIDDEN, True)
    
    .. py:method:: set_pos(x, y)

        Set the position of the msgbox.

        :param int x: The x-coordinate of the msgbox.
        :param int y: The y-coordinate of the msgbox.

        UiFlow2 Code Block:

            |set_pos.png|

        MicroPython Code Block:

            .. code-block:: python

                msgbox_0.set_pos(100, 100)

    .. py:method:: set_x(x)

        Set the x-coordinate of the msgbox.

        :param int x: The x-coordinate of the msgbox.

        UiFlow2 Code Block:

            |set_x.png|

        MicroPython Code Block:

            .. code-block:: python

                msgbox_0.set_x(100)

    .. py:method:: set_y(y)

        Set the y-coordinate of the msgbox.

        :param int y: The y-coordinate of the msgbox.

        UiFlow2 Code Block:

            |set_y.png|

        MicroPython Code Block:

            .. code-block:: python

                msgbox_0.set_y(100)

    .. py:method:: set_size(width, height)

        Set the size of the msgbox.

        :param int width: The width of the msgbox.
        :param int height: The height of the msgbox.
        :return: None

        UiFlow2 Code Block:

            |set_size.png|

        MicroPython Code Block:

            .. code-block:: python

                msgbox_0.set_size(100, 50)

    .. py:method:: align_to(obj, align, x, y)

        Align the msgbox to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.

        UiFlow2 Code Block:

            |align_to.png|

        MicroPython Code Block:

            .. code-block:: python

                msgbox_0.align_to(page0, lv.ALIGN.CENTER, 0, 0)

    .. py:method:: set_state(state, value)

        Set the state of the msgbox. If ``value`` is True, the state is set; if False, the state is unset.

        :param int state: The state to set.
        :param bool value: If True, the state is set; if False, the state is unset.
        :return: None

        UiFlow2 Code Block:

            |button_set_state.png|

        MicroPython Code Block:

            .. code-block:: python

                msgbox_0.set_state(lv.STATE.PRESSED, True)

    .. py:method:: toggle_flag(flag)

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

            |button_toggle_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                msgbox_0.toggle_flag(lv.obj.FLAG.HIDDEN)

    .. py:method:: set_style_radius(radius, part)

        Set the corner radius of the msgbox.

        :param int radius: The radius to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |button_set_radius.png|

        MicroPython Code Block:

            .. code-block:: python

                msgbox_0.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)

    .. py:method:: toggle_state(state)

        Toggle the state of the msgbox. If the state is set, it is unset; if not set, it is set.

        :param int state: The state to toggle.
        :return: None

        UiFlow2 Code Block:

            |button_toggle_state.png|

        MicroPython Code Block:

            .. code-block:: python

                msgbox_0.toggle_state(lv.STATE.PRESSED)

    .. py:method:: add_event_cb(handler, event, user_data)

        Add an event callback to the msgbox. The callback will be called when the specified event occurs.

        :param function handler: The callback function to call.
        :param int event: The event to listen for.
        :param Any user_data: Optional user data to pass to the callback.
        :return: None

        UiFlow2 Code Block:

            |button_event.png|

        MicroPython Code Block:

            .. code-block:: python

                def on_clicked(event):
                    print("Clicked")

                msgbox_0.add_event_cb(on_clicked, lv.EVENT.CLICKED, None)
