.. currentmodule:: m5ui

M5Keyboard
==========

.. include:: ../refs/m5ui.keyboard.ref

M5Keyboard is a widget that can be used to create virtual keyboards in the user interface. It provides an on-screen keyboard that can be used for text input with support for different keyboard modes and layouts.


UiFlow2 Example
---------------

basic keyboard
^^^^^^^^^^^^^^

Open the |cores3_keyboard_basic_example.m5f2| project in UiFlow2.

This example demonstrates how to create a virtual keyboard and connect it to a text input area.

UiFlow2 Code Block:

    |cores3_keyboard_basic_example.png|

Example output:

    None


MicroPython Example
-------------------

basic keyboard
^^^^^^^^^^^^^^

This example demonstrates how to create a virtual keyboard and connect it to a text input area.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/keyboard/cores3_keyboard_basic_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

M5Keyboard
^^^^^^^^^^

.. autoclass:: m5ui.keyboard.M5Keyboard
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

                keyboard_0.set_flag(lv.obj.FLAG.HIDDEN, True)

    .. py:method:: toggle_flag(flag)

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

            |toggle_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                keyboard_0.toggle_flag(lv.obj.FLAG.HIDDEN)

    .. py:method:: set_state(state, value)

        Set the state of the keyboard. If ``value`` is True, the state is set; if False, the state is unset.

        :param int state: The state to set.
        :param bool value: If True, the state is set; if False, the state is unset.
        :return: None

        UiFlow2 Code Block:

            |set_state.png|

        MicroPython Code Block:

            .. code-block:: python

                keyboard_0.set_state(lv.STATE.PRESSED, True)

    .. py:method:: toggle_state(state)

        Toggle the state of the keyboard. If the state is set, it is unset; if not set, it is set.

        :param int state: The state to toggle.
        :return: None

        UiFlow2 Code Block:

            |toggle_state.png|

        MicroPython Code Block:

            .. code-block:: python

                keyboard_0.toggle_state(lv.STATE.PRESSED)

    .. py:method:: add_event_cb(handler, event, user_data)

        Add an event callback to the keyboard. The callback will be called when the specified event occurs.

        :param function handler: The callback function to call.
        :param int event: The event to listen for.
        :param Any user_data: Optional user data to pass to the callback.
        :return: None

        UiFlow2 Code Block:

            |event.png|

        MicroPython Code Block:

            .. code-block:: python

                def keyboard_0_value_changed_event(event_struct):
                    global page0, textarea0
                    print("Key pressed")

                def keyboard_0_ready_event(event_struct):
                    global page0, textarea0
                    print("Ready")

                def keyboard_0_event_handler(event_struct):
                    event = event_struct.code
                    if event == lv.EVENT.VALUE_CHANGED:
                        keyboard_0_value_changed_event(event_struct)
                    elif event == lv.EVENT.READY:
                        keyboard_0_ready_event(event_struct)
                    return

                keyboard_0.add_event_cb(keyboard_0_event_handler, lv.EVENT.ALL, None)

    .. py:method:: set_textarea(textarea)

        Set the text area that this keyboard should control. When keys are pressed, the text will be entered into the specified text area.

        :param lv.textarea textarea: The text area object to connect to the keyboard.
        :return: None

        UiFlow2 Code Block:

            |set_textarea.png|

        MicroPython Code Block:

            .. code-block:: python

                keyboard_0.set_textarea(textarea_0)

    .. py:method:: get_textarea()

        Get the text area that is currently connected to this keyboard.

        :return: The connected text area object, or None if no text area is connected.
        :rtype: lv.textarea or None

        UiFlow2 Code Block:

            |get_textarea.png|

        MicroPython Code Block:

            .. code-block:: python

                ta = keyboard_0.get_textarea()

    .. py:method:: set_mode(mode)

        Set the keyboard mode to display different keyboard layouts.

        :param int mode: The keyboard mode to set.
        :return: None

        Available modes include:

            - lv.keyboard.MODE.TEXT_LOWER: 0.
            - lv.keyboard.MODE.TEXT_UPPER: 1.
            - lv.keyboard.MODE.SYMBOL: 2.
            - lv.keyboard.MODE.NUMBER: 3.

        UiFlow2 Code Block:

            |set_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                keyboard_0.set_mode(lv.keyboard.MODE.TEXT_LOWER)

    .. py:method:: get_mode()

        Get the current keyboard mode.

        :return: The current keyboard mode.
        :rtype: int

        Keyboard modes include:

            - lv.keyboard.MODE.TEXT_LOWER: 0.
            - lv.keyboard.MODE.TEXT_UPPER: 1.
            - lv.keyboard.MODE.SYMBOL: 2.
            - lv.keyboard.MODE.NUMBER: 3.

        UiFlow2 Code Block:

            |get_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                mode = keyboard_0.get_mode()

    .. py:method:: set_popovers(en)

        Enable or disable popovers for the keyboard. Popovers are additional UI elements that can be displayed when certain keys are pressed.

        :param bool en: If True, popovers are enabled; if False, they are disabled.
        :return: None

        UiFlow2 Code Block:

            |set_popovers.png|

        MicroPython Code Block:

            .. code-block:: python

                keyboard_0.set_popovers(True)

    .. py:method:: get_selected_button()

        Get the index of the last released button. This can be useful to determine which key was last pressed.

        :return: index of the last released button.
        :rtype: int

        UiFlow2 Code Block:

            |get_selected_button.png|

        MicroPython Code Block:

            .. code-block:: python

                btn = keyboard_0.get_selected_button()

    .. py:method:: get_button_text(btn_id)

        Get the text of a button by its index.

        :param int btn: The index of the button.
        :return: The text of the button.
        :rtype: str

        UiFlow2 Code Block:

            |get_button_text.png|

        MicroPython Code Block:

            .. code-block:: python

                keyboard_0.get_button_text(3)

    .. py:method:: set_pos(x, y)

        Set the position of the keyboard.

        :param int x: The x-coordinate of the keyboard.
        :param int y: The y-coordinate of the keyboard.
        :return: None

        UiFlow2 Code Block:

            |set_pos.png|

        MicroPython Code Block:

            .. code-block:: python

                keyboard_0.set_pos(100, 100)

    .. py:method:: set_x(x)

        Set the x-coordinate of the keyboard.

        :param int x: The x-coordinate of the keyboard.
        :return: None

        UiFlow2 Code Block:

            |set_x.png|

        MicroPython Code Block:

            .. code-block:: python

                keyboard_0.set_x(100)

    .. py:method:: set_y(y)

        Set the y-coordinate of the keyboard.

        :param int y: The y-coordinate of the keyboard.
        :return: None

        UiFlow2 Code Block:

            |set_y.png|

        MicroPython Code Block:

            .. code-block:: python

                keyboard_0.set_y(100)

    .. py:method:: set_size(width, height)

        Set the size of the keyboard.

        :param int width: The width of the keyboard.
        :param int height: The height of the keyboard.
        :return: None

        UiFlow2 Code Block:

            |set_size.png|

        MicroPython Code Block:

            .. code-block:: python

                keyboard_0.set_size(300, 200)

    .. py:method:: set_width(width)

        Set the width of the keyboard.

        :param int width: The width of the keyboard.
        :return: None

        UiFlow2 Code Block:

            |set_width.png|

        MicroPython Code Block:

            .. code-block:: python

                keyboard_0.set_width(300)

    .. py:method:: get_width()

        Get the width of the keyboard.

        :return: The width of the keyboard.
        :rtype: int

        UiFlow2 Code Block:

            |get_width.png|

        MicroPython Code Block:

            .. code-block:: python

                width = keyboard_0.get_width()

    .. py:method:: set_height(height)

        Set the height of the keyboard.

        :param int height: The height of the keyboard.
        :return: None

        UiFlow2 Code Block:

            |set_height.png|

        MicroPython Code Block:

            .. code-block:: python

                keyboard_0.set_height(200)

    .. py:method:: get_height()

        Get the height of the keyboard.

        :return: The height of the keyboard.
        :rtype: int

        UiFlow2 Code Block:

            |get_height.png|

        MicroPython Code Block:

            .. code-block:: python

                height = keyboard_0.get_height()

    .. py:method:: align_to(obj, align, x, y)

        Align the keyboard to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.
        :return: None

        UiFlow2 Code Block:

            |align_to.png|

        MicroPython Code Block:

            .. code-block:: python

                keyboard_0.align_to(page_0, lv.ALIGN.BOTTOM_MID, 0, -10)
