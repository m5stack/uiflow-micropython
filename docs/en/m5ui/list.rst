.. currentmodule:: m5ui

M5List
=======

.. include:: ../refs/m5ui.list.ref

M5List is a widget that can be used to create lists in user interfaces. It is basically a rectangle with vertical layout to which Buttons and Text can be added.


UiFlow2 Example
---------------

list example
^^^^^^^^^^^^

Open the |cores3_list_example.m5f2| project in UiFlow2.

This example demonstrates how to create a list that displays a series of items.

UiFlow2 Code Block:

    |cores3_list_example.png|

Example output:

    None


MicroPython Example
-------------------

list example
^^^^^^^^^^^^

This example demonstrates how to create a list that displays a series of items.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/list/cores3_list_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

M5List
^^^^^^^

.. autoclass:: m5ui.list.M5List
    :members:

    .. py:method:: add_text(text:str)

        Add text to the list end.

        :param str text: The text to add.

        UiFlow2 Code Block:

            |add_text.png|

        MicroPython Code Block:

            .. code-block:: python

                text_0 = list_0.add_text("Item 1")

    .. py:method:: add_button(icon, text)

        Add a button to the list end.

        :param int icon: The icon to display on the button, `refer icon list <https://docs.lvgl.io/9.3/details/main-modules/font.html#special-fonts>`_ .
        :param str text: The text to display on the button.

        UiFlow2 Code Block:

            |add_button.png|

        MicroPython Code Block:

            .. code-block:: python

                button_0 = list_0.add_button(lv.SYMBOL.BULLET, "Button0")

    .. py:method:: move_background()

        Move the background of the list to the end.

        UiFlow2 Code Block:

            |move_background.png|

        MicroPython Code Block:

            .. code-block:: python

                button_0.move_background()
                text_0.move_background()

    
    .. py:method:: move_foreground()

        Move the foreground of the list to the end.

        UiFlow2 Code Block:

            |move_foreground.png|

        MicroPython Code Block:

            .. code-block:: python

                button_0.move_foreground()
                text_0.move_foreground()

    .. py:method:: move_to_index(index)

        Move the item at the specified index to the end of the list.

        UiFlow2 Code Block:

            |move_to_index.png|

        MicroPython Code Block:

            .. code-block:: python

                button_0.move_to_index(0)
                text_0.move_to_index(1)

    .. py:method:: delete()

        Delete the item from the list.

        UiFlow2 Code Block:

            |delete.png|

        MicroPython Code Block:

            .. code-block:: python

                button_0.delete()
                text_0.delete()
                list_0.delete()

    .. py:method:: add_event_cb(handler, event, user_data)

        Add an event callback to the button. The callback will be called when the specified event occurs.

        :param function handler: The callback function to call.
        :param int event: The event to listen for.
        :param Any user_data: Optional user data to pass to the callback.
        :return: None

        UiFlow2 Code Block:

            |event.png|

        MicroPython Code Block:

            .. code-block:: python

                def button0_event_handler(event_struct):
                    code = event_struct.code
                    obj = event_struct.get_target_obj()
                    if code == lv.EVENT.CLICKED:
                        print("Clicked: list1" + list_0.get_button_text(obj))


                def button1_event_handler(event_struct):
                    code = event_struct.code
                    obj = event_struct.get_target_obj()
                    if code == lv.EVENT.CLICKED:
                        print("Clicked: list1" + list_0.get_button_text(obj))


                button_0.add_event_cb(button0_event_handler, lv.EVENT.CLICKED, None)
                button_1.add_event_cb(button1_event_handler, lv.EVENT.CLICKED, None)

    .. py:method:: set_flag(flag, value)

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.
        :return: None

        UiFlow2 Code Block:

            |set_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.set_flag(lv.obj.FLAG.HIDDEN, True)

    .. py:method:: set_pos(x, y)

        Set the position of the label.

        :param int x: The x-coordinate of the label.
        :param int y: The y-coordinate of the label.
        :return: None

        UiFlow2 Code Block:

            |set_pos.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.set_pos(100, 100)


    .. py:method:: set_x(x)

        Set the x-coordinate of the label.

        :param int x: The x-coordinate of the label.
        :return: None

        UiFlow2 Code Block:

            |set_x.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.set_x(100)


    .. py:method:: set_y(y)

        Set the y-coordinate of the label.

        :param int y: The y-coordinate of the label.
        :return: None

        UiFlow2 Code Block:

            |set_y.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.set_y(100)


    .. py:method:: set_size(width, height)

        Set the size of the label.

        :param int width: The width of the label.
        :param int height: The height of the label.
        :return: None

        UiFlow2 Code Block:

            |set_size.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.set_size(100, 50)


    .. py:method:: set_width(width)

        Set the width of the label.

        :param int width: The width of the label.
        :return: None

        UiFlow2 Code Block:

            |set_width.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.set_width(100)


    .. py:method:: align_to(obj, align, x, y)

        Align the label to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.
        :return: None

        UiFlow2 Code Block:

            |align_to.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
