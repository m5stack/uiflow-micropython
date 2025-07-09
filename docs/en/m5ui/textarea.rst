.. currentmodule:: m5ui

M5TextArea
==========

.. include:: ../refs/m5ui.textarea.ref

M5TextArea is a widget that can be used to create text input areas in the user interface. It allows users to input and edit multi-line text with support for placeholders, scrolling, and various styling options.


UiFlow2 Example
---------------

basic textarea
^^^^^^^^^^^^^^

Open the |cores3_textarea_basic_example.m5f2| project in UiFlow2.

This example demonstrates how to add text content to a text box and clear the content of the text box using a button.

UiFlow2 Code Block:

    |cores3_textarea_basic_example.png|

Example output:

    None


MicroPython Example
-------------------

basic textarea
^^^^^^^^^^^^^^

This example demonstrates how to add text content to a text box and clear the content of the text box using a button.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/textarea/cores3_textarea_basic_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

M5TextArea
^^^^^^^^^^

.. autoclass:: m5ui.textarea.M5TextArea
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

                textarea_0.set_flag(lv.obj.FLAG.HIDDEN, True)

    .. py:method:: toggle_flag(flag)

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

            |toggle_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                textarea_0.toggle_flag(lv.obj.FLAG.HIDDEN)

    .. py:method:: set_state(state, value)

        Set the state of the textarea. If ``value`` is True, the state is set; if False, the state is unset.

        :param int state: The state to set.
        :param bool value: If True, the state is set; if False, the state is unset.
        :return: None

        UiFlow2 Code Block:

            |set_state.png|

        MicroPython Code Block:

            .. code-block:: python

                textarea_0.set_state(lv.STATE.PRESSED, True)

    .. py:method:: toggle_state(state)

        Toggle the state of the textarea. If the state is set, it is unset; if not set, it is set.

        :param int state: The state to toggle.
        :return: None

        UiFlow2 Code Block:

            |toggle_state.png|

        MicroPython Code Block:

            .. code-block:: python

                textarea_0.toggle_state(lv.STATE.PRESSED)

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

                def textarea_0_ready_event(event_struct):
                    global page0, button0
                    print("released")

                def textarea_0_value_changed_event(event_struct):
                    global page0, button0
                    print("value changed")

                def textarea_0_focused_event(event_struct):
                    global page0, button0
                    print("focused")

                def textarea_0_defocused_event(event_struct):
                    global page0, button0
                    print("focused")

                def textarea_0_event_handler(event_struct):
                    event = event_struct.code
                    if event == lv.EVENT.VALUE_CHANGED and True:
                        textarea_0_value_changed_event(event_struct)
                    elif event == lv.EVENT.READY and True:
                        textarea_0_ready_event(event_struct) # 单行模式下才会触发
                    elif event == lv.EVENT.FOCUSED:
                        textarea_0_focused_event(event_struct)
                    elif event == lv.EVENT.DEFOCUSED:
                        textarea_0_defocused_event(event_struct)
                    return

                textarea_0.add_event_cb(textarea_0_event_handler, lv.EVENT.ALL, None)

    .. py:method:: set_bg_color(color, opa, part)

        Set the background color of the textarea.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |set_bg_color.png|

        MicroPython Code Block:

            .. code-block:: python

                textarea_0.set_bg_color(lv.color_hex(0xFFFFFF), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

    .. py:method:: set_style_radius(radius, part)

        Set the corner radius of the slider components.

        :param int radius: The radius to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |set_style_radius.png|

        MicroPython Code Block:

            .. code-block:: python

                slider_0.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)

    .. py:method:: set_border_color(color, opa, part)

        Set the border color of the textarea.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |set_border_color.png|

        MicroPython Code Block:

            .. code-block:: python

                textarea_0.set_border_color(lv.color_hex(0xE0E0E0), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

    .. py:method:: set_style_border_width(width, part)

        Set the border width of the textarea.

        :param int width: The width to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |set_style_border_width.png|

        MicroPython Code Block:

            .. code-block:: python

                textarea_0.set_style_border_width(2, lv.PART.MAIN | lv.STATE.DEFAULT)

    .. py:method:: set_placeholder_text(text)

        Set the placeholder text that appears when the textarea is empty.

        :param str text: The placeholder text to set.
        :return: None

        UiFlow2 Code Block:

            |set_placeholder_text.png|

        MicroPython Code Block:

            .. code-block:: python

                textarea_0.set_placeholder_text("Enter text here...")

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

                textarea_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)

    .. py:method:: set_style_text_font(font, part)

        Set the font of the textarea text.

        :param lv.font_t font: The font to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |set_placeholder_font.png|

            |set_text_font.png|

        MicroPython Code Block:

            .. code-block:: python

                textarea_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN | lv.STATE.DEFAULT)


    .. py:method:: set_style_text_align(align, part)

        Set the text alignment of the textarea.

        :param int align: The alignment to set (e.g., lv.TEXT_ALIGN.LEFT, lv.TEXT_ALIGN.CENTER).
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |set_placeholder_align.png|

            |set_text_align.png|

        MicroPython Code Block:

            .. code-block:: python

                textarea_0.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN | lv.STATE.DEFAULT)

    .. py:method:: set_text(text)

        Set the text content of the textarea.

        :param str text: The text to set.
        :return: None

        UiFlow2 Code Block:

            |set_text.png|

        MicroPython Code Block:

            .. code-block:: python

                textarea_0.set_text("Hello World")
                textarea_0.set_text("") # Clear the text content

    .. py:method:: get_text()

        Get the current text content of the textarea.

        :return: The current text content.
        :rtype: str

        UiFlow2 Code Block:

            |get_text.png|

        MicroPython Code Block:

            .. code-block:: python

                text = textarea_0.get_text()

    .. py:method:: add_text(text)

        Add text to the current content of the textarea.

        :param str text: The text to add.
        :return: None

        UiFlow2 Code Block:

            |add_text.png|

        MicroPython Code Block:

            .. code-block:: python

                textarea_0.add_text(" Additional text")

    .. py:method:: set_max_length(length)

        Set the maximum length of text that can be entered in the textarea.

        :param int length: The maximum length of text.
        :return: None

        UiFlow2 Code Block:

            |set_max_length.png|

        MicroPython Code Block:

            .. code-block:: python

                textarea_0.set_max_length(256)

    .. py:method:: set_password_mode(en)

        Set whether the textarea should be in password mode (i.e., characters are hidden).

        :param bool en: True to enable password mode, False to disable.
        :return: None

        UiFlow2 Code Block:

            |set_password_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                textarea_0.set_password_mode(True)

    .. py:method:: set_one_line(text)

        Set whether the textarea should be single line or multi-line.

        :param bool text: True for single line, False for multi-line.
        :return: None

        UiFlow2 Code Block:

            |set_one_line.png|

        MicroPython Code Block:

            .. code-block:: python

                textarea_0.set_one_line(True)

    .. py:method:: set_accepted_chars(chars)

        Set the characters that are accepted in the textarea. Only these characters can be entered.

        :param str chars: The string of accepted characters.
        :return: None

        UiFlow2 Code Block:

            |set_accepted_chars.png|

        MicroPython Code Block:

            .. code-block:: python

                textarea_0.set_accepted_chars("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

    .. py:method:: set_pos(x, y)

        Set the position of the textarea.

        :param int x: The x-coordinate of the textarea.
        :param int y: The y-coordinate of the textarea.
        :return: None

        UiFlow2 Code Block:

            |set_pos.png|

        MicroPython Code Block:

            .. code-block:: python

                textarea_0.set_pos(100, 100)

    .. py:method:: set_x(x)

        Set the x-coordinate of the textarea.

        :param int x: The x-coordinate of the textarea.
        :return: None

        UiFlow2 Code Block:

            |set_x.png|

        MicroPython Code Block:

            .. code-block:: python

                textarea_0.set_x(100)

    .. py:method:: set_y(y)

        Set the y-coordinate of the textarea.

        :param int y: The y-coordinate of the textarea.
        :return: None

        UiFlow2 Code Block:

            |set_y.png|

        MicroPython Code Block:

            .. code-block:: python

                textarea_0.set_y(100)

    .. py:method:: align_to(obj, align, x, y)

        Align the textarea to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.
        :return: None

        UiFlow2 Code Block:

            |align_to.png|

        MicroPython Code Block:

            .. code-block:: python

                textarea_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)

    .. py:method:: set_size(width, height)

        Set the size of the textarea.

        :param int width: The width of the textarea.
        :param int height: The height of the textarea.
        :return: None

        UiFlow2 Code Block:

            |set_size.png|

        MicroPython Code Block:

            .. code-block:: python

                textarea_0.set_size(200, 100)

    .. py:method:: set_width(width)

        Set the width of the textarea.

        :param int width: The width of the textarea.
        :return: None

        UiFlow2 Code Block:

            |set_width.png|

        MicroPython Code Block:

            .. code-block:: python

                textarea_0.set_width(200)

    .. py:method:: set_height(height)

        Set the height of the textarea.

        :param int height: The height of the textarea.
        :return: None

        UiFlow2 Code Block:

            |set_height.png|

        MicroPython Code Block:

            .. code-block:: python

                textarea_0.set_height(100)

    .. py:method:: get_width()

        Get the width of the textarea.

        :return: The width of the textarea.
        :rtype: int

        UiFlow2 Code Block:

            |get_width.png|

        MicroPython Code Block:

            .. code-block:: python

                width = textarea_0.get_width()

    .. py:method:: get_height()

        Get the height of the textarea.

        :return: The height of the textarea.
        :rtype: int

        UiFlow2 Code Block:

            |get_height.png|

        MicroPython Code Block:

            .. code-block:: python

                height = textarea_0.get_height()
