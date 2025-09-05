.. currentmodule:: m5ui

M5Window
========

.. include:: ../refs/m5ui.win.ref

M5Window is a widget that can be used to create windows in the user interface.

UiFlow2 Example
---------------

window event
^^^^^^^^^^^^^^

Open the |window_core2_example.m5f2| project in UiFlow2.

This example creates a window and associates it with events.

UiFlow2 Code Block:

    |example.png|

Example output:

    None


MicroPython Example
-------------------

window event
^^^^^^^^^^^^^^

This example creates a window and associates it with events.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/window/window_core2_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------
M5Win
^^^^^^^^

.. autoclass:: m5ui.win.M5Win
    :members:
    
    .. py:method:: delete()

        Delete the item from the window.

        UiFlow2 Code Block:

            |label_delete.png|

            |button_delete.png|

            |title_delete.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.delete()

                button_0.delete()

                text_0.delete()

    
    .. py:method:: set_text(txt)

        Set text of the window button/label/title.

        :param str txt: The text to set for the window button/label/title.
        :return: None

        UiFlow2 Code Block:

            |button_set_text.png|

            |label_set_text.png|

            |title_set_text.png|

        MicroPython Code Block:
    
            .. code-block:: python

                button_0.set_text("Select an option")

                label_0.set_text("M5Stack")

                title_0.set_text("Hello M5Stack")

    .. py:method:: set_style_text_font(font, part)

        Set the font of the window button text.

        :param lv.lv_font_t font: The font to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |button_set_font.png|

        MicroPython Code Block:

            .. code-block:: python

                button_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN | lv.STATE.DEFAULT)

    .. py:method:: set_text_color(color, opa, part)

        Set the color of the window button/label/title.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |button_set_text_color.png|

            |label_set_text_color.png|

            |title_set_text_color.png|

        MicroPython Code Block:

            .. code-block:: python

                button_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

                label_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

                title_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

    .. py:method:: set_bg_color(color, opa, part)

        Set the background color of the window button/label/title.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |button_set_bg_color.png|

            |label_set_bg_color.png|

            |title_set_bg_color.png|

        MicroPython Code Block:

            .. code-block:: python

                button_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

                label_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

                title_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

    .. py:method:: set_long_mode(mode)

        Set the long mode of the window label/title.

        :param int mode: The long mode to set.

        UiFlow2 Code Block:

            |label_set_long_mode.png|

            |title_set_long_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.set_long_mode(lv.label.LONG_MODE.WRAP)

    .. py:method:: set_flag(flag, value)

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.

        UiFlow2 Code Block:

            |button_set_flag.png|

            |label_set_flag.png|

            |title_set_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                window_0.set_flag(lv.obj.FLAG.HIDDEN, True)
    
    .. py:method:: set_pos(x, y)

        Set the position of the window.

        :param int x: The x-coordinate of the window.
        :param int y: The y-coordinate of the window.

        UiFlow2 Code Block:

            |set_pos.png|

        MicroPython Code Block:

            .. code-block:: python

                window_0.set_pos(100, 100)

    .. py:method:: set_x(x)

        Set the x-coordinate of the window.

        :param int x: The x-coordinate of the window.

        UiFlow2 Code Block:

            |set_x.png|

        MicroPython Code Block:

            .. code-block:: python

                window_0.set_x(100)

    .. py:method:: set_y(y)

        Set the y-coordinate of the window.

        :param int y: The y-coordinate of the window.

        UiFlow2 Code Block:

            |set_y.png|

        MicroPython Code Block:

            .. code-block:: python

                window_0.set_y(100)

    .. py:method:: set_size(width, height)

        Set the size of the window.

        :param int width: The width of the window.
        :param int height: The height of the window.
        :return: None

        UiFlow2 Code Block:

            |set_size.png|

        MicroPython Code Block:

            .. code-block:: python

                window_0.set_size(100, 50)


    .. py:method:: align_to(obj, align, x, y)

        Align the windowto another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.

        UiFlow2 Code Block:

            |align_to.png|

        MicroPython Code Block:

            .. code-block:: python

                window_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)

    .. py:method:: set_state(state, value)

        Set the state of the bar. If ``value`` is True, the state is set; if False, the state is unset.

        :param int state: The state to set.
        :param bool value: If True, the state is set; if False, the state is unset.
        :return: None

        UiFlow2 Code Block:

            |button_set_state.png|

        MicroPython Code Block:

            .. code-block:: python

                window_0.set_state(lv.STATE.PRESSED, True)

    .. py:method:: toggle_flag(flag)

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

            |button_toggle_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                window_0.toggle_flag(lv.obj.FLAG.HIDDEN)


    .. py:method:: set_style_radius(radius, part)

        Set the corner radius of the window button.

        :param int radius: The radius to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |button_set_radius.png|

        MicroPython Code Block:

            .. code-block:: python

                button_0.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)

    .. py:method:: set_shadow(color, opa, align, offset_x, offset_y)
        
        Set a shadow for the label/title.

        :param int color: The color of the shadow in hexadecimal format or an integer.
        :param int opa: The opacity of the shadow (0-255).
        :param int align: The alignment of the shadow relative to the label/title.
        :param int offset_x: The horizontal offset of the shadow.
        :param int offset_y: The vertical offset of the shadow.
        :return: None

        UiFlow2 Code Block:

            |label_set_shadow.png|

            |title_set_shadow.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.set_shadow(color=0x000000, opa=128, align=lv.ALIGN.BOTTOM_RIGHT, offset_x=5, offset_y=5)

    .. py:method:: unset_shadow()

        Remove the shadow from the label/title.

        UiFlow2 Code Block:

            |label_unset_shadow.png|

            |title_unset_shadow.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.unset_shadow()

    .. py:method:: get_text()

        Get the text of the button/label/title.

        :return: The text of the button/label/title.
        :rtype: str

        UiFlow2 Code Block:

            |button_get_text.png|

            |label_get_text.png|

            |title_get_text.png|
            
        MicroPython Code Block:

            .. code-block:: python

                button_0.get_text()

                label_0.get_text()

                text_0.get_text()


    .. py:method:: toggle_state(state)

        Toggle the state of the button. If the state is set, it is unset; if not set, it is set.

        :param int state: The state to toggle.
        :return: None

        UiFlow2 Code Block:

            |button_toggle_state.png|

        MicroPython Code Block:

            .. code-block:: python

                button_0.toggle_state(lv.STATE.PRESSED)

    .. py:method:: add_event_cb(handler, event, user_data)

        Add an event callback to the button. The callback will be called when the specified event occurs.

        :param function handler: The callback function to call.
        :param int event: The event to listen for.
        :param Any user_data: Optional user data to pass to the callback.
        :return: None

        UiFlow2 Code Block:

            |button_event.png|

        MicroPython Code Block:

            .. code-block:: python

                def btn_ono_clicked_event(event_struct):
                    global page0, window_0, label_lkg, btn_ono, btn_pjm, label0

                    print('hello M5')


                def btn_ono_event_handler(event_struct):
                    global page0, window_0, label_lkg, btn_ono, btn_pjm, label0
                    event = event_struct.code
                    if event == lv.EVENT.CLICKED and True:
                        btn_ono_clicked_event(event_struct)
                    return

                btn_ono.add_event_cb(btn_ono_event_handler, lv.EVENT.ALL, None)

