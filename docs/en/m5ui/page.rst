.. currentmodule:: m5ui

M5Page
======

.. include:: ../refs/m5ui.page.ref

M5Page is a widget that can be used to create pages in the user interface. It can be used to organize other widgets and provide navigation between different pages.

UiFlow2 Example
---------------

page event
^^^^^^^^^^

Open the |cores3_page_event_example.m5f2| project in UiFlow2.

When you press and hold the screen, the screen background color turns black. When you release the screen, the background color returns to white.

UiFlow2 Code Block:

    |cores3_page_event_example.png|

Example output:

    None


MicroPython Example
-------------------

page event
^^^^^^^^^^

When you press and hold the screen, the screen background color turns black. When you release the screen, the background color returns to white.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/page/cores3_page_event_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

M5Button
^^^^^^^^

.. autoclass:: m5ui.page.M5Page
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

                page_0.set_flag(lv.obj.FLAG.HIDDEN, True)


    .. py:method:: toggle_flag(flag)

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

            |toggle_flag.png|

        MicroPython Code Block:

            .. code-block:: python

                page_0.toggle_flag(lv.obj.FLAG.HIDDEN)


    .. py:method:: set_state(state, value)

        Set the state of the page. If ``value`` is True, the state is set; if False, the state is unset.

        :param int state: The state to set.
        :param bool value: If True, the state is set; if False, the state is unset.
        :return: None

        UiFlow2 Code Block:

            |set_state.png|

        MicroPython Code Block:

            .. code-block:: python

                page_0.set_state(lv.STATE.PRESSED, True)


    .. py:method:: toggle_state(state)

        Toggle the state of the page. If the state is set, it is unset; if not set, it is set.

        :param int state: The state to toggle.
        :return: None

        UiFlow2 Code Block:

            |toggle_state.png|

        MicroPython Code Block:

            .. code-block:: python

                page_0.toggle_state(lv.STATE.PRESSED)


    .. py:method:: set_bg_color(color, opa, part)

        Set the background color of the page.

        :param int color: The color to set.
        :param int opa: The opacity of the color.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |set_bg_color.png|

        MicroPython Code Block:

            .. code-block:: python

                page_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)


    .. py:method:: add_event_cb(handler, event, user_data)

        Add an event callback to the page. The callback will be called when the specified event occurs.

        :param function handler: The callback function to call.
        :param int event: The event to listen for.
        :param Any user_data: Optional user data to pass to the callback.
        :return: None

        UiFlow2 Code Block:

            |event.png|

        MicroPython Code Block:

            .. code-block:: python

                def page0_pressed_event(event_struct):
                    global page0
                    page0.set_bg_color(0x000000, 255, 0)

                def page0_released_event(event_struct):
                    global page0
                    page0.set_bg_color(0xffffff, 255, 0)

                def page0_clicked_event(event_struct):
                    global page0
                    page0.set_bg_color(0x000000, 255, 0)

                def page0_event_handler(event_struct):
                    global page0
                    event = event_struct.code
                    if event == lv.EVENT.PRESSED and True:
                        page0_pressed_event(event_struct)
                    if event == lv.EVENT.RELEASED and True:
                        page0_released_event(event_struct)
                    if event == lv.EVENT.CLICKED and True:
                        page0_clicked_event(event_struct)
                    if event == lv.EVENT.LONG_PRESSED and True:
                        page0_long_pressed_event(event_struct)
                    return

                page_0.add_event_cb(page0_event_handler, lv.EVENT.ALL, None)
