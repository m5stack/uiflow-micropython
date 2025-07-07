.. currentmodule:: m5ui

M5Switch
========

.. include:: ../refs/m5ui.switch.ref

M5Switch is a widget that can be used to create switch in the user interface. It can be used to trigger actions when checked and uncheked.

UiFlow2 Example
---------------

event switch
^^^^^^^^^^^^

Open the |cores3_switch_event_example.m5f2| project in UiFlow2.

This example creates a switch that triggers an event when checked and uncheked.

UiFlow2 Code Block:

    |cores3_switch_event_example.png|

Example output:

    None


MicroPython Example
-------------------

event switch
^^^^^^^^^^^^

This example creates a switch that triggers an event when checked and uncheked.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/switch/cores3_switch_event_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

M5Switch
^^^^^^^^

.. autoclass:: m5ui.switch.M5Switch
    :members:
    :member-order: bysource

    .. py:method:: set_bg_color(color, opa, part)

        Set the background color of the switch.

        :param int color: The color to set.
        :param int opa: The opacity of the color. The value should be between 0 (transparent) and 255 (opaque).
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).

        UiFlow2 Code Block:

            |set_bg_color_default.png|

            |set_bg_color_checked.png|

            |set_knob_color_checked.png|

            |set_knob_color_default.png|

        MicroPython Code Block:

            .. code-block:: python

                switch_0.set_bg_color(0xE7E3E7, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
                switch_0.set_bg_color(0x2196F3, 255, lv.PART.INDICATOR | lv.STATE.CHECKED)

    .. py:method:: set_state(state, value)

        Set the state of the Switch.

        :param int state: The state to set.
        :param bool value: If True, the state is set; if False, the state is unset.

        UiFlow2 Code Block:

            |set_state.png|

        MicroPython Code Block:

            .. code-block:: python

                switch_0.set_state(lv.STATE.CHECKED, True)

    .. py:method:: has_state(state)

        Get the state of the Switch.

        :param int state: The state to get.
        :return: True if the state is set, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |has_state.png|

        MicroPython Code Block:

            .. code-block:: python

                switch_0.has_state(lv.STATE.CHECKED)

    .. py:method:: set_pos(x, y)

        Set the position of the switch.

        :param int x: The x-coordinate of the switch.
        :param int y: The y-coordinate of the switch.

        UiFlow2 Code Block:

            |set_pos.png|

        MicroPython Code Block:

            .. code-block:: python

                switch_0.set_pos(100, 100)

    .. py:method:: set_x(x)

        Set the x-coordinate of the switch.

        :param int x: The x-coordinate of the switch.

        UiFlow2 Code Block:

            |set_x.png|

        MicroPython Code Block:

            .. code-block:: python

                switch_0.set_x(100)

    .. py:method:: set_y(y)

        Set the y-coordinate of the switch.

        :param int y: The y-coordinate of the switch.

        UiFlow2 Code Block:

            |set_y.png|

        MicroPython Code Block:

            .. code-block:: python

                switch_0.set_y(100)

    .. py:method:: set_size(width, height)

        Set the size of the switch.

        :param int width: The width of the switch.
        :param int height: The height of the switch.

        UiFlow2 Code Block:

            |set_size.png|

        MicroPython Code Block:

            .. code-block:: python

                switch_0.set_size(100, 50)

    .. py:method:: set_width(width)

        Set the width of the switch.

        :param int width: The width of the switch.

        UiFlow2 Code Block:

            |set_width.png|

        MicroPython Code Block:

            .. code-block:: python

                switch_0.set_width(100)

    .. py::method:: get_width()

        Get the width of the switch.

        :return: The width of the switch.
        :rtype: int

        UiFlow2 Code Block:

            |get_width.png|

        MicroPython Code Block:

            .. code-block:: python

                switch_0.get_width()

    .. py:method:: set_height(height)

        Set the height of the switch.

        :param int height: The height of the switch.

        UiFlow2 Code Block:

            |set_height.png|

        MicroPython Code Block:

            .. code-block:: python

                switch_0.set_height(50)

    .. py::method:: get_height()

        Get the height of the switch.

        :return: The height of the switch.
        :rtype: int

        UiFlow2 Code Block:

            |get_height.png|

        MicroPython Code Block:

            .. code-block:: python

                switch_0.get_height()

    .. py:method:: align_to(obj, align, x, y)

        Align the switch to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.

        UiFlow2 Code Block:

            |align_to.png|

        MicroPython Code Block:

            .. code-block:: python

                switch_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)

    .. py:method:: add_event_cb(handler, event, user_data)

        Add an event callback to the switch. The callback will be called when the specified event occurs.

        :param function handler: The callback function to call.
        :param int event: The event to listen for.
        :param Any user_data: Optional user data to pass to the callback.

        UiFlow2 Code Block:

            |event.png|

        MicroPython Code Block:

            .. code-block:: python

                def switch0_checked_event(event_struct):
                    global page0, button0
                    print("checked")

                def switch0_unchecked_event(event_struct):
                    global page0, button0
                    print("unchecked")

                def switch0_event_handler(event_struct):
                    global page0, button0
                    event = event_struct.code
                    obj = event_struct.get_target_obj()
                    if event == lv.EVENT.VALUE_CHANGED:
                        if obj.has_state(lv.STATE.CHECKED):
                            switch0_checked_event(event_struct)
                        else:
                            switch0_unchecked_event(event_struct)
                    return

                switch_0.add_event_cb(switch0_event_handler, lv.EVENT.ALL, None)
