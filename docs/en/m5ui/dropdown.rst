.. currentmodule:: m5ui

M5Dropdown
==========

.. include:: ../refs/m5ui.dropdown.ref

M5Dropdown is a widget that can be used to create dropdown menus in the user
interface. It allows users to select one option from a list of available options
with a compact dropdown interface.

UiFlow2 Example
---------------

Drop down in four directions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |cores3_dropdown_directions_example.m5f2| project in UiFlow2.

This example creates a drop down, up, left and right menus.

UiFlow2 Code Block:

    |cores3_dropdown_directions_example.png|

Example output:

    None


MicroPython Example
-------------------

Drop down in four directions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example creates a drop down, up, left and right menus.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/dropdown/cores3_dropdown_directions_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

M5Dropdown
^^^^^^^^^^

.. autoclass:: m5ui.dropdown.M5Dropdown
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

                dropdown_0.set_flag(lv.obj.FLAG.HIDDEN, True)


    .. py:method:: toggle_flag(flag)

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

            |toggle_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                dropdown_0.toggle_flag(lv.obj.FLAG.HIDDEN)


    .. py:method:: set_state(state, value)

        Set the state of the dropdown. If ``value`` is True, the state is set; if False, the state is unset.

        :param int state: The state to set.
        :param bool value: If True, the state is set; if False, the state is unset.
        :return: None

        UiFlow2 Code Block:

            |set_state.png|

        MicroPython Code Block:

            .. code-block:: python

                dropdown_0.set_state(lv.STATE.CHECKED, True)


    .. py:method:: toggle_state(state)

        Toggle the state of the dropdown. If the state is set, it is unset; if not set, it is set.

        :param int state: The state to toggle.
        :return: None

        UiFlow2 Code Block:

            |toggle_state.png|

        MicroPython Code Block:

            .. code-block:: python

                dropdown_0.toggle_state(lv.STATE.CHECKED)


    .. py:method:: set_pos(x, y)

        Set the position of the dropdown.

        :param int x: The x-coordinate of the dropdown.
        :param int y: The y-coordinate of the dropdown.
        :return: None

        UiFlow2 Code Block:

            |set_pos.png|

        MicroPython Code Block:

            .. code-block:: python

                dropdown_0.set_pos(100, 100)


    .. py:method:: set_x(x)

        Set the x-coordinate of the dropdown.

        :param int x: The x-coordinate of the dropdown.
        :return: None

        UiFlow2 Code Block:

            |set_x.png|

        MicroPython Code Block:

            .. code-block:: python

                dropdown_0.set_x(100)


    .. py:method:: set_y(y)

        Set the y-coordinate of the dropdown.

        :param int y: The y-coordinate of the dropdown.
        :return: None

        UiFlow2 Code Block:

            |set_y.png|

        MicroPython Code Block:

            .. code-block:: python

                dropdown_0.set_y(100)


    .. py:method:: set_size(width, height)

        Set the size of the dropdown.

        :param int width: The width of the dropdown.
        :param int height: The height of the dropdown.
        :return: None

        UiFlow2 Code Block:

            |set_size.png|

        MicroPython Code Block:

            .. code-block:: python

                dropdown_0.set_size(100, 50)


    .. py:method:: set_width(width)

        Set the width of the dropdown.

        :param int width: The width of the dropdown.
        :return: None

        UiFlow2 Code Block:

            |set_width.png|

        MicroPython Code Block:

            .. code-block:: python

                dropdown_0.set_width(100)


    .. py:method:: get_width()

        Get the width of the dropdown.

        :return: The width of the dropdown.
        :rtype: int

        UiFlow2 Code Block:

            |get_width.png|

        MicroPython Code Block:

            .. code-block:: python

                dropdown_0.get_width()


    .. py:method:: set_height(height)

        Set the height of the dropdown.

        :param int height: The height of the dropdown.
        :return: None

        UiFlow2 Code Block:

            |set_height.png|

        MicroPython Code Block:

            .. code-block:: python

                dropdown_0.set_height(50)


    .. py:method:: get_height()

        Get the height of the dropdown.

        :return: The height of the dropdown.
        :rtype: int

        UiFlow2 Code Block:

            |get_height.png|

        MicroPython Code Block:

            .. code-block:: python

                dropdown_0.get_height()

    .. py:method:: align_to(obj, align, x, y)

        Align the dropdown to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.
        :return: None

        UiFlow2 Code Block:

            |align_to.png|

        MicroPython Code Block:

            .. code-block:: python

                dropdown_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)


    .. py:method:: get_selected()

        Get the index of the currently selected option.

        :return: The index of the selected option.
        :rtype: int

        UiFlow2 Code Block:

            |get_selected.png|

        MicroPython Code Block:

            .. code-block:: python

                selected_index = dropdown_0.get_selected()


    .. py:method:: set_selected_highlight(enable)

        Enable or disable highlighting of the selected option.

        :param bool enable: True to enable highlighting, False to disable.
        :return: None

        UiFlow2 Code Block:

            |set_selected_highlight.png|

        MicroPython Code Block:

            .. code-block:: python

                dropdown_0.set_selected_highlight(True)


    .. py:method:: get_option_count()

        Clear all options in a drop-down list.

        :return: The number of options in the dropdown.
        :rtype: int

        UiFlow2 Code Block:

            |get_option_count.png|

        MicroPython Code Block:

            .. code-block:: python

                option_count = dropdown_0.get_option_count()

    .. py:method:: get_option_index(option)

        Get the index of an option.

        :param str option: The option to find.
        :return: The index of the option, or -1 if not found.
        :rtype: int

        UiFlow2 Code Block:

            |get_option_index.png|

        MicroPython Code Block:

            .. code-block:: python

                index = dropdown_0.get_option_index("Option 1")
                if index != -1:
                    print(f"Option found at index: {index}")
                else:
                    print("Option not found")


    .. py:method:: get_text()

        Get text of the drop-down list's button.

        :return: The text of the dropdown button.
        :rtype: str

        UiFlow2 Code Block:

            |get_text.png|

        MicroPython Code Block:

            .. code-block:: python

                text = dropdown_0.get_text()
                print(f"Dropdown button text: {text}")


    .. py:method:: set_text(txt)

        Set text of the drop-down list's button.

        :param str txt: The text to set for the dropdown button.
        :return: None

        UiFlow2 Code Block:

            |set_text.png|

        MicroPython Code Block:
    
            .. code-block:: python

                dropdown_0.set_text("Select an option")


    .. py:method:: add_event_cb(handler, event, user_data)

        Add an event callback to the dropdown. The callback will be called when the specified event occurs.

        :param function handler: The callback function to call.
        :param int event: The event to listen for.
        :param Any user_data: Optional user data to pass to the callback.
        :return: None

        UiFlow2 Code Block:

            |event.png|

        MicroPython Code Block:

            .. code-block:: python

                def dropdown_0_value_changed_event(event_struct):
                    global dropdown_0
                    selected = dropdown_0.get_selected_str()
                    print(f"Selected: {selected}")

                def dropdown_0_event_handler(event_struct):
                    global dropdown_0
                    event = event_struct.code
                    if event == lv.EVENT.VALUE_CHANGED:
                        dropdown_0_value_changed_event(event_struct)
                    return

                dropdown_0.add_event_cb(dropdown_0_event_handler, lv.EVENT.ALL, None)
