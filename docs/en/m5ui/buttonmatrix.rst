.. currentmodule:: m5ui

M5ButtonMatrix
==============

.. include:: ../refs/m5ui.buttonmatrix.ref

M5ButtonMatrix is a widget that can be used to create a matrix of buttons in the
user interface. It provides a flexible layout for displaying multiple buttons in
a grid format with support for different button configurations and text labels.


UiFlow2 Example
---------------

basic buttonmatrix
^^^^^^^^^^^^^^^^^^

Open the |cores3_buttonmatrix_basic_example.m5f2| project in UiFlow2.

This example demonstrates how to create a button matrix with custom labels and handle button press events.

UiFlow2 Code Block:

    |cores3_buttonmatrix_basic_example.png|

Example output:

    None


MicroPython Example
-------------------

basic buttonmatrix
^^^^^^^^^^^^^^^^^^

This example demonstrates how to create a button matrix with custom labels and handle button press events.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/buttonmatrix/cores3_buttonmatrix_basic_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

M5ButtonMatrix
^^^^^^^^^^^^^^

.. autoclass:: m5ui.buttonmatrix.M5ButtonMatrix
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

                buttonmatrix_0.set_flag(lv.obj.FLAG.HIDDEN, True)


    .. py:method:: toggle_flag(flag)

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

            |toggle_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                buttonmatrix_0.toggle_flag(lv.obj.FLAG.HIDDEN)


    .. py:method:: set_state(state, value)

        Set the state of the buttonmatrix. If ``value`` is True, the state is set; if False, the state is unset.

        :param int state: The state to set.
        :param bool value: If True, the state is set; if False, the state is unset.
        :return: None

        UiFlow2 Code Block:

            |set_state.png|

        MicroPython Code Block:

            .. code-block:: python

                buttonmatrix_0.set_state(lv.STATE.PRESSED, True)


    .. py:method:: toggle_state(state)

        Toggle the state of the buttonmatrix. If the state is set, it is unset; if not set, it is set.

        :param int state: The state to toggle.
        :return: None

        UiFlow2 Code Block:

            |toggle_state.png|

        MicroPython Code Block:

            .. code-block:: python

                buttonmatrix_0.toggle_state(lv.STATE.PRESSED)


    .. py:method:: add_event_cb(handler, event, user_data)

        Add an event callback to the buttonmatrix. The callback will be called when the specified event occurs.

        :param function handler: The callback function to call.
        :param int event: The event to listen for.
        :param Any user_data: Optional user data to pass to the callback.
        :return: None

        UiFlow2 Code Block:

            |event.png|

        MicroPython Code Block:

            .. code-block:: python

                def buttonmatrix_0_pressed_event(event_struct):
                    global page0
                    btn_id = buttonmatrix_0.get_selected_button()
                    print(f"Button {btn_id} pressed")

                def buttonmatrix_0_event_handler(event_struct):
                    event = event_struct.code
                    if event == lv.EVENT.VALUE_CHANGED:
                        buttonmatrix_0_pressed_event(event_struct)
                    return

                buttonmatrix_0.add_event_cb(buttonmatrix_0_event_handler, lv.EVENT.ALL, None)


    .. py:method:: set_button_width(btn_id, width)

        Set the relative width of a specific button.

        :param int btn_id: The index of the button.
        :param int width: The relative width (1-7, where 1 is normal width).
        :return: None

        UiFlow2 Code Block:

            |set_button_width.png|

        MicroPython Code Block:

            .. code-block:: python

                buttonmatrix_0.set_button_width(0, 2)  # Make first button twice as wide


    .. py:method:: get_selected_button()

        Get the index of the last pressed button.

        :return: The index of the last pressed button, or lv.buttonmatrix.BUTTON.NONE if no button is pressed.
        :rtype: int

        UiFlow2 Code Block:

            |get_selected_button.png|

        MicroPython Code Block:

            .. code-block:: python

                btn_id = buttonmatrix_0.get_selected_button()


    .. py:method:: get_button_text(btn_id)

        Get the text of a specific button.

        :param int btn_id: The index of the button.
        :return: The text of the button.
        :rtype: str

        UiFlow2 Code Block:

            |get_button_text.png|

        MicroPython Code Block:

            .. code-block:: python

                text = buttonmatrix_0.get_button_text(0)


    .. py:method:: clear_button_ctrl(btn_id, ctrl)

        Clear control flags for a specific button.

        :param int btn_id: The button ID to clear control flags for.
        :param int ctrl: The control flags to clear.

        UiFlow2 Code Block:

            |clear_button_ctrl.png|

        MicroPython Code Block:

            .. code-block:: python

                buttonmatrix_0.clear_button_ctrl(0, lv.buttonmatrix.CTRL.HIDDEN)


    .. py:method:: set_button_ctrl(btn_id, ctrl)

        Set control flags for a specific button.

        :param int btn_id: The button ID to set control flags for.
        :param int ctrl: The control flags to set.

        UiFlow2 Code Block:

            |set_button_ctrl.png|

        MicroPython Code Block:

            .. code-block:: python

                buttonmatrix_0.set_button_ctrl(0, lv.buttonmatrix.CTRL.HIDDEN)


    .. py:method:: set_button_ctrl_all(ctrl)

        Set control flags for all buttons.

        :param int ctrl: The control flags to set for all buttons.

        UiFlow2 Code Block:

            |set_button_ctrl_all.png|

        MicroPython Code Block:

            .. code-block:: python

                buttonmatrix_0.set_button_ctrl_all(lv.buttonmatrix.CTRL.HIDDEN)


    .. py:method:: clear_button_ctrl_all(ctrl)

        Clear control flags for all buttons.

        :param int ctrl: The control flags to clear for all buttons.

        UiFlow2 Code Block:

            |clear_button_ctrl_all.png|

        MicroPython Code Block:

            .. code-block:: python

                buttonmatrix_0.clear_button_ctrl_all(lv.buttonmatrix.CTRL.HIDDEN)


    .. py:method:: set_one_checked(btn_id)

        Set a specific button as checked.

        :param int btn_id: The button ID to set as checked.

        UiFlow2 Code Block:

            |set_one_checked.png|

        MicroPython Code Block:

            .. code-block:: python

                buttonmatrix_0.set_one_checked(0)


    .. py:method:: set_pos(x, y)

        Set the position of the buttonmatrix.

        :param int x: The x-coordinate of the buttonmatrix.
        :param int y: The y-coordinate of the buttonmatrix.
        :return: None

        UiFlow2 Code Block:

            |set_pos.png|

        MicroPython Code Block:

            .. code-block:: python

                buttonmatrix_0.set_pos(100, 100)


    .. py:method:: set_x(x)

        Set the x-coordinate of the buttonmatrix.

        :param int x: The x-coordinate of the buttonmatrix.
        :return: None

        UiFlow2 Code Block:

            |set_x.png|

        MicroPython Code Block:

            .. code-block:: python

                buttonmatrix_0.set_x(100)


    .. py:method:: set_y(y)

        Set the y-coordinate of the buttonmatrix.

        :param int y: The y-coordinate of the buttonmatrix.
        :return: None

        UiFlow2 Code Block:

            |set_y.png|

        MicroPython Code Block:

            .. code-block:: python

                buttonmatrix_0.set_y(100)


    .. py:method:: set_size(width, height)

        Set the size of the buttonmatrix.

        :param int width: The width of the buttonmatrix.
        :param int height: The height of the buttonmatrix.
        :return: None

        UiFlow2 Code Block:

            |set_size.png|

        MicroPython Code Block:

            .. code-block:: python

                buttonmatrix_0.set_size(300, 200)


    .. py:method:: set_width(width)

        Set the width of the buttonmatrix.

        :param int width: The width of the buttonmatrix.
        :return: None

        UiFlow2 Code Block:

            |set_width.png|

        MicroPython Code Block:

            .. code-block:: python

                buttonmatrix_0.set_width(300)


    .. py:method:: get_width()

        Get the width of the buttonmatrix.

        :return: The width of the buttonmatrix.
        :rtype: int

        UiFlow2 Code Block:

            |get_width.png|

        MicroPython Code Block:

            .. code-block:: python

                width = buttonmatrix_0.get_width()


    .. py:method:: set_height(height)

        Set the height of the buttonmatrix.

        :param int height: The height of the buttonmatrix.
        :return: None

        UiFlow2 Code Block:

            |set_height.png|

        MicroPython Code Block:

            .. code-block:: python

                buttonmatrix_0.set_height(200)


    .. py:method:: get_height()

        Get the height of the buttonmatrix.

        :return: The height of the buttonmatrix.
        :rtype: int

        UiFlow2 Code Block:

            |get_height.png|

        MicroPython Code Block:

            .. code-block:: python

                height = buttonmatrix_0.get_height()


    .. py:method:: align_to(obj, align, x, y)

        Align the buttonmatrix to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.
        :return: None

        UiFlow2 Code Block:

            |align_to.png|

        MicroPython Code Block:

            .. code-block:: python

                buttonmatrix_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
